import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install','pynput'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','requests'])