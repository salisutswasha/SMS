@echo off
REM Activate the virtual environment
call venv\Scripts\activate

REM Start the Django development server
python manage.py runserver
pause