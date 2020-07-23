1. Create a Virtual Environment
>>> python -m venv env_name

2. Activate the venv
>>> cd env_name
>>> cd Script
>>> activate
>>> cd..

3. Download file (Windows)
>>> git clone https://github.com/bita639/ghuri.git
>>> cd ghuri

4. Install dependicies 
>>> pip install -r requirement.txt

5. Make sure that xampp server is running and crate a table name "travel"

6. migrate the database by the following code:
>>>python manage.py makemigartions
>>>python manage.py migrate

7. create superuser for system admin
>>>python manage.py createsuperuser

give a user name and email and a password and then press Y and then press enter

8. now run the server
>>>python manage.py runserver

NB: If you get any error og module missing or not found please install or upgrade the modeule version. Thank You.
