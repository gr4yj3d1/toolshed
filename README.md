# toolshed

## Installation / Development

``` bash
git clone https://github.com/gr4yj3d1/toolshed.git
```
or
``` bash
git clone https://git.neulandlabor.de/j3d1/toolshed.git
```

### Backend

``` bash
cd toolshed/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python configure.py
python manage.py runserver 0.0.0.0:800 --insecure
```
to run this in properly in production, you need to configure a webserver to serve the static files and proxy the requests to the backend, then run the backend with just `python manage.py runserver` without the `--insecure` flag.

### Frontend

``` bash
cd toolshed/frontend
npm install
npm run dev
```

### Docs

``` bash
cd toolshed/docs
mkdocs serve
```



## CLI Client

### Requirements

- python3
- python3-nacl

### Usage Example

``` bash
cli-client/toolshed-client.py --key <hex private key> --user name@example.com --host 1.2.3.4:8000 getinventory
```