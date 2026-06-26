import random
from datetime import datetime, timezone

def generate_mock_telemetry():
    """Generates realistic-looking fallback telemetry data."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "timestamp": now,
        "goes_xrs_b": random.uniform(1e-7, 5e-5),
        "goes_xrs_a": random.uniform(1e-8, 5e-6),
        "solexs_sdd2_ctr": random.uniform(10, 5000),
        "helios_czt_broad_ctr": random.uniform(5, 1000),
        "proton_flux_>10MeV": random.uniform(0.1, 10),
        "kp_index": random.uniform(0, 5),
        "sunspot_count": random.randint(10, 150)
    }

def generate_mock_physics():
    """Generates realistic-looking fallback physics features."""
    return {
        "temperature_mk": random.uniform(2.0, 25.0),
        "emission_measure_norm": random.uniform(1e47, 1e49),
        "neupert_score": random.uniform(-0.5, 0.95),
        "spectral_centroid": random.uniform(0.1, 10.0),
        "spectral_flatness": random.uniform(0.01, 0.9),
        "spectral_rolloff": random.uniform(1.0, 20.0),
        "shannon_entropy": random.uniform(1.0, 8.0)
    }

def generate_mock_forecast():
    """Generates realistic-looking fallback forecast data."""
    prob = random.uniform(0.01, 0.99)
    goes_classes = ["A", "B", "C", "M", "X"]
    flux_class = random.choices(goes_classes, weights=[30, 40, 20, 8, 2])[0] + str(round(random.uniform(1.0, 9.9), 1))
    return {
        "probability": prob,
        "estimated_flux": random.uniform(1e-7, 1e-3),
        "estimated_goes_class": flux_class,
        "confidence": random.uniform(0.7, 0.99)
    }
