# Python SDK

Source repository: https://github.com/goldworm-icon/gw-iconsdk

## Prerequisite

## Installation

## Using the SDK

### SendTransaction

### Query

```python
import icon

provider = icon.HttpProvider()
client = icon.Client(provider)

try:
    request = icon.TransactionBuilder()
    response = client.call(request)
    print(response)
except icon.IconServiceBaseException as e:
    print(e)
```

## Code Examples
