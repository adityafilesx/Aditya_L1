import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiTaskLoss(nn.Module):
    """
    Joint loss layer combining probability (binary cross-entropy), 
    flux regression (MSE), classification loss (CrossEntropy),
    time-to-peak (MSE), lead-time (MSE), morphology (CrossEntropy), and confidence (MSE).
    """
    def __init__(self, use_uncertainty_weighting=False):
        super(MultiTaskLoss, self).__init__()
        self.use_uncertainty_weighting = use_uncertainty_weighting
        
        if use_uncertainty_weighting:
            # Learnable log variances for 7 tasks
            self.log_vars = nn.Parameter(torch.zeros(7))
        else:
            # Fixed weights
            self.register_buffer('weights', torch.ones(7))

    def forward(self, preds, targets):
        loss_prob = F.binary_cross_entropy(preds['prob'], targets['prob_target'])
        loss_flux = F.mse_loss(preds['flux'], targets['flux_target'])
        loss_class = F.cross_entropy(preds['class_logits'], targets['class_target'])
        loss_ttp = F.mse_loss(preds['time_to_peak'], targets['ttp_target'])
        loss_lead = F.mse_loss(preds['lead_time'], targets['lead_target'])
        loss_morph = F.cross_entropy(preds['morphology_logits'], targets['morph_target'])
        loss_conf = F.mse_loss(preds['confidence'], targets['conf_target'])
        
        losses = [loss_prob, loss_flux, loss_class, loss_ttp, loss_lead, loss_morph, loss_conf]
        
        if self.use_uncertainty_weighting:
            total_loss = sum(0.5 * torch.exp(-self.log_vars[i]) * losses[i] + 0.5 * self.log_vars[i] for i in range(7))
        else:
            total_loss = sum(self.weights[i] * losses[i] for i in range(7))
                         
        return total_loss, {
            'loss_prob': loss_prob.item(),
            'loss_flux': loss_flux.item(),
            'loss_class': loss_class.item(),
            'loss_ttp': loss_ttp.item(),
            'loss_lead': loss_lead.item(),
            'loss_morph': loss_morph.item(),
            'loss_conf': loss_conf.item()
        }

class MultiTaskHead(nn.Module):
    """
    Given a fused temporal representation, outputs probability, flux, class, 
    time to peak, lead time, morphology, and confidence.
    """
    def __init__(self, hidden_dim, num_classes=5, num_morphologies=4):
        super(MultiTaskHead, self).__init__()
        
        def build_head(out_dim, activation=None):
            layers = [nn.Linear(hidden_dim, hidden_dim // 2), nn.ReLU(), nn.Linear(hidden_dim // 2, out_dim)]
            if activation: layers.append(activation)
            return nn.Sequential(*layers)
            
        self.prob_head = build_head(1, nn.Sigmoid())
        self.flux_head = build_head(1)
        self.class_head = build_head(num_classes)
        self.ttp_head = build_head(1, nn.ReLU()) # Time to peak must be positive
        self.lead_head = build_head(1, nn.ReLU())
        self.morph_head = build_head(num_morphologies)
        self.conf_head = build_head(1, nn.Sigmoid())

    def forward(self, x):
        return {
            'prob': self.prob_head(x).squeeze(-1),
            'flux': self.flux_head(x).squeeze(-1),
            'class_logits': self.class_head(x),
            'time_to_peak': self.ttp_head(x).squeeze(-1),
            'lead_time': self.lead_head(x).squeeze(-1),
            'morphology_logits': self.morph_head(x),
            'confidence': self.conf_head(x).squeeze(-1)
        }
