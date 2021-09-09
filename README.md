# API YaMDb
## How to install
1. Clone repo to your local computer
2. Create a virtual env ($python -m venv venv)
3. Activate virtual env ($source venv/Scripts/activate if u use Windows and $source venv/bin/activate if u use Linux)
4. Install requirements ($pip install -r requirements.txt)
5. Migrate DB (
$cd yatube_api/
$python manage.py migrate
)
6. Run server ($python manage.py runserver)
## Read the docs at http://127.0.0.1:8000/redoc and have fun!
