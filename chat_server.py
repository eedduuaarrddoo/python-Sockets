import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor de chat iniciado em {self.host}:{self.port}")

    def handle_client(self, client_socket, addr):
        print(f"Conexão estabelecida com {addr}")
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Mensagem de {addr}: {message}")
                
                if message.startswith("/exit"):
                    exit_username = message.split()[1]
                    self.broadcast(f"{exit_username} saiu do chat")
                    break
                
                self.broadcast(message)

        except Exception as e:
            print(f"Erro durante a comunicação com {addr}: {e}")

        finally:
            client_socket.close()
            print(f"Conexão encerrada com {addr}+{exit_username}")

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar mensagem para cliente: {e}")
        self.clients = [client for client in self.clients if client.fileno() != -1]

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == "__main__":
    server = ChatServer('localhost', 5555)
    server.start()