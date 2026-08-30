from __future__ import annotations

from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError as exc:
    raise SystemExit(
        "This script requires the 'cryptography' package. Install it with: pip install cryptography"
    ) from exc


def decrypt_file(encrypted_file_path: str, key_file_path: str, output_path: str | None = None) -> str:
    """Decrypt the encrypted file using the given key and save it."""
    encrypted_file = Path(encrypted_file_path)
    key_file = Path(key_file_path)

    if not encrypted_file.exists():
        raise FileNotFoundError(f"Encrypted file not found: {encrypted_file}")
    if not key_file.exists():
        raise FileNotFoundError(f"Key file not found: {key_file}")

    key = key_file.read_bytes()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_file.read_bytes())

    if output_path is None:
        output_path = str(encrypted_file.with_suffix(".decrypted"))

    output_file = Path(output_path)
    output_file.write_bytes(decrypted_data)
    return str(output_file)


if __name__ == "__main__":
    encrypted_path = input("Enter encrypted file path: ").strip()
    key_path = input("Enter key file path: ").strip()
    default_output = "decrypted_output.txt"
    output_path = input(f"Output file path [{default_output}]: ").strip() or default_output

    try:
        saved_output = decrypt_file(encrypted_path, key_path, output_path)
        print(f"Decrypted data saved to: {saved_output}")
    except Exception as exc:
        print(f"Decryption failed: {exc}")
