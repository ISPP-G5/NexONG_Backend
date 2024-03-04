[![Bluejay Dashboard](https://img.shields.io/badge/Bluejay-Dashboard_05-blue.svg)](http://dashboard.bluejay.governify.io/dashboard/script/dashboardLoader.js?dashboardURL=https://reporter.bluejay.governify.io/api/v4/dashboards/tpa-ISPP-2024-GH-ISPP-G5_NexONG_Backend/main) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1f8b66f6985f491885213d03ba711707)](https://app.codacy.com/gh/ISPP-G5/NexONG_Backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Getting started with NexONG_Backend

Follow this guide to setup the project:

### Configure virtual enviroment
- Install virtualenv `pip install virtualenv`
- Create a project directory `mkdir nexong-env`
- Move to env directory with `cd nexong-env`
- Create virtual enviroment `virtualenv venv -p python3.11`
- Activate virtual enviroment
    - **(Unix)** with `source venv/bin/activate` 
    - **(Windows)** follow this guide https://linuxhint.com/activate-virtualenv-windows/
> Note: if you are not going to use the app, dont forget to deactivate the virtualenv by simply writing `deactivate`
  
### Clone and install requirements
- Clone NexONG-backend repository `git clone https://github.com/ISPP-G5/NexONG_Backend.git`
- Move to NexOng repo with `cd NexONG_Backend`
- Install project dependencies `pip install -r requirements.txt`

### Create the database
- Install postgres from the official website https://www.postgresql.org/download/
#### Unix
- Access the postgres instance with `sudo su - postgres`
- Create the user for the database `psql -c "create user nexong with password 'nexong'"`
- Create the database `psql -c "create database nexongdb owner nexong"`
- Set the role `psql -c "ALTER USER nexong CREATEDB"`

#### Windows
- Access the instalation folder `C:\Program Files\PostgreSQL\16\bin` and execute `psql -U postgres`
- Create the user for the database `CREATE USER nexong WITH PASSWORD 'nexong';`
- Create the database `create database nexongdb owner nexong;`
- Set the role `ALTER USER nexong CREATEDB;`

_You can check if the database is corrrectly created using `\l` in the psql instance_

### Migrate the app
- Migrate the app `./manage.py makemigrations` & `./manage.py migrate` or `manage.py makemigrations` & `manage.py migrate`

### Create superuser
- `./manage.py createsuperuser`

### Done! now run the app
- Run the API `./manage.py runserver` or `manage.py runserver`
- Access to the DEMO API on `http://127.0.0.1:8000/demoapi/`

### Populate the database
- Populate the database `./manage.py loaddata populate.json` or `manage.py loaddata populate.json`
