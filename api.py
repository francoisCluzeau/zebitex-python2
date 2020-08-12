#!/usr/bin/env python2
# coding: utf-8
from collections import OrderedDict
import time
import requests
import hashlib
import hmac
import json

class Zebitex:
    def __init__(self, apikey,private_key, is_dev=False):
        self.apikey = apikey
        self.priv = private_key
        self.url = 'https://api-staging.zebitex.com/' if is_dev else 'https://api.zebitex.com/'

    def _build_auth_header(self, nonce, signature, query=None):
        params = ";".join(query.keys()) if query else ''
        header = '''ZEBITEX-HMAC-SHA256 access_key=%s, signature=%s, tonce=%s, signed_params=%s'''%(self.apikey, signature, nonce, params)
        return {'Authorization':header}

    def _sign_request(self,method, path, nonce, query=None):
        args = json.dumps(query) if query else '{}'
        payload = "|".join([method, '/' + path, str(nonce), args ]).replace(' ', '')
        return hmac.new(self.priv, payload, hashlib.sha256).hexdigest()

    def _private_request(self, method, path, query=None):
        params ={k: str(v) for k,v in OrderedDict(query).items()} if query else None
        nonce = int(time.time()*1000)
        signature = self._sign_request(method, path, nonce, params)
        header = self._build_auth_header(nonce, signature, params)
        url = self.url+path
        return requests.request(method,url, params=params, headers=header, json=True)

    def _public_request(self, path, query = None):
        url = self.url+path
        return requests.get(url, params=query, json=True)

    def _post_private_request(self, path, query=None):
        return self._private_request('POST', path, query)


    def _get_private_request(self, path, query=None):
        return self._private_request('GET', path, query)


    def _delete_private_request(self, path, query=None):
        return self._private_request('DELETE', path, query)

    def funds(self):
        return self._get_private_request('api/v1/funds')

    def tickers(self):
        return self._public_request('api/v1/orders/tickers')

    def ticker(self, market):
        return self._public_request('api/v1/orders/ticker_summary/'+market)

    def orderbook(self, market):
        return self._public_request('api/v1/orders/orderbook', {"market":market})

    def public_trade_history(self, market):
        return self._public_request('api/v1/orders/trade_history', {"market":market})

    def get_withdrawal_addresses(self, asset):
        params = { "currency": asset}
        return self._get_private_request('api/v1/fund_sources', params)
    
    def new_withdrawal(self,currency, fund_id, amount):
        params = {"code":currency, "fund_source_id": fund_id, "sum":amount}
        return self._post_private_request('api/v1/withdrawals', params)

    def open_orders(self, page=1, per=10):
        params = {"page":page, "per":per}
        return self._get_private_request('api/v1/orders/current', params)

    def trade_history(self, side, start_date, end_date, page, per):
        params = {"side":side, "start_date":start_date, "end_date":end_date, "page":page, "per":per}
        return self._get_private_request('api/v1/history/trades', params)

    def cancel_all_orders(self):
        return self._delete_private_request('api/v1/orders/cancel_all')

    def cancel_order(self,id_order):
        return self._delete_private_request('api/v1/orders/'+str(id_order)+'/cancel', { 'id':str(id_order) })

    def new_order(self,bid, ask, side, price, amount, market, ord_type):
        params={"bid":bid, "ask":ask, "side":side, "price":price,
                "amount":amount, "market":market, "ord_type":ord_type}
        return self._post_private_request('api/v1/orders', params)
    def new_market_order(self,bid, ask, side,  amount, market ):
        params={"bid":bid, "ask":ask, "side":side,
                "amount":amount, "market":market, "ord_type":'market'}
        return self._post_private_request('api/v1/orders', params)
