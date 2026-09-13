import os
import requests
import threading
import random
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import customtkinter as ctk
from tkinter import messagebox

# ==========================================
# Configuration & Environment
# ==========================================
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY", "5ffc3e0ddd2162d71d3123e19373de50")
GEO_IP_URL = "http://ip-api.com/json/"

# Set CustomTkinter to Dark Mode
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ==========================================
# Matte Black & Cyber UI Color Palette
# ==========================================
COLORS = {
    "bg_main": "#0A0A0A",       # True Matte Black
    "bg_card": "#141414",       # Slightly lighter matte for cards
    "bg_input": "#1F1F1F",      # Inputs and buttons
    "bg_hover": "#2A2A2A",      # Hover states
    "accent_cyan": "#00E5FF",   # Cyber Cyan (Primary Accent)
    "accent_red": "#FF2A2A",    # Neon Red (Errors/Alerts)
    "accent_green": "#00E676",  # Neon Green (Success)
    "text_primary": "#F5F5F5",  # Bright White/Gray
    "text_secondary": "#888888",# Muted Gray
    "border": "#222222"         # Subtle borders
}

# ==========================================
# BeautifulSoup Utility Functions
# ==========================================
def get_weather_tips():
    html_tips = """
    <div class="weather-tips">
        <p>☀️ Wear sunscreen if the UV index is high (5+).</p>
        <p>💧 Stay hydrated when temperatures exceed 30°C.</p>
        <p>🧥 Dress in layers when it's chilly below 15°C.</p>
        <p>☔ Carry an umbrella if rain or thunderstorms are expected.</p>
        <p>🌬️ Secure loose objects if wind speeds exceed 40 km/h.</p>
        <p>🌫️ Check the Air Quality Index before going for a run.</p>
        <p>🌡️ Heat index can make it feel 5° hotter than actual temp.</p>
    </div>
    """
    soup = BeautifulSoup(html_tips, 'html.parser')
    return [p.get_text() for p in soup.find_all('p')]

def parse_api_error(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        error_msg = soup.find('p') or soup.find('div') or soup.find('body')
        if error_msg: return error_msg.get_text(strip=True)[:150]
    except Exception: pass
    return "Unknown API error. Check your connection or API key."

# ==========================================
# Chatbot Assistant (Enhanced)
# ==========================================
class ChatBotAssistant:
    DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    @classmethod
    def generate_response(cls, message, weather_data=None, aqi_data=None):
        query = str(message).lower()
        if not weather_data:
            return "⚠️ System offline. Please search for a city to initialize data streams."
        
        if any(w in query for w in ['hello', 'hi', 'hey', 'status']):
            return "👋 Systems online. I can analyze temperature, precipitation, wind vectors, and air quality. What do you need?"
        if 'temp' in query or 'hot' in query or 'cold' in query:
            return f"🌡️ Thermal Scan: {weather_data['main']['temp']:.1f}°C\n🔥 Feels Like: {weather_data['main']['feels_like']:.1f}°C"
        if 'rain' in query or 'precipitation' in query:
            cond = weather_data['weather'][0]['main'].lower()
            return "☔ Precipitation detected. Deploy umbrella." if 'rain' in cond else "☀️ No precipitation in current radar."
        if 'wind' in query or 'breeze' in query:
            speed = weather_data['wind']['speed']
            deg = weather_data['wind'].get('deg', 0)
            direction = cls.DIRECTIONS[int((deg + 11.25) / 22.5) % 16]
            return f"💨 Wind Vector: {speed*3.6:.1f} km/h\n🧭 Trajectory: {direction}"
        if 'air' in query or 'aqi' in query or 'pollution' in query:
            if aqi_data and 'list' in aqi_data:
                aqi_val = aqi_data['list'][0]['main']['aqi']
                aqi_map = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
                return f"🌫️ Air Quality Index: {aqi_map.get(aqi_val, 'Unknown')} (Level {aqi_val})"
            return "⏳ Air quality sensors are still calibrating..."
        if 'help' in query or 'commands' in query:
            return "📡 Available queries: temp, rain, wind, air quality, or general recommendations."
        return "🤖 Query unrecognized. Try asking about 'temperature', 'rain', 'wind', or 'air quality'."

# ==========================================
# API Fetching Functions (Threaded & Parallel)
# ==========================================
def fetch_geocoding(city_name, callback=None):
    def _fetch():
        try:
            url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data: callback(data[0], None)
            else: callback(None, "City not found in geocoding database.")
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

def fetch_weather(lat, lon, callback=None):
    def _fetch():
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            if response.status_code == 200: callback(response.json(), None)
            else: callback(None, parse_api_error(response.text))
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

def fetch_forecast(lat, lon, callback=None):
    def _fetch():
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            callback(response.json(), None)
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

def fetch_air_quality(lat, lon, callback=None):
    def _fetch():
        try:
            url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            callback(response.json(), None)
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

def fetch_open_meteo(lat, lon, callback=None):
    def _fetch():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=uv_index_max,sunrise,sunset&timezone=auto"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            callback(response.json(), None)
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

def fetch_location(callback=None):
    def _fetch():
        try:
            response = requests.get(GEO_IP_URL, timeout=5)
            data = response.json()
            if data.get('status') == 'success':
                callback({'lat': data['lat'], 'lon': data['lon'], 'city': data['city']}, None)
            else: callback(None, "Geolocation failed.")
        except Exception as e: callback(None, str(e))
    threading.Thread(target=_fetch, daemon=True).start()

# ==========================================
# Main Application UI (Matte Black Cyber Theme)
# ==========================================
class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.title("HACK N CODE'S WEATHER DASHBOARD")
        self.geometry("450x850")
        self.minsize(400, 700)
        self.configure(fg_color=COLORS["bg_main"])
        
        self.weather_data = None
        self.aqi_data = None
        self.tips = get_weather_tips()
        
        self._build_ui()
        self.after(500, self.auto_detect_location)

    def _build_ui(self):
        # --- HEADER ---
        header_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_main"], height=60)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text="HACK N CODE'S", font=ctk.CTkFont(size=14, weight="bold", family="Consolas"), 
                     text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(header_frame, text="WEATHER DASHBOARD", font=ctk.CTkFont(size=18, weight="bold"), 
                     text_color=COLORS["accent_cyan"]).pack(side="left", padx=10)
        
        self.auto_btn = ctk.CTkButton(header_frame, text="📍", width=40, height=40, corner_radius=20,
                                      fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
                                      text_color=COLORS["accent_cyan"], font=ctk.CTkFont(size=18),
                                      command=self.auto_detect_location)
        self.auto_btn.pack(side="right")

        # --- SEARCH BAR ---
        search_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        search_frame.pack(fill="x", padx=20, pady=5)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city coordinates or name...", height=42,
                                         fg_color=COLORS["bg_card"], border_color=COLORS["border"],
                                         text_color=COLORS["text_primary"], placeholder_text_color=COLORS["text_secondary"])
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.on_search_submit())
        
        self.search_btn = ctk.CTkButton(search_frame, text="SCAN", width=80, height=42, corner_radius=8,
                                        fg_color=COLORS["accent_cyan"], hover_color="#00B8D4",
                                        text_color=COLORS["bg_main"], font=ctk.CTkFont(size=14, weight="bold"),
                                        command=self.on_search_submit)
        self.search_btn.pack(side="right")

        # --- MAIN SCROLLABLE AREA ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_main"], scrollbar_button_color=COLORS["bg_card"],
                                                   scrollbar_button_hover_color=COLORS["bg_hover"])
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- CURRENT WEATHER CARD ---
        self.current_card = ctk.CTkFrame(self.scroll_frame, corner_radius=16, fg_color=COLORS["bg_card"], border_color=COLORS["border"], border_width=1)
        self.current_card.pack(fill="x", pady=(0, 20), padx=10)
        
        self.loc_label = ctk.CTkLabel(self.current_card, text="📍 INITIALIZING SYSTEM...", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLORS["text_secondary"])
        self.loc_label.pack(pady=(20, 5))
        
        self.temp_label = ctk.CTkLabel(self.current_card, text="--°C", font=ctk.CTkFont(size=54, weight="bold"), text_color=COLORS["accent_cyan"])
        self.temp_label.pack()
        
        self.cond_label = ctk.CTkLabel(self.current_card, text="Awaiting Data Stream", font=ctk.CTkFont(size=16), text_color=COLORS["text_primary"])
        self.cond_label.pack(pady=(0, 5))
        
        self.feels_label = ctk.CTkLabel(self.current_card, text="Feels like --°C", font=ctk.CTkFont(size=14), text_color=COLORS["text_secondary"])
        self.feels_label.pack(pady=(0, 20))

        # --- HIGHLIGHTS GRID ---
        ctk.CTkLabel(self.scroll_frame, text="SYSTEM METRICS", font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", padx=20, pady=(10, 5))
        
        self.highlights_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["bg_main"])
        self.highlights_frame.pack(fill="x", padx=10)
        
        self.highlight_labels = {}
        highlights = [("💨 Wind", "wind"), ("💧 Humidity", "humidity"), ("☀️ UV Index", "uv"), 
                      ("👁️ Visibility", "visibility"), ("🌅 Sunrise", "sunrise"), ("🌇 Sunset", "sunset"),
                      ("🌫️ Air Quality", "aqi"), ("🌡️ Feels Like", "feels")]
        
        for i, (title, key) in enumerate(highlights):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(self.highlights_frame, corner_radius=12, fg_color=COLORS["bg_card"], border_color=COLORS["border"], border_width=1)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.highlights_frame.grid_columnconfigure((0, 1), weight=1)
            
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color=COLORS["text_secondary"]).pack(pady=(12, 2))
            lbl = ctk.CTkLabel(card, text="--", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["text_primary"])
            lbl.pack(pady=(0, 12))
            self.highlight_labels[key] = lbl

        # --- 5-DAY FORECAST ---
        ctk.CTkLabel(self.scroll_frame, text="5-DAY PROJECTION", font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        
        self.forecast_scroll = ctk.CTkScrollableFrame(self.scroll_frame, orientation="horizontal", height=140, 
                                                      fg_color=COLORS["bg_main"], scrollbar_button_color=COLORS["bg_card"])
        self.forecast_scroll.pack(fill="x", padx=10)

        # --- WEATHER TIPS (BeautifulSoup) ---
        ctk.CTkLabel(self.scroll_frame, text="INTELLIGENCE BRIEFING", font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        self.tip_label = ctk.CTkLabel(self.scroll_frame, text=random.choice(self.tips), font=ctk.CTkFont(size=13), 
                                      fg_color=COLORS["bg_card"], text_color=COLORS["accent_cyan"], 
                                      corner_radius=12, wraplength=380, height=50, border_color=COLORS["border"], border_width=1)
        self.tip_label.pack(fill="x", padx=10, pady=(0, 20))

        # --- QUICK CITIES ---
        ctk.CTkLabel(self.scroll_frame, text="QUICK NODES", font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", padx=20, pady=(0, 5))
        quick_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["bg_main"])
        quick_frame.pack(fill="x", padx=10, pady=(0, 20))
        for city in ["Bangalore", "Mumbai", "Delhi", "London", "New York"]:
            ctk.CTkButton(quick_frame, text=city, width=75, height=34, corner_radius=17,
                          fg_color=COLORS["bg_card"], hover_color=COLORS["bg_hover"],
                          text_color=COLORS["text_primary"], border_color=COLORS["border"], border_width=1,
                          font=ctk.CTkFont(size=12),
                          command=lambda c=city: self.search_city(c)).pack(side="left", padx=4)

        # --- CHATBOT TERMINAL ---
        ctk.CTkLabel(self.scroll_frame, text="AI WEATHER ASSISTANT", font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", padx=20, pady=(0, 5))
        
        chat_card = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS["bg_card"], corner_radius=12, border_color=COLORS["border"], border_width=1)
        chat_card.pack(fill="x", padx=10, pady=(0, 20))
        
        self.chat_box = ctk.CTkTextbox(chat_card, height=140, corner_radius=8, fg_color=COLORS["bg_main"],
                                       text_color=COLORS["accent_cyan"], font=ctk.CTkFont(family="Consolas", size=13))
        self.chat_box.pack(fill="x", padx=10, pady=(10, 5))
        self.chat_box.insert("0.0", "> SYSTEM ONLINE. Awaiting queries...\n")
        self.chat_box.configure(state="disabled")
        
        chat_input_frame = ctk.CTkFrame(chat_card, fg_color=COLORS["bg_card"])
        chat_input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.chat_entry = ctk.CTkEntry(chat_input_frame, placeholder_text="Enter command...", height=38,
                                       fg_color=COLORS["bg_main"], border_color=COLORS["border"],
                                       text_color=COLORS["text_primary"], placeholder_text_color=COLORS["text_secondary"])
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", lambda e: self.on_send_chat())
        
        ctk.CTkButton(chat_input_frame, text="EXEC", width=70, height=38, corner_radius=8,
                      fg_color=COLORS["accent_cyan"], hover_color="#00B8D4",
                      text_color=COLORS["bg_main"], font=ctk.CTkFont(size=13, weight="bold"),
                      command=self.on_send_chat).pack(side="right")

    # ==========================================
    # Logic & API Orchestration
    # ==========================================
    def show_status(self, message, is_error=False):
        color = COLORS["accent_red"] if is_error else COLORS["accent_green"]
        self.loc_label.configure(text_color=color)
        old_text = self.cond_label.cget("text")
        self.cond_label.configure(text=message, text_color=color)
        self.after(3000, lambda: self.cond_label.configure(text=old_text, text_color=COLORS["text_primary"]))

    def on_search_submit(self):
        city = self.search_entry.get().strip()
        if city: self.search_city(city)
        else: self.show_status("❌ ERROR: Null input", True)

    def search_city(self, city_name):
        self.show_status(f"🔄 Triangulating {city_name}...")
        fetch_geocoding(city_name, self.on_geocoding_received)

    def on_geocoding_received(self, data, error):
        if data:
            lat, lon = data['lat'], data['lon']
            fetch_weather(lat=lat, lon=lon, callback=self.on_weather_received)
        else:
            self.show_status(f"❌ {error}", True)

    def auto_detect_location(self):
        self.show_status("📍 Pinging IP Geolocation...")
        def callback(data, error):
            if data: fetch_weather(lat=data['lat'], lon=data['lon'], callback=self.on_weather_received)
            else: self.show_status("❌ Geolocation ping failed", True)
        fetch_location(callback=callback)

    def on_weather_received(self, data, error):
        if data:
            self.weather_data = data
            self.update_current_weather(data)
            lat, lon = data['coord']['lat'], data['coord']['lon']
            
            # Fire all supplementary APIs in parallel
            fetch_forecast(lat, lon, callback=self.on_forecast_received)
            fetch_air_quality(lat, lon, callback=self.on_air_quality_received)
            fetch_open_meteo(lat, lon, callback=self.on_sun_uv_received)
            
            self.show_status(f"✅ DATA STREAM ACTIVE: {data['name']}", False)
        else:
            self.show_status(f"❌ {error}", True)

    def update_current_weather(self, data):
        self.loc_label.configure(text=f"📍 {data['name']}, {data['sys']['country']}", text_color=COLORS["text_primary"])
        self.temp_label.configure(text=f"{data['main']['temp']:.1f}°C")
        self.cond_label.configure(text=data['weather'][0]['description'].title(), text_color=COLORS["text_primary"])
        self.feels_label.configure(text=f"Feels like {data['main']['feels_like']:.1f}°C")
        
        # Update Highlights
        wind_kmh = round(data['wind']['speed'] * 3.6, 1)
        deg = data['wind'].get('deg', 0)
        direction = ChatBotAssistant.DIRECTIONS[int((deg + 11.25) / 22.5) % 16]
        self.highlight_labels['wind'].configure(text=f"{wind_kmh} km/h {direction}")
        self.highlight_labels['humidity'].configure(text=f"{data['main']['humidity']}%")
        self.highlight_labels['feels'].configure(text=f"{data['main']['feels_like']:.1f}°C")
        
        vis_km = round(data['visibility'] / 1000, 1)
        self.highlight_labels['visibility'].configure(text=f"{vis_km} km")

    def on_air_quality_received(self, data, error):
        if data and 'list' in data:
            self.aqi_data = data
            aqi_val = data['list'][0]['main']['aqi']
            aqi_map = {1: ("Good", COLORS["accent_green"]), 2: ("Fair", "#FFEB3B"), 3: ("Moderate", "#FF9800"), 
                       4: ("Poor", COLORS["accent_red"]), 5: ("Very Poor", "#9C27B0")}
            text, color = aqi_map.get(aqi_val, ("Unknown", COLORS["text_secondary"]))
            self.highlight_labels['aqi'].configure(text=f"{aqi_val} - {text}", text_color=color)

    def on_sun_uv_received(self, data, error):
        if data and 'daily' in data:
            daily = data['daily']
            uv = daily['uv_index_max'][0]
            sunrise = daily['sunrise'][0].split('T')[1]
            sunset = daily['sunset'][0].split('T')[1]
            
            uv_color = COLORS["accent_green"] if uv < 3 else "#FF9800" if uv < 6 else COLORS["accent_red"]
            self.highlight_labels['uv'].configure(text=f"{uv:.1f} Index", text_color=uv_color)
            self.highlight_labels['sunrise'].configure(text=sunrise)
            self.highlight_labels['sunset'].configure(text=sunset)

    def on_forecast_received(self, data, error):
        if not data: return
        
        # Safely clear old cards (Prevents CustomTkinter TclError)
        for widget in self.forecast_scroll.winfo_children():
            try: widget.destroy()
            except Exception: pass
            
        daily_data = {}
        for item in data['list']:
            date_str = item['dt_txt'][:10]
            if date_str not in daily_data:
                daily_data[date_str] = {'min': float('inf'), 'max': float('-inf'), 'desc': {}}
            daily_data[date_str]['min'] = min(daily_data[date_str]['min'], item['main']['temp_min'])
            daily_data[date_str]['max'] = max(daily_data[date_str]['max'], item['main']['temp_max'])
            desc = item['weather'][0]['description'].lower()
            daily_data[date_str]['desc'][desc] = daily_data[date_str]['desc'].get(desc, 0) + 1
        
        for date_str, d in sorted(daily_data.items())[:5]:
            card = ctk.CTkFrame(self.forecast_scroll, width=85, height=120, corner_radius=12, 
                                fg_color=COLORS["bg_card"], border_color=COLORS["border"], border_width=1)
            card.pack(side="left", padx=5)
            card.pack_propagate(False)
            
            weekday = datetime.strptime(date_str, '%Y-%m-%d').strftime('%a')
            dominant_desc = max(d['desc'], key=d['desc'].get)
            emoji = "☀️" if 'clear' in dominant_desc else "☁️" if 'cloud' in dominant_desc else "🌧️" if 'rain' in dominant_desc else "🌤️"
            
            ctk.CTkLabel(card, text=weekday, font=ctk.CTkFont(size=14, weight="bold"), text_color=COLORS["text_secondary"]).pack(pady=(12, 0))
            ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=28)).pack()
            ctk.CTkLabel(card, text=f"{int(d['min'])}° / {int(d['max'])}°", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLORS["text_primary"]).pack()
            ctk.CTkLabel(card, text=dominant_desc.title(), font=ctk.CTkFont(size=10), text_color=COLORS["text_secondary"]).pack()

    def on_send_chat(self):
        msg = self.chat_entry.get().strip()
        if not msg: return
        
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"\n> USER: {msg}\n")
        self.chat_entry.delete(0, "end")
        
        response = ChatBotAssistant.generate_response(msg, self.weather_data, self.aqi_data)
        
        def add_response():
            self.chat_box.insert("end", f"> SYS: {response}\n")
            self.chat_box.see("end")
            self.chat_box.configure(state="disabled")
        
        self.after(300, add_response)

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
