from multiprocessing import Process, Manager
from datetime import datetime
from Group import *
import socket

def store_message(destinatario, mensagem, pending_messages):
    """Armazena mensagens para usuários offline."""
    if destinatario in pending_messages:
        pending_messages[destinatario].append(mensagem)
    else:
        pending_messages[destinatario] = [mensagem]

def conection_client(nome_cliente, client_socket, client_address, clientes_on, clientes_off, groups, pending_messages):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        if data.lower() == 'exit':
            clientes_on.pop(client_address)
            clientes_off.append(nome_cliente)
            return client_socket.close()
        elif data.startswith('-criargrupo'):
            group_name = data.split()[1]
            response = create_group(group_name, groups)
            client_socket.send(response.encode('utf-8'))

        elif data.startswith('-listargrupos'):
            response = list_groups(groups)
            client_socket.send(str(response).encode('utf-8'))

        elif data.startswith('-listausrgrupo'):
            group_name = data.split()[1]
            response = list_users_groups(group_name, groups)
            client_socket.send(str(response).encode('utf-8'))

        elif data.startswith('-entrargrupo'):
            group_name = data.split()[1]
            response = join_group(group_name, groups, nome_cliente)
            client_socket.send(response.encode('utf-8'))

        elif data.startswith('-sairgrupo'):
            group_name = data.split()[1]
            response = leave_group(group_name, groups, nome_cliente)
            client_socket.send(response.encode('utf-8'))

        elif data.startswith('-msg'):
            parts = data.split(' ', 3)
            if len(parts) < 3:
                client_socket.send("Uso: -msg <U/G> <NICK/GRUPO> <mensagem>".encode('utf-8'))
                continue
            tipo_destinatario, destinatario, mensagem = parts[1], parts[2], parts[3]
            mensagem_formatada = f"({nome_cliente}, {destinatario}, {now}) {mensagem}"

            if tipo_destinatario == 'U':
                destinatario_socket = None
                for addr, (cliente, sock) in clientes_on.items():
                    if cliente == destinatario:
                        destinatario_socket = sock
                        break

                if destinatario_socket:
                    destinatario_socket.send(mensagem_formatada.encode('utf-8'))
                else:
                    store_message(destinatario, mensagem_formatada, pending_messages)
                    client_socket.send("Mensagem armazenada para entrega posterior.".encode('utf-8'))

            elif tipo_destinatario == 'G':
                if destinatario in groups:
                    for member in groups[destinatario]:
                        if member in [cliente for _, (cliente, _) in clientes_on.items()]:
                            for addr, (cliente, sock) in clientes_on.items():
                                if cliente == member:
                                    sock.send(mensagem_formatada.encode('utf-8'))
                        else:
                            store_message(member, mensagem_formatada, pending_messages)
                    client_socket.send(f"Mensagem enviada para o grupo {destinatario}.".encode('utf-8'))
                else:
                    client_socket.send("Grupo não encontrado.".encode('utf-8'))

        elif data.startswith('-msgt'):
            parts = data.split(' ', 2)
            if len(parts) < 3:
                client_socket.send("Uso: -msgt <C/D/T> <mensagem>".encode('utf-8'))
                continue

            tipo_mensagem, mensagem = parts[1], parts[2]
            mensagem_formatada = f"({nome_cliente}, {now}) {mensagem}"

            if tipo_mensagem == 'C':  # Para todos os usuários conectados
                for addr, (cliente_local, socket_cliente_local) in clientes_on.items():
                    if addr != client_address:
                        socket_cliente_local.send(mensagem_formatada.encode('utf-8'))

            elif tipo_mensagem == 'D':  # Para todos os usuários offline
                for cliente in clientes_off:
                    store_message(cliente, mensagem_formatada, pending_messages)
                client_socket.send("Mensagem enviada para usuários offline.".encode('utf-8'))

            elif tipo_mensagem == 'T':  # Para todos os usuários (online e offline)
                for addr, (cliente_local, socket_cliente_local) in clientes_on.items():
                    socket_cliente_local.send(mensagem_formatada.encode('utf-8'))

                for cliente in clientes_off:
                    store_message(cliente, mensagem_formatada, pending_messages)

                client_socket.send("Mensagem enviada para todos os usuários.".encode('utf-8'))

        # Verifica se o cliente tem mensagens pendentes
        if nome_cliente in pending_messages:
            for msg in pending_messages[nome_cliente]:
                client_socket.send(msg.encode('utf-8'))
            pending_messages.pop(nome_cliente)


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5000

    with Manager() as manager:
        CLIENTES_OFFLINE = manager.list()
        CLIENTES_CONNECT = manager.dict()
        GROUPS = manager.dict()
        PENDING_MESSAGES = manager.dict()

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
            elif nome_cliente in [nome for _, nome in CLIENTES_CONNECT.values()]:
                client_socket.send("Erro: Usuário já conectado.".encode('utf-8'))
                client_socket.close()
                continue

            CLIENTES_CONNECT[client_address] = (nome_cliente, client_socket)
            client_process = Process(target=conection_client, args=(
                nome_cliente, client_socket, client_address, CLIENTES_CONNECT, CLIENTES_OFFLINE, GROUPS, PENDING_MESSAGES))
            print(f"Cliente {nome_cliente} conectado de {client_address}")
            print(f'clientes on --> {CLIENTES_OFFLINE }')
            print(f'clientes off --> {CLIENTES_CONNECT }')
            client_process.start()
