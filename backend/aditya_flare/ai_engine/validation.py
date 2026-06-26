import torch
import numpy as np

class RobustnessValidator:
    """
    Validation suite for testing model robustness against noise, missing data, and cross-mission anomalies.
    """
    def __init__(self, model):
        self.model = model
        self.model.eval()
        
    def add_gaussian_noise(self, x, snr_db=20):
        """ Adds Gaussian noise to the input tensor based on a target Signal-to-Noise Ratio (SNR) """
        signal_power = torch.mean(x ** 2)
        snr_linear = 10 ** (snr_db / 10)
        noise_power = signal_power / snr_linear
        noise = torch.randn_like(x) * torch.sqrt(noise_power)
        return x + noise
        
    def simulate_missing_data(self, x, missing_rate=0.1):
        """ Randomly masks (zeros out) a percentage of the input time steps """
        mask = torch.rand(x.shape[:2], device=x.device) > missing_rate
        mask = mask.unsqueeze(-1).expand_as(x)
        return x * mask.float()

    def run_robustness_check(self, sxr_x, hxr_x, physics_x, metric_fn, target):
        """
        Runs predictions under various perturbations and calculates performance degradation.
        metric_fn: a function that takes (predictions_dict, target) and returns a scalar score (higher is better)
        """
        results = {}
        
        # 1. Baseline
        with torch.no_grad():
            base_out = self.model(sxr_x, hxr_x, physics_x)
            results['baseline_score'] = metric_fn(base_out, target)
            
        # 2. Gaussian Noise (Low SNR)
        noisy_sxr = self.add_gaussian_noise(sxr_x, snr_db=10)
        noisy_hxr = self.add_gaussian_noise(hxr_x, snr_db=10)
        noisy_phys = self.add_gaussian_noise(physics_x, snr_db=10)
        
        with torch.no_grad():
            noisy_out = self.model(noisy_sxr, noisy_hxr, noisy_phys)
            results['noise_score'] = metric_fn(noisy_out, target)
            
        # 3. Missing Data (20% missing)
        drop_sxr = self.simulate_missing_data(sxr_x, missing_rate=0.2)
        drop_hxr = self.simulate_missing_data(hxr_x, missing_rate=0.2)
        drop_phys = self.simulate_missing_data(physics_x, missing_rate=0.2)
        
        with torch.no_grad():
            drop_out = self.model(drop_sxr, drop_hxr, drop_phys)
            results['missing_data_score'] = metric_fn(drop_out, target)
            
        # Calculate degradations
        if results['baseline_score'] > 0:
            results['noise_degradation'] = (results['baseline_score'] - results['noise_score']) / results['baseline_score']
            results['missing_data_degradation'] = (results['baseline_score'] - results['missing_data_score']) / results['baseline_score']
        else:
            results['noise_degradation'] = 0.0
            results['missing_data_degradation'] = 0.0
            
        return results
