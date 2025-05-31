import shutil
import os

MyProgram = os.path.abspath(__file__)
MyFolder = os.path.dirname(os.path.abspath(__file__))
MusicFolder = rf"C:\Users\bad production\Music"
WorkFolder = os.path.join(MyFolder, "TEST")
ShowMessage = True
ClearText = True

def clear():
    if ClearText:
        os.system("cls")
clear()

def message(text):
    if ShowMessage:
        print(text)

def copy(origin, destiny):
    shutil.copy2(origin, destiny)

if not os.path.exists(WorkFolder):
    message("work folder created\n")
    os.mkdir(WorkFolder)


def find(RootDir):
    for root, dirs, files in os.walk(RootDir):
        for file in files:
            FilePath = os.path.join(root, file)
            clear()
            message(f"file found: {FilePath}")
            copy(FilePath, WorkFolder)
find(MusicFolder)

clear()
os.listdir(WorkFolder)