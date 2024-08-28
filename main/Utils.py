DOC = """
Comandos Disponíveis:

0. -exit
   - Desconectar do servidor.

1. -listarusuarios:  
   - Lista todos os usuários conectados ao servidor.

2. -criargrupo NOME_DO_GRUPO:  
   - Cria um novo grupo com o nome especificado.  
   - Erro: Caso o grupo já exista, será retornado: 
     "Error, grupo já existente"

3. -listargrupos:  
   - Lista todos os grupos disponíveis.  
   - Erro: Se não houver nenhum grupo cadastrado, será retornado: 
     "Erro, nenhum grupo cadastrado"

4. -listausrgrupo NOME_DO_GRUPO:  
   - Lista todos os usuários que fazem parte de um grupo específico.  
   - Erro: Caso o grupo especificado não exista, será retornado: 
     "Erro, grupo não cadastrado"

5. -entrargrupo NOME_DO_GRUPO:  
   - Entra no grupo especificado.  
   - Erro: Se o grupo não existir, será retornado: 
     "Erro, grupo não existe"

6. -sairgrupo NOME_DO_GRUPO:  
   - Sai do grupo especificado.  
   - Erro: Se o grupo não existir, será retornado: 
     "Erro, grupo não existe"

7. -msg ("U" para usuário ou "G" para grupo) NICK/GRUPO MENSAGEM:  
   - Envia uma mensagem para um usuário (U) ou para um grupo (G).  
   - A mensagem será formatada pelo servidor da seguinte forma: 
     (NICK, GRUPO, DATA/HORA) MENSAGEM

8. -msgt ("C" para todos os usuários online; "D" para desconectados; "T" para todos):  
   - Envia uma mensagem para todos os usuários online (C), desconectados (D) ou para todos os usuários (T).  
   - Exemplo: 
     -msgt C MENSAGEM


"""
