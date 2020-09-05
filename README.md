# gw-iconsdk

* Repository: https://github.com/goldworm-icon/gw-iconsdk

# Prerequisite

* [coincurve](https://pypi.org/project/coincurve/)
* [eth_keyfile](https://github.com/ethereum/eth-keyfile)
* [multimethod](https://pypi.org/project/multimethod/)
* [requests](https://pypi.org/project/requests/)

# Installation

```bash
$ pip install gw-iconsdk
```

# How to use API

## send_transaction

```python
import icon
import icon.builder
from icon.data import unit, Address
from icon.provider import HTTPProvider
from icon.wallet import KeyWallet


provider = HTTPProvider("http://localhost:9000", 3)
client = icon.Client(provider)
wallet = KeyWallet()
to = Address.from_string("hx0123456789012345678901234567890123456789")

try:
    tx: icon.builder.Transaction = icon.builder.TransactionBuilder() \
        .from_(wallet.address) \
        .to(to) \
        .value(unit.icx(10)) \
        .step_limit(100_000) \
        .nonce(0) \
        .build()
    tx.sign(wallet.private_key)

    tx_hash: bytes = client.send_transaction(tx)
except icon.SDKException as e:
    print(e)
```

### estimate_step

* Estimate the quantity of steps required to process a transaction

```python
from typing import Dict

import icon

provider = icon.HTTPProvider("https://localhost:9000")
client = icon.Client(provider)
wallet = icon.KeyWallet()
to = icon.Address.from_string("hx0123456789012345678901234567890123456789")

try:
    params: Dict[str, str] = icon.TransactionBuilder() \
        .from_(wallet.address) \
        .to(to) \
        .value(10 * 10 ** 18) \
        .step_limit(100_000) \
        .nonce(0) \
        .build()

    estimated_step: int = client.estimate_step(params)
except icon.SDKException as e:
    print(e)
```

### get_block_by_hash

* Query block information with given block hash

### get_block_by_height

### get_transaction

### get_transactionResult

### get_totalSupply

### get_balance

### get_score_api

### call

## References

* [ICON JSON-RPC API v3 Specification](https://www.icondev.io/docs/icon-json-rpc-v3)
* [ICON SDK for Python](https://github.com/icon-project/icon-sdk-python)
* [Web3.py](https://web3py.readthedocs.io/en/stable/) 
