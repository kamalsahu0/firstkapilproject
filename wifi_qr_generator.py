import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import qrcode as qr


def on_submit():
    ssid = username_entry.get()
    password = password_entry.get()
    encryption = encryption_var.get()  # Get encryption from dropdown

    if not ssid or not password or encryption == "Select Encryption":
        print("Please enter all details and choose an encryption type.")
        return

    try:
        wifi_info = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        img = qr.make(wifi_info)
        img.save("Westack(wifi).png")

        img = Image.open("Westack(wifi).png")
        img = img.resize((150, 150))  # Resize image
        img_tk = ImageTk.PhotoImage(img)

        qr_label.config(image=img_tk)
        qr_label.image = img_tk  # Keep reference to avoid garbage collection

        print(f"QR Code generated and saved as 'Westack(wifi).png' for SSID: {ssid}, Password: {password}")
    except Exception as e:
        print(f"Error generating QR code: {e}")


def on_username_entry_focus_in(event):
    if username_entry.get() == 'Enter your username':
        username_entry.delete(0, tk.END)
        username_entry.config(foreground='black')


def on_username_entry_focus_out(event):
    if not username_entry.get():
        username_entry.insert(0, 'Enter your username')
        username_entry.config(foreground='gray')


root = tk.Tk()
root.title("WESTACK_WIFI")
root.geometry("400x400")

frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

username_label = ttk.Label(frame, text="SSID:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

username_entry = ttk.Entry(frame, width=30)
username_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry.insert(0, 'Enter your username')
username_entry.config(foreground='gray')
username_entry.bind("<FocusIn>", on_username_entry_focus_in)
username_entry.bind("<FocusOut>", on_username_entry_focus_out)

password_label = ttk.Label(frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

password_entry = ttk.Entry(frame, width=30, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Encryption dropdown
encryption_var = tk.StringVar(root)
encryption_var.set("Select Encryption")  # Default selection
encryption_options = ["WPA", "WPA2", "WEP"]  # Available options
encryption_dropdown = ttk.Combobox(frame, textvariable=encryption_var, values=encryption_options)
encryption_dropdown.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

submit_button = ttk.Button(frame)
