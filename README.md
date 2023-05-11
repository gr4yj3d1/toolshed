# toolshed

## Installation

``` bash
git clone https://github.com/gr4yj3d1/toolshed.git
```

### Backend

``` bash
cd toolshed/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

``` bash
cd toolshed/frontend
npm install
npm run serve
```

### Docs

``` bash
cd toolshed/docs
mkdocs serve
```
