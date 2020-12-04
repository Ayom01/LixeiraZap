import socket
import threading

nickname = input("Nickname: ")
server_ip = input("Server ip: ")
PORT = int(input("Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = input('')
        if message == "/exit":
            break
        else:
            nick_message = '{}: {}'.format(nickname, message)
            client.send(nick_message.encode("ascii"))

recieve_thread = threading.Thread(target=receive)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
