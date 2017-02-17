import requests
import time
import hmac
import hashlib
import logging

class BitcoinAverageClient:
    """REST Client for fetching bitcoin exchange average prices"""

    def __init__(self, public_key, secret_key):
        self.__public_key = public_key
        self.__secret_key = secret_key

    def __signature(self):
        timestamp = int(time.time())
        payload = '{0}.{1}'.format(timestamp, self.__public_key)
        digest = hmac.new(self.__secret_key.encode(), msg=payload.encode(),
                digestmod=hashlib.sha256).hexdigest()
        signature = '{0}.{1}'.format(payload, digest)
        return signature

    def enableLogging(self):
        import http.client as http_client
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig(level=logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def disableLogging(self):
        import http.client as http_client
        http_client.HTTPConnection.debuglevel = 0
        logging.basicConfig(level=logging.WARNING)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.WARNING)
        requests_log.propagate = True

    def fetchPrice(self):
        url = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTCUSD'
        resp = requests.get(url, headers={'X-signature': self.__signature()})
        if resp.status_code != 200:
            resp.raise_for_status()
            return
        
        return resp.json()


if __name__ == "__main__":
    # Create API keys at https://bitcoinaverage.com/en/apikeys
    public_key = '<PUBLIC_KEY>'
    secret_key = '<SECRET_KEY>'
    client = BitcoinAverageClient(public_key, secret_key)
    client.enableLogging()
    try:
        data = client.fetchPrice()
    except Exception as err:
        print(err)
    else:
        print(data)

