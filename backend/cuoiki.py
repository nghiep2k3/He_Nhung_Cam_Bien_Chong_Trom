from pnhLCD1602 import LCD1602
from EmulatorGUI import GPIO
from DHT22 import readSensor
from twilio.rest import Client
import time
import tkinter as tk
import pygame
import requests
import os
from dotenv import load_dotenv #Thêm vào

load_dotenv() #Thêm vào 

alarm_triggered = False
motion_deetected = False
lcd = LCD1602()
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)  
GPIO.setup(18, GPIO.OUT)  
root = tk.Tk()

url = 'http://127.0.0.1:5000/toggle'
system_activated = False  # Để theo dõi trạng thái hệ thống từ API

# Biến trạng thái để theo dõi báo động và hệ thống

def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play()

def send_sms():
    #Thêm token vào đây
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Đã phát hiện chuyển động lạ! Hệ thống báo động của bạn đã được kích hoạt.",
        from_='+19892678453',
        to='+84333078031'
    )
    print(f"Message sent: {message.sid}")

def display_temperature_humidity():
    pin = 4
    temperature, humidity = readSensor(pin)
    lcd.set_cursor(0, 0)
    lcd.write_string(f"Temp: {temperature:.1f}C Hum: {humidity:.1f}%")

def check_motion_sensor():
    global alarm_triggered
    if GPIO.input(25) == GPIO.HIGH:
        lcd.clear()
        display_temperature_humidity()
        lcd.set_cursor(1, 0)
        lcd.write_string("Đã phát hiện chuyển động!")
        GPIO.output(18, GPIO.HIGH)
        if not alarm_triggered:
            if not pygame.mixer.music.get_busy():
                play_alarm()
            send_sms()
            alarm_triggered = True
    else:
        lcd.clear()
        display_temperature_humidity()
        lcd.set_cursor(1, 0)
        lcd.write_string("Không có chuyển động")
        GPIO.output(18, GPIO.LOW)
        pygame.mixer.music.stop()
        alarm_triggered = False

def toggle_system(active):
    global system_activated
    system_activated = active
    if system_activated:
        print("Kích hoạt hệ thống")
        lcd.set_cursor(0, 0)
        lcd.write_string("DA KICH HOAT")
    else:
        print("Tắt hệ thống")
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.write_string("DA TAT")

def update():
    global system_activated

    # Gửi yêu cầu GET đến API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            api_status = data.get('status')

            # Chỉ cập nhật nếu trạng thái từ API khác với trạng thái hiện tại
            if api_status != system_activated:
                system_activated = api_status
                toggle_system(system_activated)  # Kích hoạt/tắt hệ thống từ API

        else:
            print(f"Lỗi: {response.status_code}")

    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi yêu cầu API: {e}")

    # Nếu hệ thống đang bật, kiểm tra cảm biến chuyển động
    if system_activated:
        display_temperature_humidity()
        check_motion_sensor()

    root.after(1000, update)

# Thêm nút kích hoạt/tắt hệ thống vào giao diện tkinter
activate_button = tk.Button(root, text="Bật/Tắt", command=toggle_system)
activate_button.pack()

# Bắt đầu vòng lặp kiểm tra API và hệ thống
root.after(1000, update)
root.mainloop()
