
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
BIP0039_DIR = os.path.normpath(os.path.join(ROOT_DIR, 'bip39_word_list'))

ECDSA_SEC256K1_ORDER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

NILE_TESTNET = 3448148188
SHASTA_TESTNET = 2494104990
MAINNET = 728126428

API_BASE_URLS = {MAINNET:'https://api.trongrid.io',
                SHASTA_TESTNET:'https://api.shasta.trongrid.io',
                NILE_TESTNET:'https://nile.trongrid.io'}

TRANSFER_METHOD = 'transfer(address,uint256)'
APPROVE_METHOD = 'approve(address,uint256)'
TRANSFER_FROM_METHOD = 'transferFrom(address,address,uint256)'

TRC20_METHODS = [TRANSFER_METHOD,APPROVE_METHOD,TRANSFER_FROM_METHOD]
