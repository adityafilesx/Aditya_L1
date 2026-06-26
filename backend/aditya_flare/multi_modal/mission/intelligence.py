import torch
import torch.nn as nn
import logging

logger = logging.getLogger("AdityaL1.MultiModal.MissionIntelligence")

class FoundationEmbeddingHead(nn.Module):
    """
    Module 9: Foundation Embeddings.
    Projects the fused multi-modal representation into a shared latent space
    useful for Retrieval, Similarity Search, Clustering, and Anomaly Detection.
    """
    def __init__(self, fused_dim=128, foundation_dim=256):
        super(FoundationEmbeddingHead, self).__init__()
        self.projection = nn.Sequential(
            nn.Linear(fused_dim, foundation_dim),
            nn.LayerNorm(foundation_dim),
            nn.ReLU(),
            nn.Linear(foundation_dim, foundation_dim)
        )
        
    def forward(self, fused_rep):
        # Normalize the embedding to unit length for cosine similarity retrieval
        embed = self.projection(fused_rep)
        return torch.nn.functional.normalize(embed, p=2, dim=1)

class MissionIntelligenceEngine(nn.Module):
    """
    Module 10: Mission Intelligence (Phase 5C Revision).
    Computes evidence-based risk indicators:
    - Mission Risk Index
    - Radiation Context Index
    - HF Blackout Risk Index
    """
    def __init__(self, foundation_dim=256):
        super(MissionIntelligenceEngine, self).__init__()
        self.foundation_head = FoundationEmbeddingHead(fused_dim=128, foundation_dim=foundation_dim)
        
        # Risk Index Heads (Output scale 0-10)
        self.mission_risk_head = nn.Sequential(nn.Linear(foundation_dim, 64), nn.ReLU(), nn.Linear(64, 1))
        self.radiation_context_head = nn.Sequential(nn.Linear(foundation_dim, 64), nn.ReLU(), nn.Linear(64, 1))
        self.hf_blackout_risk_head = nn.Sequential(nn.Linear(foundation_dim, 64), nn.ReLU(), nn.Linear(64, 1))
        
    def forward(self, fused_rep):
        foundation_emb = self.foundation_head(fused_rep)
        
        # Using sigmoid * 10 to keep indices bounded 0-10
        mri = torch.sigmoid(self.mission_risk_head(foundation_emb)).squeeze(-1) * 10.0
        rci = torch.sigmoid(self.radiation_context_head(foundation_emb)).squeeze(-1) * 10.0
        hf = torch.sigmoid(self.hf_blackout_risk_head(foundation_emb)).squeeze(-1) * 10.0
        
        return {
            'foundation_embedding': foundation_emb,
            'mission_risk_index': mri,
            'radiation_context_index': rci,
            'hf_blackout_risk_index': hf
        }
        
    def generate_mission_recommendations(self, indices):
        mri = indices['mission_risk_index'].item()
        rci = indices['radiation_context_index'].item()
        hf = indices['hf_blackout_risk_index'].item()
        
        recommendations = []
        
        if hf > 8.0:
            recommendations.append("CRITICAL: Severe HF Blackout Risk.")
        elif hf > 5.0:
            recommendations.append("WARNING: Elevated HF Blackout Risk.")
            
        if mri > 7.0:
            recommendations.append("ALERT: High Mission Risk Index. Context suggests eruptive event.")
            
        if rci > 6.0:
            recommendations.append("WARNING: High Radiation Context Index. Monitor proton fluxes closely.")
            
        if not recommendations:
            recommendations.append("NOMINAL: Space Weather indices are stable.")
            
        return recommendations

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Simulate a fused representation from Module 6
    dummy_fused_rep = torch.randn(1, 128)
    
    engine = MissionIntelligenceEngine()
    
    preds = engine(dummy_fused_rep)
    recs = engine.generate_mission_recommendations(preds)
    
    print("Mission Intelligence Output:")
    print(f"CME Probability: {preds['cme_prob'].item():.2f}")
    print(f"SEP Probability: {preds['sep_prob'].item():.2f}")
    print(f"HF Blackout Probability: {preds['hf_blackout_prob'].item():.2f}")
    
    print("\nMission Recommendations:")
    for r in recs:
        print("-", r)
