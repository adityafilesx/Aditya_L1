# Event Association Engine

## Overview
The `EventAssociator` is a critical physics-based module within the Nowcasting Engine. Its responsibility is to take independent detection events from the SoLEXS and HEL1OS detectors and determine if they belong to the same underlying solar flare, creating a `UnifiedFlareEvent`.

## The Physics of Association
The core validation for association is based on the **Neupert Effect**, a well-established empirical relationship in solar physics which states that the hard X-ray flux (impulsive phase, observed by HEL1OS) is proportional to the time derivative of the soft X-ray flux (gradual phase, observed by SoLEXS):

`F_HXR(t) ∝ d/dt [F_SXR(t)]`

## Association Logic
1. **Temporal Overlap**: The engine first checks if a HEL1OS event occurs during the `PRE_FLARE` or early `ACTIVE` state of a SoLEXS event.
2. **Neupert Validation**: If temporal overlap is found, the engine compares the peak of the HEL1OS burst with the maximum derivative (steepest rise) of the SoLEXS flux. 
3. **Scoring**: A `neupert_score` (0.0 to 1.0) is calculated based on how closely the hard X-ray profile matches the soft X-ray derivative.
4. **Unification**: If the score exceeds a predefined threshold (e.g., 0.6) and the time window aligns, the two independent `DetectorEvents` are merged into a single `UnifiedFlareEvent`.
5. **Orphan Events**: If a SoLEXS event occurs without a corresponding HEL1OS burst, it is still cataloged (as many flares lack a strong impulsive phase). A HEL1OS burst without a SoLEXS rise is heavily penalized and often discarded as sensor noise or a non-flare transient, unless confidence is exceptionally high.

## Subsystem Integration
The Event Associator does not hold state itself. It is called by the `NowcastManager` every tick, evaluating the active events currently held by the detectors. Once a unified event is finalized (e.g., the flare ends), it is pushed to the `MasterCatalog`.
