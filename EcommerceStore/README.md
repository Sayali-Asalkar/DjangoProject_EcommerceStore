# Ecommerce Website — Django + Bootstrap

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Store: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

Create categories/products in Admin. Product images are uploaded to media/products/.
