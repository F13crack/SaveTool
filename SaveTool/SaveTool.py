import json
import pyperclip
import os
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import getopt
import configparser
import logging

# --------------------------------------------------------
# version
# --------------------------------------------------------
version = "1.0"

# --------------------------------------------------------
# setting up logger
# --------------------------------------------------------
with open('output/Logs/SaveTool_logs.log', 'w'):
    pass
logger = logging.getLogger(__name__)
logging.basicConfig(filename='output/Logs/SaveTool_logs.log', format='[%(filename)s->%(funcName)s():%(lineno)s] %(levelname)s: %(message)s', datefmt='%m/%d/%Y|%H:%M:%S', encoding='utf-8', level=logging.DEBUG)


# --------------------------------------------------------
# design
# --------------------------------------------------------
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


# --------------------------------------------------------
# usage & help
# --------------------------------------------------------
def printUsage():
    Usage = """
Usage: (Version %s)
-------
  savetool help
  savetool version
  savetool config       [--print] [--locate] [--edit <title> --content <value>] [--delete <filename>]
  savetool file         [--new <new-filename>] [--print] [--locate] [--delete <filename>]

  savetool              [--search <title>] [--show-all] [--save <title> --content <content>] \n  \t\t\t[--edit <title>] [--delete <title>] [--verbose]

  Global (or alomost global) options:
    --new                   : creates a new file
    --print                 : prints out the content
    --locate                : prints the location of the file
    --delete                : deletes the specified file/title
-------

  Try 'savetool help' for more information.

""" % (version)
    print(Usage)
    quit()

# --------------------------------------------------------
# file management
# --------------------------------------------------------
def read_conf_value(name):
    config = configparser.ConfigParser()
    config.read('src/config.ini')
    val = config.get('Database', name)
    return val

def set_conf_value(name, value):
    config = configparser.ConfigParser()
    config.read('src/config.ini')
    config.set('Database', name, value)
    with open('src/config.ini', 'w') as conf_file:
        config.write(conf_file)
    logger.info("value: " + read_conf_value('first_start'))
    return read_conf_value('first_start')

def read_config():
    try:
        j_path = read_conf_value('json_path')
        cnf_path = read_conf_value('config_path')
        f_s = read_conf_value('first_start')
        
        if j_path == 'None' or cnf_path == 'None' or f_s == 'None':
            create_config()
        logger.debug("It worked :)")
        return j_path, cnf_path, f_s
    except configparser.NoSectionError as error_noSec:
        logger.error(f"NoSectionError: {error_noSec}")
        # user_path = input('Please input your path to the json file, where you want to save your data (WITHOUT ""): ')
        create_config()

def create_new_json(name):
    global sPathFile
    logger.debug("name = " + name)
    current_dir = os.path.abspath(os.getcwd())
    dir = "src"
    path = os.path.join(current_dir, dir)
    if not os.path.exists(path):
        os.makedirs(path)
    logger.debug("(to del) sPathFile = " + str(sPathFile))
    os.remove(read_conf_value('json_path'))
    sPathFile = (f"{path}\\{name}.json")
    set_conf_value('json_path', sPathFile)
    create_save("Information", "Welcome.\n\nYou can delete this entry. It was automatically created at the first start.\n\nHave Fun :)")
    return sPathFile

def create_config():
    logger.info("create .ini")
    global sPath
    global sPathConfig
    current_dir = os.path.abspath(os.getcwd())
    dir = "src"
    path = os.path.join(current_dir, dir)
    if not os.path.exists(path):
        os.makedirs(path)
    sPathFile = (path + "\\SavedContentTest.json")
    config = configparser.ConfigParser()
    config['Database'] = {'json_path': (sPathFile), 'config_path': (path + "\\config.ini"), 'first_start': (True)}
    with open(path + '\\config.ini', 'w') as configfile:
        config.write(configfile)
    with open(path + "\\SavedContentTest.json", 'w'):
        pass
    read_config()
    return

# --------------------------------------------------------
# Functions
# --------------------------------------------------------
def get_version():
    if version:
        # logger.debug("Version output: " + version)
        return version
    else:
        # logger.warning("No version found!")
        return "No version found"
    
# A U T O C O M P E T E
def load_suggestions():
    try:
        with open(sPathFile, 'r') as file:
            return json.load(file)
    except json.decoder.JSONDecodeError as error_json_dec:
        logger.error(f"JsonDecodeError: {error_json_dec}")
        create_save("Information", "Welcome.\n\nYou can delete this entry. It was automatically created at the first start.\n\nHave Fun :)")
        return False
# - - - - - - - - - - -

def window_exit():
    close = messagebox.askyesno("Exit without saving?", "Are you sure you want to exit without saving?")
    if close:
        check_stat()
        # print(bcolors.WARNING + "\n\n>> closed window without saving\n" + bcolors.ENDC)
        root.destroy()

def edit(title):
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
    with open(sPathFile, "r") as f:
        data = json.load(f)
    try:
        text.insert(END, data[title])
    except KeyError:
        print(bcolors.FAIL + "\n>> NO TITLE FOUND" + bcolors.ENDC + f"\t'{title}'")
        return
    save_button = tk.Button(root, text=">> SAVE <<", command=lambda: SaveEdited(title), bg="#29d65d")
    save_button.pack(side=BOTTOM)
    root.protocol("WM_DELETE_WINDOW", window_exit)
    root.mainloop()
    if root.mainloop() == False:
        check_stat()
    return True

def SaveEdited(title):
    t = text.get("1.0", "end-1c")
    with open("Teste.txt", "w", encoding="utf-8") as file:
        file.write(t)
    file.close()
    os.remove("Teste.txt")
    root.destroy()
    create_save(title, t)
    return True

def create_save(title, content):
    try:
        with open(sPathFile, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data={}
    data[title] = content
    with open(sPathFile, 'w') as file:
        json.dump(data, file, indent=4)
    return True

def Search(title):
    try:
        check_stat()
        with open(sPathFile, 'r') as file:
            obj = json.load(file)
            if title in obj:
                print(bcolors.OKCYAN + "\n\nHere is the result:\n"+"-"*60+"\n" + bcolors.ENDC + obj[title] + bcolors.OKCYAN + "\n"+"-"*60 + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "\n\n>> NO CONTENT FOUND" + bcolors.ENDC)
    except KeyError:
        logger.error("KeyError: " + KeyError + "\n(Unexpected error)")
        print(bcolors.FAIL + "\n--------------\nUNEXPECTED ERROR\n--------------" + bcolors.ENDC)

def show_all():
    check_stat()
    with open(sPathFile) as file:
        data = json.load(file)
    print(bcolors.OKCYAN + "\n\nHere is the result:\n"+"-"*60+"\n" + bcolors.ENDC)
    for title in sorted(data.keys(), key=str.casefold):
        print(bcolors.BOLD + ">> " + title + bcolors.ENDC)
    print(bcolors.OKCYAN + "\n"+"-"*60 + bcolors.ENDC)
    return

def delete(title):
    if title:
        uSure = input(bcolors.WARNING + f"Do you want to delete \"{title}\" ? (Y/N): " + bcolors.ENDC)
        if uSure:
            if uSure.lower() == "n":
                check_stat()
                return
            elif uSure.lower() == "y":
                check_stat()
                if (sFile or sConfig):
                    # delete specific file
                    pass
                else:
                    with open(sPathFile) as file:
                        data = json.load(file)
                    if title in data:
                        del data[title]
                        print(bcolors.OKGREEN + "\n>> Title '" + title + "' successfully deleted" + bcolors.ENDC)
                    else:
                        print(bcolors.FAIL + "\n>> NO TITLE FOUND" + bcolors.ENDC)
                    with open(sPathFile, 'w') as file:
                        json.dump(data, file, indent=4)
                        return
        check_stat()
        print(bcolors.FAIL + "\n\n>> NO VALID INPUT <<" + bcolors.ENDC)
        return
    check_stat()

def check_stat():
    if sMain:
        os.system('cls')
    return


# --------------------------------------------------------
# MAIN Functions
# --------------------------------------------------------
def main_programm():
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
    print("\t\t\tBy Luca Elija Mauro")
    while sMain:
        try:
            logger.info(sPath)
            print(bcolors.HEADER + "\n\n---------------- C O M M A N D S ---------------\n" + bcolors.ENDC + "1: Search \n2: Show all \n3: Save new \n4: Edit\n5: Delete\n6: EXIT\n" + bcolors.HEADER +"-"*48 + bcolors.ENDC)
            suggestions = load_suggestions()
            completer = WordCompleter(suggestions, ignore_case=True)
            session = PromptSession(completer=completer)
            
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
                os.system('cls')
                if create_save(newTitle, newContent):
                    print(bcolors.OKCYAN + "\n\n>> Data saved\n" + bcolors.ENDC)
            elif user_input == 2:
                show_all()
            elif user_input == 5:
                delete_input = session.prompt("\nTitle: ")
                delete(delete_input)
            elif user_input == 6:
                os.system('cls')
                print(bcolors.WARNING + "\n\n>>> program closed <<<\n" + bcolors.ENDC)
                quit()
            elif user_input == 4:
                usr_in = session.prompt("\nTitle: ")
                if edit(usr_in):
                    check_stat()
                    print(bcolors.OKCYAN + "\n\n>> Data saved\n" + bcolors.ENDC)
            else:
                os.system('cls')
        except KeyboardInterrupt:
            os.system('cls')
            print(bcolors.WARNING + "\n\n>>> program stopped <<<\n" + bcolors.ENDC)
            quit()
        except (NameError) as error_name:
            logger.error(f"NameError: {error_name} \n(expected error)")
            os.system('cls')
            print(bcolors.FAIL + "\n"+"-"*14+"\nEXPECTED ERROR\n"+"-"*14 + bcolors.ENDC)
        except (SyntaxError):
            os.system('cls')
            print(bcolors.WARNING + "\n>> no input" + bcolors.ENDC)

def main(argv):
    try:

        # ----- Initialize variables
        global sMain
        global sVerbose
        global sFile
        global sConfig
        global sPath
        global sPathFile
        global sPathConfig
        global sFirst_start

        sAction = None

        sPath = None
        sPathFile = None
        sPathConfig = None

        sMain = False
        sFirst_start = True
        sFile = False
        sConfig = False

        sContent = None
        sVerbose = False
        sVersion = False
        sSearch = None
        sShow_all = False
        sSave_new = None
        sEdit = None
        sDelete = None
        sPrint = False
        sNew_File = False
        sLocate = False

        # --------------------------------------------------------
        # check path
        # --------------------------------------------------------
        try:
            sPathFile, sPathConfig, sFirst_start = read_config()
        except TypeError:
            read_config()
            sPathFile, sPathConfig, sFirst_start = read_config()


        logger.info("sFirst_start: " + str(sFirst_start))

        if sFirst_start == True:
            logger.debug("create Inf")
            create_save("Information", "Welcome.\n\nYou can delete this entry. It was automatically created at the first start.\n\nHave Fun :)")
            sFirst_start = set_conf_value('first_start', 'False')

        # --------------------------------------------------------
        # Figure out the action
        # --------------------------------------------------------
        if len(sys.argv) < 2:
            sMain = True
            main_programm()
            return
        
        sAction = sys.argv[1].lower()

        # --------------------------------------------------------
        # Parse the command line
        # --------------------------------------------------------
        args = None
        place = sys.argv[1:]

        if sAction in ["-?", "-h", "/?", "/h", "--help"]:
            printUsage()
            return
        if sAction == "help":
            pass

        if sAction == "file":
            sFile = True
            place = sys.argv[2:]

        if sAction == "config":
            sConfig = True
            place = sys.argv[2:]

        opts, args = getopt.getopt(place, "vr:os:c:e:d:pn:l", [
            "verbose", "search=", "show-all", "save=", "content=", "edit=", "delete=", "version", "print", "new=", "locate"
        ])

        listOptions = []

        for o, a in opts:
            listOptions.append(o)

            if o in ["-r", "--search"]:
                sSearch = str(a)
            if o in ["-o", "--show-all"]:
                sShow_all = True
            if o in ["-s", "--save"]:
                sSave_new = str(a)
            elif o in ["-e", "--edit"]:
                sEdit = str(a)
            if o in ["-d", "--delete"]:
                sDelete = str(a)
            elif o in ["-c", "--content"]:
                sContent = str(a)
            elif o in ["-v", "--verbose"]:
                sVerbose = True
            elif o in ["--version"]:
                sVersion = True
            elif o in ["-p", "--print"] and (sFile or sConfig):
                sPrint = True
            elif o in ["-n", "--new"] and (sFile or sConfig):
                sNew_File = str(a)
            elif o in ["-l", "--locate"] and (sFile or sConfig):
                sLocate = True

        if sVersion:
            print("Version: " + get_version())

        if sVerbose:
            print("Version: " + get_version())

        if sSearch:
            Search(sSearch)

        if sShow_all:
            show_all()

        if sSave_new:
            if len(listOptions) > 1:
                create_save(sSave_new, sContent)
            else:
                print("content?")
                return "stop"
            
        if sEdit:
            if sConfig:
                set_conf_value(sEdit, sContent)
            else:
                edit(sEdit)
            print(bcolors.OKCYAN + ">> Data saved" + bcolors.ENDC)


        if sDelete:
            delete(sDelete)

        if sPrint:
            if sFile:
                path = sPathFile
                info = "Show json-file: "
            if sConfig:
                path = sPathConfig
                info = "Show config-file: "
            f = open(path)
            print(bcolors.OKCYAN + f"\n{info} \n\n" + bcolors.ENDC + f.read() + "\n")
        

        if sNew_File:
            logger.debug("sNew_File = " + sNew_File)
            if sFile:
                usr = input(bcolors.WARNING + "Do you want to create a new file? The old content will be deleted (y/n)?" + bcolors.ENDC)
                if usr.lower() == "y":
                    sPathFile = create_new_json(sNew_File)
                    logger.debug("sNew_File = " + sNew_File)
                elif usr.lower() == "n":
                    return
                
        
        if sLocate:
            if sFile:
                print(f"\nPath:\t{read_conf_value('json_path')}\n")
            if sConfig:
                print(f"\nPath:\t{read_conf_value('config_path')}\n")


    except getopt.GetoptError as error_getopt:
        # logger.error(f"getopt.GetoptError: {error_getopt}")
        print(f"-------------------- reason: --------------------\n\n\t{error_getopt} \n\n" + "-"*49 + "\n\tYou probably forgot to add a value to an option (like '-v' or '-t'):\n")
        # print_usage()
        return False
    

if __name__ == "__main__":
    main(sys.argv[1:])