import socket
import threading

class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username

    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(message)
            except Exception as e:
                print(f"Erro durante a recepção de mensagens: {e}")
                break

    def send_messages(self, client_socket):
        while True:
            message = input()
            
            if message == "/exit":
                client_socket.sendall(f"/exit {self.username}" . encode('utf-8'))
                client_socket.close()
                break
            try:
                client_socket.sendall(f"[{self.username}] says: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                break

    def connect(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            print("Conexão estabelecida com o servidor")

            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            send_thread = threading.Thread(target=self.send_messages, args=(client_socket,))
            receive_thread.start()
            send_thread.start()
        except Exception as e:
            print(f"Erro ao conectar-se ao servidor: {e}")

if __name__ == "__main__":
    username = input("Digite seu nome de usuário: ")
    client = ChatClient('localhost', 5555, username)
    client.connect()