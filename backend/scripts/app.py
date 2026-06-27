import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import xgboost as xgb
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.models.dataset import load_and_prepare_dataset, get_train_test_split

st.set_page_config(
    page_title="Aditya-L1 Nowcasting",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Dark/Neon Vibe ---
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .metric-container {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h1 {
        color: #00d2ff;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = Path("data/models/xgboost_nowcast.json")
    if not model_path.exists():
        st.error("Model file not found! Please run train_xgboost.py first.")
        st.stop()
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    return model

@st.cache_data
def load_simulation_data():
    processed_dir = Path("data/processed")
    df = load_and_prepare_dataset(processed_dir, target_threshold=500, horizon_minutes=15)
    
    # We just need the test split to simulate unseen data
    X_train, X_test, y_train, y_test = get_train_test_split(df, test_size=0.2)
    test_df = df.iloc[len(X_train):].copy()
    
    # Extract the massive flare event around April 24, 2026
    max_flare_idx = test_df['solexs_sdd2_ctr'].idxmax()
    start_time = max_flare_idx - pd.Timedelta(hours=4)
    end_time = max_flare_idx + pd.Timedelta(hours=8)
    
    window_df = test_df.loc[start_time:end_time]
    
    if len(window_df) == 0:
        window_df = test_df.iloc[:60*12] # Fallback to 12 hours
    return window_df

def main():
    st.title("🛰️ Aditya-L1 Mission Control: Flare Nowcasting")
    st.markdown("Real-time telemetry and predictive machine learning models tracking Solar Soft X-Ray flux.")
    
    with st.spinner("Initializing telemetry and loading XGBoost model..."):
        model = load_model()
        df = load_simulation_data()
        
    features = [
        'solexs_sdd2_ctr', 'helios_czt_broad_ctr', 'hardness_ratio',
        'hr_diff_5m', 'hr_roll_mean_10m', 'solexs_roll_mean_10m', 'czt_roll_max_5m',
        'suit_uv_mean', 'suit_uv_max'
    ]
    
    # Generate predictions
    X_sim = df[features]
    df['flare_prob'] = model.predict_proba(X_sim)[:, 1]
    
    # --- UI Simulation Controls ---
    st.sidebar.header("Simulation Controls")
    time_step = st.sidebar.slider("Timeline Playhead", 0, len(df)-1, int(len(df)*0.3))
    
    current_time = df.index[time_step]
    current_flux = df.iloc[time_step]['solexs_sdd2_ctr']
    current_hr = df.iloc[time_step]['hardness_ratio']
    current_prob = df.iloc[time_step]['flare_prob']
    
    # --- Top Metrics Row ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Current UTC Time", value=current_time.strftime("%H:%M:%S"))
    with col2:
        st.metric(label="SoLEXS Flux (counts/s)", value=f"{current_flux:.1f}")
    with col3:
        st.metric(label="Hardness Ratio", value=f"{current_hr:.3f}")
    with col4:
        # Dynamic warning
        if current_prob > 0.5:
            st.error(f"🚨 FLARE WARNING: {current_prob*100:.1f}%")
        else:
            st.success(f"✅ SYSTEM CLEAR: {current_prob*100:.1f}%")
            
    st.markdown("---")
    
    # --- Plotly Chart ---
    st.subheader("Live Telemetry & Predictive Horizon")
    
    # We plot the data up to the current time step
    visible_df = df.iloc[:time_step+1]
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, 
                        row_heights=[0.6, 0.4])
    
    # 1. Actual Flux Plot
    fig.add_trace(
        go.Scatter(x=visible_df.index, y=visible_df['solexs_sdd2_ctr'],
                   mode='lines', name='SoLEXS SDD2 Flux',
                   line=dict(color='#00d2ff', width=2),
                   fill='tozeroy', fillcolor='rgba(0, 210, 255, 0.1)'),
        row=1, col=1
    )
    # Threshold Line
    fig.add_hline(y=500, line_dash="dash", line_color="red", 
                  annotation_text="Flare Threshold (500)", row=1, col=1)
    
    # 2. Predicted Probability Plot
    fig.add_trace(
        go.Scatter(x=visible_df.index, y=visible_df['flare_prob'],
                   mode='lines', name='15-Min Flare Probability',
                   line=dict(color='#ff4b4b', width=2),
                   fill='tozeroy', fillcolor='rgba(255, 75, 75, 0.2)'),
        row=2, col=1
    )
    # 50% Threshold Line
    fig.add_hline(y=0.5, line_dash="dash", line_color="orange", 
                  annotation_text="Warning Threshold (50%)", row=2, col=1)
    
    # Format layout for Dark Mode
    fig.update_layout(
        template="plotly_dark",
        height=600,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Lock the x-axis so the chart doesn't jitter
    fig.update_xaxes(range=[df.index[0], df.index[-1]], showgrid=False)
    fig.update_yaxes(title_text="Soft X-Rays (counts/s)", row=1, col=1, showgrid=True, gridcolor='#333333')
    fig.update_yaxes(title_text="Probability", range=[0, 1.05], row=2, col=1, showgrid=True, gridcolor='#333333')
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
