# Desafio de Projeto 2 da Formação Python Developer da DIO
## Autor: Thiago Daniel Pessoa

O desafio de projeto sugere que seja melhorado o sistema desenvolvido no desafio 1 acrescentando novas operações à lista e, utilizando de funções, organize as ações do código.  
### As novas operações propostas e acrescentadas foram:
+ Cadastrar usuário (aka. titulares de contas);
+ Listar os usuários cadastrados;
+ Se identificar como um dos usuários;
+ Abrir conta no nome do usuário; 
+ Listar as contas cadastradas; e
+ Acessar as operações para movimentações e extrato de uma conta.  
### Acrescentei algumas funcionalidades para comodidade:
+ A operação no menu principal que lista os usuários oculta informações privilegiadas (CPF), o qual é necessário para a identificação (só é necessário digitar um dos CPFs cadastrados). 
+ Para facilitar correções, se digitado `debug_usuarios`, serão listados os usuários da mesma forma, porém sem o ocultamento das informações;
+ O acesso às operações da conta também necessita que seja digitado a agência e conta desejada, mas só é permitido acesso se a conta pertencer ao usuário identificado anteriormente;
+ Todas as formas de listar os dados é dada por formatação do texto em colunas;
+ Os dados da sessão são salvos em arquivo `.txt` quando devidamente encerrada; e
+ Quando o arquivo de dados (`BancoDeDados.txt`) existir, a sessão será retomada como anteriormente salva.
## Das funções:
### cadastrar_usuario() -> str:  
    Força a entrada de um cpf válido para o banco de dados, quando é 
    satisfeito, requisita os outros dados.
    Salva em `cad_usuarios` e encerra com uma mensagem.

    :return: A mensagem de sucesso no armazenamento do usuário
### listar_usuarios(mascara=True) -> str:  
    Organiza os dados de todos usuários cadastrados em uma string, 
    sendo reservada uma linha por usuário.

    :return: a tabela dos usuários ou a mensagem de nenhum usuário
### abrir_conta(indice_usuario: int) -> str:
    Recupera a instância de usuário que consta no indice passado e 
    instancia uma nova conta iterando os dados de identificação das
    contas e atribui os dados base de uma nova conta.

    :param indice_usuario: Posição referente aos dados do usuário
    :return: A mensagem de sucesso na abertura da conta
### listar_contas_de(indice_usuario=-1) -> str:
    Itera sobre o comprimento dos registros em `cad_usuario` e verifica
    se o usuario corresponde ao filtro quando solicitado ou qualquer 
    usuario quando não.
    
    :param indice_usuario: Posição referente aos dados do usuário
    :return: Os dados das contas cadastradas, formatados em linhas.
### validar_accesso_a_conta(num_conta: str, indice_usuario: int) -> tuple:
    Cuida da verificação se a conta passada pertence ao usuario em 
    sessão.

    :param num_conta: O valor entrado via teclado pelo usuário
    :param indice_usuario: Posição referente aos dados do usuário
    :return resposta: O código de autorização referente à conferência
    :return indice_conta: Posição referente aos dados da conta
### login_conta(indice_usuario: int) -> int:
    Cuida do acesso ao usuário, solicitando identificação e validando 
    a mesma.

    :param indice_usuario: Posição referente aos dados do usuário
    :return indice_conta: Posição referente aos dados da conta
### sessao_conta(indice_usuario: int) -> None:
    Cuida da iteração do acesso a um usuário à conta e suas operações.

    :param indice_usuario: Posição referente aos dados do usuário
### depositar_em_conta(indice_conta: int, valor: float) -> str:
    Atualiza os dados da conta referentes a um depósito, saldo e 
    extrato.

    :param indice_conta: Posição referente aos dados da conta
    :param valor: O valor que se deseja depositar em conta
    :return: A mensagem de sucesso no depósito em conta
### sacar_de_conta(indice_conta: int, valor: float) -> str:
    Confere se o valor passado é válido e retorna a mensagem 
    correspondente.
    Quando o valor é valido, atualiza os dados referentes ao saque.

    :param indice_conta: Posição referente aos dados da conta
    :param valor: O valor que se deseja sacar da conta
    :return: Mensagem de sucesso ou falha do saque
### imprimir_extrato(indice_conta: int) -> str:
    Lê os dados contidos no extrato referênte e formata-o de acordo.

    :param indice_conta: Posição referente aos dados da conta
    :return: A lista vazia ou com as operações.
### salvar_dados() -> None:
    Salva em arquivo os dados obtidos na sessão.
### ler_banco_de_dados() -> None:
    Acessa o arquivo onde estão salvos os dados da ultima sessão
    e instancia os dados para seus respectivos objetos.
### sessao_usuario() -> None:
    Cuida do acesso do usuário, validando login e operações.
### sessao_sistema() -> None:
    Cuida do menu do sistema e as operações padrão do mesmo.
