from .key import *
import sha3
from py_ecc.secp256k1 import privtopub
import base58

def private_key_to_address(privkey):
    k = normalize_key(privkey)
    x, y = privtopub(k)
    return b'\x41' + sha3.keccak_256(encode_int32(x) + encode_int32(y)).digest()[12:]

def public_key_to_address(key):
    pub_key = key.to_string()
    return b'\x41' + sha3.keccak_256(pub_key)[-20:]

def to_hex_address(raw_addr) -> str:
    addr = normalize_address(raw_addr)
    return base58.b58decode_check(addr).hex()

def to_raw_address(raw_addr) -> bytes:
    addr = normalize_address(raw_addr)
    return base58.b58decode_check(addr)

def normalize_address(raw_addr) -> str:
    """Convert hex address or base58check address to base58check address(and verify it)."""
    if isinstance(raw_addr, (str,)):
        if raw_addr[0] == "T" and len(raw_addr) == 34:
            try:
                # assert checked
                base58.b58decode_check(raw_addr)
            except ValueError:
                raise Exception("bad base58check format")
            return raw_addr
        elif len(raw_addr) == 42:
            if raw_addr.startswith("0x"):  # eth address format
                return base58.b58encode_check(b"\x41" + bytes.fromhex(raw_addr[2:])).decode()
            else:
                return base58.b58encode_check(bytes.fromhex(raw_addr)).decode()
        elif raw_addr.startswith("0x") and len(raw_addr) == 44:
            return base58.b58encode_check(bytes.fromhex(raw_addr[2:])).decode()
    elif isinstance(raw_addr, (bytes, bytearray)):
        if len(raw_addr) == 21 and int(raw_addr[0]) == 0x41:
            return base58.b58encode_check(raw_addr).decode()
        if len(raw_addr) == 20:  # eth address format
            return base58.b58encode_check(b"\x41" + raw_addr).decode()
        return normalize_address(raw_addr.decode())
    raise Exception(repr(raw_addr))

def int_to_addr(x):
    o = [b''] * 20
    for i in range(20):
        o[19 - i] = ascii_chr(x & 0xff)
        x >>= 8
    return b''.join(o)


def is_address_valid(address):
    return normalize_address(address) == address