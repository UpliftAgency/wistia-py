# Wistia Python API wrapper

**Please let me know if you start using this so we can collaborate on improving it.**

Wraps the [Wistia API](https://wistia.com/support/developers) using python's `requests` module.

Officially supports:

* Python 3.6+
* Python 2.7+

Also works on all the versions of python in [./tox.ini](./tox.ini).

```bash
pip install wistia-py
```

## Example use

Generate a Wistia API password at `https://<YOUR DOMAIN>.wistia.com/account/api`.

```python
import wistia_py
wistia = wistia_py.WistiaAPI(api_password=api_password)
response = wistia.project_create(name)
```

`response` is a python dict from the JSON returned by wistia

Not a lot of custom endpoints are implemented. (Please contribute!)

For now, if you need to make a generic call, you can do this:

```python
# Example of projects_update
response = wistia.call(
    'projects/<hashed id>.json',
    data=dict(name='updated project name'),
    method='PUT')
```

See mapping to: https://wistia.com/support/developers/data-api#projects_update

## Example Django integration

Create a file called `wistia.py` in your project somewhere:

```python
from django.conf import settings

_wistia = None


def get_wistia():
    global _wistia

    if not _wistia:
        import wistia_py
        _wistia = wistia_py.WistiaAPI(api_password=settings.WISTIA_API_PASSWORD)

    return _wistia
```

Meanwhile, elsewhere in Djangoland:

```python

from above_path.wistia import get_wistia
wistia = get_wistia()
response = wistia.project_create(name)
```

### A note on API keys, security and permissions

If you want more granular API control and tighter security, you can instantiate
multiple `WistiaAPI`s with different `api_password`s.

### Credits

This project was inspired by https://github.com/MattFisher/wistiapy.
