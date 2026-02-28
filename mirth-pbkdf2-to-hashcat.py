#!/usr/bin/env python3

import sys
import argparse
import base64

DEFAULT_ITERATIONS = 600000


def get_args():
    parser = argparse.ArgumentParser(description="Converts Mirth Connect PBKDF2WithHmacSHA256 raw hash values into a Hashcat-compatible format.")

    parser.add_argument(
        "--hash",
        dest="hash_value",
        type=str,
        help="Hash value as a string"
    )

    parser.add_argument(
        "--iterations",
        dest="iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"Iteration count (default: {DEFAULT_ITERATIONS})"
    )

    args = parser.parse_args()

    if args.iterations <= 0:
        parser.error("Iterations must be a positive integer.")

    if args.hash_value:
        hash_input = args.hash_value.strip()
    elif not sys.stdin.isatty():
        hash_input = sys.stdin.read().strip()
    else:
        parser.error("No hash provided via --hash or stdin.")

    return hash_input, args.iterations


def parse_hash(hash_string: str) -> bytes:
    try:
        decoded = base64.b64decode(hash_string, validate=True)
    except Exception:
        raise ValueError("Error decoding Base64")

    if len(decoded) != 40:
        raise ValueError("Decoded value must be exactly 40 bytes")

    return decoded


def main():
    hash_input, iterations = get_args()

    try:
        decoded = parse_hash(hash_input)

        salt = decoded[:8]
        derived_key = decoded[8:]

        salt_b64 = base64.b64encode(salt).decode()
        derived_b64 = base64.b64encode(derived_key).decode()

        hashcat_format = f"sha256:{iterations}:{salt_b64}:{derived_b64}"

        print(hashcat_format)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
