# Persona API

New implementation of persona api using Python 3 and Falcon framework.
Python 2 and Flask framework version could be find at: https://github.com/MicheDev3/persona-api

### Setting up the container:

##### BUILD CONTAINER:

    docker build -t persona-api:<version> .

##### RUN CONTAINER:

    docker run -p <local_port>:<docker_port> -it persona-api:<version>

IMPORTANT: The first port (local port) can be what ever I want the second port (docker port) must be the same as the PORT env in the docker file. If you want, you can change the docker port when starting the container like so:

    docker run -p <local_port>:<docker_port> -e PORT=<docker_port> -it persona-api:<version>

### Setting up the local environment for debugging using Pycharm:

##### USING VIRTUALENV:

Create a virtual environment:

    virtualenv <env_name> --python=<path_to_python>

Create a virtual environment (inheriting systems package):

    virtualenv <env_name> --python=<path_to_python> --system-site-packages

Activate virtual environment:

    source <env_name>/bin/activate

Deactivate virtual environment:

    deactivate

##### USING VIRTUALENVWRAPPER:

###### UNIX:

Install virtualenvwrapper:

    pip install virtualenvwrapper

Setting virtualenvwrapper in bash_profile:

    # Setting virtualenvwrapper

    # set where virutal environments will live
    export WORKON_HOME=$HOME/environment/.virtualenvs
    # ensure all new environments are isolated from the site-packages directory
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
    # use the same directory for virtualenvs as virtualenvwrapper
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    # use a default python version
    export VIRTUALENV_PYTHON=<path-to-python-version>
    # makes pip detect an active virtualenv and install to it
    export PIP_RESPECT_VIRTUALENV=true

    if [[ -r <path-to-virtualenvwrapper.sh> ]]; then
    source <path-to-virtualenvwrapper.sh>
    else
        echo "WARNING: Can't find virtualenvwrapper.sh"
    fi
    
###### WINDOWS:

Install virtualenvwrapper:

    pip install virtualenvwrapper-win
    
Add the following environment variables:

    set WORKON_HOME=%HOMEPATH%/environment/.virtualenvs
    set VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
    set PIP_VIRTUALENV_BASE=$WORKON_HOME
    set VIRTUALENV_PYTHON=<path-to-python-version>
    set PIP_RESPECT_VIRTUALENV=true

##### VIRTUALENV COMMANDS:

Create a virtual environment:

    mkvirtualenv <env_name> --python=<path_to_python>

Create a virtual environment (inheriting systems package):

    mkvirtualenv <env_name> --python=<path_to_python> --system-site-packages

Activate virtual environment:

    workon <env_name>

Deactivate virtual environment:

    deactivate

IMPORTANT: If using PyCharm make sure to associate the virtual env to the project.

##### INSTALL DEPENDENCIES:

Install all the project requirements:

    pip install -r requirements.txt
    
### CONFIGURE PYCHARM DEBUGGING SERVER CONFIGURATION:
* go to edit configuration
* create a new python configuration (if you use the enterprise edition you may choose a flask configuration)
* set in the script panel the path to the main flask entrypoint (in this case run.py)
* set the following environment variables: HOST, PORT, SECRET_KEY, LOG_LEVEL, SQLALCHEMY_DATABASE_URI
* set the proper python runtime (should point to the virtualenv if used one)
* set the working directory (in this case the path to src folder)

### CONFIGURE VIRTUALENV WITH ENVIRONMENT (IF USING VIRTUALENVWRAPPER):

###### UNIX:

Add the following environment variables inside activate.sh:
    
    export HOST=<ip-address>
    export PORT=<port>
    export SECRET_KEY=<secret-key>
    export LOG_LEVEL=<log-level>
    export SQLALCHEMY_DATABASE_URI=<connection-uri>
    
Add into PYTHONPATH the root project folder path inside activate.sh:
    
    export OLD_PYTHON_PATH=$PYTHONPATH
    export PYTHONPATH=$PYTHONPATH:<path-to-persona-api>
    
Remove the environment variables from deactivate.sh:

    unset HOST
    unset PORT
    unset SECRET_KEY
    unset LOG_LEVEL
    unset SQLALCHEMY_DATABASE_URI

Remove changes into PYTHONPATH inside deactivate.sh:

    export PYTHONPATH=$OLD_PYTHON_PATH
    
IMPORTANT: I am not 100% sure about PYTHONPATH changes since I did it this only on Windows (I created this project using Windows and right now I cannot use an Unix System in order to see what changes need to be performed), where I changed activate.bat and deactivate.bat in order to modify the PYTHONPATH only for this virtual enviroment.

###### WINDOWS

Add the following environment variables inside activate.bat:
    
    set "HOST=<ip-address>"
    set "PORT=<port>"
    set "SECRET_KEY=<secret-key>"
    set "LOG_LEVEL=<log-level>"
    set "SQLALCHEMY_DATABASE_URI=<connection-uri>"
    
Add into PYTHONPATH the root project folder path inside activate.bat::

    set "PYTHONPATH=<path-to-persona-api>;%PYTHONPATH%"
    
Remove the environment variables from deactivate.bat:

    set HOST=
    set PORT=
    set SECRET_KEY=
    set LOG_LEVEL=
    set SQLALCHEMY_DATABASE_URI=

Change the if-else statement into deactivate.bat with this statement:
       
    if defined _OLD_VIRTUAL_PYTHONPATH (
        set "PYTHONPATH=%_OLD_VIRTUAL_PYTHONPATH%"
        REM added
        set _OLD_VIRTUAL_PYTHONPATH=
    ) else (
        REM added
        set PYTHONPATH=
    )

IMPORTANT: Those configuration would allow you to use alembic commands, projects commands (in src/commands) and start the server using python run.py into the terminal.

IMPORTANT: Pycharm automatically, when open a new terminal, source the virtualenv but it will not call the activate.bat (I think it would not call activate.sh either but I am not sure of this I would need to perform some test with virtualenvwrapper for Unix) so I deactivate in Pycharm Terminal settings the virtualenv source (every time I open a new terminal I workon the virtualenviroment for this project). 

### DATABASE:

Initialize database folder and configuration:
 
    alembic init migrations

NB: This command should be run into the root folder and only one time.

IMPORTANT: In order to have the migrations folder into src you need to move it into src (since the folder is created where the command has been run). After that you need to modify alembic.ini script_location with the new path (src/migrations and not migrations).

Create database migrations (with no specific migration name):

    alembic revision --autogenerate 
    
Create database migrations (with specific migration name):

    alembic revision -m "<migration-name>" --autogenerate
    
IMPORTANT: In order to use the --autogenerate keyword you need to have this snippet inside src/migrations/env.py (a good place could be before the functions):

    from src.models.persona import Model
    target_metadata = Model.metadata
    
IMPORTANT: In order to be alembic.ini agnostic about the database connection uri you need to add this snippet into src/migrations/env.py inside run_migrations_online function:

    # overriding the sqlalchemy.url based on env settings
    from src import settings
    config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DATABASE_URI)
    
Apply migration into the database:

    alembic upgrade head

Rollback database migration:

    alembic downgrade -1
    
Import persona data into database (after getting inside path src/commands):

    python import.py persona mysql://<user>:<password>@<ip-address>/<db-name> fake_profiles.json 
    
### API DESCRIPTION:

The Api are versioned in order to upgrade (but always having the possibility to serve the older versions) more easily.

NB: There is a debate about how to version APIs some tells to version them using a HTTP Header in order to have permanent links (this does not "break" the REST philosophy) others that is fine to version using the urls. I think they are both correct and depends on the situation maybe if using a reverse proxy it is fine since the client could still use permanent links with the server proxy and the server proxy use with the actual backend server the url versioned,  anyway in this case I am using the latter.

There are two major resources:
* Search
  * GET api/v1/search?username={username}
* People
  * GET api/v1/people?offset={offset}&limit={limit}
  * DELETE api/v1/people?username={username}
  
All the resources are based on the Persona Model in order to retrieve data needed.

There are four middleware used to perform a specific behavior for the resources, instead of using hooks:
* AuthenticationManager: check if the authentication is correct using HTTP Header 
* SessionManager: inject the db session into the resources, opening and closing the connection. It will commit only if no error occurred.
* ValidatorManager: validate the inputs based on resource conditions

For intercepting error different from falcon.HTTPError I had to create a custom error handler:
* src/\__init\__.py : custom_error_handler log unsuccessfully response (generic exception and falcon.HTTPError) 

As server I am using waitress, since I am developing this project using Windows and not Unix, otherwise I would maybe use Gunicorn.

For running the server by terminal use the following command:

    python run.py
    
IMPORTANT: All the environment variables must be properly set. 
