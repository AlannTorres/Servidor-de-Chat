from multiprocessing import Process, Manager
import socket
from Group import *


def conection_client(nome_cliente, client_socket, client_address, clientes_on, clientes_off, groups):
    while True:
        print("aquiii 1 -- ")
        data = client_socket.recv(1024).decode('utf-8')
        if data.lower() == "exit":
            clientes_on.pop(client_address)
            clientes_off.append(nome_cliente)
            return client_socket.close()
        elif data.startswith("criargrupo"):
            print("aquiii 2 -- cri")
            client_name = data.split()[1]
            answer = create_group(client_name, groups)
            client_socket.send(answer.encode('utf-8'))
            return
        else:
            pass
        mensagem = f"{nome_cliente}: {data}"
        print(clientes_on)
        print(clientes_off)
        print(f"Cliente {nome_cliente} conectado de {client_address}")
        for address_local, socket_cliente_local in clientes_on.items():
            if address_local != client_address:
                socket_cliente_local.send(mensagem.encode('utf-8'))


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000

    with Manager() as manager:
        CLIENTES_OFFLINE = manager.list()
        CLIENTES_CONNECT = manager.dict()
        GROUPS = manager.dict()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor ouvindo em {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            nome_cliente = client_socket.recv(1024).decode('utf-8')

            if nome_cliente in CLIENTES_OFFLINE:
                CLIENTES_OFFLINE.remove(nome_cliente)
                print(f"Cliente {nome_cliente} foi restaurado.")

            for client in CLIENTES_CONNECT:
                if client == nome_cliente:
                    CLIENTES_OFFLINE.remove(client)
                print(f"Cliente {nome_cliente} foi restaurado.")

            CLIENTES_CONNECT[client_address] = client_socket
            client_process = Process(target=conection_client, args=(nome_cliente, client_socket, client_address, CLIENTES_CONNECT, CLIENTES_OFFLINE, GROUPS))
            client_process.start()
