import torch
import torch.nn as nn
import torchvision.models as models

class SolarVisionEncoder(nn.Module):
    """
    Module 5: Computer Vision Encoder for Solar Imagery.
    Extracts spatial embeddings from SDO AIA and HMI images.
    Uses a lightweight ResNet or Vision Transformer backbone.
    """
    def __init__(self, in_channels=6, embedding_dim=128, backbone_type='resnet18'):
        """
        in_channels: e.g., 5 AIA wavelengths + 1 HMI magnetogram
        """
        super(SolarVisionEncoder, self).__init__()
        self.embedding_dim = embedding_dim
        
        if backbone_type == 'resnet18':
            # Load a base resnet18 without pretrained weights since solar images are very different from ImageNet
            self.backbone = models.resnet18(pretrained=False)
            
            # Modify first conv layer to accept 'in_channels' instead of 3 (RGB)
            self.backbone.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
            
            # Replace the final fully connected layer to output our desired embedding dimension
            num_ftrs = self.backbone.fc.in_features
            self.backbone.fc = nn.Sequential(
                nn.Linear(num_ftrs, 512),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(512, embedding_dim)
            )
            
        else:
            raise NotImplementedError(f"Backbone {backbone_type} not currently implemented.")
            
        # Optional: Segmentation Heads for Active Regions, Coronal Holes, Filaments
        # In a full segmentation model (like UNet), this would branch off the feature maps.
        # Here we just output segmentation proxy scores from the embeddings.
        self.segmentation_proxy_head = nn.Sequential(
            nn.Linear(embedding_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 4), # 4 classes: AR, Coronal Hole, Filament, Loop
            nn.Sigmoid()
        )

    def forward(self, images):
        """
        images: Tensor of shape [Batch, Channels, Height, Width]
        Returns: Spatial Embeddings [Batch, embedding_dim], Segmentation proxy scores
        """
        # Extract features
        embeddings = self.backbone(images)
        
        # Predict spatial object presences
        seg_scores = self.segmentation_proxy_head(embeddings)
        
        return embeddings, seg_scores

def simulate_vision_extraction():
    """
    Simulate passing a batch of multi-wavelength SDO cutouts through the encoder.
    """
    batch_size = 8
    channels = 6 # 5 AIA + 1 HMI
    height = 256
    width = 256
    
    # Simulate a tensor of images
    dummy_images = torch.randn(batch_size, channels, height, width)
    
    model = SolarVisionEncoder(in_channels=channels, embedding_dim=128)
    
    # Extract
    model.eval()
    with torch.no_grad():
        embeddings, seg_scores = model(dummy_images)
        
    print(f"Input shape: {dummy_images.shape}")
    print(f"Extracted Vision Embeddings: {embeddings.shape}")
    print(f"Segmentation Proxy Scores: {seg_scores.shape}")
    return embeddings

if __name__ == "__main__":
    simulate_vision_extraction()
