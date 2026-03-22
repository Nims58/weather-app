1. Install Python (if not installed) and create/activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run migrations and start the server:
   - `python manage.py migrate`
   - `python manage.py runserver`

## App wiring

The weather app is installed and its URLs are included at the project root (/).

## OpenWeatherMap

The app loads secrets from `.env` in the project root.

PowerShell example:
  $env:OPENWEATHERMAP_API_KEY = "your_key"

Local `.env` example:
  OPENWEATHERMAP_API_KEY=your_key
  OPENWEATHERMAP_DEFAULT_CITY=Berlin
  OPENWEATHERMAP_DEFAULT_UNITS=metric

Then call:
  /weather/?city=Berlin
