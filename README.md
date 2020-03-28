# gw-iconsdk

Source repository: https://github.com/goldworm-icon/gw-iconsdk

## Prerequisite

* [coincurve](https://pypi.org/project/coincurve/)
* [multipledispatch](https://pypi.org/project/multipledispatch/)
* [requests](https://pypi.org/project/requests/)

## Installation

```
$ pip install gw-iconsdk
```

## How to use API

```python
import icon

provider = icon.HttpProvider()
client = icon.Client(provider)

try:
    builder = icon.TransactionBuilder()
    Transaction

    request = builder.build()
    response = client.icx.call(request)
    print(response)
except icon.IconServiceBaseException as e:
    print(e)
```

### send_transaction

### estimate_step

### get_block

* Query block information with given parameters

### get_transaction

### get_transactionResult

### get_totalSupply

### get_balance

### get_scoreApi

### call

## References

* [Web3.py](https://web3py.readthedocs.io/en/stable/) 
* 