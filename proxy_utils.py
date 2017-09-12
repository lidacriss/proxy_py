import requests
from core.models import Proxy


def getThroughProxy(proxy, url, params=None, **kwargs):
    return requestThroughProxy(proxy, url, params=params, **kwargs)


def postThroughProxy(proxy, url, data=None, json=None, **kwargs):
    return requestThroughProxy(proxy, url, data=data, json=json, **kwargs)


def requestThroughProxy(proxy, url, **kwargs):
    if type(proxy) == str:
        proxy = Proxy.fromString(proxy)

    kwargs['proxies'] = getProxyDict(proxy.toRawProxy(), proxy.getProtocol())

    if 'headers' not in kwargs:
        kwargs['headers'] = {
            'User-Agent': getRandomUserAgent()
        }
    else:
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = getRandomUserAgent()

    if 'data' in kwargs and 'json' in kwargs:
        # do post request
        return requests.post(url, **kwargs)
    # else do get request
    return requests.get(url, **kwargs)


# TODO: add multiple checks with several sites
def checkProxy(proxy):
    try:
        getThroughProxy(proxy, 'http://google.com', timeout=10)
    except Exception as ex:
        return False
    return True


# method gets proxy in any of the supported formats
# and return proxy protocols
# supported raw proxy formats:
# ip:port
# domain:port
# user:pass@ip:port
# user:pass@domain:port
def detectRawProxyProtocols(rawProxy):
    result = []

    protocols = ['http', 'socks5', 'socks4', 'socks']
    for protocol in protocols:
        # TODO: add other test sites
        try:
            # TODO: remove redirect forwarding
            res = requests.get('http://google.com', timeout=10,
                               proxies=getProxyDict(rawProxy, protocol))
            if res.status_code == 200:
                result.append(protocol)
        except Exception as ex:
            pass
    return result


def getProxyDict(rawProxy, protocol):
    proxiesTypesList = {
        'http': {
            'http': 'http://' + rawProxy,
            'https': 'https://' + rawProxy
        },
        'socks5': {
            'http': 'socks5://' + rawProxy,
            'https': 'socks5://' + rawProxy
        },
        'socks4': {
            'http': 'socks4://' + rawProxy,
            'https': 'socks4://' + rawProxy
        },
        'socks': {
            'http': 'socks://' + rawProxy,
            'https': 'socks://' + rawProxy
        }
    }
    try:
        return proxiesTypesList[protocol]
    except:
        return proxiesTypesList['http']


def getRandomUserAgent():
    # TODO: do it
    return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'