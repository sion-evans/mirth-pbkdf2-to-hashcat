# Mirth Connect PBKDF2 Hash Converter

## Overview

In **Mirth Connect 4.4**, the default password digest algorithm was changed from SHA256 to PBKDF2WithHmacSHA256. As a result, password hashes are no longer directly usable with tools such as Hashcat without additional formatting.

Password hashes stored in the PERSON_PASSWORD table are no longer simple SHA-256 digests. Instead, they are:

- Base64-encoded
- PBKDF2-derived
- Composed of both the salt and derived key

This script converts the raw value extracted from the database into a Hashcat-compatible format to aid with password recovery or similar tasks.

---

## Usage

The script accepts input as either a command line argument or standard input (stdin):

```
python3 script.py --hash "<BASE64_HASH>"
echo "<BASE64_HASH>" | python3 script.py
```

It also supports specifying a custom iteration count if the installation's configuration differs from the default:

```
python3 script.py --hash "<BASE64_HASH>" --iterations 750000
echo "<BASE64_HASH>" | python3 script.py --iterations 750000
```

This string can then be supplied directly to Hashcat (with the appropriate mode):

```
python3 script.py --hash "<BASE64_HASH>" > hash.txt
hashcat -m 10900 -a 0 hash.txt wordlist.txt
```
