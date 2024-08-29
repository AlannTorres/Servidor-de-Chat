from multiprocessing import Process, Manager
from datetime import datetime
from Group import *
from Utils import DOC
import socket

def store_message(destinatario, mensagem, pending_messages):
    if destinatario in pending_messages:
        pending_messages[destinatario].append(mensagem)
    else:
        pending_messages[destinatario] = [mensagem]

# Processo em andamento
def conection_client(nome_cliente, client_socket, client_address, clientes_on, clientes_off, groups, pending_messages):
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Solicitar informações sobre o comando
        if data.startswith('-help'):
            client_socket.send(DOC.encode('utf-8'))

        # Listar usuarios
        elif data.startswith('-listarusuarios'):
            if clientes_on:
                usuarios_conectados = "\n".join(clientes_on.keys())
                client_socket.send(f"Usuários conectados:\n{usuarios_conectados}".encode('utf-8'))
            else:
                client_socket.send("Nenhum usuário conectado no momento.".encode('utf-8'))
        
        # Desconectar do servidor
        elif data.startswith('-exit'):
            clientes_on.pop(nome_cliente)
            clientes_off.append(nome_cliente)
            print(f"Usuario: {nome_cliente} desconectou")
            return(client_socket.close())
            
        # Criar Grupos
        elif data.startswith('-criargrupo'):
            group_name = data.split()[1]
            response = create_group(group_name, groups)
            client_socket.send(response.encode('utf-8'))

        # Listar Grupos
        elif data.startswith('-listargrupos'):
            response = list_groups(groups)
            client_socket.send(str(response).encode('utf-8'))
            
        # Listar usuarios de um grupo
        elif data.startswith('-listausrgrupo'):
            group_name = data.split()[1]
            response = list_users_groups(group_name, groups)
            client_socket.send(str(response).encode('utf-8'))

        # Entrar em um grupo
        elif data.startswith('-entrargrupo'):
            group_name = data.split()[1]
            response = join_group(group_name, groups, nome_cliente)
            client_socket.send(response.encode('utf-8'))

        # Sair de um grupo
        elif data.startswith('-sairgrupo'):
            group_name = data.split()[1]
            response = leave_group(group_name, groups, nome_cliente)
            client_socket.send(response.encode('utf-8'))

        # Enviar MSG para todos os usuario (Online ou Offline)
        elif data.startswith('-msgt'):
            parts = data.split(' ', 2)
            if len(parts) < 3:
                client_socket.send("Uso: -msgt <C/D/T> <mensagem>".encode('utf-8'))
                continue

            tipo_mensagem, mensagem = parts[1], parts[2]
            mensagem_formatada = f"({nome_cliente}, {now}) {mensagem}"

            # Para todos os usuários conectados
            if tipo_mensagem == 'C':  
                for cliente_local, (addr, socket_cliente_local) in clientes_on.items():
                    if addr != client_address:
                        socket_cliente_local.send(mensagem_formatada.encode('utf-8'))

            # Para todos os usuários offline
            elif tipo_mensagem == 'D':  
                for cliente in clientes_off:
                    store_message(cliente, mensagem_formatada, pending_messages)
                client_socket.send("Mensagem enviada para usuários offline.".encode('utf-8'))

            # Para todos os usuários (online e offline)
            elif tipo_mensagem == 'T':  
                for cliente_local, (addr, socket_cliente_local) in clientes_on.items():
                    socket_cliente_local.send(mensagem_formatada.encode('utf-8'))

                for cliente in clientes_off:
                    store_message(cliente, mensagem_formatada, pending_messages)

                client_socket.send("Mensagem enviada para todos os usuários.".encode('utf-8'))

        # Enviar MSG para os usuario ou grupos especificos (Online ou Offline)
        elif data.startswith('-msg'):
            parts = data.split(' ', 3)
            if len(parts) < 3:
                client_socket.send("Uso: -msg <U/G> <NICK/GRUPO> <mensagem>".encode('utf-8'))
                continue
            tipo_destinatario, destinatario, mensagem = parts[1], parts[2], parts[3]
            mensagem_formatada = f"({nome_cliente}, {destinatario}, {now}) {mensagem}"

            # Para um usuario especifico
            if tipo_destinatario == 'U':
                destinatario_socket = None
                for cliente, (addr, sock) in clientes_on.items():
                    if cliente == destinatario:
                        destinatario_socket = sock
                        break
                if destinatario_socket:
                    destinatario_socket.send(mensagem_formatada.encode('utf-8'))
                else:
                    store_message(destinatario, mensagem_formatada, pending_messages)
                    client_socket.send("Mensagem armazenada para entrega posterior.".encode('utf-8'))

            # Para um grupo especifico
            elif tipo_destinatario == 'G':
                if destinatario in groups:
                    for member in groups[destinatario]:
                        if member != nome_cliente:
                            if member in clientes_on:
                                clientes_on[member][1].send(mensagem_formatada.encode('utf-8'))
                            else:
                                store_message(member, mensagem_formatada, pending_messages)
                    client_socket.send(f"Mensagem enviada para o grupo {destinatario}.".encode('utf-8'))
                else:
                    client_socket.send("Grupo não encontrado.".encode('utf-8'))

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
                client_socket.send(f"Cliente {nome_cliente} foi restaurado.".encode('utf-8'))
                if nome_cliente in PENDING_MESSAGES:
                    print("Mensagens restauradas:")
                    for msg in PENDING_MESSAGES[nome_cliente]:
                        client_socket.send(msg.encode('utf-8'))
                    PENDING_MESSAGES.pop(nome_cliente)
            elif nome_cliente in CLIENTES_CONNECT.keys():
                print("Erro: Usuário já conectado.")
                client_socket.send("Erro: Usuário já conectado.".encode('utf-8'))
                client_socket.close()
                continue

            CLIENTES_CONNECT[nome_cliente] = (client_address, client_socket)
            client_process = Process(target=conection_client, args=(
                nome_cliente, 
                client_socket, 
                client_address, 
                CLIENTES_CONNECT, 
                CLIENTES_OFFLINE, 
                GROUPS, 
                PENDING_MESSAGES))
            
            
            print(f"Cliente {nome_cliente} conectado de {client_address}")
            client_process.start()
