import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ===== 🔐 CONFIGURATION (HARDCODED - SEE WARNING BELOW) =====

API_KEY = "5ffc3e0ddd2162d71d3123e19373de50"
EMAIL_ADDRESS = "meetmalpani9b.school@gmail.com"
EMAIL_PASSWORD = "awaiwwidcjzyqoob"
RECIPIENT_EMAIL = "meetmalpani.5b@gmail.com"

# 📍 Location (Surat, India)
LAT = 19.8036
LON = 72.756

# 🌦️ API Endpoint (fixed: removed trailing spaces)
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ===== FUNCTIONS =====

def get_forecast(lat, lon, api_key, cnt=40):
    """Fetch 3-hour interval weather forecast from OpenWeatherMap"""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",  # Temperature in Celsius
        "cnt": cnt
    }
    response = requests.get(FORECAST_URL, params=params)
    response.raise_for_status()  # Raise error if API call fails
    return response.json()

def check_rain_next_12h(forecast_data):
    """
    Check next 4 forecast intervals (12 hours) for rain conditions.
    Returns: (bool, list_of_rain_events)
    """
    rain_events = []
    
    # Each forecast item = 3 hours; 4 items = 12 hours
    for item in forecast_data["list"][:4]:
        description = item["weather"][0]["description"].lower()
        rain_keywords = ["rain", "drizzle", "shower", "thunderstorm"]
        
        if any(keyword in description for keyword in rain_keywords):
            rain_events.append({
                "time": datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d %H:%M"),
                "description": item["weather"][0]["description"].title(),
                "temperature": item["main"]["temp"],
                "rainfall_mm": item.get("rain", {}).get("3h", 0)
            })
    
    return len(rain_events) > 0, rain_events

def send_email_alert(rain_events, recipient):
    """Send a formatted rain alert email via Gmail SMTP"""
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = f"🌧️ RAIN ALERT: {len(rain_events)} occurrence(s) in next 12 hours"
    
    # Build email body
    body = f"""🌦️ RAIN ALERT SYSTEM
{'='*50}

📍 Location: Latitude {LAT}, Longitude {LON}
🕐 Checked at: {datetime.now().strftime("%Y-%m-%d %H:%M")}

"""
    for i, event in enumerate(rain_events, 1):
        body += f"""⚠️  Alert #{i}
   🕐 Time: {event['time']}
   🌧️  Condition: {event['description']}
   🌡️  Temperature: {event['temperature']}°C"""
        if event['rainfall_mm'] > 0:
            body += f"\n   💧 Expected Rainfall: {event['rainfall_mm']}mm"
        body += "\n\n"
    
    body += """💡 Tip: Carry an umbrella! ☔
— Sent by your Rain Alert Bot 🤖"""
    
    msg.set_content(body)
    
    # Send via Gmail SMTP (port 587 + STARTTLS)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Secure the connection
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.send_message(msg)
    
    print(f"✅ Email alert sent to {recipient}")

def run_rain_check():
    """Main function: Fetch forecast, check for rain, send alert if needed"""
    try:
        print(f"🔍 Checking rain forecast for next 12 hours...")
        
        # Get forecast data from API
        forecast = get_forecast(LAT, LON, API_KEY)
        
        # Check if rain is expected
        is_rain, rain_events = check_rain_next_12h(forecast)
        
        if is_rain:
            print(f"🌧️ Rain expected! Sending alert for {len(rain_events)} occurrence(s)...")
            send_email_alert(rain_events, RECIPIENT_EMAIL)
        else:
            print("☀️ No rain expected in next 12 hours. No alert sent.")
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ API Error: {e}")
        if "401" in str(e):
            print("💡 Fix: Check API key at https://home.openweathermap.org/api_keys")
    except smtplib.SMTPAuthenticationError:
        print("❌ Email Auth Failed!")
        print("💡 Fix: Generate a NEW App Password at:")
        print("   https://myaccount.google.com/apppasswords")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")

# ===== RUN THE SCRIPT =====
if __name__ == "__main__":
    run_rain_check()
