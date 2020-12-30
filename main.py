from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.config import Config
import socket
import threading

# Conexão com o Server.py
nickname = input("Nickname: ")
server_ip = input("Server ip: ")
PORT = int(input("Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, PORT))


# Configs da interface
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')


# Classe que sustenta o FloatLayout
class MyFloatLayout(FloatLayout):
    # Envio da mensagem para o servidor
    def write(self, text, *args):
        nick_message = '{}: {}'.format(nickname, text)
        client.send(nick_message.encode("ascii"))

        self.ids.chat.add_widget(Label(text=text, font_size=40, size_hint_y=None, height=100)) # Aqui, o cliente recebe a própria mensagem. Uma vez que o bug esteja resolvido, ela não será mais necessária 
    
    # Recepção das mensagens do servidor
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
                    
                    self.ids.chat.add_widget(Label(text=message, font_size=40, size_hint_y=None, height=100)) # Esta linha não tá funcionando
            except:
                print("An error occured!")
                client.close()
                break


# Start na interface
class MainApp(App):
    def build(self):
        recieve_thread = threading.Thread(target=MyFloatLayout().receive)
        recieve_thread.start()
        return MyFloatLayout()


# Thread
interface_thread = threading.Thread(target=MainApp().run)
interface_thread.start()
