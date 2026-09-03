import hashlib
import json


# -----------------------------
# Generate Verification Hash
# -----------------------------

def generate_verification_hash(
    user_id,
    verification_result,
    similarity_score
):

    verification_record = {
        "user_id": user_id,
        "result": verification_result,
        "similarity": round(similarity_score, 6)
    }

    # Convert record to deterministic JSON
    record_string = json.dumps(
        verification_record,
        sort_keys=True
    )

    # Generate SHA-256 hash
    verification_hash = hashlib.sha256(
        record_string.encode()
    ).hexdigest()

    return (
        verification_record,
        record_string,
        verification_hash
    )


# -----------------------------
# Test Verification Record
# -----------------------------

if __name__ == "__main__":

    user_id = "user_001"

    verification_result = "VERIFIED"

    similarity_score = 0.981606


    (
        verification_record,
        record_string,
        verification_hash
    ) = generate_verification_hash(
        user_id,
        verification_result,
        similarity_score
    )


    # -----------------------------
    # Display result
    # -----------------------------

    print(
        "========== VERIFICATION RECORD =========="
    )

    print(
        "User ID:",
        user_id
    )

    print(
        "Result:",
        verification_result
    )

    print(
        "Similarity:",
        similarity_score
    )

    print(
        "\nRecord:"
    )

    print(
        record_string
    )

    print(
        "\nSHA-256 Hash:"
    )

    print(
        verification_hash
    )

    print(
        "\nHash length:",
        len(verification_hash)
    )