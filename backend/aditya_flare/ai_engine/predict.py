import torch
import time

class RealTimePredictor:
    """
    Highly optimized inference engine tailored for <50ms prediction.
    """
    def __init__(self, model, device='cpu'):
        self.device = torch.device(device)
        self.model = model.to(self.device)
        self.model.eval()
        
        # We attempt to use torch.compile for optimization on newer PyTorch versions
        # fallback to raw model if torch.compile is not available or fails
        try:
            self.model = torch.compile(self.model)
        except Exception:
            pass

    def predict(self, sxr_x, hxr_x, physics_x):
        """
        Expects numpy arrays or torch tensors of shape [1, Time, Features]
        """
        start_time = time.perf_counter()
        
        if not isinstance(sxr_x, torch.Tensor):
            sxr_x = torch.tensor(sxr_x, dtype=torch.float32).to(self.device)
            hxr_x = torch.tensor(hxr_x, dtype=torch.float32).to(self.device)
            physics_x = torch.tensor(physics_x, dtype=torch.float32).to(self.device)
            
        with torch.no_grad():
            outputs = self.model(sxr_x, hxr_x, physics_x)
            
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        
        results = {
            'prob': outputs['prob'].item(),
            'flux': outputs['flux'].item(),
            'class': torch.argmax(outputs['class_logits'], dim=-1).item(),
            'latency_ms': latency_ms
        }
        
        if latency_ms > 50:
            print(f"Warning: Inference took {latency_ms:.2f}ms, which exceeds the 50ms budget.")
            
        return results
