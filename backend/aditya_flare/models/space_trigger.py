"""
Space-Segment Onboard Flare Trigger Model
Designed for: Spacecraft Payload Protection & Telemetry Reconfiguration
Hardware Targets: Radiation-hardened microprocessors (LEON3 / SPARC V8 at 20–50 MHz)
RAM Budget: <16 KB
Dependencies: Standard Python library only (zero external packages like NumPy, Pandas, or Scikit-Learn)
Arithmetic: Low-compute integer operations
"""

class SpaceOnboardTrigger:
    # State Machine Constants
    STATE_QUIET = 0
    STATE_WATCH = 1
    STATE_ALERT = 2

    def __init__(self, watch_threshold=30, alert_threshold=150, absolute_limit=400, cooldown_seconds=60):
        # Parameters (in counts/sec and counts/sec^2)
        self.watch_threshold = int(watch_threshold)  # Minimum dF/dt to enter WATCH
        self.alert_threshold = int(alert_threshold)  # Minimum dF/dt to enter ALERT from WATCH
        self.absolute_limit = int(absolute_limit)    # Absolute SXR count rate to force ALERT
        self.cooldown_seconds = int(cooldown_seconds)

        # State Variables
        self.state = self.STATE_QUIET
        self.peak_flux = 0
        self.alert_start_time = 0
        self.state_timer = 0

        # Circular buffer for raw counts (last 5 seconds) to calculate derivatives
        # Implemented using a simple list to avoid any library dependencies
        self.buffer_size = 5
        self.counts_buffer = []
        self.time_buffer = []

    def update(self, timestamp_seconds, sxr_counts):
        """
        Updates the state machine with a new 1Hz telemetry packet.
        Returns:
            int: Current state (0 = QUIET, 1 = WATCH, 2 = ALERT)
            float: Current derivative dF/dt (counts/sec^2)
        """
        # Ensure input is cast to integer for fixed-point safety
        counts = int(sxr_counts)
        t_sec = int(timestamp_seconds)

        # Append to circular buffer
        self.counts_buffer.append(counts)
        self.time_buffer.append(t_sec)
        if len(self.counts_buffer) > self.buffer_size:
            self.counts_buffer.pop(0)
            self.time_buffer.pop(0)

        # Ensure we have enough buffer data to calculate derivatives
        if len(self.counts_buffer) < 3:
            return self.state, 0.0

        # Calculate discrete derivatives (dF/dt) using last 2 points
        dt = self.time_buffer[-1] - self.time_buffer[-2]
        if dt <= 0:
            dt = 1
        df_dt = (self.counts_buffer[-1] - self.counts_buffer[-2]) / dt

        # Calculate second derivative (d2F/dt2) for curvature detection
        prev_dt = self.time_buffer[-2] - self.time_buffer[-3]
        if prev_dt <= 0:
            prev_dt = 1
        prev_df_dt = (self.counts_buffer[-2] - self.counts_buffer[-3]) / prev_dt
        d2f_dt2 = (df_dt - prev_df_dt) / dt

        # State Machine Transitions
        if self.state == self.STATE_QUIET:
            # Transition to WATCH: dF/dt exceeds watch_threshold
            if df_dt >= self.watch_threshold:
                self.state = self.STATE_WATCH
                self.state_timer = 0
                # print(f"[Onboard Trigger] QUIET -> WATCH at t={t_sec}s (dF/dt={df_dt})")
            # Absolute limit fallback
            elif counts >= self.absolute_limit:
                self.state = self.STATE_ALERT
                self.peak_flux = counts
                self.alert_start_time = t_sec

        elif self.state == self.STATE_WATCH:
            self.state_timer += dt
            
            # Transition to ALERT: strong derivative or convex rise (positive acceleration)
            if df_dt >= self.alert_threshold or (counts > 250 and d2f_dt2 > 5):
                self.state = self.STATE_ALERT
                self.peak_flux = counts
                self.alert_start_time = t_sec
                # print(f"[Onboard Trigger] WATCH -> ALERT at t={t_sec}s (dF/dt={df_dt}, d2F/dt2={d2f_dt2})")
            elif counts >= self.absolute_limit:
                self.state = self.STATE_ALERT
                self.peak_flux = counts
                self.alert_start_time = t_sec

            # Watch timeout: if activity subsides, return to QUIET
            elif df_dt < (self.watch_threshold // 2) and self.state_timer >= 10:
                self.state = self.STATE_QUIET
                # print(f"[Onboard Trigger] WATCH -> QUIET at t={t_sec}s (Activity subsided)")

        elif self.state == self.STATE_ALERT:
            # Track peak flux during alert phase
            if counts > self.peak_flux:
                self.peak_flux = counts

            # Hysteresis decay to return to QUIET: counts fall below 70% of peak observed
            # and we have passed the minimum cooldown window
            cooldown_passed = (t_sec - self.alert_start_time) >= self.cooldown_seconds
            decayed_below_threshold = counts < (self.peak_flux * 70 // 100)
            
            if cooldown_passed and (decayed_below_threshold or counts < 100):
                self.state = self.STATE_QUIET
                self.peak_flux = 0
                # print(f"[Onboard Trigger] ALERT -> QUIET at t={t_sec}s (Cooled down)")

        return self.state, df_dt
