cad_usuario = {
    'idUsuario': [],
    'cpf': [],
    'nome': [],
    'dataNascimento': [],
    'endereco': []}
cad_conta = {
    'idConta': [],
    'numeroConta': [],
    'saldo': [],
    'extrato': [],
    'saquesEfetuados': [],
    'idUsuario': []}
LIMITE_PERMITIDO_PARA_SAQUES = 500
LIMITE_SAQUES = 3


def cadastrar_usuario() -> str:
    """
    Força a entrada de um cpf novo no banco de dados, quando é 
    satisfeito, requisita os outros dados.
    Salva em `cad_usuarios` e encerra com uma mensagem.

    :return: A mensagem de sucesso no armazenamento do usuário
    """
    while True:
        novo_cpf = str(input('Digite o CPF (somente números)'))
        cpf_valido, novo_cpf_f = validar_cpf(novo_cpf)
        if cpf_valido:
            break

    novo_nome = str(input('Digite o nome :')).title()
    nova_data_nasc = str(input('Digite a data de nascimento (formato, '
                               '"dd/mm/aaaa"):'))
    novo_logradouro = str(input('Digite o logradouro, abreviando o tipo, '
                                'seguido de uma vírgula e o número da '
                                'residencia:')).title()
    novo_bairro = str(input('Digite o nome do bairro:')).title()
    nova_cidade = str(input('Digite o nome do município:')).title()
    nova_uf = str(input('Digite a UF:')).upper()

    novo_endereco = (f'{novo_logradouro} - {novo_bairro} - {nova_cidade}/'
                     f'{nova_uf}')

    novo_id = len(cad_usuario['idUsuario']) + 1

    cad_usuario['idUsuario'].append(novo_id)
    cad_usuario['cpf'].append(novo_cpf_f)
    cad_usuario['nome'].append(novo_nome)
    cad_usuario['dataNascimento'].append(nova_data_nasc)
    cad_usuario['endereco'].append(novo_endereco)

    return f'Usuário nº{novo_id:04d} cadastrado com sucesso!'


def listar_usuarios(mascara=True) -> str:
    """
    Organiza os dados de todos usuários cadastrados em uma string, 
    sendo reservada uma linha por usuário.

    :return: a tabela dos usuários ou a mensagem de nenhum usuário
    """
    msg = ''
    for n in range(len(cad_usuario['idUsuario'])):
        if mascara:
            cpf_usuario = cad_usuario['cpf'][n][:3] + '.***.***-**'
        else:
            cpf_usuario = cad_usuario['cpf'][n]

        id_usuario = f"{cad_usuario['idUsuario'][n]:04d}"
        msg += (
            f"{id_usuario:>9} | "
            f"{cpf_usuario:>14} | "
            f"{cad_usuario['nome'][n][:20]:>20} [...] | "
            f"{cad_usuario['dataNascimento'][n]:>10} | "
            f"{cad_usuario['endereco'][n][:20]:>20} [...] | "
            f"{cad_conta['idUsuario'].count(cad_usuario['idUsuario'][n]):02d}\n"
        )

    if msg != '':
        msg = (
            f'IdUsuario_|_'
            f'CPF{"_"*12}|_'
            f'Nome{"_"*23}|_'
            f'DataNasc{"_"*3}|_'
            f'Endereco{"_"*19}|_'
            f'QuantContas\n' +
            msg
        )
        return msg.strip()

    else:
        return 'Nenhum usuários cadastrado.'


def abrir_conta(indice_usuario: int) -> str:
    """
    Recupera a instância de usuário que consta no indice passado e 
    instancia uma nova conta iterando os dados de identificação das
    contas e atribui os dados base de uma nova conta.

    :param indice_usuario: Posição referente aos dados do usuário
    :return: A mensagem de sucesso na abertura da conta
    """
    id_usuario = cad_usuario['idUsuario'][indice_usuario]
    nome_usuario = cad_usuario['nome'][indice_usuario]
    
    novo_id = len(cad_conta['idConta']) + 1
    novo_numero = f'0001-{novo_id:04d}'
    
    cad_conta['idConta'].append(novo_id)
    cad_conta['numeroConta'].append(novo_numero)
    cad_conta['saldo'].append(0)
    cad_conta['extrato'].append('')
    cad_conta['saquesEfetuados'].append(0)
    cad_conta['idUsuario'].append(id_usuario)
    
    return (f'Conta nº{novo_numero} do usuário {nome_usuario} aberta '
            f'com sucesso!')


def listar_contas_de(indice_usuario=-1) -> str:
    """
    Itera sobre o comprimento dos registros em `cad_usuario` e verifica
    se o usuario corresponde ao filtro quando solicitado ou qualquer 
    usuario quando não.
    
    :param indice_usuario: Posição referente aos dados do usuário
    :return: Os dados das contas cadastradas, formatados em linhas.
    """
    id_usuario = cad_usuario['idUsuario'][indice_usuario]
    msg = ''
    for n in range(len(cad_conta['idConta'])):
        id_usuario_conta_atual = cad_conta['idUsuario'][n]

        id_conta_f = f"{cad_conta['idConta'][n]:04d}"
        id_usuario_f = f"{cad_conta['idUsuario'][n]:04d}"

        saldo_conta = f'{cad_conta["saldo"][n]:.2f}'

        detalhe_conta = (
            f"{id_conta_f:>6}  | "
            f"{cad_conta['numeroConta'][n]:>10} | "
            f"{saldo_conta:>20} | "
            f"{cad_conta['saquesEfetuados'][n]:>12} | "
            f"{id_usuario_f}\n"
        )
        if indice_usuario != -1 and id_usuario == id_usuario_conta_atual:
            msg += detalhe_conta

        elif indice_usuario == -1:
            msg += detalhe_conta
            msg += f"{'-'*70}\nExtrato da conta: {cad_conta['numeroConta'][n]}\n"
            msg += imprimir_extrato(n)

    if msg != '':
        msg = (
            f'IdConta_|_'
            f'NumConta___|_'
            f'SaldoEmConta_________|_'
            f'SaquesEfet___|_'
            f'IdUsuario\n' +
            msg
        )
        return msg

    elif indice_usuario != -1:
        return "Este usuário não possui contas cadastradas."

    else:
        return "Não existe nenhuma conta cadastrada"


def validar_accesso_a_conta(num_conta: str, indice_usuario: int) -> tuple:
    """
    Cuida da verificação se a conta passada pertence ao usuario em 
    sessão.

    :param num_conta: O valor entrado via teclado pelo usuário
    :param indice_usuario: Posição referente aos dados do usuário
    :return resposta: O código de autorização referente à conferência
    :return indice_conta: Posição referente aos dados da conta
    """
    try:
        indice_conta = cad_conta['numeroConta'].index(num_conta)
        id_usuario = cad_usuario['idUsuario'][indice_usuario]
        id_usuario_conta = cad_conta['idUsuario'][indice_conta]
        if id_usuario == id_usuario_conta:
            # Sucesso na autorização
            resposta = 1

        else:
            # Falha na autorização
            resposta = 0
            indice_conta = -1

    except ValueError:
        # Erro na autorização
        resposta = -1
        indice_conta = -1

    return resposta, indice_conta


def login_conta(indice_usuario: int) -> int:
    """
    Cuida do acesso ao usuário, solicitando identificação e validando 
    a mesma.

    :param indice_usuario: Posição referente aos dados do usuário
    :return indice_conta: Posição referente aos dados da conta
    """
    indice_conta = -1
    MENSAGEM_ENTRAR_EM_CONTA = (
        'Me diga o número da agência e da conta (formato, "0000-0000"); ou\n'
        'digite "s" para voltar ao menu do usuário.\n'
        'Operação =>'
    )
    while True:
        numero_conta = input(MENSAGEM_ENTRAR_EM_CONTA)
        if numero_conta == 's':
            print('Voltando ao menu do usuário.')
            break

        validacao, indice_conta = validar_accesso_a_conta(
            numero_conta, indice_usuario
            )
        if validacao == 1:
            print('Acesso autorizado!')
            break

        elif validacao == 0:
            print('Operação inválida! Acesso negado.')

        elif validacao == -1:
            print('Operação inválida! Esta conta não existe.')

        else:
            print('Erro! Não foi possível prosseguir.')

    return indice_conta


def sessao_conta(indice_usuario: int) -> None:
    """
    Cuida da iteração do acesso a um usuário à conta e suas operações.

    :param indice_usuario: Posição referente aos dados do usuário
    """
    indice_conta = login_conta(indice_usuario)
    MENU_CONTA = (
        'Operando em conta nº{}\n'
        '[d] - Depositar em Conta\n'
        '[s] - Sacar da Conta\n'
        '[e] - Exibir Extrato\n'
        '[q] - Sair da Conta\n'
        'Operação =>'
    )
    if indice_conta >= 0:
        while True:
            operacao = input(MENU_CONTA.format(
                cad_conta['numeroConta'][indice_conta])
            )
            if operacao == 'd':
                valor_deposito = float(input("Valor do depósito:"))
                if valor_deposito > 0:
                    print(depositar_em_conta(indice_conta, valor_deposito))

            elif operacao == 's':
                valor_saque = float(input("Valor do saque:"))
                if valor_saque > 0:
                    print(sacar_de_conta(indice_conta, valor_saque))

            elif operacao == 'e':
                imprimir_extrato(indice_conta)

            elif operacao == 'q':
                print('Saindo da conta.')
                break

            else:
                print('Operação inválida, por favor selecione novamente a '
                      'operação desejada.')


def depositar_em_conta(indice_conta: int, valor: float) -> str:
    """
    Atualiza os dados da conta referentes a um depósito, saldo e 
    extrato.

    :param indice_conta: Posição referente aos dados da conta
    :param valor: O valor que se deseja depositar em conta
    :return: A mensagem de sucesso no depósito em conta
    """
    numero_conta = cad_conta['numeroConta'][indice_conta]
    cad_conta['saldo'][indice_conta] += valor
    cad_conta['extrato'][indice_conta] += f'+{valor:.2f}_'
    return (f'Depósito de R${valor:.2f} na conta {numero_conta} realizado com '
            f'sucesso!')


def sacar_de_conta(indice_conta: int, valor: float) -> str:
    """
    Confere se o valor passado é válido e retorna a mensagem 
    correspondente.
    Quando o valor é valido, atualiza os dados referentes ao saque.

    :param indice_conta: Posição referente aos dados da conta
    :param valor: O valor que se deseja sacar da conta
    :return: Mensagem de sucesso ou falha do saque
    """
    saldo_conta = cad_conta['saldo'][indice_conta]
    saques_efetuados = cad_conta['saquesEfetuados'][indice_conta]

    if saldo_conta < valor:
        msg = 'Operação Inválida! O valor em conta não permite este saque.'

    elif valor > LIMITE_PERMITIDO_PARA_SAQUES:
        msg = ('Operação Inválida! O valor desejado ultrapassa o limite '
               'permitido.')

    elif saques_efetuados == LIMITE_SAQUES:
        msg = ('Operação Inválida! Vocâ já realizou o limite de saques '
               'permitidos para o dia de hoje.')

    else:
        numero_conta = cad_conta['numeroConta'][indice_conta]
        cad_conta['saldo'][indice_conta] -= valor
        cad_conta['saquesEfetuados'][indice_conta] += 1
        cad_conta['extrato'][indice_conta] += f'-{valor:.2f}_'
        msg = (f'Saque de R${valor:.2f} da conta {numero_conta} realizado com '
               f'sucesso!')

    return msg


def imprimir_extrato(indice_conta: int) -> str:
    """
    Lê os dados contidos no extrato referênte e formata-o de acordo.

    :param indice_conta: Posição referente aos dados da conta
    :return: A lista vazia ou com as operações.
    """
    saldo = cad_conta['saldo'][indice_conta]
    try:
        extrato = cad_conta['extrato'][indice_conta].split('_')
        msg = ''
        for linha in extrato:
            if '+' in linha or '-' in linha:
                sinal = linha[0]
                valor = linha[1:]
                msg += f'\t  R$ {sinal} {valor:>32}\n'
    except IndexError:
        msg = ''

    if msg == '':
        msg += '\tNão houveram movimentações para esta conta.\n'

    msg += '-' * 70
    msg += '\n\t  R$   {:>32}\t\tTOTAL\n'.format(f'{saldo:.2f}')

    return msg


def salvar_dados() -> None:
    """
    Salva em arquivo os dados obtidos na sessão.
    """
    with open('banco_de_dados.txt', 'w+', encoding='utf-8') as arquivo:
        arquivo.write("usuarios\n")
        for u in range(len(cad_usuario['idUsuario'])):
            dados_usuario = (
                f"{cad_usuario['idUsuario'][u]};"
                f"{cad_usuario['cpf'][u]};"
                f"{cad_usuario['nome'][u]};"
                f"{cad_usuario['dataNascimento'][u]};"
                f"{cad_usuario['endereco'][u]}\n"
            )
            arquivo.write(dados_usuario)

        arquivo.write("contas\n")
        for c in range(len(cad_conta['idConta'])):
            dados_conta = (
                f"{cad_conta['idConta'][c]};"
                f"{cad_conta['numeroConta'][c]};"
                f"{cad_conta['saldo'][c]};"
                f"{cad_conta['extrato'][c]};"
                f"{cad_conta['saquesEfetuados'][c]};"
                f"{cad_conta['idUsuario'][c]}\n"
            )
            arquivo.write(dados_conta)

        print("Dados salvos com sucesso!")


def ler_banco_de_dados() -> None:
    """
    Acessa o arquivo onde estão salvos os dados da ultima sessão
    e instancia os dados para seus respectivos objetos.
    """
    try:
        with open('banco_de_dados.txt', 'r', encoding='utf-8') as arquivo:
            alvo = ''
            for linha in arquivo:
                if ';' not in linha:
                    alvo = linha.strip()

                else:
                    if alvo == 'usuarios':
                        dados_usuario = linha.split(';')
                        cad_usuario['idUsuario'].append(int(
                            dados_usuario[0].strip()
                            ))
                        cad_usuario['cpf'].append(
                            dados_usuario[1].strip()
                            )
                        cad_usuario['nome'].append(
                            dados_usuario[2].strip()
                            )
                        cad_usuario['dataNascimento'].append(
                            dados_usuario[3].strip()
                            )
                        cad_usuario['endereco'].append(
                            dados_usuario[4].strip()
                            )

                    elif alvo == 'contas':
                        dados_conta = linha.split(';')
                        cad_conta['idConta'].append(int(
                            dados_conta[0].strip()
                            ))
                        cad_conta['numeroConta'].append(
                            dados_conta[1].strip()
                            )
                        cad_conta['saldo'].append(float(
                            dados_conta[2].strip()
                            ))
                        cad_conta['extrato'].append(
                            dados_conta[3].strip()
                            )
                        cad_conta['saquesEfetuados'].append(int(
                            dados_conta[4].strip()
                            ))
                        cad_conta['idUsuario'].append(int(
                            dados_conta[5].strip()
                            ))

    except FileNotFoundError:
        pass


def sessao_usuario() -> None:
    """
    Cuida do acesso do usuário, validando login e operações.
    """
    indice_usuario = -1
    MENSAGEM_LOGIN = (
        'Identifique-se com:\n'
        'CPF (insira pontos e traço); ou\n'
        'digite "s" para voltar ao menu do sistema\n'
        'Operação =>'
    )

    while True:
        forma_login = input(MENSAGEM_LOGIN)
        if forma_login == 's':
            print('Retornando ao menu do sistema.')
            break
        elif forma_login in cad_usuario['cpf']:
            indice_usuario = cad_usuario['cpf'].index(forma_login)
            break
        else:
            print('CPF não cadastrado! Por favor, tente novamente.')

    MENU_USUARIO = (
        'Logado em usuário de CPF {}\n'
        '[n] - Abrir Nova Conta\n'
        '[e] - Entrar em Conta\n'
        '[c] - Listar Contas do Usuário\n'
        '[q] - Sair do Usuário\n'
        'Operação =>'
    )
    if indice_usuario >= 0:
        while True:
            operacao = input(MENU_USUARIO.format(
                cad_usuario['cpf'][indice_usuario]
                ))
            if operacao == 'n':
                print(abrir_conta(indice_usuario))

            elif operacao == 'e':
                sessao_conta(indice_usuario)

            elif operacao == 'c':
                print(listar_contas_de(indice_usuario))

            elif operacao == 'q':
                print('Retornando ao menu do sistema.')
                break

            else:
                print('Operação inválida, por favor selecione novamente a '
                      'operação desejada.')


def sessao_sistema() -> None:
    """
    Cuida do menu do sistema e as operações padrão do sistema.
    """
    MENU_SISTEMA = (
        '[n] - Cadastrar Novo Usuário\n'
        '[e] - Entrada Usuário\n'
        '[l] - Listar Usuários\n'
        '[q] - Sair do sistema\n'
        'Operação =>'
    )
    ler_banco_de_dados()
    while True:
        operacao = input(MENU_SISTEMA)
        if operacao == 'n':
            print(cadastrar_usuario())
        elif operacao == 'e':
            sessao_usuario()
        elif operacao == 'l':
            print(listar_usuarios())
        elif operacao == 'q':
            print('Saindo do Sistema')
            salvar_dados()
            break
        else:
            if operacao == 'debug_contas':
                print(listar_contas_de())
            elif operacao == 'debug_usuarios':
                print(listar_usuarios(False))
            else:
                print('Operação inválida, por favor selecione novamente a '
                      'operação desejada.')


def validacao_calculada_de_cpf(combinacao: str) -> bool:
    """
    Validação de duas etapas para confiarmar a validade da combinação
    de números
    """
    calc_cpf = 0
    c = 10
    for n in range(9):
        calc_cpf += int(combinacao[n]) * c
        c -= 1

    ver_digito_a = ((calc_cpf * 10) % 11) == int(combinacao[9])
    calc_cpf = 0
    c = 11
    for n in range(10):
        calc_cpf += int(combinacao[n]) * c
        c -= 1

    ver_digito_b = ((calc_cpf * 10) % 11) == int(combinacao[10])

    return ver_digito_a and ver_digito_b


def validar_cpf(cpf_usuario: str) -> tuple:
    """
    Verifica se o valor satisfaz as diretrizes do sistema para um CPF
    válido.

    :param cpf_usuario: A combinação de números que representa o cpf
    :return [0]: Valor booleano do sucesso na verificação
    :return [1]: O CPF formatado com pontos após o terceiro e sexto
    número, e o traço do dígito
    """
    if not cpf_usuario.isnumeric():
        print('Operação Inválida! A combinação passada contém um ou mais '
              'caracteres não permitidos.')
        return False, 0
    if len(cpf_usuario) != 11:
        print('Operação Inválida! A combinação passada não tem o comprimento '
              'normal de um CPF (11 caractéres).')

    else:
        novo_cpf_f = (
            f'{cpf_usuario[:3]}.'
            f'{cpf_usuario[3:6]}.'
            f'{cpf_usuario[6:9]}-'
            f'{cpf_usuario[9:]}'
        )
        if novo_cpf_f in cad_usuario['cpf']:
            print('O CPF passado já consta vinculado a outro usuário nos cadastros')

        elif validacao_calculada_de_cpf(cpf_usuario):
            return True, novo_cpf_f

        else:
            print('Operação inválida! A combinação passada não é um CPF válido.')
            return False, 0


if __name__ == '__main__':
    sessao_sistema()
