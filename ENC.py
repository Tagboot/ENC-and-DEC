from __future__ import annotations

from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError as exc:
    raise SystemExit(
        "This script requires the 'cryptography' package. Install it with: pip install cryptography"
    ) from exc


def encrypt_text(plain_text: str, key: bytes | None = None) -> tuple[bytes, bytes]:
    """Encrypt plain text and return (key, encrypted_data)."""
    if key is None:
        key = Fernet.generate_key()

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(plain_text.encode("utf-8"))
    return key, encrypted_data


def save_encrypted_file(plain_text: str, output_path: str, key_path: str) -> tuple[str, str]:
    """Encrypt data and save it to files."""
    key, encrypted_data = encrypt_text(plain_text)

    output_file = Path(output_path)
    key_file = Path(key_path)

    output_file.write_bytes(encrypted_data)
    key_file.write_bytes(key)

    return str(output_file), str(key_file)


if __name__ == "__main__":
    user_input = input("Enter the text to encrypt: ")

    default_output = "encrypted_data.bin"
    default_key = "encryption_key.key"

    output_path = input(f"Output file path [{default_output}]: ").strip() or default_output
    key_path = input(f"Key file path [{default_key}]: ").strip() or default_key

    saved_output, saved_key = save_encrypted_file(user_input, output_path, key_path)

    print(f"Encrypted data saved to: {saved_output}")
    print(f"Encryption key saved to: {saved_key}")
    print("Keep the key file safe. It is required to decrypt the data.")
