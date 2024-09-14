import json
import pyperclip
import os
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

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


# A U T O C O M P E T E
def load_suggestions():
    with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'r') as file:
        return json.load(file)
# - - - - - - - - - - -


def create_save(title, content):
    try:
        os.system('cls')
        with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data={}
    data[title] = content
    with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'w') as file:
        json.dump(data, file, indent=4)
    print(bcolors.OKCYAN + "\n\n>> Data saved\n" + bcolors.ENDC)

#IN WORK
def change_data(title):
    with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'r') as file:
        data = json.load(file)
    #print(data[title])
    input(data[title])
#-------------

def Search(title):
    try:
        os.system('cls')
        with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'r') as file:
            obj = json.load(file)
            if title in obj:
                print(bcolors.OKCYAN + "\n\nHere is the result:\n------------------------------------------------------------\n" + bcolors.ENDC + obj[title] + bcolors.OKCYAN + "\n------------------------------------------------------------" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "\n>> NO CONTENT FOUND" + bcolors.ENDC)
    except KeyError:
        print(bcolors.FAIL + "\n--------------\nUNEXPECTED ERROR\n--------------" + bcolors.ENDC)

def show_all():
    os.system('cls')
    with open("C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json") as file:
        data = json.load(file)
    print(bcolors.OKCYAN + "\n\nHere is the result:\n------------------------------------------------------------\n" + bcolors.ENDC)
    for title in sorted(data.keys(), key=str.casefold):
        print(bcolors.BOLD + ">> " + title + bcolors.ENDC)
    print(bcolors.OKCYAN + "\n------------------------------------------------------------" + bcolors.ENDC)

def delete(title):
    os.system('cls')
    with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json') as file:
        data = json.load(file)
    if title in data:
        del data[title]
        print(bcolors.WARNING + "\n>> Title '" + title + "' successfully deleted" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "\n>> NO TITLE FOUND" + bcolors.ENDC)
    with open('C:\\Users\\lucae\\Documents\\GitHub\\SaveTool\\code\\SavedContent.json', 'w') as file:
        json.dump(data, file, indent=4)


def main():
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
        #print(bcolors.OKGREEN + bcolors.BOLD + "\n--- WELCOME - TO - SAVETOOL ï¼ˆï¿£ï¸¶ï¿£ï¼‰â†— ---" + bcolors.ENDC + bcolors.OKBLUE + "\nBy Luca Elija Mauro\n\n" + bcolors.ENDC)

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
        print(bcolors.HEADER + "\n\n---------------- C O M M A N D S ---------------\n" + bcolors.ENDC + "1: Search \n2: Show all \n3: Save new \n4: Delete\n5: exit\n" + bcolors.HEADER + "------------------------------------------------" + bcolors.ENDC)
        suggestions = load_suggestions()
        completer = WordCompleter(suggestions, ignore_case=True)
        session = PromptSession(completer=completer)
        try:
            user_input = eval(input("> "))
            if user_input == 1:
                searchTitle = session.prompt("\nTitle: ")
                Search(searchTitle)
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
                create_save(newTitle, newContent)
            elif user_input == 2:
                show_all()
            elif user_input == 4:
                delete_input = input(bcolors.BOLD + "\nTitle: " + bcolors.ENDC)
                delete(delete_input)
            elif user_input == 5:
                os.system('cls')
                print(bcolors.WARNING + "\n\n>>> program closed <<<\n" + bcolors.ENDC)
                quit()
            elif user_input == 6:
                usr_in = input(">> ")
                change_data(usr_in)
            else:
                os.system('cls')
        except KeyboardInterrupt:
            os.system('cls')
            print(bcolors.WARNING + "\n\n>>> program stopped <<<\n" + bcolors.ENDC)
            quit()
        except (NameError, SyntaxError):
            os.system('cls')
            print(bcolors.FAIL + "\n--------------\nEXPECTED ERROR\n--------------" + bcolors.ENDC)