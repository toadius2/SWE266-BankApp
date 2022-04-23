# SWE266-BankApp

This is just for project study before we decide what techniques we will use. I followed the flask official [tutorial](https://flask.palletsprojects.com/en/2.1.x/tutorial/) to set up the project.

The tech stack in the project:
- Flask
- SQLite3

## Development

### Prerequisite
- Python 3.7 and newer

### Clone the project
```bash
# clone the project
$ git clone https://github.com/toadius2/SWE266-BankApp.git
$ cd SWE266-BankApp
```

### Create a `.flaskenv` file to put flask env variables under the root directory
```bash
# Linus/MacOS
export FLASK_APP='bankapp'
export FLASK_ENV='development'

# Windows
set FLASK_APP='bankapp'
set FLASK_ENV='development'
```

### Create a `.env` file to put app env variables under the root directory
```bash
SECRET_KEY='dev'
```

### Run Flask
```bash
# create an virtual environement for project
$ python3 -m venv venv

# activate virtual machine
# Unix or MacOS, run:
$ source venv/bin/activate
#Windows, run:
$ venv\Scripts\activate.bat

# install dependencies if needed
$ pip install -r "requirements.txt"

# If setting up database for the first time, initialize the sqlite database:
$ flask init-db

# run the application
$ flask run

# deactivate virtual machine
$ deactivate
```

Server will run at http://127.0.0.1:5000, and for development, you can use Postman to verify API, or use SQLite GUI to browse database.
