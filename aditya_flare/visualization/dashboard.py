import os
import sys
import time
import pickle
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))
from aditya_flare.processing.features import extract_features

st.set_page_config(
    page_title="AditSolarFlare Mission Control",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling for Tactical Layout ---
st.markdown("""
<style>
    .reportview-container { background: #0b0f19; }
    .alert-banner {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .alert-normal { background-color: rgba(0, 255, 100, 0.1); color: #00ff88; border: 1px solid #00ff88; }
    .alert-critical { background-color: rgba(255, 0, 50, 0.2); color: #ff3366; border: 2px solid #ff3366; animation: blink 1s linear infinite; }
    @keyframes blink { 50% { opacity: 0.5; } }
    .gauge-container { text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 1. State Initialization ---
@st.cache_resource
def load_assets():
    processed_dir = Path("data/processed")
    model_path = Path("data/models/ensemble_forecaster.pkl")
    
    if not model_path.exists():
        st.error("Model file not found! Please run Phase 3 training first.")
        st.stop()
        
    with open(model_path, "rb") as f:
        ensemble_data = pickle.load(f)
        
    # Load 5 days of data for the simulation
    df = extract_features(processed_dir, max_days=5, flare_threshold=500.0)
    
    # Locate a major flare
    max_flare_idx = df['solexs_sdd2_ctr'].idxmax()
    if df.loc[max_flare_idx, 'solexs_sdd2_ctr'] < 500:
        # Fallback if no flare in first 5 days
        df = extract_features(processed_dir, flare_threshold=500.0)
        max_flare_idx = df['solexs_sdd2_ctr'].idxmax()
        
    # Isolate a 12-hour slice around the flare
    start_time = max_flare_idx - pd.Timedelta(hours=4)
    end_time = max_flare_idx + pd.Timedelta(hours=8)
    sim_df = df.loc[start_time:end_time].copy()
    
    # Generate predictions ahead of time for the simulation
    X_sim = sim_df[ensemble_data['features']].values
    p_lgb = ensemble_data['lgb'].predict_proba(X_sim)[:, 1]
    p_knn = ensemble_data['knn'].predict_proba(X_sim)[:, 1]
    sim_df['forecast_prob'] = (0.7 * p_lgb) + (0.3 * p_knn)
    
    # Generate a mock flare catalog from the data
    catalog = []
    in_flare = False
    f_start = None
    f_peak_time = None
    f_peak_val = 0
    
    for idx, row in df.iterrows():
        flux = row['solexs_sdd2_ctr']
        if flux >= 500:
            if not in_flare:
                in_flare = True
                f_start = idx
                f_peak_val = flux
                f_peak_time = idx
            else:
                if flux > f_peak_val:
                    f_peak_val = flux
                    f_peak_time = idx
        else:
            if in_flare:
                in_flare = False
                f_class = "X-Class" if f_peak_val > 5000 else ("M-Class" if f_peak_val > 1000 else "C-Class")
                catalog.append({
                    'flare_id': f"FLR-{f_start.strftime('%Y%m%d-%H%M')}",
                    'start_time': f_start,
                    'peak_time': f_peak_time,
                    'end_time': idx,
                    'class': f_class,
                    'peak_flux': f_peak_val
                })
    
    catalog_df = pd.DataFrame(catalog)
    return sim_df, catalog_df, ensemble_data

def init_session_state():
    if 'sim_playhead' not in st.session_state:
        st.session_state.sim_playhead = 0
    if 'is_playing' not in st.session_state:
        st.session_state.is_playing = False
    if 'zoom_window' not in st.session_state:
        st.session_state.zoom_window = None

# --- 2. Header Alerts ---
def render_header_alerts(current_row):
    flux = current_row['solexs_sdd2_ctr']
    prob = current_row['forecast_prob']
    
    is_critical = flux > 500
    is_warning = prob > 0.5 and not is_critical
    
    if is_critical:
        alert_class = "alert-critical"
        alert_text = f"🚨 CRITICAL: ACTIVE FLARE DETECTED (Flux: {flux:.0f})"
    elif is_warning:
        alert_class = "alert-critical"
        alert_text = f"⚠️ WARNING: HIGH PROBABILITY SHIFT - INCOMING PEAK ANTICIPATED"
    else:
        alert_class = "alert-normal"
        alert_text = f"✅ NORMAL: BACKGROUND SOLAR ACTIVITY STABLE"
        
    st.markdown(f'<div class="alert-banner {alert_class}">{alert_text}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("UTC Timestamp", current_row.name.strftime("%H:%M:%S"))
    col2.metric("SoLEXS SDD2 Flux", f"{flux:.1f} cps")
    col3.metric("Hardness Ratio", f"{current_row['hardness_ratio']:.3f}")
    col4.metric("15-Min Forecast Prob", f"{prob*100:.1f}%")

# --- 3. Interactive Charts ---
def build_interactive_charts(df_buffer, current_time):
    # Downsample for rendering speed if window is large
    render_df = df_buffer
    if len(render_df) > 360: # 6 hours of 1-min data
        render_df = render_df.iloc[::2] 
        
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, 
                        row_heights=[0.4, 0.3, 0.3])
    
    # Panel A: Soft X-Rays
    fig.add_trace(go.Scatter(x=render_df.index, y=render_df['solexs_sdd2_ctr'],
                             name="SoLEXS (2-22 keV)", line=dict(color="#00d2ff")), row=1, col=1)
    
    rolling_bg = render_df['solexs_sdd2_ctr'].rolling(60, min_periods=1).mean()
    fig.add_trace(go.Scatter(x=render_df.index, y=rolling_bg,
                             name="Background", line=dict(color="gray", dash="dash")), row=1, col=1)
                             
    # Panel B: Hard X-Rays
    if 'helios_czt_broad_ctr' in render_df.columns:
        fig.add_trace(go.Scatter(x=render_df.index, y=render_df['helios_czt_broad_ctr'],
                                 name="HEL1OS (Broad)", line=dict(color="#ff9900")), row=2, col=1)
                                 
    # Panel C: Composite Physical Indicators (Hardness Ratio)
    fig.add_trace(go.Scatter(x=render_df.index, y=render_df['hardness_ratio'],
                             name="Hardness Ratio", line=dict(color="#ff3366")), row=3, col=1)
                             
    # Layout and Formatting
    fig.update_layout(
        template="plotly_dark",
        height=700,
        margin=dict(l=40, r=40, t=20, b=20),
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Zoom Window Logic
    if st.session_state.zoom_window:
        x_start, x_end = st.session_state.zoom_window
        fig.update_xaxes(range=[x_start, x_end])
    else:
        fig.update_xaxes(range=[df_buffer.index[0], current_time + pd.Timedelta(hours=1)])
        
    fig.update_yaxes(title_text="Soft Flux", row=1, col=1)
    fig.update_yaxes(title_text="Hard Flux", row=2, col=1)
    fig.update_yaxes(title_text="HR", row=3, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

# --- 4. Catalog Table ---
def render_catalog_table(catalog_df):
    st.subheader("Historical Flare Catalog")
    st.markdown("Select a flare to automatically drill down into the time window and prepare PyXspec joint fitting.")
    
    # Display table
    event_list = st.dataframe(
        catalog_df, 
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    if len(event_list.selection['rows']) > 0:
        idx = event_list.selection['rows'][0]
        selected_flare = catalog_df.iloc[idx]
        
        start = selected_flare['start_time'] - pd.Timedelta(minutes=30)
        end = selected_flare['end_time'] + pd.Timedelta(minutes=30)
        
        st.session_state.zoom_window = (start, end)
        st.success(f"Drill-down activated for {selected_flare['flare_id']}.")
        
        if st.button("🚀 Run PyXspec Joint Fit (Placeholder)"):
            st.info("HEASoft Environment is still installing. This button will activate the XSPEC spectral fitting pipeline once completed.")
    else:
        if st.button("Reset View"):
            st.session_state.zoom_window = None

def main():
    init_session_state()
    
    with st.spinner("Initializing Phase 4 Tactical Screen..."):
        sim_df, catalog_df, ensemble_data = load_assets()
        
    st.sidebar.title("Simulation Controls")
    
    # Play controls
    play = st.sidebar.checkbox("Start Live Telemetry Stream")
    if play != st.session_state.is_playing:
        st.session_state.is_playing = play
        
    st.session_state.sim_playhead = st.sidebar.slider(
        "Simulation Playhead", 
        0, len(sim_df)-1, 
        st.session_state.sim_playhead
    )
    
    # Ensure playhead doesn't exceed data
    if st.session_state.sim_playhead >= len(sim_df):
        st.session_state.sim_playhead = 0
        st.session_state.is_playing = False
        
    # Get current state
    current_idx = st.session_state.sim_playhead
    current_time = sim_df.index[current_idx]
    current_row = sim_df.iloc[current_idx]
    buffer_df = sim_df.iloc[:current_idx+1]
    
    # Render layout
    render_header_alerts(current_row)
    build_interactive_charts(buffer_df, current_time)
    render_catalog_table(catalog_df)
    
    # Simulation Loop execution
    if st.session_state.is_playing:
        time.sleep(1.0)
        st.session_state.sim_playhead += 1
        st.rerun()

if __name__ == "__main__":
    main()
