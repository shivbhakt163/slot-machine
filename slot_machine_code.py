'''
some of the additional symbols are also given in case you want to add extra symbols.
--> sym = ['🍒','🍌','🍇','🍉','🍏']
'''
import tkinter as tk
from tkinter import messagebox
import random as rd
import time as tm
import mysql.connector
from PIL import Image, ImageTk
import pygame

db = mysql.connector.connect(
    host="host",
    user="userid",
    password="password",
    database="slot_machine"
)
cursor = db.cursor()
#table which stores the records is named to be slot_machine_records
def register_player(name, age, phone_number, consent, bet_amount, agreed_rules):
    cursor.execute("INSERT INTO slot_machine_records (name, age, phone_number, consent, bet_amount, agreed_rules) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, age, phone_number, consent, bet_amount, agreed_rules))
    db.commit()
#you may add more sound effects as per your requirements but you can also use the sounds i gave you and use them
def play_sound2():
    sound_path = r"C:\add_your_path_to\mixkit-slot-machine-wheel-1932.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_sound1():
    sound_path = r"C:\add_your_path_to\mixkit-positive-interface-beep-221.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_soundwin():
    sound_path = r"C:\add_your_path_to\mixkit-slot-machine-win-siren-1929.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_soundlose():
    sound_path = r"C:\add_your_path_to\mixkit-retro-arcade-lose-2027.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_sounderror():
    sound_path = r"C:\add_your_path_to\mixkit-losing-marimba-2025.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()  
def spin():
    result_label.config(text="")
    for _ in range(10):
        tm.sleep(0.1+float((_)/10))
        x1 = rd.choice(sym)
        x2 = rd.choice(sym)
        x3 = rd.choice(sym)
        display_label.config(text=f"[ {x1} | {x2} | {x3} ]")
        root.update()
    return {x1, x2, x3}
def check_result():
    global name, phn_number
    phone_number = phn_number_entry.get()
    result_label.config(text="")
    play_sound2()
    result = spin()
    if len(set(result)) == 1:
        play_soundwin()
        messagebox.showinfo("Congratulations!", f"Yay, {name}! You have a matching case, and your bet is doubled: currency {(bet_amt)*2}") #make sure to change the currency as per your region and country
        result_label.config(text = "congratulations! , you have a matching case so you bet will increase and doubled", font=("Arial", 27))
        db = mysql.connector.connect(host = "host",
                                     user = "userid",
                                     password = "your_password",
                                     database = "slot_machine") #you change the database name as per your wish.
        cursor1 = db.cursor()
        update_query = f"UPDATE slot_machine_records SET rounds_won = rounds_won + 1 WHERE phone_number = '{phone_number}'"
        cursor1.execute(update_query)
        db.commit()
    else:
        result_label.config(text="Your bet remains the same. No amount increased. Would you like to give it another try?", font=("Arial", 27))
        play_soundlose()
    
def start_game():
    global name, bet_amt, phn_number, sym, display_label, result_label

    name = name_entry.get()
    bet_amt = int(bet_amt_entry.get())
    phn_no = phn_number_entry.get()
    play_sound1()
    if bet_amt <= 0:
        messagebox.showwarning("Invalid Bet", "Please enter a valid bet amount to play the game.")
        play_sounderror()
        return

    result_label.config(text="")
    check_result_button.config(state=tk.NORMAL)
    start_game_button.config(state=tk.DISABLED)

def register_user():
    register_window = tk.Toplevel(root)
    register_window.title("Registration")
    register_window.geometry("400x400")

    name_label = tk.Label(register_window, text="Name:")
    age_label = tk.Label(register_window, text="Age:")
    phone_label = tk.Label(register_window, text="Phone Number:")
    bet_amt_label = tk.Label(register_window, text="Bet Amount:")

    consent_var = tk.IntVar()
    rules_var = tk.IntVar()

    consent_checkbutton = tk.Checkbutton(register_window, text="I am playing with my will and any kind of loss is upto me", variable=consent_var)
    rules_checkbutton = tk.Checkbutton(register_window, text="I agree to follow all the rules of the game and will play fair and square without any kind of cheating.", variable=rules_var)

    name_entry = tk.Entry(register_window)
    age_entry = tk.Entry(register_window)
    phone_entry = tk.Entry(register_window)
    bet_amt_entry = tk.Entry(register_window)

    def submit_registration():
        name = name_entry.get()
        age = int(age_entry.get())
        phone_number = phone_entry.get()
        bet_amount = int(bet_amt_entry.get())
        consent = consent_var.get()
        agreed_rules = rules_var.get()

        if not name or not age or not phone_number or not bet_amount or not consent or not agreed_rules:
            messagebox.showwarning("Incomplete Registration", "Please fill in all the details.")
            return

        register_player(name, age, phone_number, consent, bet_amount, agreed_rules)
        messagebox.showinfo("Registration Successful", "You have successfully registered!")
        register_window.destroy()

    submit_button = tk.Button(register_window, text="Submit", foreground="blue", command=submit_registration) 

    name_label.pack(pady=5)
    name_entry.pack(pady=5)
    age_label.pack(pady=5)
    age_entry.pack(pady=5)
    phone_label.pack(pady=5)
    phone_entry.pack(pady=5)
    bet_amt_label.pack(pady=5)
    bet_amt_entry.pack(pady=5)
    consent_checkbutton.pack(pady=5)
    rules_checkbutton.pack(pady=5)
    submit_button.pack(pady=10)

if __name__ == '__main__':
    sym = ['🍒','🍌','🍇']
    
    root = tk.Tk()
    root.title("SLOT_MACHINE") #change the name to your desired name of your file
    root.geometry("1920x1080") #adjust as per your screen size

    icon_image = ImageTk.PhotoImage(file=r"path_to_your_icon_image") #make sure your image is in png format
    root.iconphoto(True, icon_image)
    
    bg = ImageTk.PhotoImage(file = "path_to_your_background_image" ) #make sure to provide the path to png or other supported files
    label1 = tk.Label(root, image=bg)
    label1.place(x=0, y=0, relwidth=1, relheight=1)

    name_label = tk.Label(root, text="       Enter your name ↓       ", font=("Arial", 26))
    name_entry = tk.Entry(root, font=("Arial", 26), width=25)
    #make sure to put in the correct phone number cause if there will be a difference in the phone number so your check_result will fail and this code will get screwed up
    phn_number_label = tk.Label(root, text=" Enter the phone number ↓ ", font=("Arial", 26))
    phn_number_entry = tk.Entry(root, font=("Arial",26), width=25)

    bet_amt_label = tk.Label(root, text="    Enter the bet amount ↓    ", font=("Arial", 26))
    bet_amt_entry = tk.Entry(root, font=("Arial", 26), width=25)

    start_game_button = tk.Button(root, text="Start Game", foreground="blue", command=start_game, font=("Arial", 24), width=25, height=1)
    check_result_button = tk.Button(root, text="Check Result", foreground="red", command=check_result, state=tk.DISABLED, font=("Arial", 24), width=25, height=1)

    display_label = tk.Label(root, text="", font=("Arial", 80), fg="blue")
    result_label = tk.Label(root, text="", fg="red", font=("Arial", 35))

    register_button = tk.Button(root, text="Register", foreground="red", command=register_user, font=("Arial", 24), width=25, height=1)
    register_button.pack(pady=10)

    name_label.pack(pady=5)
    name_entry.pack(pady=5)
    phn_number_label.pack(pady=5)
    phn_number_entry.pack(pady=5)
    bet_amt_label.pack(pady=5)
    bet_amt_entry.pack(pady=5)
    start_game_button.pack(pady=10)
    check_result_button.pack(pady=10)
    display_label.pack(pady=10)
    result_label.pack(pady=10)

    root.mainloop()
