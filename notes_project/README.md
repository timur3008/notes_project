// ======================= > STEP 1. < ========================
First, create a virtual environment by running "py -m venv venv"
Then, activate venv with command "venv/Scripts/activate"
Run command "pip install -r requirements.txt"
// ============================================================
// ======================= > STEP 2. < ========================
Then, commit migrations by commands below
"py manage.py makemigrations"
"py manage.py migrate"
After, you need to create a superuser and enter you username, email and password
"py manage.py createsuperuser"
// ============================================================
// ======================= > STEP 3. < ========================
After all, it is time to run server
Before, change you directory by command "cd notes_project"
There is a "manage.py" file and run this file with command "py manage.py runserver"
If your server is running, find directory with name "frontend" and run by hand file "index.html"
// ============================================================
