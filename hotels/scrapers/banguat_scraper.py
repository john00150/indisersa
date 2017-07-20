import requests

url = 'http://banguat.gob.gt/default.asp'
proxy = 'http://159.203.117.131:3128'

def get_rate():
    r = requests.get(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        },
        proxies={
            'http': proxy,
        }
        )
    return r.content


if __name__ == '__main__':
    print get_rate()


