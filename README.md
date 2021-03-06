# proxy_py

proxy_py is a program which collects proxies, saves them in database and makes periodically checks. It has server for getting proxies with nice API(see below). 

## How to build?

1 Clone this repository

`git clone https://github.com/DevAlone/proxy_py.git`

2 Install requirements

```bash
cd proxy_py
pip3 install -r requirements.txt
```

3 Create settings file

`cp config_examples/settings.py proxy_py/settings.py`

4 (Optional) Change database in settings.py file

5 (Optional) Configure alembic

6 Run your application

`python3 main.py`

7 Enjoy!

## I'm too lazy. Can I just use it?

Yes, you can download virtualbox image [here](https://drive.google.com/file/d/1oPf6xwOADRH95oZW0vkPr1Uu_iLDe9jc/view?usp=sharing). After downloading check that port forwarding is still working, you need forwarding of 55555 host port to 55555 guest. 

## How to get proxies?

proxy_py has server based on aiohttp which is listening 127.0.0.1:55555
(you can change it in settings file) and provides proxies.
To get proxies you should send following json request:

```json
{
	"model": "proxy",
	"method": "get",
	"order_by": "response_time, uptime"
}
```

Note: order_by makes result sorting by one or more fields separated by comma.
You can skip it. The required fields are `model` and `method`.

It will return json response like this:

```json
{
	"count": 1,
	"data": [{
			"address": "http://127.0.0.1:8080",
			"auth_data": "",
			"bad_proxy": false,
			"domain": "127.0.0.1",
			"last_check_time": 1509466165,
			"number_of_bad_checks": 0,
			"port": 8080,
			"protocol": "http",
			"response_time": 461691,
			"uptime": 1509460949
		}
	],
	"has_more": false,
	"status": "ok",
	"status_code": 200
}
```

Note: All fields except *protocol*, *domain*, *port*, *auth_data*,
*checking_period* and *address* can be null

Or error if something went wrong:

```json
{
    "error_message": "You should specify \"model\"",
    "status": "error",
    "status_code": 400
}
```

Note: status_code is also duplicated in HTTP status code

Example using curl:

`curl -X POST http://example.com:55555 -H "Content-Type: application/json" --data '{"model": "proxy", "method": "get"}'`

Example using httpie:

`http POST http://example.com:55555 model=proxy method=get`

Example using python requests library:

```python
import requests
import json


def get_proxies():
    result = []
    json_data = {
        "model": "proxy",
        "method": "get",
    }

    response = requests.post('http://example.com:55555', json=json_data)
    if response.status_code == 200:
        response = json.loads(response.text)
        for proxy in response['data']:
            result.append(proxy['address'])
    else:
        # check error here
        pass
    
    return result
```
Example using aiohttp library:

```python
import aiohttp


async def get_proxies():
    result = []
    json_data = {
        "model": "proxy",
        "method": "get",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('http://example.com:55555', json=json_data) as response:
            if response.status == 200:
                response = json.loads(await response.text())
                for proxy in response['data']:
                    result.append(proxy['address'])
            else:
                # check error here
                pass
                
    return result
```

## How to interact with API?

Read more about API  [here](https://github.com/DevAlone/proxy_py/tree/master/docs/API.md)

## How to test it?

If you made changes to code and want to check that you didn't break
anything, go [here](https://github.com/DevAlone/proxy_py/tree/master/docs/tests.md)

## How to deploy on production using supervisor, nginx and postgresql in 8 steps?

1 Install supervisor, nginx and postgresql

`root@server:~$ apt install supervisor nginx postgresql`

2 Create virtual environment and install requirements on it

3 Install psycopg2

`(proxy_py) proxy_py@server:~/proxy_py$ pip3 install psycopg2`

4 create unprivileged user in postgresql database and add database authentication data to settings.py

```bash
proxy_py@server:~/proxy_py$ vim proxy_py/settings.py
```

```bash
DATABASE_CONNECTION_ARGS = (
    'postgresql://USERNAME:PASSWORD@localhost/DB_NAME',
)
```

5 Copy supervisor config example and change it for your case

```bash
root@server:~$ cp /home/proxy_py/proxy_py/config_examples/proxy_py.supervisor.conf /etc/supervisor/conf.d/proxy_py.conf
root@server:~$ vim /etc/supervisor/conf.d/proxy_py.conf
```

6 Copy nginx config example, enable it and change if you need

```bash
root@server:~$ cp /home/proxy_py/proxy_py/config_examples/proxy_py.nginx.conf /etc/nginx/sites-available/proxy_py
root@server:~$ ln -s /etc/nginx/sites-available/proxy_py /etc/nginx/sites-enabled/
root@server:~$ vim /etc/nginx/sites-available/proxy_py
```

7 Restart supervisor and nginx

```bash
root@server:~$ supervisorctl reread
root@server:~$ supervisorctl update
root@server:~$ /etc/init.d/nginx configtest
root@server:~$ /etc/init.d/nginx restart
```

8 Enjoy using it on your server!

## What is it depend on?

See requirements.txt
