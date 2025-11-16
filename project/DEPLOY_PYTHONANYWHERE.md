# Deploying LINEVA to PythonAnywhere

These instructions assume that the project is stored in `~/tkuv11/project/backend`.

## 1. Prepare the code

1. Push the repository to GitHub (or zip download).
2. Copy `.env.example` to `.env` locally and fill in real values.  
   When deploying to PythonAnywhere you can use SQLite by setting:
   ```
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
   DB_ENGINE=sqlite
   SQLITE_NAME=db.sqlite3
   ```

## 2. Upload to PythonAnywhere

1. Create an account and start a **Manual configuration** web app (Python 3.10 or higher).
2. In the **Files** tab upload the project or pull from Git (clone into `/home/yourusername/tkuv11`).
3. Create a virtual environment:
   ```bash
   mkvirtualenv lineva --python=/usr/bin/python3.10
   pip install -r ~/tkuv11/project/requirements.txt
   ```

## 3. Environment variables

PythonAnywhere doesn't read `.env` automatically. In the **Web** tab → **Environment variables** section,
add the values from your `.env` file (DJANGO_SECRET_KEY, DJANGO_DEBUG, etc.).  
For SQLite set `DB_ENGINE=sqlite` and `SQLITE_NAME=/home/yourusername/tkuv11/project/backend/db.sqlite3`.

## 4. WSGI configuration

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py` to point to the project:

```python
import os
import sys

path = '/home/yourusername/tkuv11/project/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. Database and static files

1. Open a bash console within the virtualenv:
   ```bash
   workon lineva
   cd ~/tkuv11/project/backend
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
2. In the **Web** tab map static files: URL `/static/` → `/home/yourusername/tkuv11/project/backend/staticfiles`.

## 6. Reload

Click **Reload** on the Web tab. Your site should now be available at
`https://yourusername.pythonanywhere.com`.

If you see errors, check the error log at `/var/log/yourusername.pythonanywhere.com.error.log`.
