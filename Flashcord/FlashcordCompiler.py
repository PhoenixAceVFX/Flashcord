import os
import time

File_Name = "sid.css"

# Logging System + Getting current time and date in preferred format
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}/{CTime.tm_mon:02d}/{CTime.tm_year}"
    return Time, Date

def WriteLog(Log):
    Time, Date = GetTime()
    PrintLog = f"[{Time} - {Date}] {Log}"
    print(PrintLog)

def ls():
    ReturnFiles = []
    Path = os.getcwd()
    for root, dirs, files in os.walk(Path):
        for f in files:
            if f.endswith('.css'):
                # Use os.path.join and normalize paths to be Linux-compliant
                Temp = os.path.relpath(os.path.join(root, f), Path)
                ReturnFiles.append(Temp)

    # Exclude specific files
    try:
        ReturnFiles.remove("main.css")
        ReturnFiles.remove(File_Name)
    except ValueError:
        pass  # Ignore if files are not found in the list

    # Sort the files alphanumerically
    ReturnFiles.sort()
    return ReturnFiles

def Build_Date():
    WriteLog("Adding Build Date variable...")
    Time, Date = GetTime()
    Build_Date = f'"{Time} - {Date}"'
    WriteLog(f"Flashcord was built at {Build_Date}.")
    Build_String = f'\n:root {{ --FlashCore-Build_Date: {Build_Date}; }}'
    return Build_String

def Flashcord_Compiler():
    WriteLog(f"Parsing CSS Files...")
    CSS_Files = ls()
    WriteLog(f"Parsed the following files (sorted): {CSS_Files}")
    try:
        with open(File_Name, 'w', encoding='utf-8') as Final_File:
            for CSS_File in CSS_Files:
                try:
                    with open(CSS_File, 'r', encoding='utf-8') as Source_File:
                        Final_File.write(Source_File.read())
                except FileNotFoundError:
                    WriteLog(f"Warning: File '{CSS_File}' not found!")
            Final_File.write(Build_Date())
        WriteLog("Flashcord has been compiled successfully!")
    except Exception as Error:
        WriteLog(f"ERROR COMPILING FLASHCORD: {Error}")

if __name__ == "__main__":
    Flashcord_Compiler()
