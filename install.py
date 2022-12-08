import json
import subprocess
import sys
import requests
import base64

subprocess.check_call([sys.executable, '-m', 'pip', 'install','pynput'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install','requests'])