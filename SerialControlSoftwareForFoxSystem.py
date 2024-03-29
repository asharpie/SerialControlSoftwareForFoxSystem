import tkinter as tk
from tkinter import messagebox
import serial
import time
stop = 0
fully_fun = False
syringe_diameter = ""
withdraw_rate = ""
withdraw_volume = ""
withdraw_force = ""
valve_position = ""
delay_withdraw_switch = ""
delay_infuse_switch = ""
infuse_rate = ""
infuse_volume = ""
infuse_force = ""
#reset = 0
#serial_text = "Received Serial Messages:\n"
# Configure serial connection
ser2 = serial.Serial(
    port='COM6',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS)

# function to send commands to first serial device and receive response
def send_and_receive(command):
    #global serial_text
    window.update()
    input=command
    out=''
    #send the input to device
    ser.write(str(input + '\r\n').encode('utf-8'))
    time.sleep(1)
    while ser.inWaiting()>0:
        out += ser.read(1).decode('utf-8')
    #Print response
##          if out != '':
##              serial_text += out
    return(out)
    window.update()

# function to send commands to second serial device and receive response
def send_and_receive_ser2(command):
    #global serial_text
    window.update()
    input=command
    out=''
    ser2.write(str(input + '\r').encode('utf-8'))
    ser2.flush()
    ser2.timeout = .1
    out = ser2.readline().decode('utf-8')
    #serial_text += out
    window.update()

#function used to clear GUI when transitioning from setup GUI to Stop/Reset functions
def hide_components():
    for widget in window.winfo_children():
        widget.destroy()

#function used to determine when serial device one is finished with the withdraw process
def withdraw_process():
    #global serial_text
    response=''
    break_var = False
    send_and_receive("wrun")
    while True:
        window.update()
        while ser.inWaiting()>0:
            response += ser.read(1).decode('utf-8').strip()
##            if response != '':
##                serial_text+=response
            if response == 'T*':
                break_var = True
                break
        if break_var == True:
            break


#function used to determine when serial device one is finished with the infuse process
def infuse_process():
    #global serial_text
    response=''
    break_var = False
    send_and_receive("irun")
    while True:
        window.update()
        while ser.inWaiting()>0:
            response += ser.read(1).decode('utf-8').strip()
##            if response != '':
##                serial_text+=response
            if response == 'T*':
                break_var = True
                break
        if break_var == True:
            break

def reset_infuse_process():
    #global serial_text
    global fully_run
    response=''
    break_var = False
    if not fully_run:
        send_and_receive("irun")
        while True:
            if "S" in send_and_receive("status"):
                break
            window.update()
            while ser.inWaiting()>0:
                response += ser.read(1).decode('utf-8').strip()
    ##            if response != '':
    ##                serial_text+=response
                print(response)
                if response == 'T*' or '*':
                    break_var = True
                    break
            if break_var == True:
                break

#main function declares variables, and completes serial process using send_and_receive function    
def start_button_clicked():
    global fully_run
    global syringe_diameter
    global withdraw_rate
    global withdraw_volume
    global withdraw_force
    global valve_position
    global delay_withdraw_switch
    global delay_infuse_switch
    global infuse_rate
    global infuse_volume
    global infuse_force
    syringe_diameter = ""
    withdraw_rate = ""
    withdraw_volume = ""
    withdraw_force = ""
    valve_position = ""
    delay_withdraw_switch = ""
    delay_infuse_switch = ""
    infuse_rate = ""
    infuse_volume = ""
    infuse_force = ""

    if not all(entry.get() for entry in entry_widgets):
        messagebox.showerror("Error","Please fill out all parameters.")
    else:
        syringe_diameter = str(entry_widgets[0].get())
        withdraw_rate = str(entry_widgets[1].get())
        withdraw_volume = str(entry_widgets[2].get())
        withdraw_force = str(entry_widgets[3].get())
        valve_position = str(entry_widgets[4].get())
        delay_withdraw_switch = str(entry_widgets[5].get())
        delay_infuse_switch = str(entry_widgets[6].get())
        infuse_rate = str(entry_widgets[7].get())
        infuse_volume = str(entry_widgets[8].get())
        infuse_force = str(entry_widgets[9].get())
        if valve_position == "a":
            valve_position = "A"
        hide_components()
##        received_label = tk.Label(window, text = "Received Serial Messages:\n", bg = "white", fg="black", font=("Helvetica",12))
##        received_label.place(relx=.85, rely=0.1, anchor=tk.CENTER)
        label = tk.Label(window, text="No Current Process",bg="white",fg="black",font=("Helvetica, 20"))
        label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        stop_button = tk.Button(window, text="Stop", command = stop_button_clicked, bg="#FF0000", fg="white",font=("Arial", 12),padx=10,pady=5)
        stop_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        window.update()
        if stop==0:
            send_and_receive_ser2('NP2')
        if stop==0:
            send_and_receive_ser2('CP')
        if stop==0:
            if valve_position =='A':
                send_and_receive_ser2('GO1')
            else:
                send_and_receive_ser2('GO2')
        if stop==0:
            send_and_receive("diameter "+syringe_diameter)
            label.config(text="Changing diameter to "+syringe_diameter+"mm")
            time.sleep(.5)
        if stop==0:
            label.config(text="Setting withdraw rate to "+withdraw_rate+"ul/min")
            send_and_receive("wrate "+withdraw_rate+" ul/min")
            time.sleep(.05)
        if stop==0:
            label.config(text="Setting withdraw volume to "+withdraw_volume+"ul")
            send_and_receive("tvolume "+withdraw_volume+" ul")
            time.sleep(.05)
        if stop==0:
            label.config(text="Setting withdraw force to "+withdraw_force+"%")
            send_and_receive("force "+withdraw_force)
            time.sleep(.05)
        if stop==0:
            label.config(text="Withdrawing...")
            withdraw_process()
            time.sleep(int(delay_withdraw_switch))
        if stop==0:
            if valve_position =='A':
                label.config(text="Switching valve position to valve B")
                send_and_receive_ser2('GO2')
                send_and_receive_ser2('CP')
            else:
                label.config(text="Switching valve position to valve A")
                send_and_receive_ser2('GO1')
                send_and_receive_ser2('CP')
            time.sleep(.05)
        if stop==0:
            label.config(text="Setting infuse rate to "+infuse_rate+"ul/min")
            send_and_receive("irate "+infuse_rate+" ul/min")
            time.sleep(.05)
        if stop==0:
            label.config(text="Setting infuse volume to "+infuse_volume+"ul")
            send_and_receive("tvolume "+infuse_volume+" ul")
            time.sleep(.05)
        if stop==0:
            label.config(text="Setting infuse force to "+infuse_force+"%")
            send_and_receive("force "+infuse_force)
            time.sleep(.05)
        if stop==0:
            label.config(text="Infusing...")
            infuse_process()
            time.sleep(int(delay_infuse_switch))
        if stop==0:
            if valve_position =='A':
                label.config(text="Switching valve position to valve A")
                send_and_receive_ser2('GO1')
                send_and_receive_ser2('CP')
            else:
                label.config(text="Switching valve position to valve B")
                send_and_receive_ser2('GO2')
                send_and_receive_ser2('CP')
        if stop==0:
            label.config(text="Process completed, "+withdraw_volume+"ul withdrawn, and "+infuse_volume+"ul infused")
        else:
            label.config(text="No Current Proccess")
        fully_run = True
        stop_button_clicked()

#function changes stop variable to 1 (or false), and tells serial device one to stop, and makes the reset button appear
def stop_button_clicked():
    global stop
    send_and_receive("stop")
    stop = 1
    hide_components()
    reset_button = tk.Button(window,text="Reset",command=reset_button_clicked, bg="#FF0000",fg="white",font=("Arial",12),padx=10, pady=5)
    reset_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    window.update()

#dictates what happens with reset button is clicked, currently it does nothing
def reset_button_clicked():
    global stop
    #global reset
    #reset = 1
    hide_components()
    close_button = tk.Button(window,text="Close(terminate)",command=window.destroy, bg="#FF0000",fg="white",font=("Arial",12),padx=10, pady=5)
    close_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    ##reset code here
    label2 = tk.Label(window, text="No Current Process",bg="white",fg="black",font=("Helvetica, 20"))
    label2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    label2.config(text="Switching valve position to valve A")
    send_and_receive_ser2('GO1')
    send_and_receive_ser2('CP')
    label2.config(text="Setting infuse rate to "+withdraw_rate+"ul/min")
    print("1"+send_and_receive("irate "+withdraw_rate+" ul/min"))
    time.sleep(.05)
    label2.config(text="Setting infuse force to "+withdraw_force+"%")
    print("2"+send_and_receive("force "+withdraw_force))
    time.sleep(.05)
    label2.config(text="Setting infuse volume to "+withdraw_volume+"ul")
    print("3"+send_and_receive("tvolume "+withdraw_volume+" ul"))
    time.sleep(.05)
    label2.config(text="Infusing...")
    reset_infuse_process()
    label2.config(text="Reset")
    window.update()
    time.sleep(3)
    hide_components()
    stop=0
    startup()

def startup():
    global fully_run
    fully_run = False
    global entry_widgets
    entry_widgets = []

    # Syringe diameter label and entry
    syringe_diameter_label = tk.Label(window, text="Syringe Diameter(mm)", bg="white", fg="black")
    syringe_diameter_label.place(relx=0.32, rely=0.1, anchor=tk.CENTER)
    syringe_diameter_entry = tk.Entry(window, width=15, font=("Arial", 10), bd=3, relief=tk.SOLID)
    syringe_diameter_entry.place(relx=0.42, rely=0.1, anchor=tk.CENTER)
    entry_widgets.append(syringe_diameter_entry)

    # Define labels for inputs
    withdraw_labels = [
        "Withdraw Rate(uL/min)", "Withdraw Volume(uL)", "Withdraw Force(%)",
    ]
    infuse_labels = [
        "Infuse Rate(uL/min)", "Infuse Volume(uL)", "Infuse Force(%)",
    ]
    other_labels = [
        "Valve Starting Position(A or B)", "Delay Withdraw Switch(s)", "Delay Infuse Switch(s)",
    ]


    # Withdraw inputs on the left
    for i, label_text in enumerate(withdraw_labels):
        label = tk.Label(window, text=label_text, bg="white", fg="black")
        label.place(relx=0.07, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry = tk.Entry(window, width=15, font=("Arial", 10), bd=3, relief=tk.SOLID)
        entry.place(relx=0.17, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry_widgets.append(entry)

    # Other inputs in the middle
    for i, label_text in enumerate(other_labels):
        label = tk.Label(window, text=label_text, bg="white", fg="black")
        label.place(relx=0.32, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry = tk.Entry(window, width=15, font=("Arial", 10), bd=3, relief=tk.SOLID)
        entry.place(relx=0.42, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry_widgets.append(entry)

    # Infuse inputs on the right
    for i, label_text in enumerate(infuse_labels):
        label = tk.Label(window, text=label_text, bg="white", fg="black")
        label.place(relx=0.57, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry = tk.Entry(window, width=15, font=("Arial", 10), bd=3, relief=tk.SOLID)
        entry.place(relx=0.67, rely=0.2 + i * 0.1, anchor=tk.CENTER)
        entry_widgets.append(entry)

    # Create the start button
    start_button = tk.Button(window, text="Start", command=start_button_clicked, bg="#4CAF50", fg="white",font=("Arial", 12), padx=10, pady=5)
    start_button.place(relx=0.37, rely=0.6, anchor=tk.CENTER)

    # Create the stop button
    stop_button = tk.Button(window, text="Stop", command=stop_button_clicked, bg="#FF0000", fg="white",font=("Arial", 12), padx=10, pady=5)
    stop_button.place(relx=0.47, rely=0.6, anchor=tk.CENTER)

##    received_label = tk.Label(window, text = serial_text, bg = "white", fg="black", font=("Helvetica",12))
##    received_label.place(relx=.85, rely=0.1, anchor=tk.CENTER)
def on_key_press(event):
    if event.keysym == "Escape":
        if messagebox.askokcancel("Quit", "Are you sure you want to quit? Make sure all processes are complete!"):
            window.destroy()
# Start the GUI event loop
# Create the tkinter window
window = tk.Tk()
window.title("Syringe Control GUI")
window.configure(bg="white")
window.attributes("-fullscreen", True)
window.bind("<KeyPress>", on_key_press)

startup()
window.mainloop()


