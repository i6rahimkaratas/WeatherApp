import customtkinter as ctk
from tkinter import messagebox
import threading
from weather_api import WeatherAPI

class WeatherApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Hava Durumu Uygulaması")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.weather_api = WeatherAPI()
        
        self.create_widgets()
        
        
        self.load_current_location()
    
    def create_widgets(self):
        
        title_label = ctk.CTkLabel(
            self.root, 
            text="🌤️ Hava Durumu", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=20)
        
        
        mode_frame = ctk.CTkFrame(self.root)
        mode_frame.pack(pady=5, padx=20, fill="x")

        mode_label = ctk.CTkLabel(mode_frame, text="Veri Kaynağı:", font=ctk.CTkFont(size=12))
        mode_label.pack(side="left", padx=10, pady=5)

        self.mode_switch = ctk.CTkSwitch(
            mode_frame,
            text="Gerçek API",
            command=self.toggle_api_mode,
            onvalue="real",
            offvalue="mock"
        )
        self.mode_switch.pack(side="right", padx=10, pady=5)
        
        
        location_frame = ctk.CTkFrame(self.root)
        location_frame.pack(pady=10, padx=20, fill="x")
        
        
        self.current_location_btn = ctk.CTkButton(
            location_frame,
            text="📍 Mevcut Konumum",
            command=self.load_current_location,
            height=40
        )
        self.current_location_btn.pack(side="left", padx=10, pady=10)
        
        
        search_frame = ctk.CTkFrame(self.root)
        search_frame.pack(pady=10, padx=20, fill="x")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Şehir adı giriniz...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Ara",
            command=self.search_city,
            height=40,
            width=80
        )
        search_btn.pack(side="right", padx=(5, 10), pady=10)
        
        
        self.weather_frame = ctk.CTkFrame(self.root)
        self.weather_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        
        self.loading_label = ctk.CTkLabel(
            self.weather_frame,
            text="Hava durumu yükleniyor...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.pack(expand=True)
        
        
        self.search_entry.bind("<Return>", lambda event: self.search_city())
    
    def toggle_api_mode(self):
        
        is_real_api = self.mode_switch.get() == "real"
        self.weather_api.toggle_mock_mode(not is_real_api)
        
        if is_real_api:
            messagebox.showinfo("Bilgi", "Gerçek API moduna geçildi. API key'inizin aktif olduğundan emin olun.")
        else:
            messagebox.showinfo("Bilgi", "Mock data moduna geçildi.")
    
    def clear_weather_display(self):
        
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        self.loading_label = ctk.CTkLabel(
            self.weather_frame,
            text="Hava durumu yükleniyor...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.pack(expand=True)
    
    def display_weather(self, weather_data, city_name=None):
        
        
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        if not weather_data:
            error_label = ctk.CTkLabel(
                self.weather_frame,
                text="❌ Hava durumu bilgisi alınamadı",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )
            error_label.pack(expand=True)
            return
        
        
        city_label = ctk.CTkLabel(
            self.weather_frame,
            text=city_name or weather_data.get('name', 'Bilinmeyen Şehir'),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        city_label.pack(pady=(20, 10))
        
        
        temp = weather_data['main']['temp']
        temp_label = ctk.CTkLabel(
            self.weather_frame,
            text=f"{temp:.1f}°C",
            font=ctk.CTkFont(size=48, weight="bold")
        )
        temp_label.pack(pady=10)
        
        
        description = weather_data['weather'][0]['description'].title()
        desc_label = ctk.CTkLabel(
            self.weather_frame,
            text=description,
            font=ctk.CTkFont(size=18)
        )
        desc_label.pack(pady=5)
        
        
        details_frame = ctk.CTkFrame(self.weather_frame)
        details_frame.pack(pady=20, padx=20, fill="x")
        
        
        feels_like = weather_data['main']['feels_like']
        feels_like_label = ctk.CTkLabel(
            details_frame,
            text=f"🌡️ Hissedilen: {feels_like:.1f}°C",
            font=ctk.CTkFont(size=14)
        )
        feels_like_label.pack(pady=5)
        
        
        humidity = weather_data['main']['humidity']
        humidity_label = ctk.CTkLabel(
            details_frame,
            text=f"💧 Nem: %{humidity}",
            font=ctk.CTkFont(size=14)
        )
        humidity_label.pack(pady=5)
        
        
        wind_speed = weather_data['wind']['speed']
        wind_label = ctk.CTkLabel(
            details_frame,
            text=f"💨 Rüzgar: {wind_speed} m/s",
            font=ctk.CTkFont(size=14)
        )
        wind_label.pack(pady=5)
        
        
        pressure = weather_data['main']['pressure']
        pressure_label = ctk.CTkLabel(
            details_frame,
            text=f"🌊 Basınç: {pressure} hPa",
            font=ctk.CTkFont(size=14)
        )
        pressure_label.pack(pady=5)
    
    def load_current_location(self):
        
        def load_location():
            self.clear_weather_display()
            lat, lon, city = self.weather_api.get_current_location()
            
            if lat and lon:
                weather_data = self.weather_api.get_weather_by_coords(lat, lon)
                self.root.after(0, lambda: self.display_weather(weather_data, city))
            else:
                self.root.after(0, lambda: messagebox.showerror("Hata", "Konum bilgisi alınamadı"))
        
        threading.Thread(target=load_location, daemon=True).start()
    
    def search_city(self):
        
        city_name = self.search_entry.get().strip()
        if not city_name:
            messagebox.showwarning("Uyarı", "Lütfen bir şehir adı giriniz")
            return
        
        def search_and_load():
            self.clear_weather_display()
            cities = self.weather_api.search_city(city_name)
            
            if cities:
                
                city = cities[0]
                weather_data = self.weather_api.get_weather_by_coords(city['lat'], city['lon'])
                self.root.after(0, lambda: self.display_weather(weather_data, city['name']))
            else:
                self.root.after(0, lambda: messagebox.showerror("Hata", f"'{city_name}' şehri bulunamadı"))
        
        threading.Thread(target=search_and_load, daemon=True).start()
    
    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()