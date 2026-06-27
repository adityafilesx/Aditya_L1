# Scientific Event Characterization & Physics Intelligence Platform (Milestone 3)

## Objective
The Physics Characterization Engine is the third major milestone of the Forecasting Engine. It transforms raw detected flare events (from the Nowcasting Engine) into physically characterized scientific phenomena.

A flare is no longer simply "an event that occurred at time T." It is a scientifically described event, possessing thermal profiles, spectral fits, plasma states, and adherence to physical laws (like the Neupert Effect).

## Architecture
The engine uses a modular, physics-first approach:

1. **Thermal Engine**: Derives peak temperatures, heating/cooling rates, and emission measures using soft X-ray fluxes (SoLEXS).
2. **NonThermal Engine**: Derives electron acceleration, burst energy, and impulsive phase duration from hard X-ray counts (HEL1OS).
3. **Spectral Engine**: Analyzes the energy spectrum to determine power-law indices and thermal vs. non-thermal fractions.
4. **Plasma Engine**: Characterizes the plasma state (density, pressure, total kinetic and thermal energy).
5. **Neupert Engine**: Calculates the Neupert effect correlation between the derivative of soft X-rays and the hard X-ray flux to determine the consistency of the flare with standard models.
6. **Classification Engine**: Maps the peak soft X-ray flux to the standard GOES classification scale (e.g., M2.3, X1.0).
7. **Characterization Engine**: Summarizes timing, duration, rise/decay times, and integrated fluxes.
8. **Derived Indices Engine**: Generates synthesized indices (Heating Index, Spectral Hardness, Thermal Dominance, Impulsiveness) that act as direct features for downstream Machine Learning models (Milestone 4).

## Data Flow
1. The **NowcastManager** detects a completed solar event via SoLEXS and HEL1OS, associates them, and creates a `MasterFlareEntry`.
2. It passes this entry and the recent flux history (300 ticks for SoLEXS, 120 for HEL1OS) to the **PhysicsManager**.
3. The **PhysicsManager** orchestrates the 8 sub-engines to produce a `PhysicsCharacterization` product.
4. The product is stored in the **PhysicsRepository** and assigned a unique `physics_product_id` (e.g., `PHY-20260625-1A2B3C`).
5. The `MasterFlareEntry` records this `physics_product_id` instead of embedding the entire object, keeping the catalog lightweight.
6. Downstream systems (Feature Store, Forecasting, API) retrieve the detailed physics by referencing the ID.

## Quality & Confidence
Unlike simple probabilities, this milestone introduces **Physics Quality**. Each sub-engine produces a quality object specifying data coverage, residual errors, and a `computation_status` (`GOOD`, `DEGRADED`, `INSUFFICIENT`). If a calculation fails due to insufficient data, the engine gracefully degrades instead of failing.

## Benchmarks & Health
The engine tracks its own operational benchmarks:
- **DetectorBenchmarkSnapshot**: Exposes live statistics on detection latency, false trigger rates, stability, and total tracked events.
- **DetectorHealthSnapshot**: Exposes memory, CPU, and operational fps.

## Upcoming Milestones
The output of this engine—the **Physics-Enriched Master Flare Catalog**—forms the exclusive input to the **Feature Engineering Platform (Milestone 4)**. No raw telemetry will bypass this physics layer.
