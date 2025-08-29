import os
from flask import Flask, render_template, request
import requests
from datetime import datetime
from dotenv import load_dotenv 


load_dotenv()

app = Flask(__name__)



API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"


def fetch_apod_data(selected_date=None):
    
    if not API_KEY:
        return {"error": "NASA API key is missing. Please check your .env file."}
        
    params = {'api_key': API_KEY}
    if selected_date:
        params['date'] = selected_date
    
    try:
        response = requests.get(NASA_APOD_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NASA API: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_date = request.form.get("date")
    else:
        selected_date = datetime.today().strftime('%Y-%m-%d')

    apod_data = fetch_apod_data(selected_date)
    
    
    if apod_data and 'error' in apod_data:
        return render_template("index.html", error=apod_data['error'], date=selected_date)
    elif apod_data:
        return render_template("index.html", data=apod_data)
    else:
        error_message = "Could not retrieve the picture for the selected date. Please try another."
        return render_template("index.html", error=error_message, date=selected_date)

if __name__ == "__main__":
    app.run(debug=True)