# SaveTool
 A tool for managing and saving code snippets and other stuff.
### History
I wrote this "masterpiece" ;) during my Apprenticeship. I wanted to save a code-snippet from one of my projects, but I didn't want to use a txt file and especially not paper. So I made a tool for purpose.


> [!IMPORTANT]
># Requirements
>- Python is installed on you computer
>- following libaries installed
>  ```
>  json
>  pyperclip
>  prompt_toolkit
>  ```

# How to Install + Setup
1. Download the "SaveTool" folder and place it in a folder of your choice on your PC. 
2. Open the "SaveTool" folder and copy the path of the .json file
3. Open your terminal and navigate to the "SaveTool" folder
4. Use ```python SaveTool.py``` to start the program
5. Paste the copied path and hit ENTER
6. Have fun

> [!TIP]
>I personaly don't want to navigate to the folder every time I want to use the program. 
>So I made me a little script that let's me use just the command ```savetool``` from everywhere
><details>
>
>**<summary>Here's how</summary>**
>
>1. Go in a folder that is in your PATH (for example: "C:\Users\you\AppData\Local\Programs\Python\Python312").
>2. Create a .bat file and name it "savetool".
>3. Now copy and paste this in this file:
>
> (pls change the path to your's)
> ```ruby
> @echo off
> python "C:\path\to\your\SaveTool.py" %*
> ```
>
>Now you should be able to start SaveTool.py via ```savetool```
>
></details>

## If you have any problems, feel free to contact me :)
 

# future plans
I'm currently working on a function to edit the saved content

# License/Terms of use
Feel free to use the programm for yourself and group activities (don't know what you could do with such a programm in a group ¯\\_(ツ)_/¯ ).
Don't do soething with this code that could harm other beings. I, the developer, do not take any responsibility or liability for damages and/or problems to your system that my have been caused by my program.
Feel free to costumise and modify the code.
