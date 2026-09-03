# BioVerify-Synthetic
Synthetic prototype-only multimodal biometric dataset.

It is INSPIRED BY the structure of real multimodal biometric corpora such as
BioSec/NIST SD301, but it is NOT real biometric data and must not be presented
as BioSec or NIST data.

30 synthetic subjects × 2 sessions × 3 samples × 3 modalities = 540 images.
Modalities: face, fingerprint, iris. All three modalities are deliberately
linked by the same synthetic subject/session ID.

Use: preprocessing → feature extraction → adaptive fusion → verification →
SHA-256 → Solidity smart contract → Sepolia/MetaMask.

For the report/viva call it: "synthetic multimodal biometric dataset created
for prototype validation." Do not claim real-world biometric accuracy.
