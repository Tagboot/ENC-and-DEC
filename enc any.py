from __future__ import annotations

from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError as exc:
    raise SystemExit(
        "This script requires the 'cryptography' package. Install it with: pip install cryptography"
    ) from exc


def encrypt_file(input_file: str, output_file: str, key_file: str | None = None) -> tuple[str, str]:
    """Encrypt a binary file and save the encrypted result and key."""
    source = Path(input_file)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted_data = cipher.encrypt(source.read_bytes())

    dest = Path(output_file)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(encrypted_data)

    if key_file is None:
        key_file = str(source.with_suffix(source.suffix + ".key"))

    key_path = Path(key_file)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_bytes(key)

    return str(dest), str(key_path)


if __name__ == "__main__":
    source_path = input("Enter the file path to encrypt: ").strip()
    default_output = "encrypted_file.bin"
    default_key = "encryption_key.key"

    output_path = input(f"Output encrypted file path [{default_output}]: ").strip() or default_output
    key_path = input(f"Key file path [{default_key}]: ").strip() or default_key

    try:
        saved_output, saved_key = encrypt_file(source_path, output_path, key_path)
        print(f"Encrypted file saved to: {saved_output}")
        print(f"Key saved to: {saved_key}")
        print("Keep the key file safe. You will need it to decrypt the file.")
    except Exception as exc:
        print(f"Encryption failed: {exc}")
