from web3 import Web3
from dotenv import load_dotenv
import os

from ai.verification import generate_verification_hash
# -----------------------------
# Load private key
# -----------------------------

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not PRIVATE_KEY:
    raise Exception("PRIVATE_KEY not found in .env file")


# -----------------------------
# Connect to Sepolia
# -----------------------------

RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

web3 = Web3(
    Web3.HTTPProvider(RPC_URL)
)

print("Connected:", web3.is_connected())


# -----------------------------
# Wallet
# -----------------------------

account = web3.eth.account.from_key(PRIVATE_KEY)

print("Python wallet:", account.address)


# -----------------------------
# Existing contract
# -----------------------------

CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0x9fF12Ec64E31CD40a82513DcA33e86675DFF9c5c"
)


# -----------------------------
# Contract ABI
# -----------------------------

ABI = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_userId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_verificationHash",
                "type": "string"
            },
            {
                "internalType": "bool",
                "name": "_verified",
                "type": "bool"
            }
        ],
        "name": "recordVerification",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "verifications",
        "outputs": [
            {
                "internalType": "string",
                "name": "userId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "verificationHash",
                "type": "string"
            },
            {
                "internalType": "bool",
                "name": "verified",
                "type": "bool"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


# -----------------------------
# Create contract object
# -----------------------------

contract = web3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=ABI
)

print("Contract connected successfully!")


# -----------------------------
# BIOMETRIC VERIFICATION RESULT
# -----------------------------

user_id = "user_001"

similarity_score = 0.981606

verified = True

verification_result = (
    "VERIFIED"
    if verified
    else "REJECTED"
)


# Generate SHA-256 verification hash

(
    verification_record,
    record_string,
    verification_hash
) = generate_verification_hash(
    user_id,
    verification_result,
    similarity_score
)


print("\n========== BIOMETRIC VERIFICATION ==========")

print("User ID:", user_id)
print("Similarity Score:", similarity_score)
print("Verification Result:", verification_result)

print("\nSHA-256 Hash:")
print(verification_hash)


# -----------------------------
# BLOCKCHAIN WRITE
# -----------------------------

print("\n========== BLOCKCHAIN WRITE ==========")

print("User ID:", user_id)
print("Verification Hash:", verification_hash)
print("Verified:", verified)




# Get transaction nonce
nonce = web3.eth.get_transaction_count(
    account.address
)


# Build transaction
transaction = contract.functions.recordVerification(
    user_id,
    verification_hash,
    verified
).build_transaction({
    "from": account.address,
    "nonce": nonce,
    "chainId": 11155111,
    "gas": 200000,
    "gasPrice": web3.eth.gas_price
})


# Sign transaction locally
signed_transaction = account.sign_transaction(
    transaction
)


# Send transaction
tx_hash = web3.eth.send_raw_transaction(
    signed_transaction.raw_transaction
)

print("\nTransaction sent!")
print("Transaction hash:", tx_hash.hex())


# Wait for confirmation
receipt = web3.eth.wait_for_transaction_receipt(
    tx_hash
)


print("\n========== TRANSACTION RESULT ==========")

print("Block number:", receipt.blockNumber)
print("Transaction status:", receipt.status)

if receipt.status == 1:
    print("Blockchain write: SUCCESS")
else:
    print("Blockchain write: FAILED")