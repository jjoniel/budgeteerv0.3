"""
Personal Financier

Created by Joniel Augustine Jerome
06/20/2024

This module defines the Budgeteer program that allows users to track
their income and expenses.


"""

# standard imports
import os
import time
import locale
from datetime import date, datetime

# external imports
from flask import Flask, request, render_template, g
from cryptography.fernet import Fernet
from maskpass import askpass

# local imports
from transaction import Transaction

KEY = b'ZfTpJ-ExWHiDFA_BNxi1kLKv97u_DLlE6fGLwqD1OXQ='
f = Fernet(KEY)
USERS = {}
USER_SECRETS = {}
USER = "JOJO"
u_list = []
locale.setlocale(locale.LC_ALL, "en_US")

app = Flask(__name__)

entities = set()
descriptions = set()

@app.route("/", methods=["GET"])
def home():
    """
    This method renders the main landing page of the Budgeteer program.

    """
    return render_template("home.html")

@app.route("/add_transaction", methods=["GET"])
def add_transaction():
    """
    This method processes and renders a web form allowing users to
    input a transaction that they completed and the purchases 
    associated with it.

    """
    ents = [e.upper() for e in entities]
    ents.sort()

    return render_template("transaction.html", ents=ents, m=date.today().month, d=date.today().day, y=date.today().year)

@app.route("/add_transaction", methods=["POST"])
def process_transaction():
    """
    This method processes and renders a web form allowing users to
    input a transaction that they completed and the purchases 
    associated with it.

    """
    u_entities = request.form.getlist("entity[]")
    dates = request.form.getlist("date[]")
    total_prices = request.form.getlist("total_price[]")
    for i in range(len(dates)):
        add_expense(dates[i], u_entities[i], total_prices[i])
    save_all_info()
    return render_template("receipt.html", transactions=[u.datestr() for u in u_list])


"""
File IO Functions

"""
def extract_all_info():
    with open(os.path.join("data/", "logins.txt"), "r", encoding="utf-8") as access_logins:
        lines = access_logins.readlines()
        for line in lines:
            line = f.decrypt(line.strip().encode()).decode()
            u = line[:line.index(",")]
            p = line[line.index(",") + 1 : line.rindex(",")]
            s = line[line.rindex(",") + 1:]
            USERS[u] = p
            USER_SECRETS[u] = s
        access_logins.close()
    
    with open(os.path.join("data/", "entities.txt"), "r", encoding="utf-8") as access_entities:
        lines = access_entities.readlines()
        for line in lines:
            entities.add(f.decrypt(line.strip().encode()).decode())
    
    with open(os.path.join("data/", USER_SECRETS[USER]), "r", encoding="utf-8") as u_file:
        u_info = u_file.readlines()
        if len(u_info) >= 1:
            u_stats = f.decrypt(u_info[0].strip().encode()).decode()
            parse_file(u_info[1:])
            u_entries = int(u_stats[:u_stats.index(",")])
            u_amount = float(u_stats[u_stats.index(",") + 1:])
        else:
            u_entries = 0
            u_amount = 0
        print("WELCOME", USER, "YOU HAVE", u_entries, "TRANSACTIONS ENTERED AND A BALANCE OF", locale.currency(u_amount))
        u_file.close()

def adjust_entity(string):
    string = string.upper()
    updated = ""
    for e in string:
        if e == "&":
            updated += "AND"
        elif e == "," or e == "'" or e == ".":
            pass
        else:
            updated += e
    
    return updated


def save_all_info():
    with open(os.path.join("data/", "logins.txt"), "w", encoding="utf-8") as save_logins:
        for u, p in USERS.items():
            login_str = u + "," + p + "," + USER_SECRETS[u]
            save_logins.write(encrypt_to_file(login_str))
        save_logins.close()
    
    with open(os.path.join("data/", USER_SECRETS[USER]), "w", encoding="utf-8") as u_file:
        total = 0
        for t in u_list:
            total += t.net
        u_file.write(encrypt_to_file(f"{len(u_list)},{total}"))
        for item in u_list:
            u_file.write(encrypt_to_file(item.csv()))
        u_file.close()
    
    with open(os.path.join("data/", "entities.txt"), "w", encoding="utf-8") as save_entities:
        for e in entities:
            save_entities.write(encrypt_to_file(e))

def parse_file(user_list):
    for line in user_list:
        decrypted = f.decrypt(line.strip().encode()).decode()
        decrypted = decrypted.strip().split(",")
        u_list.append(Transaction(float(decrypted[0]), decrypted[1], date(int(decrypted[2]), int(decrypted[3]), int(decrypted[4]))))

def encrypt_to_file(text):
    return f.encrypt((text.encode())).decode() + "\n"


def authenticate():
    user = ""
    passw = ""
    while user.upper() not in USERS:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("ENTER YOUR USERNAME ['NEW' TO CREATE AN ACCOUNT]: ", end="")
        user = input()
        if user.strip().upper() == 'NEW':
            return create_new_user()
        if user.strip().upper() not in USERS:
            print("USER DOES NOT EXIST")
            time.sleep(.5)

    while passw == "":
        print("ENTER YOUR PASSWORD: ", end="")
        passw = askpass(prompt="", mask="*") 
        if passw != USERS[user.strip().upper()]:
            print("INCORRECT PASSWORD")
            passw = ""
            time.sleep(.5)
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            print("ENTER YOUR USERNAME: ", user, "\n", end="")

    return user.strip().upper()


def create_new_user():
    user = ""
    passw = ""
    passw2 = " "
    while user == "":
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("CREATE A USERNAME: ", end="")
        user = input()
        if user.strip().upper() in USERS:
            print("USERNAME TAKEN")
            user = ""
            time.sleep(.5)
        if ',' in user:
            print("ILLEGAL CHARACTER ',' IN USERNAME!")
            user = ""
            time.sleep(.5)

    passw2 = " "
    while passw != passw2:
        print("Create a password: ", end="")
        passw = askpass(prompt="", mask="*")
        print("Confirm password: ", end="")
        passw2 = askpass(prompt="", mask="*")
        if passw != passw2:
            print("PASSWORDS DO NOT MATCH")
            time.sleep(.5)
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            print("CREATE A USERNAME:", user, "\n", end="")
    
    USERS[user.strip().upper()] = passw
    file_name = str(f.encrypt(user.strip().upper().encode()))
    USER_SECRETS[user.strip().upper()] = file_name
    temp = open(os.path.join("data/", USER_SECRETS[user.strip().upper()]), "w", encoding="utf-8")
    temp.write(encrypt_to_file("0,0.00"))
    temp.close()
    return user.strip().upper()

def add_expense(date, entity, money):
    entity = adjust_entity(entity.strip())
    entities.add(entity)
    u_list.append(Transaction(-1*float(money), entity, datetime.strptime(date, "%m/%d/%y").date()))
    print("ADDED EXPENSE: ", u_list[-1].datestr())

if __name__ == "__main__":
    extract_all_info()
    app.run(host='0.0.0.0', port=8080, debug=False)
    
