from tkinter import *
import tkinter as tk
import tkinter.font as TkFont
from datetime import datetime
import requests

AIRTABLE_BASE_ID='xxxxxx'
AIRTABLE_API_KEY='xxxxx'
AIRTABLE_NAME='projects'


running = False

seconds, milliseconds = 1, 0


# start function
def start():
    global running
    if not running:
        update()
        running = True


# pause function
def stop():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False



# reset function
def reset():
    global running
    if running:
        # cancel updating of time using after_cancel()
        stopwatch_label.after_cancel(update_time)
        running = False
    # set variables back to zero
    global seconds, milliseconds
    seconds, milliseconds = 1, 0
    # set label back to zero
    stopwatch_label.config(text='0.00')

# update stopwatch function
def update():
    # update seconds with (addition) compound assignment operator
    global seconds, milliseconds
    milliseconds += 1
    #if seconds == 60:
    #    minutes += 1
    #    seconds = 0
    if milliseconds == 99:
        seconds += 1
        milliseconds = 0
    # format time to include leading zeros
    #hours_string = f'{hours}' if hours > 9 else f'0{hours}'
    #minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}'
    milliseconds_string = f'{milliseconds}' if milliseconds > 99 else f'{milliseconds}'
    # update timer label after 1000 ms (1 second)
    stopwatch_label.config(text=seconds_string + '.' + milliseconds_string)
    # after each second (1000 milliseconds), call update function
    # use update_time variable to cancel or pause the time using after_cancel
    global update_time
    global last_update
    update_time = stopwatch_label.after(10, update)

    last_update = seconds_string + '.' + milliseconds_string

def update_arch():

    recId = str.get()
    print(recId)

    print(last_update)


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
            "Archiving Time": float(last_update)
          }
        },
      ]
    }

    r = requests.patch(endpoint, json=data, headers=headers)
    print(r.json())

    root.destroy()

def update_send():

    recId = str.get()
    print(recId)

    print(last_update)


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
            "Sending Time": float(last_update)
          }
        },
      ]
    }

    r = requests.patch(endpoint, json=data, headers=headers)
    print(r.json())

    root.destroy()

# create main window
root = tk.Tk()
root.geometry('350x420')
root.title('Project Tracker')

str = tk.StringVar()

# label to display time
stopwatch_label = tk.Label(text='0.00', font=('System', 80))
stopwatch_label.pack()

# start, pause, reset, quit buttons
start_button = tk.Button(text='start', width=30, font=('Arial', 10), command=start)
start_button.pack(pady = 1)
stop_button = tk.Button(text='stop', width=30, font=('Arial', 10), command=stop)
stop_button.pack(pady = 1)
reset_button = tk.Button(text='reset', width=30, font=('Arial', 10), command=reset)
reset_button.pack(pady = 1)

# Id Record Entry box
tk.Label(root, text="Enter Record ID : ", font='Helvetica 10 bold').pack(pady = 5)

recid_entry = tk.Entry(textvariable = str, width=30)
recid_entry.pack(pady = 10)

archived_button = tk.Button(text='Archived', width=30, font=('Arial', 10), command=update_arch, bg="#6eb9f3")
archived_button.pack(pady = 10)
sent_button = tk.Button(text='Sent', width=30, font=('Arial', 10), command=update_send, bg="#ffa981")
sent_button.pack()

# run app
root.mainloop()


