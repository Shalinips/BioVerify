from flask import Flask, jsonify, request, send_from_directory
from web3 import Web3
from dotenv import load_dotenv
import os
import sys

from ai.live_ai import compare_users
from ai.verification import generate_verification_hash


# ============================================================
# Flask Application
# ============================================================

app = Flask(
    __name__,
    static_folder="frontend"
)


# ============================================================
# Blockchain Configuration
# ============================================================

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not PRIVATE_KEY:
    raise Exception(
        "PRIVATE_KEY not found in .env file"
    )


RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

web3 = Web3(
    Web3.HTTPProvider(RPC_URL)
)


CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0x3282F0ce1D856b69d69aAF0e424E98C9e5f351bd"
)


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
                "internalType": "string",
                "name": "_userId",
                "type": "string"
            }
        ],
        "name": "getVerification",
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
    },
    {
        "inputs": [],
        "name": "verificationCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
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


# ============================================================
# Wallet / Contract
# ============================================================

account = web3.eth.account.from_key(
    PRIVATE_KEY
)

contract = web3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=ABI
)


# ============================================================
# Project Information
# ============================================================

NETWORK_NAME = "Ethereum Sepolia"

CHAIN_ID = 11155111


# ============================================================
# Home Page
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        "frontend",
        "index.html"
    )


# ============================================================
# Blockchain Connection Information
# ============================================================

@app.route("/api/blockchain")
def blockchain_info():

    connected = web3.is_connected()

    return jsonify({
        "connected": connected,
        "wallet": account.address,
        "network": NETWORK_NAME,
        "chain_id": CHAIN_ID,
        "contract": CONTRACT_ADDRESS
    })


# ============================================================
# Live Biometric Verification
# ============================================================

@app.route("/api/verify", methods=["POST"])
def verify():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data received"
        }), 400


    user_id = data.get(
        "user_id",
        "user_001"
    )


    # --------------------------------------------------------
    # Compare Session 1 and Session 2
    # --------------------------------------------------------

    try:

        (
            face_score,
            fingerprint_score,
            iris_score,
            final_score
        ) = compare_users(
            user_id,
            "session_1",
            user_id,
            "session_2"
        )

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


    # --------------------------------------------------------
    # Prototype Verification Threshold
    # --------------------------------------------------------

    PROTOTYPE_THRESHOLD = 0.965


    verified = (
        final_score >= PROTOTYPE_THRESHOLD
    )


    verification_result = (
        "VERIFIED"
        if verified
        else "REJECTED"
    )


    # --------------------------------------------------------
    # Generate SHA-256
    # --------------------------------------------------------

    (
        verification_record,
        record_string,
        verification_hash
    ) = generate_verification_hash(
        user_id,
        verification_result,
        final_score
    )


    # --------------------------------------------------------
    # Blockchain Write
    # --------------------------------------------------------

    blockchain_status = "NOT RECORDED"
    transaction_hash = None
    block_number = None


    try:

        nonce = web3.eth.get_transaction_count(
            account.address
        )


        transaction = contract.functions.recordVerification(
            user_id,
            verification_hash,
            verified
        ).build_transaction({

            "from": account.address,

            "nonce": nonce,

            "chainId": CHAIN_ID,

            "gas": 200000,

            "gasPrice": web3.eth.gas_price

        })


        signed_transaction = account.sign_transaction(
            transaction
        )


        tx_hash = web3.eth.send_raw_transaction(
            signed_transaction.raw_transaction
        )


        receipt = web3.eth.wait_for_transaction_receipt(
          tx_hash,
          timeout=300,
          poll_latency=5
        )


        transaction_hash = tx_hash.hex()

        block_number = receipt.blockNumber


        if receipt.status == 1:
                  blockchain_status = "RECORDED"

                   # Retrieve the exact verification record for this user
                  blockchain_record = contract.functions.getVerification(
                      user_id
                  ).call()

        else:
                  blockchain_status = "FAILED"
                  blockchain_record = None

    except Exception as e:
        blockchain_status = "FAILED"
        blockchain_record = None

        print(
            "Blockchain error:",
            e
        )


    # --------------------------------------------------------
    # Return Result to Frontend
    # --------------------------------------------------------

    return jsonify({

        "success": True,

        "user_id": user_id,

        "face_score": round(
            face_score,
            6
        ),

        "fingerprint_score": round(
            fingerprint_score,
            6
        ),

        "iris_score": round(
            iris_score,
            6
        ),

        "similarity": round(
            final_score,
            6
        ),

        "threshold": PROTOTYPE_THRESHOLD,

        "result": verification_result,

        "verified": verified,

        "verification_hash": verification_hash,

        "blockchain_status": blockchain_status,

        "transaction_hash": transaction_hash,

        "block_number": block_number,

        "network": NETWORK_NAME,

        "contract": CONTRACT_ADDRESS,

        "wallet": account.address,

        "blockchain_user_id": (
    blockchain_record[0]
    if blockchain_record
    else None
),

"blockchain_verification_hash": (
    blockchain_record[1]
    if blockchain_record
    else None
),

"blockchain_verified": (
    blockchain_record[2]
    if blockchain_record
    else None
),

"blockchain_timestamp": (
    blockchain_record[3]
    if blockchain_record
    else None
)

    })


# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("        BIOVERIFY BACKEND SERVER")
    print("==============================================")

    print(
        "Blockchain connected:",
        web3.is_connected()
    )

    print(
        "Wallet:",
        account.address
    )

    print(
        "Network:",
        NETWORK_NAME
    )

    print(
        "Contract:",
        CONTRACT_ADDRESS
    )

    print()
    print(
        "Open in browser:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()
    print(
        "Server starting..."
    )

    print("==============================================")
    print()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )