import os
from time import sleep
import Adafruit_CharLCD as LCD
import w1thermsensor
from picamera import PiCamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = LCD.Adafruit_CharLCD(9, 11, 8, 7, 5, 6, 16, 2)
lcd.create_char(1,[7, 5, 7, 32, 32, 32, 32, 32])
lcd.clear()

def Komunikat_głosowy(tekst):
    os.system( 'espeak "'+tekst+'" --stdout -a 200 -s 180 -p 40 | aplay 2>/dev/null' )

Zmienna_pomocnicza1 = True
Zmienna_pomocnicza2 = True

Komunikat_głosowy("Witaj! Nazywam się ZW-1, jestem asystentem cyfrowym, stworzył mnie Zygmunt Wypich. Posiadam wiele umiejętności. ")

sleep(2)
Komunikat_głosowy("Informuję o zdarzeniach za pomocą buzzera.")
sleep(2)
GPIO.output(21, GPIO.HIGH)
sleep(2)
GPIO.output(21, GPIO.LOW)

sleep(2)
Komunikat_głosowy("Wyświetlam dane na wyświetlaczu LCD.")
sleep(2)
GPIO.output(13, GPIO.HIGH)
lcd.message('Witaj!')
sleep(7)
lcd.clear()
GPIO.output(13, GPIO.LOW)

sleep(2)
Komunikat_głosowy("Oświetlam otoczenie za pomocą diod LED.")
sleep(2)
GPIO.output(3, GPIO.HIGH)
sleep(7)
GPIO.output(3, GPIO.LOW)

sleep(2)
Komunikat_głosowy("Mierzę aktualną temperaturę otoczenia.")
sleep(2)
GPIO.output(13, GPIO.HIGH)
lcd.clear()
sensor = w1thermsensor.W1ThermSensor()
temp = sensor.get_temperature()
temp = round(temp, 1)
temperatura = str(temp)
lcd.message('Temperatura:')
lcd.set_cursor(0,1)
lcd.message(temperatura + '\x01' + 'C')
sleep(7)
lcd.clear()
GPIO.output(13, GPIO.LOW)

sleep(2)
Komunikat_głosowy("Odczytuję stan trzech przycisków ogólnego przeznaczenia.")
sleep(1)
while (Zmienna_pomocnicza1 == True):
    if GPIO.input(19) == False and Zmienna_pomocnicza2 == True:
        sleep(0.2)
        Komunikat_głosowy("Został naciśnięty górny przycisk.")
        Zmienna_pomocnicza1 = False
        Zmienna_pomocnicza2 = GPIO.input(19)
sleep(1)
Zmienna_pomocnicza1 = True
Zmienna_pomocnicza2 = True
while (Zmienna_pomocnicza1 == True):
    if GPIO.input(16) == False and Zmienna_pomocnicza2 == True:
        sleep(0.2)
        Komunikat_głosowy("Został naciśnięty środkowy przycisk.")
        Zmienna_pomocnicza1 = False
        Zmienna_pomocnicza2 = GPIO.input(16)
sleep(1)
Zmienna_pomocnicza1 = True
Zmienna_pomocnicza2 = True
while (Zmienna_pomocnicza1 == True):
    if GPIO.input(26) == False and Zmienna_pomocnicza2 == True:
        sleep(0.2)
        Komunikat_głosowy("Został naciśnięty dolny przycisk.")
        Zmienna_pomocnicza1 = False
        Zmienna_pomocnicza2 = GPIO.input(26)

sleep(2)        
Zmienna_pomocnicza1 = True
Komunikat_głosowy("Wykrywam ruch w swoim otoczeniu.")
sleep(2)
Komunikat_głosowy("Proszę opuść pomieszczenie na dziesięć sekund, a następnie ponownie się w nim pojaw. Kiedy wykryję twój ruch, poinformuję cię o tym. ")
sleep(10)
while (Zmienna_pomocnicza1 == True):
    if GPIO.input(12) == True:
        Komunikat_głosowy("Twój ruch został wykryty.")
        Zmienna_pomocnicza1 = False
        
sleep(2)
Komunikat_głosowy("Obserwuję otoczenie za pomocą kamery.")
sleep(2)
Komunikat_głosowy("Za pięć sekund zaświecę diody LED, a następnie zrobię zdjęcie, które zapiszę na pulpicie")
sleep(5)
GPIO.output(3, GPIO.HIGH)
Kamera = PiCamera()
Kamera.start_preview()
Kamera.capture('/home/pi/Desktop/Zdjecie.jpg')
Kamera.stop_preview()
sleep(5)
GPIO.output(3, GPIO.LOW)

sleep(2)        
Komunikat_głosowy("Dziękuję za uwagę.")


