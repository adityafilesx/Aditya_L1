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
    catalog_path = processed_dir / "master_flare_catalog.csv"
    
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
    
    # Load master catalog from CSV
    if catalog_path.exists():
        catalog_df = pd.read_csv(catalog_path)
        for col in ['start_time', 'end_time', 'peak_time_soft', 'peak_time_hard']:
            if col in catalog_df.columns:
                catalog_df[col] = pd.to_datetime(catalog_df[col], errors='coerce')
    else:
        st.warning("Master catalog database file not found. Please run generate_master_catalog.py.")
        catalog_df = pd.DataFrame(columns=[
            'flare_id', 'date', 'start_time', 'end_time', 'peak_time_soft', 
            'peak_time_hard', 'peak_flux_soft', 'peak_flux_hard', 'detection_type', 'class'
        ])
        
    metrics_path = processed_dir / "lead_time_metrics.json"
    if metrics_path.exists():
        import json
        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)
    else:
        metrics_data = None
        
    return sim_df, catalog_df, ensemble_data, metrics_data

@st.cache_data
def load_time_resolved_params(flare_id, start_time, end_time, peak_time_soft):
    if flare_id == 'FLR-20240212-0340':
        path = Path("data/processed/AL1_SOLEXS_SDD2_L1_time_resolved_params.csv")
        if path.exists():
            df = pd.read_csv(path)
            df = df.dropna(subset=['Temperature_val', 'Emission_Measure_norm'])
            df['Temperature_MK'] = (10 ** df['Temperature_val']) / 1e6
            base_time = pd.to_datetime('2024-02-12 00:00:00')
            df['Time'] = base_time + pd.to_timedelta(df['Time_Bin'] - 1, unit='s')
            df_flare = df[(df['Time_Bin'] >= 12180) & (df['Time_Bin'] <= 15000)].copy()
            return df_flare
        return None
    else:
        if pd.isna(start_time) or pd.isna(end_time):
            return None
        if pd.isna(peak_time_soft):
            peak_time_soft = start_time + (end_time - start_time) / 3
        time_range = pd.date_range(start=start_time, end=end_time, freq='10s')
        if len(time_range) < 2:
            return None
        df_sim = pd.DataFrame({'Time': time_range})
        t_sec = (df_sim['Time'] - start_time).dt.total_seconds()
        t_peak_sec = (peak_time_soft - start_time).total_seconds()
        if t_peak_sec <= 0: t_peak_sec = 10
        t_end_sec = (end_time - start_time).total_seconds()
        if t_end_sec <= t_peak_sec: t_end_sec = t_peak_sec + 10
        df_sim['Time_Bin'] = t_sec
        t_temp_peak = t_peak_sec * 0.8
        temp_rise = np.exp(-((t_sec - t_temp_peak) ** 2) / (2 * (t_temp_peak / 2) ** 2))
        temp_decay = np.exp(-(t_sec - t_temp_peak) / (t_end_sec / 2))
        df_sim['Temperature_MK'] = 5.0 + 15.0 * np.where(t_sec < t_temp_peak, temp_rise, temp_decay)
        em_rise = np.exp(-((t_sec - t_peak_sec) ** 2) / (2 * (t_peak_sec / 2) ** 2))
        em_decay = np.exp(-(t_sec - t_peak_sec) / (t_end_sec / 2))
        df_sim['Emission_Measure_norm'] = 1e4 + 5e6 * np.where(t_sec < t_peak_sec, em_rise, em_decay)
        return df_sim

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
        
        # We simulate spectral data for all flares if not present
        has_spectral_data = True
        
        if has_spectral_data:
            st.markdown("---")
            if selected_flare['flare_id'] == 'FLR-20240212-0340':
                st.subheader("📈 Thermodynamic Diagnostics (PyXspec Fit Output)")
            else:
                st.subheader(f"📈 Thermodynamic Diagnostics (Simulated profile for {selected_flare['flare_id']})")
                
            fit_df = load_time_resolved_params(selected_flare['flare_id'], selected_flare['start_time'], selected_flare['end_time'], selected_flare.get('peak_time_soft'))
            if fit_df is not None:
                col_ts, col_phase = st.columns(2)
                
                with col_ts:
                    st.markdown("**Temperature & Emission Measure Evolution**")
                    fig_ts = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
                    
                    fig_ts.add_trace(go.Scatter(
                        x=fit_df['Time'], y=fit_df['Temperature_MK'],
                        mode='lines+markers', name='Temperature (MK)',
                        line=dict(color='#ff3366', width=2),
                        marker=dict(size=4)
                    ), row=1, col=1)
                    
                    fig_ts.add_trace(go.Scatter(
                        x=fit_df['Time'], y=fit_df['Emission_Measure_norm'],
                        mode='lines+markers', name='Emission Measure',
                        line=dict(color='#00ff88', width=2),
                        marker=dict(size=4)
                    ), row=2, col=1)
                    
                    fig_ts.update_layout(
                        template="plotly_dark",
                        height=450,
                        margin=dict(l=40, r=40, t=10, b=10),
                        showlegend=False
                    )
                    fig_ts.update_yaxes(title_text="Temp (MK)", row=1, col=1)
                    fig_ts.update_yaxes(title_text="EM (norm)", row=2, col=1)
                    fig_ts.update_xaxes(title_text="Time (UTC)", row=2, col=1)
                    
                    st.plotly_chart(fig_ts, use_container_width=True)
                    
                with col_phase:
                    st.markdown("**2D Plasma Phase Space (T vs EM Hysteresis Loop)**")
                    fig_phase = go.Figure()
                    
                    fig_phase.add_trace(go.Scatter(
                        x=fit_df['Temperature_MK'], y=fit_df['Emission_Measure_norm'],
                        mode='lines+markers',
                        marker=dict(
                            size=6,
                            color=fit_df['Time_Bin'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Time Bin (s)")
                        ),
                        line=dict(color='rgba(255,255,255,0.3)', width=1.5),
                        text=fit_df['Time'].dt.strftime('%H:%M:%S'),
                        hovertemplate="<b>Time:</b> %{text}<br><b>Temp:</b> %{x:.2f} MK<br><b>EM:</b> %{y:.2e}"
                    ))
                    
                    start_pt = fit_df.iloc[0]
                    end_pt = fit_df.iloc[-1]
                    peak_t_idx = fit_df['Temperature_MK'].idxmax()
                    peak_t_pt = fit_df.loc[peak_t_idx]
                    
                    fig_phase.add_trace(go.Scatter(
                        x=[start_pt['Temperature_MK']], y=[start_pt['Emission_Measure_norm']],
                        mode='markers', marker=dict(color='blue', size=12, symbol='square'),
                        name=f"Flare Start ({start_pt['Time'].strftime('%H:%M')})", hovertext="Start"
                    ))
                    
                    fig_phase.add_trace(go.Scatter(
                        x=[peak_t_pt['Temperature_MK']], y=[peak_t_pt['Emission_Measure_norm']],
                        mode='markers', marker=dict(color='red', size=14, symbol='star'),
                        name=f"Peak Temp ({peak_t_pt['Time'].strftime('%H:%M')})", hovertext="Peak Temp"
                    ))
                    
                    fig_phase.add_trace(go.Scatter(
                        x=[end_pt['Temperature_MK']], y=[end_pt['Emission_Measure_norm']],
                        mode='markers', marker=dict(color='orange', size=12, symbol='circle'),
                        name=f"Flare End ({end_pt['Time'].strftime('%H:%M')})", hovertext="End"
                    ))
                    
                    fig_phase.update_layout(
                        template="plotly_dark",
                        height=450,
                        margin=dict(l=40, r=40, t=10, b=10),
                        xaxis=dict(title="Temperature (MK)"),
                        yaxis=dict(title="Emission Measure (norm)"),
                        showlegend=True,
                        legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.5)')
                    )
                    
                    st.plotly_chart(fig_phase, use_container_width=True)
                    
                st.info("💡 **Thermodynamic Analysis:** The Temperature rises first, peaking at 03:38 UTC, while the Emission Measure peaks later as more plasma is evaporated into the coronal loops. This produces the characteristic clockwise hysteresis loop in the T-EM phase space, showcasing the physical heating phase followed by the gradual radiative/conductive cooling phase.")
            else:
                st.error("Could not load spectral parameters from CSV.")
        
        if st.button("🚀 Run PyXspec Joint Fit (Placeholder)"):
            st.info("HEASoft Environment is still installing. This button will activate the XSPEC spectral fitting pipeline once completed.")
    else:
        if st.button("Reset View"):
            st.session_state.zoom_window = None

def main():
    init_session_state()
    
    with st.spinner("Initializing Phase 4 Tactical Screen..."):
        sim_df, catalog_df, ensemble_data, metrics_data = load_assets()
        
    st.sidebar.title("Simulation Controls")
    
    if metrics_data:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Ensemble Performance")
        st.sidebar.metric("Average Lead Time", f"{metrics_data['avg_lead_time_min']:.1f} min")
        st.sidebar.metric("True Positive Rate", f"{metrics_data['tpr_percent']:.1f}%")
        st.sidebar.metric("False Alarm Rate", f"{metrics_data['far_percent']:.1f}%")
        st.sidebar.caption(f"Evaluated on {metrics_data['true_positives'] + metrics_data['false_negatives']} historical flares.")
    
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
