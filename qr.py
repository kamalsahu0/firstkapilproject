#westackwifi....
import kapil as qr

ssid = "Airtel_WS_AI"  
password = "Empire#$2024" 
encryption = "WPA"  
wifi_info = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
img = qr.make(wifi_info)

img.save("Westack(wifi).png")

