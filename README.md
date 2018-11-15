# zebitex-python2
python 2.7 client for Zebitex exchange API

[API documentation](https://doc.zebitex.com/)

## Getting started

* Generate api keys: https://zebitex.com/profile/api-tokens (use https://staging.zebitex.com/ for testing environnement)

```
import api
test_env = true # set to false to use in production
client = api.Zebitex(apikey='<Access key>', private_key='<Secret key>', test_env) # instantiate your client
```

* retrieve you assets balances
```
client.funds().json()
```

* open a new order
```
client.new_order('ltc', # quote currency
  'btc', # base currency
  'ask', # order side (bid or ask)
  '0.321', # price
  '0.123', # volume
  'ltcbtc', # market
  'limit' # order type
)
```

* list open orders
```
client.open_orders(page='1', per='11').json()
```

* cancel an opened order
```
let order_id=1234
client.cancel_order(order_id).json()
```

* list withdrawal addresses
```
client.get_withdrawal_addresses('BTC')
#[{u'confirmed': True, u'accountName': u'', u'currency': u'BTC', u'iban': u'', u'address': u'mga4bvcHmuercgoADzLoszAvrgUD9jsxWH', u'label': u'test', u'id': 123}]

```

* create a new withdrawal
```
c.new_withdrawal("btc", 3, "0.1")
```


