import os
import sys
import re
import argparse
import getpass
from datetime import datetime, timedelta
from pathlib import Path

# Add external libraries check
try:
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError:
    print("This script requires 'requests', 'beautifulsoup4', and 'tqdm'.")
    print("Installing them using pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "tqdm"])
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm

# Constants
BASE_URL = "https://pradan1.issdc.gov.in"
BROWSE_URL = f"{BASE_URL}/al1/protected/browse.xhtml?id=suit"
IDP_URL = "https://idp.issdc.gov.in"

def authenticate(username, password):
    """
    Simulates Keycloak authentication flow to obtain the authenticated session.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    print("\n[1/3] Navigating to ISSDC PRADAN login flow...")
    # Step 1: Request the protected browse page to trigger OAuth redirect
    try:
        response = session.get(BROWSE_URL, allow_redirects=True)
    except Exception as e:
        print(f"Error connecting to ISSDC server: {e}")
        return None
    
    if "Sign in to Indian Space Science Data Center" not in response.text:
        if "suit" in response.text:
            print("Already authenticated!")
            return session
        print("Error: Could not locate the Keycloak login page.")
        return None
        
    # Step 2: Parse the login action URL from the Keycloak HTML
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", id="kc-form-login")
    if not form or not form.get("action"):
        print("Error: Could not find login form action in page.")
        return None
        
    action_url = form["action"]
    
    print("[2/3] Submitting credentials securely...")
    # Step 3: Post credentials to Keycloak
    payload = {
        "username": username,
        "password": password,
        "credentialId": ""
    }
    
    try:
        auth_response = session.post(action_url, data=payload, allow_redirects=True)
    except Exception as e:
        print(f"Error submitting login form: {e}")
        return None
    
    # Check if we successfully logged in and returned to pradan
    if "Sign in to your account" in auth_response.text or "Invalid username or password" in auth_response.text:
        print("Error: Authentication failed. Please verify your username and password.")
        return None
        
    if "pradan1.issdc.gov.in" in auth_response.url and "suit" in auth_response.text:
        print("[3/3] Authentication successful!")
        return session
        
    print(f"Error: Logged in but landed on unexpected URL: {auth_response.url}")
    return None

def fetch_suit_file_list(session, start_date, end_date):
    """
    Fetches the list of SUIT fits files available on the page.
    """
    print(f"\nQuerying SUIT file catalog...")
    
    try:
        response = session.get(BROWSE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching browse list: {e}")
        return []
    
    # Heuristically parse table rows and FITS links
    files = []
    links = soup.find_all("a")
    for link in links:
        text = link.text.strip()
        if text.endswith(".fits") or ".fits" in text:
            filename = text
            href = link.get("href")
            files.append((filename, href))
            
    if not files:
        print("Warning: No .fits links found by text name. Printing all parsed links on the page for debugging:")
        for idx, link in enumerate(links[:30]):
            print(f"  [{idx}] text='{link.text.strip()}', href='{link.get('href')}'")
        
    print(f"Parsed {len(files)} files from the active catalog view.")
    return files

def parse_filename_time(filename):
    """
    Extracts datetime from filename: e.g. SUT_T26_0900_002208_Lev1.0_2026-06-22T22.02.53.991_0973NB02.fits
    """
    match = re.search(r'_Lev\d\.\d_(\d{4}-\d{2}-\d{2})T(\d{2})\.(\d{2})\.(\d{2})\.(\d+)_', filename)
    if match:
        date_str = f"{match.group(1)} {match.group(2)}:{match.group(3)}:{match.group(4)}.{match.group(5)}"
        try:
            parts = date_str.split('.')
            if len(parts) > 1:
                parts[1] = parts[1][:6]
                date_str = '.'.join(parts)
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return None
    return None

def apply_temporal_subsampling(files, interval_hours=3):
    """
    Filters the files to select only one file per interval_hours.
    """
    if not files:
        return []
        
    valid_files = []
    for filename, href in files:
        dt = parse_filename_time(filename)
        if dt:
            valid_files.append((dt, filename, href))
            
    valid_files.sort(key=lambda x: x[0])
    
    if not valid_files:
        print("Warning: No files contained parseable timestamps in their names.")
        return []
        
    filtered = []
    last_taken_time = None
    
    for dt, filename, href in valid_files:
        if last_taken_time is None or (dt - last_taken_time) >= timedelta(hours=interval_hours):
            filtered.append((dt, filename, href))
            last_taken_time = dt
            
    return filtered

def download_files(session, filtered_files, dest_dir):
    """
    Downloads the selected files with progress bar.
    """
    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nStarting download of {len(filtered_files)} files to {dest_path.resolve()}...")
    
    for dt, filename, href in filtered_files:
        file_dest = dest_path / filename
        if file_dest.exists():
            print(f"File {filename} already exists. Skipping.")
            continue
            
        url = href if href.startswith("http") else f"{BASE_URL}{href}"
        
        try:
            response = session.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(file_dest, 'wb') as f, tqdm(
                desc=filename[:30],
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    size = f.write(chunk)
                    bar.update(size)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Aditya-L1 SUIT Data Ingestion Engine (Temporal Sub-Sampler)")
    parser.add_argument("--username", type=str, help="ISSDC Username/Email")
    parser.add_argument("--password", type=str, help="ISSDC Password")
    parser.add_argument("--start", type=str, default="2024-02-10", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-02-12", help="End date (YYYY-MM-DD)")
    parser.add_argument("--interval", type=int, default=3, help="Temporal interval in hours")
    
    args = parser.parse_args()
    
    print("="*60)
    print("       Aditya-L1 SUIT Data Ingestion Engine")
    print("             (Temporal Sub-Sampler)")
    print("="*60)
    
    # 1. Resolve Username
    username = args.username or os.environ.get("ISSDC_USERNAME")
    if not username:
        try:
            username = input("ISSDC Username/Email: ").strip()
        except EOFError:
            print("\nError: Stdin is closed (EOF). Cannot prompt for credentials.")
            print("Please run the script providing credentials via env variables or command line:")
            print("  export ISSDC_USERNAME='your_username'")
            print("  export ISSDC_PASSWORD='your_password'")
            print("  python scripts/suit_downloader.py")
            print("Or pass them as flags:")
            print("  python scripts/suit_downloader.py --username your_username --password your_password")
            sys.exit(1)
            
    # 2. Resolve Password
    password = args.password or os.environ.get("ISSDC_PASSWORD")
    if not password:
        try:
            password = getpass.getpass("ISSDC Password: ")
        except EOFError:
            print("\nError: Stdin is closed (EOF). Cannot prompt for credentials.")
            print("Please supply password via environment variable (ISSDC_PASSWORD) or CLI flag (--password).")
            sys.exit(1)
            
    if not username or not password:
        print("Error: Username and Password cannot be empty.")
        sys.exit(1)
        
    # Authenticate
    session = authenticate(username, password)
    if not session:
        sys.exit(1)
        
    dest_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "suit"
    
    # Step 1: Fetch files
    files = fetch_suit_file_list(session, args.start, args.end)
    
    if not files:
        print("\nNo files found or search parsing failed.")
        print("Note: If the page structure has changed, you can paste the file table HTML")
        print("into the scratch directory and we will parse it offline.")
        sys.exit(0)
        
    # Step 2: Filter
    filtered_files = apply_temporal_subsampling(files, args.interval)
    print(f"\nFiltered {len(files)} files down to {len(filtered_files)} files (one per {args.interval} hours).")
    
    # Step 3: Download
    download_files(session, filtered_files, dest_dir)
    print("\nIngestion complete!")

if __name__ == "__main__":
    main()
