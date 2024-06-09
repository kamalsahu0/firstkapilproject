import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import qrcode as qr

def on_submit():
    ssid = username_entry.get()
    password = password_entry.get()
    encryption = "WPA"
    wifi_info = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    img = qr.make(wifi_info)
    img.save("Westack(wifi).png")
    
    img = Image.open("Westack(wifi).png")
    img = img.resize((150, 150))  
    img_tk = ImageTk.PhotoImage(img)
    
    qr_label.config(image=img_tk)
    qr_label.image = img_tk
    
    print(f"QR as 'Westack(wifi).png' for SSID: {ssid}, Password: {password}")

def on_username_entry_focus_in(event):
    if username_entry.get() == 'Enter your username':
        username_entry.delete(0, tk.END)
        username_entry.config(foreground='white')

def on_username_entry_focus_out(event):
    if not username_entry.get():
        username_entry.insert(0, 'Enter your username')
        username_entry.config(foreground='white')

root = tk.Tk()
root.title("WESTACK_WIFI")
root.geometry("400x400")  

frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

username_label = ttk.Label(frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

username_entry = ttk.Entry(frame, width=30)
username_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry.insert(0, 'Enter your username')
username_entry.config(foreground='white')
username_entry.bind("<FocusIn>", on_username_entry_focus_in)
    
username_entry.bind("<FocusOut>", on_username_entry_focus_out)

password_label = ttk.Label(frame, text="WIFI-Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

password_entry = ttk.Entry(frame, width=30, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

qr_label = ttk.Label(frame)
qr_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()