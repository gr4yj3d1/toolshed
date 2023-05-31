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
mkdir static                       # FIXMEMAYBE "Weiß  ich auch gar nicht, ob das benötigt wird."
python manage.py makemigrations    # FIXME
python manage.py migrate
python manage.py runserver
```

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
