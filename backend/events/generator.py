import asyncio
import random
import datetime
from datetime import timezone
from backend.events.models import (
    MissionState, TelemetryState, PhysicsState, ForecastState, 
    ModelState, AlertEvent, DigitalTwinState
)
from backend.events.mission_bus import mission_bus
from backend.api.state import app_state

class MissionStateGenerator:
    def __init__(self):
        self.running = False
        self.state = MissionState()
        self.event_counter = 0

    async def start(self):
        if self.running:
            return
        self.running = True
        
        # Start individual generation loops
        asyncio.create_task(self._generate_telemetry())
        asyncio.create_task(self._generate_physics())
        asyncio.create_task(self._generate_forecast())
        asyncio.create_task(self._generate_digital_twin())
        asyncio.create_task(self._generate_system_metrics())
        asyncio.create_task(self._generate_alerts())
        asyncio.create_task(self._publish_mission_state())

    async def stop(self):
        self.running = False

    async def _generate_telemetry(self):
        while self.running:
            self.state.telemetry.timestamp = datetime.datetime.now(timezone.utc).isoformat()
            self.state.telemetry.solexs_sdd2_ctr = max(0.0, self.state.telemetry.solexs_sdd2_ctr + random.uniform(-5.0, 5.0) + (1.0 if self.state.state > 0 else 0))
            if self.state.telemetry.solexs_sdd2_ctr < 5: self.state.telemetry.solexs_sdd2_ctr = 25.0
            
            self.state.telemetry.helios_czt_broad_ctr = max(0.0, self.state.telemetry.helios_czt_broad_ctr + random.uniform(-2.0, 2.0))
            if self.state.telemetry.helios_czt_broad_ctr < 1: self.state.telemetry.helios_czt_broad_ctr = 12.0
            
            # Simulate flare rise if in WATCH or ALERT
            flux_base = 1e-7
            if self.state.state == 1:
                flux_base = 1e-6 + random.uniform(0, 5e-6)
            elif self.state.state == 2:
                flux_base = 1e-5 + random.uniform(0, 5e-5)
            
            self.state.telemetry.goes_xrs_b = flux_base * (1.0 + random.uniform(-0.1, 0.1))
            self.state.telemetry.proton_flux_10MeV = max(0.0, self.state.telemetry.proton_flux_10MeV + random.uniform(-0.01, 0.05))
            
            await mission_bus.publish("telemetry", self.state.telemetry.model_dump())
            await asyncio.sleep(1) # Frequency: 1 second

    async def _generate_physics(self):
        while self.running:
            self.state.physics.temperature_mk = 10.0 + (self.state.state * 5.0) + random.uniform(-0.5, 0.5)
            self.state.physics.neupert_score = min(1.0, max(0.0, self.state.physics.neupert_score + random.uniform(-0.05, 0.05)))
            self.state.physics.emission_measure_norm = 1.0e48 * (1.0 + random.uniform(-0.1, 0.1) + self.state.state)
            self.state.physics.spectral_centroid = 0.5 + random.uniform(-0.1, 0.1)
            self.state.physics.shannon_entropy = 0.8 + random.uniform(-0.05, 0.05)
            
            await mission_bus.publish("physics", self.state.physics.model_dump())
            await asyncio.sleep(5) # Frequency: 5 seconds

    async def _generate_forecast(self):
        while self.running:
            if self.state.state == 0:
                self.state.forecast.probability = min(1.0, max(0.0, self.state.forecast.probability + random.uniform(-0.02, 0.05)))
                if self.state.forecast.probability > 0.6:
                    self.state.state = 1 # Elevate to WATCH
                    self.state.forecast.estimated_goes_class = "M-Class"
            elif self.state.state == 1:
                self.state.forecast.probability = min(1.0, max(0.0, self.state.forecast.probability + random.uniform(-0.05, 0.1)))
                if self.state.forecast.probability > 0.85:
                    self.state.state = 2 # Elevate to ALERT
                    self.state.forecast.estimated_goes_class = "X-Class"
            else:
                self.state.forecast.probability = min(1.0, max(0.5, self.state.forecast.probability + random.uniform(-0.05, 0.05)))
                # Occasionally drop back down
                if random.random() < 0.05:
                    self.state.state = 0
                    self.state.forecast.estimated_goes_class = "Quiet"
                    self.state.forecast.probability = 0.1

            self.state.forecast.confidence = 0.8 + random.uniform(0, 0.15)
            self.state.models.ensemble_status = "ONLINE"
            self.state.models.xgb_status = "ONLINE"
            self.state.models.ai_temporal_status = "ONLINE"
            
            await mission_bus.publish("forecast", self.state.forecast.model_dump())
            await asyncio.sleep(5) # Frequency: 5 seconds

    async def _generate_digital_twin(self):
        while self.running:
            self.state.digital_twin.similarity_score = min(1.0, max(0.8, self.state.digital_twin.similarity_score + random.uniform(-0.01, 0.01)))
            self.state.digital_twin.flux_delta = max(0.0, random.uniform(0.001, 0.005))
            
            await mission_bus.publish("digital_twin", self.state.digital_twin.model_dump())
            await asyncio.sleep(5) # Frequency: 5 seconds

    async def _generate_system_metrics(self):
        while self.running:
            self.state.system_metrics["cpu"] = int(max(10, min(100, self.state.system_metrics["cpu"] + random.uniform(-5, 5))))
            self.state.system_metrics["ram"] = int(max(20, min(100, self.state.system_metrics["ram"] + random.uniform(-2, 2))))
            self.state.system_metrics["gpu"] = int(max(0, min(100, self.state.system_metrics["gpu"] + random.uniform(-10, 10))))
            
            await mission_bus.publish("system", self.state.system_metrics)
            await asyncio.sleep(2) # Frequency: 2 seconds

    async def _generate_alerts(self):
        while self.running:
            # Randomly generate an alert
            if random.random() < 0.1: # 10% chance every 3 seconds
                self.event_counter += 1
                severities = ["INFO", "WARNING", "CRITICAL"]
                types = ["SYSTEM", "TELEMETRY", "PHYSICS", "AI"]
                
                new_alert = AlertEvent(
                    id=f"EVT-{self.event_counter:04d}",
                    timestamp=datetime.datetime.now(timezone.utc).isoformat(),
                    severity=random.choice(severities),
                    type=random.choice(types),
                    description=f"Automated event anomaly detected on channel {random.choice(types)}"
                )
                
                self.state.alerts.insert(0, new_alert)
                if len(self.state.alerts) > 20:
                    self.state.alerts.pop()
                    
                await mission_bus.publish("alerts", new_alert.model_dump())
                
            await asyncio.sleep(3)
            
    async def _publish_mission_state(self):
        while self.running:
            self.state.clock_utc = datetime.datetime.now(timezone.utc).strftime("%H:%M:%S")
            # Update recommendations based on state
            if self.state.state == 0:
                self.state.recommendations = ["Maintain Science Operations"]
                self.state.confidence_bounds = [0.9, 0.95]
            elif self.state.state == 1:
                self.state.recommendations = ["Prepare for High Cadence Mode", "Verify HEL1OS calibration"]
                self.state.confidence_bounds = [0.75, 0.85]
            else:
                self.state.recommendations = ["INITIATE SUIT HIGH-CADENCE SEQUENCE", "Alert payload operators"]
                self.state.confidence_bounds = [0.85, 0.92]
                
            await mission_bus.publish("mission_state", self.state.model_dump())
            await asyncio.sleep(1) # Frequency: 1 second

generator = MissionStateGenerator()
