<div align="center">

# 🛡️ BioVerify

## Deep Biometric Verification Using Blockchain and Adaptive Attention Networks

_A multimodal biometric verification system combining Face, Fingerprint, and Iris recognition with deep learning, adaptive attention, and blockchain technology._

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep_Learning-red?style=for-the-badge&logo=pytorch)
![ResNet](https://img.shields.io/badge/ResNet--50-Feature_Extraction-purple?style=for-the-badge)
![CBAM](https://img.shields.io/badge/CBAM-Adaptive_Attention-teal?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![Solidity](https://img.shields.io/badge/Solidity-Smart_Contract-gray?style=for-the-badge&logo=solidity)
![Ethereum](https://img.shields.io/badge/Ethereum-Sepolia-blue?style=for-the-badge&logo=ethereum)
![Web3.py](https://img.shields.io/badge/Web3.py-Blockchain-purple?style=for-the-badge)

**A prototype biometric verification platform that combines three biometric modalities with deep feature extraction, adaptive attention, similarity-based verification, and blockchain-backed integrity recording.**

</div>

---

# 📑 Table of Contents

- [📖 Project Overview](#-project-overview)
- [🎯 Problem Statement](#-problem-statement)
- [💡 Proposed Solution](#-proposed-solution)
- [✨ Key Features](#-key-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [🏗️ System Architecture](#️-system-architecture)
- [🧠 AI Methodology](#-ai-methodology)
- [🔗 Blockchain Integration](#-blockchain-integration)
- [📂 Project Structure](#-project-structure)
- [📊 Dataset](#-dataset)
- [⚙️ Installation Guide](#️-installation-guide)
- [▶️ Application Workflow](#️-application-workflow)
- [🧠 Concepts Demonstrated](#-concepts-demonstrated)
- [🔐 Security Considerations](#-security-considerations)
- [🚀 Future Enhancements](#-future-enhancements)
- [👩‍💻 About the Project](#-about-the-project)
- [📄 License](#-license)

---

# 📖 Project Overview

BioVerify is a **multimodal biometric verification system** designed to verify a user's identity using multiple biometric modalities.

The system combines:

- 👤 Face
- 🖐️ Fingerprint
- 👁️ Iris

Instead of depending on a single biometric characteristic, BioVerify combines information from multiple modalities to obtain a more robust verification decision.

The deep learning pipeline uses **ResNet-50** for feature extraction and **CBAM (Convolutional Block Attention Module)** for adaptive attention.

The extracted biometric representations are converted into embeddings and compared using **cosine similarity**. Individual similarity scores are then combined using weighted multimodal fusion to obtain a final verification score.

After verification, a **SHA-256 hash** is generated as an integrity identifier for the verification record. The record is then submitted to a Solidity smart contract deployed on the **Ethereum Sepolia test network**.

---

# 🎯 Problem Statement

Traditional biometric verification systems may depend on a single biometric modality.

However, individual biometric modalities can be affected by different conditions.

For example:

- Face recognition can be affected by lighting, pose, and image quality.
- Fingerprint recognition can be affected by sensor quality and finger conditions.
- Iris recognition can be affected by image quality and acquisition conditions.

Another challenge is maintaining the integrity and traceability of verification records.

This project addresses these challenges by combining multiple biometric modalities with deep learning and blockchain-based record integrity.

---

# 💡 Proposed Solution

BioVerify provides an integrated biometric verification workflow.

The system:

1. Accepts biometric samples from Face, Fingerprint, and Iris modalities.
2. Preprocesses the biometric images.
3. Extracts deep features using ResNet-50.
4. Applies CBAM-based adaptive attention.
5. Generates biometric embeddings.
6. Calculates individual cosine similarity scores.
7. Combines the scores using weighted multimodal fusion.
8. Compares the final score with a predefined threshold.
9. Generates a SHA-256 integrity hash.
10. Records the verification information through a Solidity smart contract.
11. Stores the verification record on Ethereum Sepolia.
12. Retrieves the blockchain record using the user ID.

---

# ✨ Key Features

- 🔐 Multimodal biometric verification
- 👤 Face recognition
- 🖐️ Fingerprint recognition
- 👁️ Iris recognition
- 🧠 ResNet-50 deep feature extraction
- 🎯 CBAM adaptive attention
- 📊 2048-dimensional biometric embeddings
- 🔢 Cosine similarity calculation
- ⚖️ Weighted multimodal fusion
- ✅ Threshold-based verification
- #️⃣ SHA-256 integrity hashing
- ⛓️ Solidity smart contract integration
- 🌐 Ethereum Sepolia testnet
- 🦊 MetaMask wallet integration
- 🐍 Flask backend API
- 🔗 Web3.py blockchain communication
- 📋 User-specific blockchain record retrieval
- 🖥️ Web-based verification interface

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Deep Learning | PyTorch |
| Feature Extraction | ResNet-50 |
| Attention Mechanism | CBAM |
| Image Processing | NumPy, OpenCV |
| Backend | Flask |
| Blockchain Communication | Web3.py |
| Smart Contract | Solidity |
| Blockchain Network | Ethereum Sepolia |
| Wallet | MetaMask |
| Smart Contract IDE | Remix IDE |
| Frontend | HTML, CSS, JavaScript |
| Development Environment | Visual Studio Code |
| Version Control | Git |
| Repository Hosting | GitHub |

---

# 🏗️ System Architecture

```text
                         +----------------------+
                         |        User          |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  BioVerify Frontend  |
                         |   HTML/CSS/JavaScript |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |     Flask Backend    |
                         +----------+-----------+
                                    |
                                    v
                    +---------------+---------------+
                    |               |               |
                    v               v               v
                Face Image    Fingerprint Image   Iris Image
                    |               |               |
                    +---------------+---------------+
                                    |
                                    v
                         +----------------------+
                         |    Preprocessing     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |      ResNet-50       |
                         |  Feature Extraction  |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |        CBAM          |
                         | Channel + Spatial    |
                         |      Attention       |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  2048-D Embeddings   |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  Cosine Similarity   |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Individual Scores    |
                         | Face / FP / Iris     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Weighted Multimodal  |
                         |       Fusion         |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Final Similarity     |
                         |       Score          |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Threshold Comparison |
                         +----------+-----------+
                                    |
                         +----------+----------+
                         |                     |
                         v                     v
                    VERIFIED               REJECTED
                         |
                         v
                  +-------------+
                  |  SHA-256    |
                  |    Hash     |
                  +------+------+ 
                         |
                         v
                  +-------------+
                  |  Web3.py    |
                  +------+------+
                         |
                         v
                  +-------------+
                  |   Solidity  |
                  | Smart Contract
                  +------+------+
                         |
                         v
                  +-------------+
                  | Ethereum    |
                  |   Sepolia   |
                  +-------------+

AI Methodology

1. Preprocessing
The biometric dataset is organized according to user, session, and biometric modality.
The preprocessing stage prepares the biometric images in a consistent format before feature extraction.

2. ResNet-50 Feature Extraction
ResNet-50 is used as the deep learning backbone.
It extracts high-level feature representations from the biometric images.
The extracted features provide the basis for generating biometric embeddings.

3. CBAM Adaptive Attention
CBAM stands for:
Convolutional Block Attention Module
CBAM contains two sequential attention mechanisms.
i)Channel Attention
Channel attention determines which feature channels are important.
In simple terms:
Channel Attention = WHAT features are important?
ii)Spatial Attention
Spatial attention determines which regions of the feature map are important.
In simple terms:
Spatial Attention = WHERE are the important features?
The combination allows the network to focus on more informative biometric features.

4. Biometric Embeddings
After feature extraction and attention processing, the biometric representations are converted into 2048-dimensional embeddings.
Separate embeddings are generated for:

Face
Fingerprint
Iris

5. Cosine Similarity
The embeddings are compared using cosine similarity.
Individual similarity scores are calculated for each biometric modality.

Face Similarity
Fingerprint Similarity
Iris Similarity

These scores are then used for multimodal fusion.

6. Weighted Multimodal Fusion
The individual biometric similarity scores are combined using modality weights.
The prototype uses:

Modality	Weight
Face	0.3333
Fingerprint	0.3750
Iris	0.2917

The weights sum to approximately 1.

The final score is calculated as:

Final Score =
(Face Score × Face Weight)
+
(Fingerprint Score × Fingerprint Weight)
+
(Iris Score × Iris Weight)

7. Verification Threshold
The prototype uses a verification threshold of:

0.965

Decision rule:

If Final Score >= 0.965
        → VERIFIED

If Final Score < 0.965
        → REJECTED


🔗 Blockchain Integration

After the biometric verification stage, BioVerify generates a SHA-256 hash for the verification record.
SHA-256 provides a fixed-length cryptographic hash that acts as an integrity identifier.
The Flask backend communicates with the Solidity smart contract using Web3.py.
The smart contract is deployed on:
Ethereum Sepolia Test Network

The blockchain record contains:

User ID
Verification hash
Verification result
Timestamp

The smart contract also provides a user-specific retrieval function that allows the verification record to be retrieved using the corresponding user ID.

📂 Project Structure
BioVerify/
│
├── 📂 BioVerify_Synthetic/
│   ├── 📂 images/
│   │   ├── face/
│   │   ├── fingerprint/
│   │   └── iris/
│   │
│   └── 📂 metadata/
│       ├── samples.csv
│       └── subject_modalities.csv
│
├── 📂 ai/
│   ├── __init__.py
│   ├── live_ai.py
│   ├── preprocess.py
│   └── verification.py
│
├── 📂 blockchain/
│   └── BiometricVerification.sol
│
├── 📂 frontend/
│   └── index.html
│
├── backend.py
├── blockchain_test.py
├── .gitignore
└── README.md
📊 Dataset

BioVerify uses a synthetic multimodal biometric dataset created for prototype development.

The dataset contains synthetic biometric samples representing multiple users, sessions, and three biometric modalities:

Face
Fingerprint
Iris

Synthetic data was used to demonstrate the complete verification workflow without using real individuals' biometric information.

The dataset is organized according to user and modality information and is used during preprocessing and verification.

⚙️ Installation Guide
📋 Prerequisites

Before running the project, make sure the following are available:

Python 3.x
Git
Visual Studio Code
MetaMask
Ethereum Sepolia network access
Sepolia test ETH for blockchain transactions

📥 Step 1: Clone the Repository
git clone https://github.com/Shalinips/BioVerify.git

Move into the project directory:
cd BioVerify

🐍 Step 2: Create Virtual Environment
python -m venv venv

▶️ Step 3: Activate Virtual Environment
On Windows:
venv\Scripts\activate

📦 Step 4: Install Dependencies
Install the required Python packages:
pip install flask web3 torch torchvision numpy opencv-python python-dotenv

🔐 Step 5: Configure Environment Variables
Create a .env file in the project root.
Add the required blockchain configuration values used by the backend.
Never upload .env or private keys to GitHub.
The repository .gitignore is configured to exclude environment files and the Python virtual environment.

⛓️ Step 6: Configure Blockchain
The project uses the Ethereum Sepolia test network.
The deployed smart contract is used to record biometric verification information.
The smart contract can be compiled, deployed, and tested using Remix IDE.

🚀 Step 7: Start the Backend
Run:
python backend.py

The Flask backend runs locally at:
http://127.0.0.1:5000

🌐 Step 8: Open the Application
Open the local application in a browser.
Connect MetaMask using the Ethereum Sepolia network.
Select a synthetic user and run the biometric verification.

▶️ Application Workflow

The BioVerify application follows the workflow below:

User opens the BioVerify web interface.
MetaMask is connected to the Ethereum Sepolia network.
A synthetic user is selected.
The corresponding biometric samples are processed.
Face, Fingerprint, and Iris features are extracted.
ResNet-50 performs deep feature extraction.
CBAM applies channel and spatial attention.
2048-dimensional embeddings are generated.
Cosine similarity is calculated for each modality.
Individual similarity scores are obtained.
Weighted multimodal fusion produces the final score.
The final score is compared with the threshold.
The system produces a VERIFIED or REJECTED result.
A SHA-256 verification hash is generated.
The verification record is submitted to the smart contract.
The blockchain transaction is mined on Ethereum Sepolia.
The transaction hash and block number are obtained.
The blockchain record can be retrieved using the user ID.

🧠 Concepts Demonstrated
This project demonstrates the practical implementation of:
Multimodal biometric verification
Deep learning
Convolutional neural networks
ResNet architecture
Attention mechanisms
CBAM
Feature extraction
Embeddings
Cosine similarity
Weighted score fusion
Threshold-based classification
Cryptographic hashing
SHA-256
REST API communication
Flask backend development
Web3.py
Solidity smart contracts
Ethereum blockchain
Sepolia testnet
MetaMask integration
Git and GitHub

🔐 Security Considerations
Synthetic biometric data is used for the prototype.
Real personal biometric data is not used.
Sensitive blockchain credentials are stored in .env.
.env is excluded from Git using .gitignore.
Private keys must never be committed to the repository.
SHA-256 is used as a cryptographic hash for integrity identification.
The blockchain component uses the Ethereum Sepolia test network.
The current implementation is a prototype and is not intended as a production biometric authentication system.

🚀 Future Enhancements
Potential future improvements include:
 Larger and more diverse biometric datasets
 Formal threshold optimization using ROC, FAR, FRR, and EER
 Improved adaptive weight learning
 Real-time biometric acquisition
 Advanced anti-spoofing mechanisms
 Privacy-preserving biometric templates
 Advanced multimodal fusion strategies
 Improved model training and validation
 Production blockchain deployment
 Enhanced frontend interface
 Real-world biometric sensor integration

👩‍💻 About the Project
BioVerify

BioVerify was developed as an academic prototype to demonstrate the integration of artificial intelligence, multimodal biometrics, cryptographic hashing, and blockchain technology.

The project focuses on understanding how deep learning can be combined with decentralized record management to build a more traceable biometric verification workflow.

The prototype demonstrates an end-to-end pipeline from biometric feature extraction to blockchain-backed verification recording.

📄 License
This project is developed for academic and educational purposes.
No specific open-source license has been declared for this repository.

<div align="center">
🔐 BioVerify

Multimodal Biometrics • Adaptive Attention • Blockchain Integrity

Securing Identity. Ensuring Integrity.

</div> ```
