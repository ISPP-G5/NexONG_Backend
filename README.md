[![Bluejay Dashboard](https://img.shields.io/badge/Bluejay-Dashboard_05-blue.svg)](http://dashboard.bluejay.governify.io/dashboard/script/dashboardLoader.js?dashboardURL=https://reporter.bluejay.governify.io/api/v4/dashboards/tpa-ISPP-2024-GH-ISPP-G5_NexONG_Backend/main) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1f8b66f6985f491885213d03ba711707)](https://app.codacy.com/gh/ISPP-G5/NexONG_Backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Getting started with NexONG_Backend

Follow this guide to set up the project:

### 1. Clone the repository
- Clone NexONG-backend repository by executing `git clone https://github.com/ISPP-G5/NexONG_Backend.git` in the directory of your choice.

### 2. Configure the virtual environment
#### Linux
- Install virtualenv `pip install virtualenv`.
- In the root directory of the project you just cloned, create the virtual environment by running `python3 -m venv myenv`, myenv being what you want to name the virtual environment.
- Activate your new virtual environment with `source venv/bin/activate`.
  
#### Windows
You can create the Windows virtual environment by running commands as in Linux following this [guide](https://linuxhint.com/activate-virtualenv-windows/). However, I think the easiest option is creating it through VSCode.
- Open the cloned project in VSCode.
- Press `ctrl+shift+p` on your keyboard.
- Select the option `Python: Select Interpreter`.
- Press `+ Create Virtual Environment`.
- Select `Venv`.
- Select `Python 3.11`
- If there is a pop-up about the requirements, just press `OK`.
- If you see that it is not activated automatically, close the VSCode window and open it again.
- When it is activated, you should be able to see `(.myenv)` on the terminal, something like this:

![image](https://github.com/ISPP-G5/NexONG_Backend/assets/73229219/585b1dad-3b52-45d9-860b-d37cbbc39a6d)

### 3. Install requirements
- Install project dependencies by running `pip install -r requirements.txt` in the project's root folder.

### 4. Create the database
#### Unix
- Install postgres running `sudo apt install postgresql`.
- Access the postgres instance with `sudo su - postgres`.
- Create the user for the database `psql -c "create user nexong with password 'nexong'"`.
- Create the database `psql -c "create database nexongdb owner nexong"`.
- Set the role `psql -c "ALTER USER nexong CREATEDB"`.

#### Windows
- Install postgres on your machine from the official [website](https://www.postgresql.org/download/).
- Access the installation folder `C:\Program Files\PostgreSQL\16\bin` and execute `psql -U postgres`.
- Create the user for the database `CREATE USER nexong WITH PASSWORD 'nexong';`.
- Create the database `create database nexongdb owner nexong;`.
- Set the role `ALTER USER nexong CREATEDB;`. 

_You can check if the database is correctly created using `\l` in the psql instance_

### 5. Migrate the app and populate the database
In the root folder of the project, run:
- `python manage.py makemigrations nexong`
- `python manage.py migrate`
- `python manage.py loaddata populate.json`

### 6. Run the app
In the root folder of the project, run:
- `python manage.py runserver`
- Access to the DEMO API on `http://127.0.0.1:8000/api/`

### 7. Swagger documentation
To consult the API's Swagger documentation you can check it in `http://127.0.0.1:8000/docs` while the app is running.

# Usual errors encountered with the backend
### 1. DB has been updated
It's not unusual for the database to change. This causes an error, which usually, looks like this:

![image](https://github.com/ISPP-G5/NexONG_Backend/assets/73229219/40ccc5b1-a6e5-44eb-8d9d-a32d1f1cf3f2)

This happens because the migrations that were used to create the DB don't apply anymore. The solution is quite straightforward. Instead of executing the same commands every time and waste time, let's make shell scripts:

- Open the backend project in VSCode and create the folder `.vscode` in the root folder. It should look like this:

![image](https://github.com/ISPP-G5/NexONG_Backend/assets/73229219/05fb98af-d041-4974-a427-bb81ca86638c)

#### Linux
- Create a file called `drop_db.sh` inside `.vscode` and paste this inside it:
```bash
#!/bin/bash

# Define PostgreSQL database name
DB_NAME="nexongdb"

# Prompt for sudo password
echo "Please enter your sudo password:"
read -s SUDO_PASSWORD

# Stop PostgreSQL service
echo "$SUDO_PASSWORD"

# Drop PostgreSQL database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"
sudo -u postgres psql -c "create database $DB_NAME owner nexong"
sudo -u postgres psql -c "ALTER USER nexong CREATEDB"

echo "Database '$DB_NAME' has been deleted successfully."
```
- Then, create another file in the same folder as `drop_db.sh` called `migrations.sh` and paste the following code inside it:
```bash
#!/bin/bash

# Install requirements
pip install -r requirements.txt

# Delete previous migrations
rm -rf nexong/migrations

# Make migrations
python manage.py makemigrations nexong

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

#Loaddata
python manage.py loaddata populate.json

# Run server
python manage.py runserver
```
- Make both scripts executable by running this in the `.vscode` directory:
```bash
chmod +x drop_db.sh
chmod +x migrations.sh
```
- Finally, run first the `drop_db.sh` script and then the `migrations.sh` script.
To run them, go to the `.vscode` directory, execute `drop_db.sh` or `migrations.sh` in the terminal.

#### Windows
- Create a file called `drop_db.bat` inside `.vscode` and paste this inside it:
```bash
@echo off
cd /d "C:\Program Files\PostgreSQL\16\bin"
echo Changing directory to PostgreSQL bin folder...
echo.

set PGPASSWORD=your_postgres_password

echo Dropping existing PostgreSQL database if it exists...
echo.
psql -U postgres -c "DROP DATABASE IF EXISTS nexongdb;"
echo.

echo Creating PostgreSQL database...
echo.
psql -U postgres -c "CREATE DATABASE nexongdb WITH OWNER nexong;"
echo.

echo PostgreSQL database created successfully.

cd /d "C:\Your_backend_project_root"
echo Changing directory to the project root...
echo.
```
- Then, create another file in the same folder as `drop_db.bat` called `migrations.bat` and paste the following code inside it:
```bash
@echo off
echo Going back one directory...
cd ..

echo Deleting "migrations" folder in "/root/nexong"...
rd /s /q "nexong\migrations"

echo Installing requirements...
pip install -r requirements.txt

echo Running "python manage.py makemigrations nexong"...
python manage.py makemigrations nexong

echo Running "python manage.py migrate"...
python manage.py migrate

echo Running "python manage.py loaddata populate.json"...
python manage.py loaddata populate.json

echo All steps completed successfully.
```
_Note: if you want you can add `python manage.py runserver` at the end of the script or `python manage.py createsuperuser` after the populate command_
- Finally, run first the `drop_db.bat` script and then the `migrations.bat` script.
To run them, go to the `.vscode` directory, execute `drop_db.bat` or `migrations.bat` in the terminal.

In this way, the usual problem of DB modification is solved.
