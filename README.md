# Catalog project.
Website for book markup collaboration.
Moscow Aviation Institute @ 2019.

## Quick Start

   ```
   (* activate your virtual environment *)
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py test # Run the standard tests. These should all pass.
   python manage.py createsuperuser # Create a superuser 
   python manage.py runserver
   ```

1. Open tab to `http://127.0.0.1:8000` to see the main site.
2. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
