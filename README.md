[![Bluejay Dashboard](https://img.shields.io/badge/Bluejay-Dashboard_05-blue.svg)](http://dashboard.bluejay.governify.io/dashboard/script/dashboardLoader.js?dashboardURL=https://reporter.bluejay.governify.io/api/v4/dashboards/tpa-ISPP-2024-GH-ISPP-G5_NexONG_Backend/main) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1f8b66f6985f491885213d03ba711707)](https://app.codacy.com/gh/ISPP-G5/NexONG_Backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Getting started with NexONG_Backend

Follow this guide to set up the project:

### 1. Clone the repository
- Clone NexONG-backend repository `git clone https://github.com/ISPP-G5/NexONG_Backend.git` in the directory of your choice.

### 2. Configure the virtual environment
#### Linux
- Install virtualenv `pip install virtualenv`
- In the root directory of the project you just cloned, create the virtual environment by running 
- Create virtual environment `python3 -m venv myenv`, myenv being what you want to name the virtual environment
- Activate virtual environment with `source venv/bin/activate`
  
#### Windows
You can create the Windows virtual environment by running commands as in Linux [here](https://linuxhint.com/activate-virtualenv-windows/). However, I think the easiest option is creating it through VSCode.
- Open the cloned project in VSCode
- Press `ctrl+shift+p` on your keyboard
- Select the option `Python: Select Interpreter`
- Press `+ Create Virtual Environment`
- Select `Venv`
- Select `Python 3.11`
- If there is a pop-up about the requirements, just press `OK`
- To activate it, close the VSCode window and open it again.
- You should be able to see `(.myenv)` on the terminal, something like this:

![image](https://github.com/ISPP-G5/NexONG_Backend/assets/73229219/585b1dad-3b52-45d9-860b-d37cbbc39a6d)

### 3. Install requirements
- Install project dependencies `pip install -r requirements.txt`

### 4. Create the database
#### Unix
- Install postgres running `sudo apt install postgresql`
- Access the postgres instance with `sudo su - postgres`
- Create the user for the database `psql -c "create user nexong with password 'nexong'"`
- Create the database `psql -c "create database nexongdb owner nexong"`
- Set the role `psql -c "ALTER USER nexong CREATEDB"`

#### Windows
- Install postgres on your machine from the official website https://www.postgresql.org/download/
- Access the installation folder `C:\Program Files\PostgreSQL\16\bin` and execute `psql -U postgres`
- Create the user for the database `CREATE USER nexong WITH PASSWORD 'nexong';`
- Create the database `create database nexongdb owner nexong;`
- Set the role `ALTER USER nexong CREATEDB;`

_You can check if the database is corrrectly created using `\l` in the psql instance_

### 5. Migrate the app and populate the database
In the root folder of the project, run:
- `python manage.py makemigrations nexong`
- `python manage.py migrate`
- `python manage.py loaddata populate.json`

### 6. Run the app
In the root folder of the project, run:
- `python manage.py runserver`
- Access to the DEMO API on `http://127.0.0.1:8000/demoapi/`
