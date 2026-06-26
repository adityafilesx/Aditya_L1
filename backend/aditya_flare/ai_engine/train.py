import torch
import torch.optim as optim
from tqdm import tqdm
from .registry import ModelRegistry
from .models.multi_task import MultiTaskLoss

class AITrainer:
    """
    Training framework for the Temporal AI Engine.
    """
    def __init__(self, model, train_loader, val_loader, learning_rate=1e-3, device='cpu'):
        self.device = torch.device(device)
        self.model = model.to(self.device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = MultiTaskLoss(use_uncertainty_weighting=True).to(self.device)
        self.registry = ModelRegistry()

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        loss_components = {'loss_prob': 0, 'loss_flux': 0, 'loss_class': 0}
        
        for batch_idx, (x, y) in enumerate(self.train_loader):
            # Move to device
            x = x.to(self.device)
            # Assuming y has shape [Batch, 3] where y[:, 0] is prob, y[:, 1] is flux, y[:, 2] is class
            targets = {
                'prob_target': y[:, 0].float().to(self.device),
                'flux_target': y[:, 1].float().to(self.device),
                'class_target': y[:, 2].long().to(self.device)
            }
            
            # Since this is a demo/skeleton train, we split features evenly
            # In practice, we use actual indices for sxr, hxr, and physics
            sxr_dim = x.size(-1) // 3
            hxr_dim = sxr_dim
            sxr_x = x[:, :, :sxr_dim]
            hxr_x = x[:, :, sxr_dim:2*sxr_dim]
            physics_x = x[:, :, 2*sxr_dim:]
            
            self.optimizer.zero_grad()
            
            outputs = self.model(sxr_x, hxr_x, physics_x)
            loss, components = self.criterion(outputs, targets)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
            for k in loss_components:
                loss_components[k] += components[k]
                
        num_batches = len(self.train_loader)
        avg_loss = total_loss / num_batches
        avg_components = {k: v / num_batches for k, v in loss_components.items()}
        
        return avg_loss, avg_components

    def validate(self):
        self.model.eval()
        total_loss = 0
        loss_components = {'loss_prob': 0, 'loss_flux': 0, 'loss_class': 0}
        
        with torch.no_grad():
            for x, y in self.val_loader:
                x = x.to(self.device)
                targets = {
                    'prob_target': y[:, 0].float().to(self.device),
                    'flux_target': y[:, 1].float().to(self.device),
                    'class_target': y[:, 2].long().to(self.device)
                }
                
                sxr_dim = x.size(-1) // 3
                sxr_x = x[:, :, :sxr_dim]
                hxr_x = x[:, :, sxr_dim:2*sxr_dim]
                physics_x = x[:, :, 2*sxr_dim:]
                
                outputs = self.model(sxr_x, hxr_x, physics_x)
                loss, components = self.criterion(outputs, targets)
                
                total_loss += loss.item()
                for k in loss_components:
                    loss_components[k] += components[k]
                    
        num_batches = len(self.val_loader)
        if num_batches == 0: return 0.0, loss_components
        
        avg_loss = total_loss / num_batches
        avg_components = {k: v / num_batches for k, v in loss_components.items()}
        
        return avg_loss, avg_components

    def train(self, epochs=10, run_name="Temporal_AI_Run"):
        with self.registry.start_run(run_name=run_name):
            self.registry.log_params({"epochs": epochs, "learning_rate": self.optimizer.param_groups[0]['lr']})
            
            best_val_loss = float('inf')
            
            for epoch in range(epochs):
                train_loss, train_comps = self.train_epoch()
                val_loss, val_comps = self.validate()
                
                print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")
                
                metrics = {
                    "train_loss": train_loss,
                    "val_loss": val_loss,
                    **{f"train_{k}": v for k, v in train_comps.items()},
                    **{f"val_{k}": v for k, v in val_comps.items()}
                }
                self.registry.log_metrics(metrics, step=epoch)
                
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.registry.save_local_checkpoint(self.model, self.optimizer, epoch, "best_model.pth")
                    self.registry.log_model(self.model, "best_model")
                    
        print("Training complete.")
