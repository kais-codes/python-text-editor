from guizero import *
from requests import *

# root
file_name = None
app = App(title="Text Editor ", height=570, width=700, bg="white")


# performs first time check for showing instructions
try:
    with open("instructions.txt", "r") as check:
        if check == "Skip":
            pass

except FileNotFoundError:
    app.info("Instructions", "Thank you for using this text editor! \n"
                             "\n"
                             "In the File menu, there are options to load/save a file, as well as viewing its "
                             "location.\n"
                             "In the Edit menu, you can clear the contents with the Clear File button. \n"
                             "In the App Menu, you can find the explanations of the buttons again. \n"
                             "The Spell Check button will return a list of misspelled words. \n"
                             "If the file does not exist, you will have to enter a name when pressing save. \n"
                             "There is an auto save feature that will save your progress every 30 seconds.\n"
                             "\n"
                             "Warning: Pressing save will overwrite the current contents of the file.")
    with open("instructions.txt", "w") as check:
        check.write("Skip")


# functions for buttons when they are clicked
def select_file():
    """Function for manually selecting a file"""
    global file_name
    file = app.select_file()
    file_name = file
    with open(file, "r") as file:
        text_area.value = file.read()


def save_file():
    """Function for saving changes to text file, creates it if it doesn't exist"""
    answer = yesno("Warning?", "Saving will overwrite old content, do you want to save?")
    if answer:
        global file_name
        if file_name is None:
            file_name = question("File Name", "Enter a name for your file")
        try:
            if ".txt" not in file_name:
                with open(file_name + ".txt", "w") as file:
                    file.write(text_area.value)
        except OSError:
            error("Invalid Character", "Invalid file name detected")
        else:
            with open(file_name, "w") as file:
                file.write(text_area.value)

        if file_name is None:
            file_name = question("File Name", "Enter a name for your file")


def new_file():
    """Saves current file and clears the content for a new file"""
    global file_name
    file_name = question("Enter File Name", "Enter the name of your new file: ")
    file_name += ".txt"
    print(file_name)
    text_area.clear()
    with open(file_name, "w") as file:
        file.write(text_area.value)


def find_file():
    """Returns where the path of the file is"""
    app.info("File Details", f"Your file is located at: {file_name}")


def clear_text():
    """Function for clearing the textbox, requires confirmation"""
    answer = yesno("Confirmation?", "Do you want to clear the contents?")
    if answer:
        text_area.clear()
        return


def instructions():
    """Creates a popup displaying the instructions"""
    app.info("Function Descriptions", "In the File menu, there are options to load/save a file, as well as viewing its "
                             "location.\n"
                             "In the Edit menu, you can clear the contents with the Clear File button. \n"
                             "If the file does not exist, you will have to enter a name when pressing save. \n"
                             "The Spell Check button will return a list of misspelled words \n"
                             "There is an auto save feature which saves your progress every 30 seconds"
                             "\n"
                             "Warning: Pressing save will overwrite the current contents of the file.")

def spell_checker():
    """Calls a microservice to perform a spell check"""
    microservice = "https://linlo-cs361-microservice.uw.r.appspot.com/"
    body = {"text": text_area.value}

    post_request = post(microservice, json=body)
    response = post_request.json()
    invalid_words = []
    for words in response["invalidWords"]:
        invalid_words.append(" " + words + " ")

    if len(invalid_words) == 0:
        window = Window(app, title="Invalid words")
        word_box = Box(window)
        Text(word_box, text="No invalid words detected.")
    else:
        window = Window(app, title="Invalid words")
        word_box = Box(window)
        Text(word_box, text="Invalid words found from spell check:")
        Text(word_box, invalid_words)


def close_confirmation():
    """Asks for confirmation upon closing the app"""
    if app.yesno("Close", "Are you sure you want to close the application?"):
        app.destroy()


def auto_save():
    """Function used for auto save"""
    with open(str(file_name), "w") as file:
        file.write(text_area.value)


# auto save feature
app.repeat(30000, auto_save)

menu = MenuBar(app, toplevel=["File", "Edit", "App"], options=[
    [["New File", new_file], ["Open File", select_file], ["Save File", save_file], ["File Details", find_file]],
    [["Clear File", clear_text]],
    [["Instructions", instructions]]])

# box for the textbox and buttons associated with it
text_box = Box(app, border=1, align="bottom", width="fill", height="fill")
text_area = TextBox(text_box, width="fill", height="fill", multiline="True", text="Enter your text here")

# buttons for spell checking and saving file
spell_check = PushButton(text_box, text="Spell Checker", command=spell_checker, align="left")
save_file = PushButton(text_box, text="Save", command=save_file, align="right", width=15)

app.when_closed = close_confirmation
app.display()
