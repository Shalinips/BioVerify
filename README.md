\# BioVerify



\## Deep Biometric Verification Using Blockchain and Adaptive Attention Networks



BioVerify is a multimodal biometric verification system that combines \*\*Face, Fingerprint, and Iris\*\* biometrics with deep learning, adaptive attention, and blockchain technology.



The system uses \*\*ResNet-50\*\* for deep feature extraction and \*\*CBAM (Convolutional Block Attention Module)\*\* to focus on important channel and spatial features. The extracted features are converted into embeddings and compared using cosine similarity. The individual biometric scores are then combined using weighted multimodal fusion to obtain the final verification score.



After verification, a \*\*SHA-256 hash\*\* is generated for integrity identification, and the verification record is stored on the \*\*Ethereum Sepolia test network\*\* through a Solidity smart contract.



\---



\## Key Features



\- Multimodal biometric verification

\- Face, Fingerprint, and Iris recognition

\- ResNet-50 based feature extraction

\- CBAM-based adaptive attention

\- 2048-dimensional biometric embeddings

\- Cosine similarity for biometric comparison

\- Weighted multimodal score fusion

\- Threshold-based verification

\- SHA-256 verification hash generation

\- Solidity smart contract integration

\- Ethereum Sepolia testnet

\- Flask backend with Web3.py

\- HTML, CSS, and JavaScript frontend

\- User-specific blockchain record retrieval



\---



\## System Workflow



```text

Biometric Images

&#x20;      ↓

Preprocessing

&#x20;      ↓

ResNet-50 Feature Extraction

&#x20;      ↓

CBAM Attention

(Channel Attention + Spatial Attention)

&#x20;      ↓

2048-D Embeddings

&#x20;      ↓

Cosine Similarity

&#x20;      ↓

Individual Similarity Scores

(Face + Fingerprint + Iris)

&#x20;      ↓

Weighted Multimodal Fusion

&#x20;      ↓

Final Similarity Score

&#x20;      ↓

Threshold Comparison

&#x20;      ↓

VERIFIED / REJECTED

&#x20;      ↓

SHA-256 Hash

&#x20;      ↓

Flask + Web3.py

&#x20;      ↓

Solidity Smart Contract

&#x20;      ↓

Ethereum Sepolia Blockchain



AI Methodology

ResNet-50



ResNet-50 is used as the deep learning backbone for extracting meaningful high-level features from the biometric images.



CBAM



CBAM stands for Convolutional Block Attention Module.



It contains two sequential attention mechanisms:



Channel Attention – focuses on important feature channels.

Spatial Attention – focuses on important regions of the feature map.



This helps the network emphasize more informative biometric features.



Embeddings



The extracted biometric representations are converted into 2048-dimensional embeddings for each modality.



Cosine Similarity



Cosine similarity is used to compare the embeddings and obtain individual similarity scores for:



Face

Fingerprint

Iris

Weighted Fusion



The three individual similarity scores are combined using weighted fusion to produce a single multimodal similarity score.



The prototype uses the following modality weights:



Modality	Weight

Face	0.3333

Fingerprint	0.3750

Iris	0.2917



The weights sum to 1.



Verification Threshold



The prototype uses a verification threshold of:



0.965



If the final multimodal score is greater than or equal to the threshold, the user is classified as:



VERIFIED



Otherwise:



REJECTED

Blockchain Integration



After biometric verification, the system generates a SHA-256 hash of the verification record.



The hash is used as an integrity identifier for the verification information.



The Flask backend communicates with the Solidity smart contract using Web3.py.



The smart contract is deployed on:



Ethereum Sepolia Test Network



The blockchain record contains:



User ID

Verification hash

Verification result

Timestamp



The verification record can be retrieved using the corresponding user ID.



Technology Stack

Component	Technologies

AI / ML	Python, PyTorch, ResNet-50, CBAM

Image Processing	NumPy, OpenCV

Backend	Python, Flask, Web3.py

Blockchain	Solidity, Ethereum, Sepolia

Wallet	MetaMask

Smart Contract Tool	Remix IDE

Frontend	HTML, CSS, JavaScript

Development	VS Code, Git, GitHub, Git Bash

Dataset



The project uses a synthetic multimodal biometric dataset created for prototype development.



The dataset contains synthetic biometric samples representing multiple users, sessions, and three biometric modalities:



Face

Fingerprint

Iris



Synthetic data was used to demonstrate the complete biometric verification and blockchain workflow without using real individuals' biometric information.



Project Structure

BioVerify/

│

├── BioVerify\_Synthetic/

│   ├── images/

│   │   ├── face/

│   │   ├── fingerprint/

│   │   └── iris/

│   │

│   └── metadata/

│       ├── samples.csv

│       └── subject\_modalities.csv

│

├── ai/

│   ├── \_\_init\_\_.py

│   ├── live\_ai.py

│   ├── preprocess.py

│   └── verification.py

│

├── blockchain/

│   └── BiometricVerification.sol

│

├── frontend/

│   └── index.html

│

├── backend.py

├── blockchain\_test.py

├── .gitignore

└── README.md

How to Run

1\. Clone the repository

git clone https://github.com/Shalinips/BioVerify.git

cd BioVerify

2\. Create a virtual environment

python -m venv venv

3\. Activate the virtual environment



On Windows:



venv\\Scripts\\activate

4\. Install dependencies



Install the required Python packages for the project environment.



Example:



pip install flask web3 torch torchvision numpy opencv-python python-dotenv

5\. Configure environment variables



Create a .env file in the project root and add the required blockchain configuration.



Do not upload .env or expose private keys.



The .gitignore file is configured to exclude .env and the virtual environment.



6\. Start the backend

python backend.py



The application runs locally at:



http://127.0.0.1:5000

7\. Run the verification



Open the BioVerify frontend, connect MetaMask to the Ethereum Sepolia network, select a synthetic user, and run the biometric verification.



The system displays the biometric similarity scores, final verification result, SHA-256 hash, and blockchain transaction information.



Security Considerations

Synthetic biometric data is used for the prototype.

Sensitive environment variables are stored in .env.

.env is excluded from Git using .gitignore.

Private keys must never be committed to the repository.

SHA-256 is used as a cryptographic hash for integrity identification.

The prototype uses the Ethereum Sepolia test network.

Future Enhancements

Larger and more diverse biometric datasets

Formal threshold optimization using ROC, FAR, FRR, and EER

Improved adaptive weight learning

Real-time biometric acquisition

Stronger anti-spoofing mechanisms

Privacy-preserving biometric templates

Advanced multimodal fusion techniques

Production blockchain deployment

Project Status



Prototype Completed



BioVerify demonstrates an end-to-end workflow integrating:



Multimodal Biometrics → Deep Learning → CBAM Attention → Similarity Calculation → Multimodal Fusion → Verification → SHA-256 → Blockchain Recording

