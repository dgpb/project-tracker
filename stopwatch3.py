from tkinter import *
import tkinter as tk
import tkinter.font as TkFont
from datetime import datetime
import requests

AIRTABLE_BASE_ID='xxxxxxxx'
AIRTABLE_API_KEY='xxxxxxxx'
AIRTABLE_NAME='projects'


def run():
    current_time = datetime.now()
    diff = current_time - start_time
    txt_var.set('%d.%02d' % (diff.seconds,diff.microseconds//10000))

    if running:
        root.after(20,run)

def start():
    global running
    global start_time

    if not running:
        running = True
        start_time = datetime.now()
        root.after(10,run)

def stop():
    global running
    running = False

def reset():
    global start_time
    start_time = datetime.now()

    if not running:
        txt_var.set('0.00')


running = False
start_time = None

root = tk.Tk()
root.geometry("390x500")
root.title("Airtable Project Tracker")

str = tk.StringVar()

def update_arch():

    recId = str.get()
    print(recId)

    current_time = datetime.now()
    final = current_time - start_time
    tm = txt_var.get()
    print(tm)

    endpoint=f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_NAME}'


    headers = {
        "Authorization" : f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type" : "application/json"
    }

    data = {
      "records": [
        {
          "id": recId,
          "fields": {
            "Archiving Time": float(tm)
          }
        },
      ]
    }

    r = requests.patch(endpoint, json=data, headers=headers)
    print(r.json())

    root.destroy()


# Id Record Entry box
tk.Label(root, text="Enter Record ID : ", font='Helvetica 10 bold').pack(pady = 5)

# Get Id project form Record in Airtable
recid_entry = tk.Entry(root, textvariable = str, width=50)
recid_entry.pack(pady = 10)


txt_var = tk.StringVar()
txt_var.set('0.00')


fontStyle = TkFont.Font(family="Terminal", size = 50)
tk.Label(root, textvariable=id,font = fontStyle)
tk.Label(root, textvariable=txt_var,font = fontStyle).pack(pady = 50)




# Track time buttons
tk.Button(root, text="Start",command = start, width=50, bg="#b1b1b1").pack(pady = 5)
tk.Button(root, text="Stop",command = stop, width=50, bg="#b1b1b1").pack(pady = 5)
tk.Button(root, text="Reset",command = reset, width=50, bg="#b1b1b1").pack(pady = 5)

# Pull record data Button
id_button = tk.Button(root, text="Archived", width=50, bg="#6eb9f3", command = update_arch)
id_button.pack(pady = 5)

id_button = tk.Button(root, text="Sent", width=50, bg="#ffa981")
id_button.pack(pady = 5)

root.mainloop()
