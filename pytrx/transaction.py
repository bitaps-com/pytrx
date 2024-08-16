import coincurve
import rlp
import sha3

from rlp.sedes import CountableList
from .encode import *
from .tools import *
from .address import *
import ecdsa
import hashlib
import requests
from .constants import *

EIP155_CHAIN_ID_OFFSET = 35
V_OFFSET = 27
DYNAMIC_FEE_TRANSACTION_TYPE = b'\x02'

def ecsign(rawhash, key):
    pk = coincurve.PrivateKey(key)
    signature = pk.sign_recoverable(rawhash, hasher=None)
    v = safe_ord(signature[64:])
    r = bytes_to_int(signature[0:32])
    s = bytes_to_int(signature[32:64])
    return v, r, s

def safe_ord(value):
    if isinstance(value, int):
        return value
    else:
        return ord(value)


def create_transaction(nonce, gasprice, gaslimit, to_address, value, data, private_key, chain_id=None):
    owner_address = to_hex_address(private_key_to_address(private_key))
    if chain_id and chain_id in API_BASE_URLS:
        API_BASE_URL = API_BASE_URLS[chain_id]
    else:
        API_BASE_URL= API_BASE_URLS[MAINNET]
    if data:
        method = data[0:10]
        TRC20_METHODS_ENCODED = [contract_method_encode(m) for m in TRC20_METHODS]
        if method in TRC20_METHODS_ENCODED:
                transaction = {
                    "contract_address": to_hex_address(to_address),
                    "function_selector": TRC20_METHODS[TRC20_METHODS_ENCODED.index(method)],
                    "parameter": data[10:],
                    "fee_limit": 100000000,
                    "call_value": 0,
                    "owner_address": owner_address
                }
                resp = requests.post(API_BASE_URL + '/wallet/triggersmartcontract', json=transaction)
        else:
            raise Exception("Not implemented method")
    else:
        transaction = {
            "to_address": to_hex_address(to_address),
            "owner_address": owner_address,
            "amount": value,
            "visible": True
        }

        resp = requests.post(API_BASE_URL + '/wallet/createtransaction', json=transaction)
    payload = resp.json()
    raw_data = bytes.fromhex(payload['raw_data_hex'])
    raw_priv_key = bytes.fromhex(private_key)
    priv_key = ecdsa.SigningKey.from_string(raw_priv_key, curve=ecdsa.SECP256k1)
    signature = priv_key.sign_deterministic(raw_data, hashfunc=hashlib.sha256)

    # recover address to get rec_id
    pub_keys = ecdsa.VerifyingKey.from_public_key_recovery(
        signature[:64], raw_data, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256
    )
    for v, pk in enumerate(pub_keys):
        if public_key_to_address(pk) == to_raw_address(owner_address):
            break

    signature += bytes([v])
    payload["signature"] = signature
    return payload


async def contract_method_encode(method):
    method=method.encode('utf-8')
    method="0x%s" %sha3.keccak_256(method).hexdigest()
    return method[0:10]


def create_contract(nonce, gasprice, gaslimit, data, private_key, chain_id=None):
    return create_transaction(nonce, gasprice, gaslimit, 0, 0, data, private_key, chain_id=chain_id)