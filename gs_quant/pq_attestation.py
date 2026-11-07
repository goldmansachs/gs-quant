"""
Copyright 2026 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.

Optional post quantum attestation of analytics results. Signs a canonical
result manifest, such as a priceable with its measure and value, using FIPS 204
ML-DSA so a reader can confirm the reported result is authentic and has not been
altered, using a signature scheme that stays safe once large quantum computers
exist. This gives a pricing or risk result a tamper evident provenance record.

The scheme is provided by the optional dilithium-py package. Install it with
``pip install dilithium-py``.
"""

import base64
import hashlib
import json

SCHEME = "ML-DSA-65"
ISSUER = "Quantova"


def _backend():
    """Return the ML-DSA backend or raise if dilithium-py is not installed."""
    try:
        from dilithium_py.ml_dsa import ML_DSA_65
    except ImportError as error:
        raise RuntimeError(
            "Post quantum attestation needs dilithium-py. Install it with pip install dilithium-py."
        ) from error
    return ML_DSA_65


def canonicalize(result):
    """Return the canonical byte encoding an attestation is computed over."""
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def generate_keypair():
    """Return a fresh (public_key, secret_key) pair for the signer."""
    return _backend().keygen()


def build_attestation(payload, public_key, secret_key):
    """Return a self contained attestation over the payload bytes."""
    signature = _backend().sign(secret_key, payload, deterministic=True)
    return {
        "scheme": SCHEME,
        "issuer": ISSUER,
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "public_key": base64.b64encode(public_key).decode("ascii"),
        "signature": base64.b64encode(signature).decode("ascii"),
    }


def verify_attestation(payload, attestation, expected_public_key=None):
    """Return True when the attestation matches the payload.

    The payload digest is always checked. When expected_public_key is given the
    signer is pinned too, so a valid signature made under a different key is
    rejected.
    """
    if attestation.get("payload_sha256") != hashlib.sha256(payload).hexdigest():
        return False
    try:
        public_key = base64.b64decode(attestation["public_key"], validate=True)
        signature = base64.b64decode(attestation["signature"], validate=True)
    except (ValueError, KeyError):
        return False
    if expected_public_key is not None and public_key != expected_public_key:
        return False
    try:
        return bool(_backend().verify(public_key, payload, signature))
    except (ValueError, TypeError):
        return False


def save_signer(path, public_key, secret_key):
    """Write a signer key file that load_signer reads back."""
    data = {
        "scheme": SCHEME,
        "public_key": base64.b64encode(public_key).decode("ascii"),
        "secret_key": base64.b64encode(secret_key).decode("ascii"),
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


def load_signer(path):
    """Read (public_key, secret_key) from a signer key file."""
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return base64.b64decode(data["public_key"]), base64.b64decode(data["secret_key"])
