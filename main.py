import socket
from threading import Thread

HOST = 'localhost'
PORT = 53706

def get_input():
    print('Connected by', addr)
    while True:
        data = conn.recv(1024) #size?
        if not data: 
            break
        # conn.sendall(data)
        recieve(data)
    conn.close()

def recieve(str_in):
    print(str_in)
    send_result(str_in)

def send_result(str_out):
    conn.sendall(str_out)
    print("SENT")

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    input_thread = Thread(target = get_input)
    input_thread.start()
    input_thread.join()
    print("done")
