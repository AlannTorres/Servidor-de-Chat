from multiprocessing import Process
import socket

HOST = 'localhost'
PORT = 5000

def resgate_mensage(client_socket):
    while True:
        print(client_socket.recv(1024).decode('utf-8'))

if __name__ == "__main__":
    nome_cliente = input("Digite seu nome: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(nome_cliente.encode('utf-8'))
    resgatar = Process(target=resgate_mensage, args=(client_socket,))
    resgatar.start()
    print("Info: Caso necessite de ajuda, digite -help")
    print("Chat inciado...")

    while True:
        mensagem = input("")
        client_socket.send(mensagem.encode('utf-8'))
