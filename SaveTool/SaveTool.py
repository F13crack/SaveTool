import json
import pyperclip
import os
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import configparser
from tkinter import *
import tkinter as tk
from tkinter import messagebox

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    json_path = config.get('Database', 'json_path')
    config_values = {
        'json_path': json_path,
    }
 
    return config_values['json_path']


def create_config(path):
    config = configparser.ConfigParser()
    config['Database'] = {'json_path': path}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# A U T O C O M P E T E
def load_suggestions(path):
    with open(path, 'r') as file:
        return json.load(file)
# - - - - - - - - - - -

def window_exit():
    close = messagebox.askyesno("Exit without saving?", "Are you sure you want to exit without saving?")
    if close:
        os.system('cls')
        print(bcolors.WARNING + "\n\n>> closed window without saving\n" + bcolors.ENDC)
        root.destroy()

def edit(title, path):
    global root
    global text
    root = tk.Tk()
    root.geometry("850x490")
    root.title("SaveTool-Editor")
    root.configure(bg="#e6e6e6")
    fram = tk.Frame(root)
    fram.pack(fill=BOTH, expand=True)
    S = Scrollbar(fram)
    S.pack(side=RIGHT, fill=Y)
    text = Text(fram)
    text.pack(fill=BOTH, expand=True)
    S.config(command=text.yview)
    text.config(yscrollcommand=S.set)
    with open(path, "r") as f:
        data = json.load(f)
    text.insert(END, data[title])
    save_button = tk.Button(root, text=">> SAVE <<", command=lambda: SaveEdited(title), bg="#29d65d")
    save_button.pack(side=BOTTOM)
    root.protocol("WM_DELETE_WINDOW", window_exit)
    root.mainloop()
    if root.mainloop() == False:
        os.system('cls')

def SaveEdited(title):
    t = text.get("1.0", "end-1c")
    with open("Teste.txt", "w", encoding="utf-8") as file:
        file.write(t)
    file.close()
    os.remove("Teste.txt")
    root.destroy()
    create_save(title, t)

def create_save(title, content, path):
    try:
        os.system('cls')
        with open(path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data={}
    data[title] = content
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    print(bcolors.OKCYAN + "\n\n>> Data saved\n" + bcolors.ENDC)

def Search(title, path):
    try:
        os.system('cls')
        with open(path, 'r') as file:
            obj = json.load(file)
            if title in obj:
                print(bcolors.OKCYAN + "\n\nHere is the result:\n------------------------------------------------------------\n" + bcolors.ENDC + obj[title] + bcolors.OKCYAN + "\n------------------------------------------------------------" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "\n\n>> NO CONTENT FOUND" + bcolors.ENDC)
    except KeyError:
        print(bcolors.FAIL + "\n--------------\nUNEXPECTED ERROR\n--------------" + bcolors.ENDC)

def show_all(path):
    os.system('cls')
    with open(path) as file:
        data = json.load(file)
    print(bcolors.OKCYAN + "\n\nHere is the result:\n------------------------------------------------------------\n" + bcolors.ENDC)
    for title in sorted(data.keys(), key=str.casefold):
        print(bcolors.BOLD + ">> " + title + bcolors.ENDC)
    print(bcolors.OKCYAN + "\n------------------------------------------------------------" + bcolors.ENDC)

def delete(title, path):
    os.system('cls')
    with open(path) as file:
        data = json.load(file)
    if title in data:
        del data[title]
        print(bcolors.WARNING + "\n>> Title '" + title + "' successfully deleted" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "\n>> NO TITLE FOUND" + bcolors.ENDC)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def mainFunction(path):
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("""
                -----------------SaveTool-----------------
                Developer: Luca Elija Mauro
                Contact: F13-1nfo@outlook.com
                Version: 1.0
                Version release: 11. Septemper 2024
                ------------------------------------------""")
            quit()
        else:
            print(bcolors.FAIL + "COMMAND NOT FOUND\ndid you mean:\n\t'python .\\SaveTool.py --help'\n\t'python .\\SaveTool.py'\n" + bcolors.ENDC)
            quit()
    else:
        os.system('cls')

        text = """
    =======================================================
    |  /|  /  |‾‾‾  |     |‾‾‾  |‾‾‾|  |\\  /|  |‾‾‾
    | / | /   |———  |     |     |   |  | \\/ |  |———
    |/  |/    |___  |___  |___  |___|  |    |  |___
                    
                    ‾‾|‾‾  |‾‾‾|
                        |    |   |
                        |    |___|

    |‾‾‾   |‾‾‾| \\     /  |‾‾‾  ‾‾|‾‾  |‾‾‾|  |‾‾‾|  |
    |———|  |___|  \\   /   |———    |    |   |  |   |  |
    ___|  |   |   \\ /    |___    |    |___|  |___|  |___
    ======================================================="""

        print(bcolors.OKGREEN + text + bcolors.ENDC)
        print("                By Luca Elija Mauro")

    while True:
        try:
            print(bcolors.HEADER + "\n\n---------------- C O M M A N D S ---------------\n" + bcolors.ENDC + "1: Search \n2: Show all \n3: Save new \n4: Edit\n5: Delete\n6: EXIT\n" + bcolors.HEADER + "------------------------------------------------" + bcolors.ENDC)
            suggestions = load_suggestions(path)
            completer = WordCompleter(suggestions, ignore_case=True)
            session = PromptSession(completer=completer)
            
            user_input = eval(input("> "))
            if user_input == 1:
                searchTitle = session.prompt("\nTitle: ")
                Search(searchTitle, path)
            elif user_input == 3:
                newTitle = input(bcolors.BOLD + "\nTitle: " + bcolors.ENDC)
                usr = input(bcolors.WARNING + "Do you want to paste the copied content (y/n)?" + bcolors.ENDC)
                if usr.lower() == "y":
                    newContent = pyperclip.paste()
                elif usr.lower() == "n":
                    print(bcolors.BOLD + "\nType your content here (duoble click ENTER to save):\n" + bcolors.ENDC)
                    lines = []
                    while True:
                        line = input()
                        if line:
                            lines.append(line)
                        else:
                            break
                    newContent = '\n'.join(lines)
                create_save(newTitle, newContent, path)
            elif user_input == 2:
                show_all(path)
            elif user_input == 5:
                delete_input = session.prompt("\nTitle: ")
                delete(delete_input, path)
            elif user_input == 6:
                os.system('cls')
                print(bcolors.WARNING + "\n\n>>> program closed <<<\n" + bcolors.ENDC)
                quit()
            elif user_input == 4:
                usr_in = session.prompt("\nTitle: ")
                edit(usr_in, path)
            else:
                os.system('cls')
        except KeyboardInterrupt:
            os.system('cls')
            print(bcolors.WARNING + "\n\n>>> program stopped <<<\n" + bcolors.ENDC)
            quit()
        except (NameError):
            os.system('cls')
            print(bcolors.FAIL + "\n--------------\nEXPECTED ERROR\n--------------" + bcolors.ENDC)
        except (SyntaxError):
            os.system('cls')
            print(bcolors.WARNING + "\n>> no input" + bcolors.ENDC)

if read_config() == 'None':
    user_path = input('Please input your path to the json file, where you want to save your data (WITHOUT ""): ')
    create_config(user_path)
    mainFunction(user_path)
else:
    path = read_config()
    mainFunction(path)