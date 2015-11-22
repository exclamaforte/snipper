import socket
from threading import Thread

def get_input():
    HOST = 'localhost'
    PORT = 53706
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024) #size?
        conn.sendall(data)
        recieve(data)
    conn.close()

def recieve(str_in):
    print(str_in)

if __name__ == "__main__":
    input_thread = Thread(target = get_input)
    input_thread.start()
    input_thread.join()
    print("done")
