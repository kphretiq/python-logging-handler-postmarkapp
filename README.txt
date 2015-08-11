# python-logging-handler-postmarkapp
Python logging handler sends email via postmarkapp api

## prerequisites
- requests (pip install requests.py)
- an active postmarkapp.com account with token

## installation
This is pretty niche, so I'm not going to submit it to PyPi. Local install should be pretty straightforward.

### the usual
```bash
$ pip install requests
$ python ./setup.py install
```
### virtualenv
```bash
project$ source venv/bin/activate
(venv)project$ pip install requests
(venv)project$ pip install pip install -e /path/to/python-logging-handler-postmarkapp
```

### config object
- **url**	always "https://api.postmarkapp.com/email"
- **token**	token supplied to you by postmarkapp
- **To**	a list of one or more email addresses
- **From**	a single email address

### optional
- **ReplyTo** a single email address

```python
{
	"To": ["victimA@example.com", "victimB@example.com"],
	"From": "info@example.com",
	"ReplyTo": "info@example.com",
	"url": "https://api.postmarkapp.com/email",
	"token": "Nice-Token-From-Postmarkapp",
}

```

## usage
An example named "test.py"

```python
#!/usr/bin/env python

import logging
from PostmarkappHandler.PMAHandler import PMAHandler

pmaconfig = {
	"To": ["victim@example.com"],
	"From": "info@example.com",
	"ReplyTo": "info@example.com",
	"url": "https://api.postmarkapp.com/email",
	"token": "Nice-Token-From-Postmarkapp",
}

logger = logging.getLogger("foo")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)
logger.addHandler(stream)

pma = PMAHandler(pmaconfig) 
pma.setLevel(logging.WARNING)
pma.setFormatter(formatter)
logger.addHandler(pma)

logger.info("test")
logger.warning("email test")
```
The StreamHandler will give you a nice heads up.
```bash
python ./test.py
2015-08-11 12:18:33,836 INFO test
2015-08-11 12:18:33,836 WARNING email test
```

Your email will arrive with the error message and hostname as subject, (since one may be doing logging on multiple hosts) and a json object as the body of the email (since I am lazy).
```json
{
 "function": "<module>", 
 "host": "kreplach", 
 "file": "./test.py", 
 "logger name": "foo", 
 "time": "2015-08-11 12:18:33,836", 
 "message": "email test", 
 "error level": "WARNING", 
 "module": "test"
}
```

