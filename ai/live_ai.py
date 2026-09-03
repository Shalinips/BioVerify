import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image


# ============================================================
# Load ResNet-50
# ============================================================

model = models.resnet50(
    weights=models.ResNet50_Weights.DEFAULT
)

model.eval()


# ============================================================
# CBAM - Channel Attention
# ============================================================

import torch.nn as nn


class ChannelAttention(nn.Module):

    def __init__(self, channels, reduction=16):

        super().__init__()

        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.fc = nn.Sequential(
            nn.Conv2d(
                channels,
                channels // reduction,
                1
            ),

            nn.ReLU(),

            nn.Conv2d(
                channels // reduction,
                channels,
                1
            )
        )

        self.sigmoid = nn.Sigmoid()


    def forward(self, x):

        avg = self.fc(
            self.avg_pool(x)
        )

        maximum = self.fc(
            self.max_pool(x)
        )

        attention = self.sigmoid(
            avg + maximum
        )

        return x * attention


# ============================================================
# CBAM - Spatial Attention
# ============================================================

class SpatialAttention(nn.Module):

    def __init__(self):

        super().__init__()

        self.conv = nn.Conv2d(
            2,
            1,
            kernel_size=7,
            padding=3
        )

        self.sigmoid = nn.Sigmoid()


    def forward(self, x):

        avg = torch.mean(
            x,
            dim=1,
            keepdim=True
        )

        maximum, _ = torch.max(
            x,
            dim=1,
            keepdim=True
        )

        combined = torch.cat(
            [avg, maximum],
            dim=1
        )

        attention = self.sigmoid(
            self.conv(combined)
        )

        return x * attention


# ============================================================
# Complete CBAM
# ============================================================

class CBAM(nn.Module):

    def __init__(self, channels):

        super().__init__()

        self.channel_attention = (
            ChannelAttention(channels)
        )

        self.spatial_attention = (
            SpatialAttention()
        )


    def forward(self, x):

        x = self.channel_attention(x)

        x = self.spatial_attention(x)

        return x


cbam = CBAM(2048)

cbam.eval()


# ============================================================
# Image Preprocessing
# ============================================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# Generate Embedding
# ============================================================

def get_embedding(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")


    image_tensor = transform(
        image
    ).unsqueeze(0)


    with torch.no_grad():

        x = model.conv1(
            image_tensor
        )

        x = model.bn1(x)

        x = model.relu(x)

        x = model.maxpool(x)

        x = model.layer1(x)

        x = model.layer2(x)

        x = model.layer3(x)

        x = model.layer4(x)

        # CBAM
        x = cbam(x)

        # Global Average Pooling
        x = torch.mean(
            x,
            dim=(2, 3)
        )

        # Normalize embedding
        x = F.normalize(
            x,
            p=2,
            dim=1
        )

    return x


# ============================================================
# Create 3-Sample Modality Template
# ============================================================

def get_modality_template(
    user,
    session,
    modality
):

    embeddings = []


    for sample in range(1, 4):

        image_path = (

            "BioVerify_Synthetic/images/"

            f"{modality}/{user}/{session}/"

            f"{modality}_"
            f"{user}_"
            f"{session.replace('session_', 's')}_"
            f"sample{sample}.png"

        )


        embedding = get_embedding(
            image_path
        )


        embeddings.append(
            embedding
        )


    # Average the three samples
    template = torch.mean(
        torch.stack(
            embeddings
        ),
        dim=0
    )


    # Normalize final template
    template = F.normalize(
        template,
        p=2,
        dim=1
    )


    return template


# ============================================================
# Compare Two Users / Sessions
# ============================================================

def compare_users(
    user_a,
    session_a,
    user_b,
    session_b
):

    # --------------------------------------------------------
    # Face
    # --------------------------------------------------------

    face_a = get_modality_template(
        user_a,
        session_a,
        "face"
    )

    face_b = get_modality_template(
        user_b,
        session_b,
        "face"
    )


    # --------------------------------------------------------
    # Fingerprint
    # --------------------------------------------------------

    fingerprint_a = get_modality_template(
        user_a,
        session_a,
        "fingerprint"
    )

    fingerprint_b = get_modality_template(
        user_b,
        session_b,
        "fingerprint"
    )


    # --------------------------------------------------------
    # Iris
    # --------------------------------------------------------

    iris_a = get_modality_template(
        user_a,
        session_a,
        "iris"
    )

    iris_b = get_modality_template(
        user_b,
        session_b,
        "iris"
    )


    # --------------------------------------------------------
    # Individual Similarity Scores
    # --------------------------------------------------------

    face_score = torch.cosine_similarity(
        face_a,
        face_b
    ).item()


    fingerprint_score = torch.cosine_similarity(
        fingerprint_a,
        fingerprint_b
    ).item()


    iris_score = torch.cosine_similarity(
        iris_a,
        iris_b
    ).item()


    # --------------------------------------------------------
    # Adaptive Quality Weights
    # --------------------------------------------------------

    face_quality = 0.80

    fingerprint_quality = 0.90

    iris_quality = 0.70


    total_quality = (

        face_quality
        + fingerprint_quality
        + iris_quality

    )


    face_weight = (
        face_quality
        / total_quality
    )


    fingerprint_weight = (
        fingerprint_quality
        / total_quality
    )


    iris_weight = (
        iris_quality
        / total_quality
    )


    # --------------------------------------------------------
    # Multimodal Score Fusion
    # --------------------------------------------------------

    fused_score = (

        face_weight
        * face_score

        +

        fingerprint_weight
        * fingerprint_score

        +

        iris_weight
        * iris_score

    )


    return (

        face_score,
        fingerprint_score,
        iris_score,
        fused_score

    )