import torch
import numpy as np

class TemporalExplainer:
    """
    Extracts attention weights and feature importance for the Temporal AI Engine.
    """
    def __init__(self, model):
        self.model = model
        self.model.eval()
        
    def get_attention_weights(self, sxr_x, hxr_x, physics_x):
        """
        Runs a forward pass and extracts the cross-attention and physics attention weights.
        """
        with torch.no_grad():
            # TCN encoding
            sxr_feat = self.model.sxr_tcn(sxr_x)
            hxr_feat = self.model.hxr_tcn(hxr_x)
            
            # Cross-attention weights
            _, sxr_to_hxr_weights, hxr_to_sxr_weights = self.model.fusion(sxr_feat, hxr_feat)
            
            # Physics attention
            _, phys_weights = self.model.physics_attention(physics_x)
            
        return {
            'sxr_to_hxr_attn': sxr_to_hxr_weights.cpu().numpy(),
            'hxr_to_sxr_attn': hxr_to_sxr_weights.cpu().numpy(),
            'physics_attn': phys_weights.cpu().numpy()
        }
        
    def integrated_gradients(self, x_inputs, target_task='prob', steps=50):
        """
        Simplified Integrated Gradients for feature importance.
        x_inputs: Tuple of (sxr_x, hxr_x, physics_x)
        """
        # Baseline is zero tensors
        baselines = tuple(torch.zeros_like(x) for x in x_inputs)
        
        # We need gradients
        for x in x_inputs:
            x.requires_grad_(True)
            
        integrated_grads = []
        for x, baseline in zip(x_inputs, baselines):
            integrated_grads.append(torch.zeros_like(x))
            
        for alpha in np.linspace(0, 1, steps):
            interpolated_inputs = tuple(
                baseline + alpha * (x - baseline) 
                for x, baseline in zip(x_inputs, baselines)
            )
            
            for x_interp in interpolated_inputs:
                x_interp.requires_grad_(True)
                
            outputs = self.model(*interpolated_inputs)
            
            # Sum over batch for the target task output
            if target_task == 'class':
                target_out = outputs['class_logits'].sum()
            else:
                target_out = outputs[target_task].sum()
            
            self.model.zero_grad()
            target_out.backward()
            
            for i, x_interp in enumerate(interpolated_inputs):
                integrated_grads[i] += x_interp.grad / steps
                
        # Multiply by (input - baseline)
        attributions = tuple(
            (x - baseline) * ig 
            for x, baseline, ig in zip(x_inputs, baselines, integrated_grads)
        )
        
        return {
            'sxr_attribution': attributions[0].detach().cpu().numpy(),
            'hxr_attribution': attributions[1].detach().cpu().numpy(),
            'physics_attribution': attributions[2].detach().cpu().numpy(),
        }
