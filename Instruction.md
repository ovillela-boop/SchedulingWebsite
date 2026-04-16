# Instructions on how to run python and contribute to design

## Using Visual Studio Code and Python 3.12 
## Please create separate branch, do not work directly in main, merge before finsihing your work so we all can be up to date

# First Time Setup
 
### Step 1 Set up Python environment in Visual Studio
* Install python extensions
* Go into project folder /SchedulingWebsites
* ctrl+shift+p (This should bring up the search bar in Visual Studio)
* Type and select Python: Create Environment 
* Pick venv and python 3.12
* Open new terminal and you should see (.venv) in front of your github (Example: ((.venv) example@example))
* Next run the code below and proceed to Step 2
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
* Run the code and continue
```bash
deactivate
```
* Continue with the following code and proceed to Step 2
```bash
sudo apt update
sudp apt install mysql-server
```

### Step 2 start my sql (outside of venv)
* this integrates SQLAlchemy with flask
* pymysql is the python driver that communicates with MYSQL
* Run the code
```bash
sudo systemctl start mysql
```

* Check the status
```bash
sudo systemctl status mysql
```
* Should return active (running)

### Step 3 Enter my SQL in the terminal
* Here you can create database that you need
```bash
sudo mysql
```
### step 4 Go back into venv
```bash
cd ~/SchedulingWebsite
source .venv/bin/activate
```
# Step 5 Integrate mySQL into python

* Inside virtual environment 
```bash
pip install flask-sqlalchemy pymysql
```
* flask-sqlalchemy: integrates SQLAlchemy with Flask
* PyMySQL: This is the python driver that talks to MySQL

## step 6 
* check you are running the correct sql version
```bash
mysql --version
```
## step 7 
* install cyptography 
```bash
pip install cryptography
```
* rerun app after installing








