# // ======================= > STEP 1. < ========================
_First, create a virtual environment by running_ ```"py -m venv venv"```
_Then, activate venv with command_ ```"venv/Scripts/activate"```
_Run command_ ```"pip install -r requirements.txt"```
# // ============================================================
# // ======================= > STEP 2. < ========================
_Then, commit migrations by commands below_
```"py manage.py makemigrations"```
```"py manage.py migrate"```
_After, you need to create a superuser and enter you username, email and password_
```"py manage.py createsuperuser"```
# // ============================================================
# // ======================= > STEP 3. < ========================
_After all, it is time to run server_
_Before, change you directory by command_ ```"cd notes_project"```
_There is a ***"manage.py"*** file and run this file with command_ ```"py manage.py runserver"```
_If your server is running, find directory with name_ ***"frontend"*** _and run by hand file_ ***"index.html"***
# // ============================================================
