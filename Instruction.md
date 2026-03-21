# Instructions on how to run python and contribute to design

## Using Visual Studio Code and Python 3.12 
## Please create separate branch, do not work directly in main, merge before finsihing your work so we all can be up to date

### Step 1 Set up Python environment in Visual Studio
* Install python extensions
* Go into project folder /Schedulingwebsites
* ctrl+shift+p
* Type and select Python: Create Environment 
* Pick venv and python 3.12
* Open new terminal and you should see (.venv) in front of your github
*Run the code
```bash
pip install flask


```

### Step 2 Run the Flask Application (in (.venv))
```bash
python main.py
```
* Click ip address in "running on http://<ip-link> and open browser


# MySQL Setup and  Integration (Ubuntu/Linux)

### Step 1 install mySQL on the system
* Make sure you do this outside of venv
```
deactivate
```
* Continue
```
sudo apt update
sudp apt install mysql-server
```

### step 2 start my sql (outside venv)
* this integrates SQLAlchemy with flask
* pymysql is the python driver that communicates with MYSQL
```
sudo systemctl start mysql
```

* Check the status after running that with command 
```
sudo systemctl status mysql
```
* Should return active (running)

### Step 3 Open my SQL
* Here you can create database that you need
```
sudo mysql
```
### step 4 Go back into venv
```
cd ~/SchedulingWebsite
source .venv/bin/activate
```
# Step 5 Integrate mySQL into python

* Inside virtual environment 
```
pip install flask-sqlalchemy pymysql
```
* flask-sqlalchemy: integrates SQLAlchemy with Flask
* PyMySQL: Python driver that talks to MySQL

## step 6 
* check you are running the correct sql version
```
mysql --version
```
## step 7 
* install cyptography 
```
pip install cryptography
```
* rerun app after installing








