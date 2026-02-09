import hashlib
import sys


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_hash.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        hash_value = calculate_sha256(file_path)
        print(f"SHA256: {hash_value}")
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
