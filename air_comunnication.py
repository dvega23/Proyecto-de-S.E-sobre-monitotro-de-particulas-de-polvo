from ubidots import ApiClient
import serial
from time import sleep
import I2C_LCD_driver
mylcd = I2C_LCD_driver.lcd()
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

led1 = 12
led2 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

api = ApiClient(token="BBFF-AkByC8K47KRyrvbyJ6vzIUnFa66KmR")
CO2_ID = api.get_variable("62fa85fbcdbb010d86b27d0e")
VOC_ID = api.get_variable("62fa86094952de0c750ab96f")
PM1G_ID = api.get_variable("62fa860c4952de0c750ab970")
PM25G_ID = api.get_variable("62fa8623bd5be00987932717")
PM10G_ID = api.get_variable("62fa86289a8b17064f22eb77")
PM1T_ID = api.get_variable("62fa862ed931d10b14fe1f17")
PM25T_ID = api.get_variable("62fa88b7bd5be00986341482")
PM10T_ID = api.get_variable("62fa88b98a64dc1345a1a318")
humedad_ID = api.get_variable("6316431f2008aa0514fdaab5")
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

print(ser.isOpen())
string_value = b"\x11\x02\x01\x01\xEB"
# string_value=b"\x11\x03\x0C\x01\x1E\xC1"
# string_value = b"\x11\x03\x0D\xFF\xFF\xE1"
GPIO.output(led1,True)

GPIO.output(led2,False)

while True:
    GPIO.output(led1,True)
    GPIO.output(led2,False)
    try:
        ser.write(string_value)
        s = ser.read(25)
        C02 = int.from_bytes(s[3:5], 'big')

        VOC = int.from_bytes(s[5:7], 'big')

        humedad = int.from_bytes(s[7:9], 'big')
        temperatura = int.from_bytes(s[9:11], 'big')

        PM1G = int.from_bytes(s[11:13], 'big')

        PM25G = int.from_bytes(s[13:15], 'big')

        PM10G = int.from_bytes(s[15:17], 'big')

        PM1T = int.from_bytes(s[17:19], 'big')

        PM25T = int.from_bytes(s[19:21], 'big')

        PM10T = int.from_bytes(s[21:23], 'big')
        mylcd.lcd_clear()
        mylcd.lcd_display_string("CO2= " + str(C02), 1)
        mylcd.lcd_display_string("PM10=" + str(PM1G)+ " PM25="+str(PM25G), 2)
        while C02 >= 2500:
                ser.write(string_value)
                s = ser.read(25)
                C02 = int.from_bytes(s[3:5], 'big')
                GPIO.output(led1,False)
                GPIO.output(led2,True)
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Ambiente",1)
                mylcd.lcd_display_string("Toxico CO2="+str(C02),2)
                sleep(2)
                print(
                f"""CO2:{C02} ppm  VOC:{VOC} level  PM1.0={PM1G} GRIMM  PM2.5={PM25G} GRIMM  PM10={PM10G} GRIMM PM1.0={PM1T} TSI  PM2.5={PM25T} TSI  PM10={PM10T} TSI """)
                CO2_ID.save_value({"value": C02 if C02 <= 5000 else 5000})
                VOC_ID.save_value({"value": VOC if VOC <= 3 else 3})
                PM1G_ID.save_value({"value": PM1G if PM1G <= 1000 else 1000})
                PM25G_ID.save_value({"value": PM25G if PM25G <= 1000 else 1000})
                PM10G_ID.save_value({"value": PM10G if PM10G <= 1000 else 1000})
                PM1T_ID.save_value({"value": PM1T if PM1T <= 1000 else 1000})
                PM25T_ID.save_value({"value": PM25T if PM25T <= 1000 else 1000})
                PM10T_ID.save_value({"value": PM10T if PM10T <= 1000 else 1000})
        print(
            f"""CO2:{C02} ppm  VOC:{VOC} level  PM1.0={PM1G} GRIMM  PM2.5={PM25G} GRIMM  PM10={PM10G} GRIMM PM1.0={PM1T} TSI  PM2.5={PM25T} TSI  PM10={PM10T} TSI """)
        CO2_ID.save_value({"value": C02 if C02 <= 5000 else 5000})
        VOC_ID.save_value({"value": VOC if VOC <= 3 else 3})
        PM1G_ID.save_value({"value": PM1G if PM1G <= 1000 else 1000})
        PM25G_ID.save_value({"value": PM25G if PM25G <= 1000 else 1000})
        PM10G_ID.save_value({"value": PM10G if PM10G <= 1000 else 1000})
        PM1T_ID.save_value({"value": PM1T if PM1T <= 1000 else 1000})
        PM25T_ID.save_value({"value": PM25T if PM25T <= 1000 else 1000})
        PM10T_ID.save_value({"value": PM10T if PM10T <= 1000 else 1000})

    except KeyboardInterrupt:
        print("salir")
        
        print("datos no enviados correctamente")
        GPIO.cleanup()
        exit()
#    except :

ser.close()
