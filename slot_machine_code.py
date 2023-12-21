#sym = ['🍒','🍌','🍇','🍉','🍏']
#just a dummy record :

#table_structure is as follows :

#+----------------+-----+-----------------+---------+------------+--------------+------------+---------------+-------+
#| name           | age | phone_number    | consent | bet_amount | agreed_rules | rounds_won | rounds_played | cstid |
#+----------------+-----+-----------------+---------+------------+--------------+------------+---------------+-------+
#| aryan saraswat |  17 | +91 9XXXX XXXXX |       1 |        100 |            1 |          2 |             4 |   c-1 |
#+----------------+-----+-----------------+---------+------------+--------------+------------+---------------+-------+

import tkinter as tk
from tkinter import messagebox
import random as rd
import time as tm
import mysql.connector
from PIL import Image, ImageTk
import pygame

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="3141592653589793",
    database="slot_machine"
)
cursor = db.cursor()

def register_player(name, age, phone_number, consent, bet_amount, agreed_rules, customer_id):
    cursor.execute("INSERT INTO slot_machine_records (name, age, phone_number, consent, bet_amount, agreed_rules, customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (name, age, phone_number, consent, bet_amount, agreed_rules, customer_id))
    db.commit()
def play_sound2():
    sound_path = r"C:\Users\Aashi\Desktop\slot machine\sound_files\mixkit-slot-machine-wheel-1932.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_sound1():
    sound_path = r"C:\Users\Aashi\Desktop\slot machine\sound_files\mixkit-positive-interface-beep-221.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_soundwin():
    sound_path = r"C:\Users\Aashi\Desktop\slot machine\sound_files\mixkit-slot-machine-win-siren-1929.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_soundlose():
    sound_path = r"C:\Users\Aashi\Desktop\slot machine\sound_files\mixkit-retro-arcade-lose-2027.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
def play_sounderror():
    sound_path = r"C:\Users\Aashi\Desktop\slot machine\sound_files\mixkit-losing-marimba-2025.wav"
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
    global name, customer_id
    customer_id = customer_id_entry.get()
    result_label.config(text="")
    db1 = mysql.connector.connect(host = "localhost",
                                  user = "root",
                                  password = "3141592653589793",
                                  database = "slot_machine")
    cursor2 = db1.cursor()
    add_query = f"update slot_machine_records set rounds_played = rounds_played+1 where customer_id = '{customer_id}';"
    cursor2.execute(add_query)
    db1.commit()
    play_sound2()
    result = spin()
    if len(set(result)) == 1:
        play_soundwin()
        messagebox.showinfo("Congratulations!", f"Yay, {name}! You have a matching case, and your bet is doubled: rupees {(bet_amt)*2}")
        result_label.config(text = "congratulations! , you have a matching case so you bet will increase and doubled", font=("Arial", 27))
        db = mysql.connector.connect(host = "localhost",
                                     user = "root",
                                     password = "3141592653589793",
                                     database = "slot_machine")
        cursor1 = db.cursor()
        update_query = f"UPDATE slot_machine_records SET rounds_won = rounds_won + 1 WHERE customer_id = '{customer_id}'"
        cursor1.execute(update_query)
        db.commit()
    else:
        result_label.config(text="Your bet remains the same. No amount increased. Would you like to give it another try?", font=("Arial", 27))
        play_soundlose()
    
def start_game():
    global name, bet_amt, customer_id, sym, display_label, result_label

    name = name_entry.get()
    bet_amt = int(bet_amt_entry.get())
    cust_id = customer_id_entry.get()
    play_sound1()
    if bet_amt <= 0:
        messagebox.showwarning("Invalid Bet", "Please enter a valid bet amount.")
        play_sounderror()
        return

    result_label.config(text="RESULT WILL BE DISPLAYED HERE !")
    check_result_button.config(state=tk.NORMAL)
    start_game_button.config(state=tk.DISABLED)

def register_user():
    register_window = tk.Toplevel(root)
    register_window.title("Registration")
    register_window.geometry("450x550")

    name_label = tk.Label(register_window, text="Name:")
    age_label = tk.Label(register_window, text="Age:")
    phone_label = tk.Label(register_window, text="Phone Number:")
    customer_id_label = tk.Label(register_window, text = "Customer-ID:")
    bet_amt_label = tk.Label(register_window, text="Bet Amount:")

    consent_var = tk.IntVar()
    rules_var = tk.IntVar()

    consent_checkbutton = tk.Checkbutton(register_window, text="_____________________________________________________\nI am playing with my will and i will be held\nresponsible for any kind of loss, financial especially\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾", variable=consent_var)
    rules_checkbutton = tk.Checkbutton(register_window, text="______________________________________________________________________\nI agree to follow all the rules of the game as told by the instructor\nAnd will play fair and square, without any kind of cheating or fraud\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾", variable=rules_var)

    name_entry = tk.Entry(register_window)
    age_entry = tk.Entry(register_window)
    phone_entry = tk.Entry(register_window)
    customer_id_entry = tk.Entry(register_window)
    bet_amt_entry = tk.Entry(register_window)

    def submit_registration():
        name = name_entry.get()
        age = int(age_entry.get())
        phone_number = phone_entry.get()
        customer_id = customer_id_entry.get()
        bet_amount = int(bet_amt_entry.get())
        consent = consent_var.get()
        agreed_rules = rules_var.get()

        if not name or not age or not phone_number or not bet_amount or not consent or not agreed_rules:
            messagebox.showwarning("Incomplete Registration", "Please fill in all the details.")
            return

        register_player(name, age, phone_number, consent, bet_amount, agreed_rules, customer_id)
        messagebox.showinfo("Registration Successful", "You have successfully registered!")
        register_window.destroy()

    submit_button = tk.Button(register_window, text="Submit", foreground="blue", command=submit_registration)

    name_label.pack(pady=5)
    name_entry.pack(pady=5)
    age_label.pack(pady=5)
    age_entry.pack(pady=5)
    phone_label.pack(pady=5)
    phone_entry.pack(pady=5)
    customer_id_label.pack(pady=5)
    customer_id_entry.pack(pady=5)
    bet_amt_label.pack(pady=5)
    bet_amt_entry.pack(pady=5)
    consent_checkbutton.pack(pady=5)
    rules_checkbutton.pack(pady=5)
    submit_button.pack(pady=10)

if __name__ == '__main__':
    sym = ['⑦']
    
    root = tk.Tk()
    root.title("SlotSaFari")
    root.geometry("1920x1080")

    icon_image = ImageTk.PhotoImage(file=r"C:\Users\Aashi\Desktop\slot machine\icons\—Pngtree—triple number seven diamond for_6635671.png")
    root.iconphoto(True, icon_image)

    bg = ImageTk.PhotoImage(file = "C:\\Users\\Aashi\\Desktop\\slot machine\\slot_machine_bgimgs\\desktop-wallpaper-pin-on-casino-slot-games-slot-game.jpg" )
    label1 = tk.Label(root, image=bg)
    label1.place(x=0, y=0, relwidth=1, relheight=1)

    name_label = tk.Label(root, text="       Enter your name ↓       ", background = '#FFD700',font=("Arial", 26))
    name_entry = tk.Entry(root, font=("Arial", 26), background = '#fdfd96', width=25)

    customer_id_label = tk.Label(root, text=" Enter the Customer-ID ↓ ", background = '#FFD700',font=("Arial", 26))
    customer_id_entry = tk.Entry(root, font=("Arial",26), background = '#fdfd96', width=25)

    bet_amt_label = tk.Label(root, text="    Enter the bet amount ↓    ", background = '#FFD700',font=("Arial", 26))
    bet_amt_entry = tk.Entry(root, font=("Arial", 26), background = '#fdfd96', width=25)

    start_game_button = tk.Button(root, text="Start Game", background = '#880808',foreground="#FFD700", command=start_game, font=("Arial", 24), width=25, height=1)
    check_result_button = tk.Button(root, text="Check Result", background = '#880808',foreground="#FFD700", command=check_result, state=tk.DISABLED, font=("Arial", 24), width=25, height=1)

    display_label = tk.Label(root, text="", font=("Arial", 80), background = '#fdfd96', fg="#880808")
    result_label = tk.Label(root, text="", bg = '#FFD700',fg="red", font=("Arial", 35))

    register_button = tk.Button(root, text="Register", background = '#880808',foreground="#FFD700", command=register_user, font=("Arial", 24), width=25, height=1)
    register_button.pack(pady=10)

    name_label.pack(pady=5)
    name_entry.pack(pady=5)
    customer_id_label.pack(pady=5)
    customer_id_entry.pack(pady=5)
    bet_amt_label.pack(pady=5)
    bet_amt_entry.pack(pady=5)
    start_game_button.pack(pady=10)
    check_result_button.pack(pady=10)
    display_label.pack(pady=10)
    result_label.pack(pady=10)

    root.mainloop()
