# Chat Server

## Descrição

Este projeto implementa um servidor de chat que permite comunicação entre usuários e grupos de usuários de maneira personalizada. O servidor suporta funcionalidades de criação e gerenciamento de grupos, envio de mensagens individuais e em grupo, e entrega de mensagens quando um usuário que estava offline se reconectar.

## Funcionalidades

### 1. Conexão e Autenticação

- Ao se conectar ao servidor, o cliente deve informar seu **nickname**.
- Caso o nickname já esteja em uso, o servidor retornará um erro: `Error, Usuário já conectado`.

### 2. Comandos Disponíveis

Os comandos a seguir estão disponíveis para interação com o servidor:

#### -help
- Exibe a lista de todos os comandos do servidor.

#### -exit
- Desconectar usuario do servidor.

#### -listarusuarios
- Exibe a lista de todos os usuários conectados.

#### -criargrupo
- Cria um novo grupo.
- Sintaxe: `-criargrupo NOME_DO_GRUPO`.
- Se o grupo já existir, o servidor retorna o erro: `Error, grupo já existente`.

#### -listargrupos
- Exibe a lista de todos os grupos criados.
- Sintaxe: `-listargrupos`.
- Se não houver grupos cadastrados, o servidor retorna o erro: `Erro, nenhum grupo cadastrado`.

#### -listausrgrupo
- Lista todos os usuários pertencentes a um grupo específico.
- Sintaxe: `-listausrgrupo NOME_DO_GRUPO`.
- Se o grupo não estiver cadastrado, o servidor retorna o erro: `Erro, grupo não cadastrado`.

#### -entrargrupo
- Permite que o usuário entre em um grupo existente.
- Sintaxe: `-entrargrupo NOME_GRUPO`.
- Se o grupo não existir, o servidor retorna o erro: `Erro grupo não existe`.

#### -sairgrupo
- Permite que o usuário saia de um grupo.
- Sintaxe: `-sairgrupo NOME_GRUPO`.
- Se o grupo não existir, o servidor retorna o erro: `Erro grupo não existe`.

#### -msg
- Envia uma mensagem para um usuário específico ou grupo.
- Sintaxe: `-msg "U" NICK MENSAGEM` ou `-msg "G" NOME_DO_GRUPO MENSAGEM`.
- **Nota:** Caso o usuário ou grupo esteja offline, a mensagem será armazenada e enviada quando o usuário ficar online.

#### -msgt
- Envia uma mensagem para todos os usuários conectados ou desconectados.
- Sintaxe: `-msgt "C" MENSAGEM` (para todos os usuários conectados) ou `-msgt "D" MENSAGEM` (para todos os usuários desconectados).
- É possível também enviar para **todos os usuários** conectados e desconectados com o comando `-msgt "T" MENSAGEM`.

### 3. Tratamento de Mensagens

- Mensagens enviadas para usuários desconectados serão armazenadas no servidor e entregues quando o usuário se reconectar.
  
## Requisitos

- **Linguagem de Programação:** Python (ou linguagem preferida para sockets)
- **Bibliotecas:** Pode ser necessário utilizar bibliotecas como `socket`, `threading`, etc., para a implementação do servidor e cliente.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/chat-server.git
   ```

2. Execute o servidor:
   ```bash
   python servidor.py
   ```

3. Execute o cliente em outra instância:
   ```bash
   python cliente.py
   ```

### Notas Importantes

- O servidor deve rodar continuamente para suportar a conexão e comunicação dos clientes.
- O nickname de cada usuário deve ser único para evitar conflitos de identificação.
