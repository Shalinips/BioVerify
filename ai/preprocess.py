import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


# -----------------------------
# Load ResNet-50
# -----------------------------
model = models.resnet50(
    weights=models.ResNet50_Weights.DEFAULT
)

model.eval()


# -----------------------------
# CBAM - Channel Attention
# -----------------------------
class ChannelAttention(nn.Module):

    def __init__(self, channels, reduction=16):
        super().__init__()

        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.fc = nn.Sequential(
            nn.Conv2d(channels, channels // reduction, 1),
            nn.ReLU(),
            nn.Conv2d(channels // reduction, channels, 1)
        )

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):

        avg = self.fc(self.avg_pool(x))
        maximum = self.fc(self.max_pool(x))

        attention = self.sigmoid(avg + maximum)

        return x * attention


# -----------------------------
# CBAM - Spatial Attention
# -----------------------------
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

        avg = torch.mean(x, dim=1, keepdim=True)
        maximum, _ = torch.max(x, dim=1, keepdim=True)

        combined = torch.cat([avg, maximum], dim=1)

        attention = self.sigmoid(
            self.conv(combined)
        )

        return x * attention


# -----------------------------
# Complete CBAM
# -----------------------------
class CBAM(nn.Module):

    def __init__(self, channels):
        super().__init__()

        self.channel_attention = ChannelAttention(channels)
        self.spatial_attention = SpatialAttention()

    def forward(self, x):

        x = self.channel_attention(x)
        x = self.spatial_attention(x)

        return x


cbam = CBAM(2048)
cbam.eval()


# -----------------------------
# Image preprocessing
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# -----------------------------
# Generate embedding
# -----------------------------
def get_embedding(image_path):

    image = Image.open(image_path).convert("RGB")

    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():

        x = model.conv1(image_tensor)
        x = model.bn1(x)
        x = model.relu(x)
        x = model.maxpool(x)

        x = model.layer1(x)
        x = model.layer2(x)
        x = model.layer3(x)
        x = model.layer4(x)

        # Apply CBAM
        x = cbam(x)

        # Global Average Pooling
        x = torch.mean(x, dim=(2, 3))

    return x


# -----------------------------
# User 001 images
# -----------------------------

face_path = (
    "BioVerify_Synthetic/images/"
    "face/user_001/session_1/"
    "face_user_001_s1_sample1.png"
)

fingerprint_path = (
    "BioVerify_Synthetic/images/"
    "fingerprint/user_001/session_1/"
    "fingerprint_user_001_s1_sample1.png"
)

iris_path = (
    "BioVerify_Synthetic/images/"
    "iris/user_001/session_1/"
    "iris_user_001_s1_sample1.png"
)


# -----------------------------
# Extract embeddings
# -----------------------------

face_embedding = get_embedding(face_path)

fingerprint_embedding = get_embedding(
    fingerprint_path
)

iris_embedding = get_embedding(
    iris_path
)


# -----------------------------
# Display results
# -----------------------------

print("\n========== MULTIMODAL EMBEDDINGS ==========")

print(
    "Face embedding:",
    face_embedding.shape
)

print(
    "Fingerprint embedding:",
    fingerprint_embedding.shape
)

print(
    "Iris embedding:",
    iris_embedding.shape
)

# -----------------------------
# Adaptive modality weighting
# -----------------------------

face_quality = 0.80
fingerprint_quality = 0.90
iris_quality = 0.70

total_quality = (
    face_quality
    + fingerprint_quality
    + iris_quality
)

face_weight = face_quality / total_quality
fingerprint_weight = fingerprint_quality / total_quality
iris_weight = iris_quality / total_quality

print("\n========== ADAPTIVE WEIGHTS ==========")

print("Face weight:", face_weight)
print("Fingerprint weight:", fingerprint_weight)
print("Iris weight:", iris_weight)

print(
    "Total weight:",
    face_weight + fingerprint_weight + iris_weight
)

# -----------------------------
# Adaptive Multimodal Fusion
# -----------------------------

fused_embedding = (
    face_weight * face_embedding
    + fingerprint_weight * fingerprint_embedding
    + iris_weight * iris_embedding
)

print("\n========== FUSED EMBEDDING ==========")
print("Fused embedding shape:", fused_embedding.shape)

# -----------------------------
# Multimodal Fusion Function
# -----------------------------

def get_fused_embedding(user, session):

    face_path = (
        "BioVerify_Synthetic/images/"
        f"face/{user}/{session}/"
        f"face_{user}_{session.replace('session_', 's')}_sample1.png"
    )

    fingerprint_path = (
        "BioVerify_Synthetic/images/"
        f"fingerprint/{user}/{session}/"
        f"fingerprint_{user}_{session.replace('session_', 's')}_sample1.png"
    )

    iris_path = (
        "BioVerify_Synthetic/images/"
        f"iris/{user}/{session}/"
        f"iris_{user}_{session.replace('session_', 's')}_sample1.png"
    )

    face_embedding = get_embedding(face_path)
    fingerprint_embedding = get_embedding(fingerprint_path)
    iris_embedding = get_embedding(iris_path)

    # Quality scores
    face_quality = 0.80
    fingerprint_quality = 0.90
    iris_quality = 0.70

    total_quality = (
        face_quality
        + fingerprint_quality
        + iris_quality
    )

    face_weight = face_quality / total_quality
    fingerprint_weight = fingerprint_quality / total_quality
    iris_weight = iris_quality / total_quality

    fused_embedding = (
        face_weight * face_embedding
        + fingerprint_weight * fingerprint_embedding
        + iris_weight * iris_embedding
    )

    return fused_embedding

  # -----------------------------
# Multimodal Score-Level Verification
# -----------------------------

def get_modality_template(user, session, modality):

    embeddings = []

    # Use all 3 samples from the session
    for sample in range(1, 4):

        image_path = (
            "BioVerify_Synthetic/images/"
            f"{modality}/{user}/{session}/"
            f"{modality}_{user}_{session.replace('session_', 's')}_sample{sample}.png"
        )

        embedding = get_embedding(image_path)

        embeddings.append(embedding)

    # Average the 3 samples
    template = torch.mean(
        torch.stack(embeddings),
        dim=0
    )

    # Normalize the session template
    template = torch.nn.functional.normalize(
        template,
        p=2,
        dim=1
    )

    return template


# -----------------------------
# Compare two biometric sessions
# -----------------------------

def compare_users(user_a, session_a, user_b, session_b):

    # Face templates
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

    # Fingerprint templates
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

    # Iris templates
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

    # -----------------------------
    # Individual similarities
    # -----------------------------

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

    # -----------------------------
    # Adaptive weights
    # -----------------------------

    face_quality = 0.80
    fingerprint_quality = 0.90
    iris_quality = 0.70

    total_quality = (
        face_quality
        + fingerprint_quality
        + iris_quality
    )

    face_weight = face_quality / total_quality
    fingerprint_weight = fingerprint_quality / total_quality
    iris_weight = iris_quality / total_quality

    # -----------------------------
    # Score-level fusion
    # -----------------------------

    final_score = (
        face_weight * face_score
        + fingerprint_weight * fingerprint_score
        + iris_weight * iris_score
    )

    return (
        face_score,
        fingerprint_score,
        iris_score,
        final_score
    )


# -----------------------------
# Prototype Verification Evaluation
# -----------------------------

users = [
    "user_001",
    "user_002",
    "user_003",
    "user_004",
    "user_005"
]


# -----------------------------
# Genuine Verification
# -----------------------------

print("\n========== GENUINE VERIFICATION ==========")

genuine_scores = []

for user in users:

    (
        face_score,
        fingerprint_score,
        iris_score,
        final_score
    ) = compare_users(
        user,
        "session_1",
        user,
        "session_2"
    )

    genuine_scores.append(final_score)

    print("\n", user)

    print("Face similarity:", face_score)
    print("Fingerprint similarity:", fingerprint_score)
    print("Iris similarity:", iris_score)
    print("Fused score:", final_score)


# -----------------------------
# Impostor Verification
# -----------------------------

print("\n========== IMPOSTOR VERIFICATION ==========")

impostor_scores = []

pairs = [
    ("user_001", "user_002"),
    ("user_001", "user_003"),
    ("user_002", "user_004"),
    ("user_003", "user_005"),
    ("user_004", "user_005")
]

for user_a, user_b in pairs:

    (
        face_score,
        fingerprint_score,
        iris_score,
        final_score
    ) = compare_users(
        user_a,
        "session_1",
        user_b,
        "session_1"
    )

    impostor_scores.append(final_score)

    print("\n", user_a, "vs", user_b)

    print("Face similarity:", face_score)
    print("Fingerprint similarity:", fingerprint_score)
    print("Iris similarity:", iris_score)
    print("Fused score:", final_score)


# -----------------------------
# Final Summary
# -----------------------------

genuine_average = (
    sum(genuine_scores)
    / len(genuine_scores)
)

impostor_average = (
    sum(impostor_scores)
    / len(impostor_scores)
)

print("\n========== FINAL SUMMARY ==========")

print(
    "Number of genuine pairs:",
    len(genuine_scores)
)

print(
    "Number of impostor pairs:",
    len(impostor_scores)
)

print(
    "Average genuine score:",
    genuine_average
)

print(
    "Average impostor score:",
    impostor_average
)

print(
    "Genuine - Impostor:",
    genuine_average - impostor_average
)

if genuine_average > impostor_average:

    print(
        "Overall separation direction: "
        "GENUINE > IMPOSTOR"
    )

else:

    print(
        "Overall separation direction: "
        "IMPOSTOR >= GENUINE"
    )