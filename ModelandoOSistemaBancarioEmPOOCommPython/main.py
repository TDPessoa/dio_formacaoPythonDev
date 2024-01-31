"""Código desenvolvido para obtenção de progresso na plataforma DIO, no
curso Formação Python Developer."""
from abc import ABC, abstractmethod


class Transacao(ABC):
    @abstractmethod
    def __init__(self):
        """
        Classe abstrata para as classes que representam uma transação
        dentro do sistema bancário.
        """
        self.tipo: str
        self.valor: float


class Saque(Transacao):
    def __init__(self, valor: float):
        self.tipo = '-'
        self.valor = valor


class Deposito(Transacao):
    def __init__(self, valor: float):
        self.tipo = '+'
        self.valor = valor


class Cliente:
    def __init__(self):
        """
        Classe "pai" que representa um cliente dentro do sistema bancário.
        """
        self.contas = []
        self.endereco = ''

    @staticmethod
    def solicitar_endereco() -> str:
        """
        Requisita o endereço do cliente separadamente e devolve em uma
        unica str.
        """
        print("Agora ao seu endereço ...")
        novo_logradouro = str(input(
            'Digite o logradouro, abreviando o tipo, seguido de uma vírgula e o '
            'número da residencia:'
        )).title()
        novo_bairro = str(input('Digite o nome do bairro:')).title()
        nova_cidade = str(input('Digite o nome do município:')).title()
        nova_uf = str(input('Digite a UF:')).upper()

        return (
            f'{novo_logradouro} - {novo_bairro} - {nova_cidade}/{nova_uf}'
        )

    def listar_contas(self):
        """
        Corre pela lista de contas do cliente e retorna uma lista em
        formato de tabela com as variáveis de cada conta ou um aviso,
        se o cliente não possuir contas abertas.
        """
        mensagem = ''
        for conta in self.contas:
            mensagem += conta + '\n'
        if mensagem == '':
            print('O cliente em sessão não possui contas abertas.')
        else:
            print("Número Agência | Número Conta | Saldo")
            print(mensagem)


class PessoaFisica(Cliente):
    def __init__(self, usuario=True, cpf=''):
        """
        Classe que representa um cliente de natureza física dentro do
        sistema.

        :param usuario: Booleano que indica se a criação está sendo
        realizada pelo usuário.
        :param cpf: String validada pelo objeto BancoDeDados
        """
        super().__init__()
        if usuario:
            self.criacao_por_usuario(cpf)
        else:
            self.cpf = cpf
            self.nome = ''
            self.data_nascimento = ''
            self.endereco = ''

    def criacao_por_usuario(self, cadastro: str):
        """
        Lida com os dados da pessoa física, solicitando dados
        relevantes à classe.

        :param cadastro: String validada pelo objeto BancoDeDados
        """
        self.cpf = cadastro
        self.nome = str(input(
            'Qual é o nome do cliente?\nDigite aqui =>'
        ))
        self.data_nascimento = str(input(
            'Qual é a data de nascimento do cliente (no formato '
            '"DD/MM/AAAA")?\nDigite aqui =>'))
        self.endereco = self.solicitar_endereco()
        self.contas = []

    @property
    def tipo_cadastro(self) -> str:
        return 'cpf'


class PessoaJuridica(Cliente):
    def __init__(self, usuario=True, cnpj=''):
        """
        Classe que representa um cliente de natureza jurídica dentro do
        sistema.

        :param usuario: Booleano que indica se a criação está sendo
        realizada pelo usuário.
        :param cnpj: String validada pelo objeto BancoDeDados
        """
        super().__init__()
        if usuario:
            self.criacao_por_usuario(cnpj)
        else:
            self.cnpj = cnpj
            self.nome_fantasia = ''
            self.razao_social = ''
            self.endereco = ''

    def criacao_por_usuario(self, cadastro: str):
        """
        Lida com os dados da pessoa jurídica, solicitando dados
        relevantes à classe.

        :param cadastro: String validada pelo objeto BancoDeDados
        """
        self.cnpj = cadastro
        self.nome_fantasia = str(input(
            'Qual é o nome fantasia da empresa?\nDigite aqui =>'
        ))
        self.razao_social = str(input(
            'Qual é a razão social da empresa?\nDigite aqui =>'))
        self.endereco = self.solicitar_endereco()
        self.contas = []

    @property
    def tipo_cadastro(self) -> str:
        return 'cnpj'


class Conta:
    def __init__(self, cliente: PessoaFisica | PessoaJuridica, numero: int):
        """
        Classe "pai" que representa uma conta bancária dentro do
        sistema.

        :param cliente: Objeto "filho" da classe Cliente
        :param numero: Inteiro resultante do incremento em 1 do maior
        número de conta encontrado no objeto BandoDeDados.
        """
        self.numero = numero
        self.agencia = 1
        self._cliente = cliente
        self.historico = Historico()

    def __str__(self) -> str:
        agencia = f'{self.agencia:04d}'
        numero = f'{self.numero:04d}'
        saldo = f'{self.saldo:.2f}'
        return (
            f"{agencia:>14} | "
            f"{numero:>12} | "
            f"R${saldo:>20}"
        )

    @property
    def saldo(self) -> float:
        total = 0
        for transacao in self.historico.transacoes:
            if transacao.tipo == "+":
                total += transacao.valor
            else:
                total -= transacao.valor

        return total


class ContaCorrente(Conta):
    def __init__(self, cliente: PessoaFisica | PessoaJuridica, numero=0):
        """
        Classe que representa uma conta bancária do tipo corrente
        dentro do sistema.

        :param cliente: Objeto "filho" da classe Cliente
        :param numero: Pré-definido como 0 para a criação via
        BancoDeDados
        """
        super().__init__(cliente, numero)
        self.limite = 500
        self.limite_numero_saques = 3

    @property
    def tipo_conta(self):
        return 'CC'


class ContaPoupanca(Conta):
    def __init__(self, cliente: PessoaFisica, numero=0):
        """
        Classe que representa uma conta bancária do tipo poupança
        dentro do sistema.

        :param cliente: Objeto "filho" da classe Cliente
        :param numero: Pré-definido como 0 para a criação via
        BancoDeDados
        """
        super().__init__(cliente, numero)
        self.limite = 1000
        self.limite_numero_saques = 1

    @property
    def tipo_conta(self):
        return 'CP'


class ContaSalario(Conta):
    def __init__(self, cliente: PessoaFisica, numero=0, usuario=True):
        """
        Classe que representa uma conta bancária do tipo salário dentro
        do sistema.

        :param cliente: Objeto "filho" da classe Cliente
        :param numero: Pré-definido como 0 para a criação via
        BancoDeDados
        """
        super().__init__(cliente, numero)
        if usuario:
            self.historico.transacoes.append(Deposito(2000))
        self.limite = 2000
        self.limite_numero_saques = 1

    @property
    def tipo_conta(self):
        return 'CS'


class Historico:
    def __init__(self):
        """
        Classe que representa o histórico de uma conta dentro do
        sistema.
        """
        self.transacoes = []

    def __str__(self) -> str:
        """
        Varre a lista de transações e agrupa os dados em forma de
        tabela.
        """
        total = 0
        mensagem = ''
        for transacao in self.transacoes:
            mensagem += (
                f' {transacao.tipo} R$ {transacao.valor:>15}\n'
            )
            if transacao.tipo == '-':
                total -= transacao.valor
            elif transacao.tipo == '+':
                total += transacao.valor

        mensagem += ('-'*21)
        return f'{mensagem}\n = R$ {total:>15} TOTAL'

    @property
    def saques_efetuados(self):
        quant_saques = 0
        for transacao in self.transacoes:
            if transacao.tipo == '-':
                quant_saques += 1

        return quant_saques

    def novo_saque(
            self,
            conta: ContaCorrente | ContaPoupanca | ContaSalario,
            valor: float
    ) -> bool:
        """
        Instancia um novo saque quando todos os requisitos são
        validados.

        :param conta: Objeto 'filho' da classe Conta
        :param valor: Ponto flutuante que será utilizado na criação do
        objeto Saque
        """
        if (
                (valor > 0) and
                (conta.saldo > valor) and
                (self.saques_efetuados < conta.limite_numero_saques) and
                (valor <= conta.limite)
        ):
            self.transacoes.append(Saque(valor))
            return True
        return False

    def novo_deposito(
            self,
            conta: ContaCorrente | ContaPoupanca | ContaSalario,
            valor: float
    ) -> bool:
        """
        Instancia um novo depósito quando todos os requisitos são
        validados.

        :param conta: Objeto 'filho' da classe Conta
        :param valor: Ponto flutuante que será utilizado na criação do
        objeto Deposito
        """
        if valor > 0 and conta.tipo_conta != "CS":
            self.transacoes.append(Deposito(valor))
            return True
        return False


class BancoDeDados:
    def __init__(self):
        """
        Classe que representa o banco de dados do sistema.
        """
        self.NOME_ARQUIVO = 'BancoDeDados.txt'
        self.clientes = []
        self.ler_banco()

    @property
    def proximo_numero_conta(self) -> int:
        """
        Varre as contas cadastradas no banco de dados e retorna com o
        maior número de conta encontrado incrementado em um.
        """
        maior_numero_conta = 0
        for cliente in self.clientes:
            for conta in cliente.contas:
                if conta.numero > maior_numero_conta:
                    maior_numero_conta = conta.numero
        return maior_numero_conta + 1

    def cadastro_e_unico(self, cadastro: str) -> bool:
        """
        Varre as contas cadastradas no banco de dados e retorna se o
        CPF/CNPJ passado já consta cadastrado.

        :param cadastro: Combinação de números, pontos, traço (e
        talvez barra), já validado como um número válido para CPF ou
        CNPJ
        """
        for cliente in self.clientes:
            if cliente.tipo_cadastro == 'cpf':
                if cadastro == cliente.cpf:
                    return False

            else:
                if cadastro == cliente.cnpj:
                    return False

        return True

    def ler_banco(self):
        """
        Abre o arquivo em que os dados estão salvos em formato csv
        e distibui cada parte do arquivo em seu devido lugar.
        """
        # Formato da linha quando cliente:
        #   índice;tipoCadastro;cadastro;nome;nomeFantasia;razãoSocial;
        #   dataNascimento;endereço
        # Formato da linha quando conta:
        #   índice;tipoConta;agencia;numero;cadastroCliente
        # Formato linha quando transação:
        #   índice;tipoTransação;valor;agenciaENúmeroConta
        alvo = ''
        try:
            with open(self.NOME_ARQUIVO, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    if len(linha) <= 15:
                        alvo = linha.strip()

                    else:
                        linha_quebrada = linha.strip().split(';')
                        if alvo == "clientes":
                            if linha_quebrada[1] == 'cpf':
                                cliente = PessoaFisica(False)
                                cliente.cpf = linha_quebrada[2]
                                cliente.nome = linha_quebrada[3]
                                cliente.data_nascimento = linha_quebrada[6]
                                cliente.endereco = linha_quebrada[7]

                            elif linha_quebrada[1] == 'cnpj':
                                cliente = PessoaJuridica(False)
                                cliente.cnpj = linha_quebrada[2]
                                cliente.nome_fantasia = linha_quebrada[4]
                                cliente.razao_social = linha_quebrada[5]
                                cliente.endereco = linha_quebrada[7]

                            self.clientes.append(cliente)

                        elif alvo == 'contas':
                            cliente = self.localizar_cliente(linha_quebrada[4])
                            if linha_quebrada[1] == 'CC':
                                conta = ContaCorrente(cliente)

                            elif linha_quebrada[1] == 'CP':
                                conta = ContaPoupanca(cliente)

                            elif linha_quebrada[1] == 'CS':
                                conta = ContaSalario(cliente, usuario=False)

                            conta.agencia = int(linha_quebrada[2])
                            conta.numero = int(linha_quebrada[3])
                            cliente.contas.append(conta)

                        elif alvo == 'transacoes':
                            conta = self.localizar_conta(linha_quebrada[3])
                            valor = float(linha_quebrada[2])
                            if linha_quebrada[1] == '+':
                                conta.historico.transacoes.append(Deposito(valor))

                            elif linha_quebrada[1] == '-':
                                conta.historico.transacoes.append(Saque(valor))

        except FileNotFoundError:
            pass

    def salvar_dados(self):
        """
        Salva os dados coletados na sessao em formato csv no arquivo
        designado.
        """
        cad_clientes = []
        cad_contas = []
        cad_transacoes = []
        for cliente in self.clientes:
            if cliente.tipo_cadastro == 'cpf':
                cadastro_cliente = cliente.cpf
                dados_cliente = (
                    f'{len(cad_clientes) + 1};'
                    f'{cliente.tipo_cadastro};'
                    f'{cliente.cpf};'
                    f'{cliente.nome};'
                    f';'
                    f';'
                    f'{cliente.data_nascimento};'
                    f'{cliente.endereco}\n'
                )
            else:
                cadastro_cliente = cliente.cnpj
                dados_cliente = (
                    f'{len(cad_clientes) + 1};'
                    f'{cliente.tipo_cadastro};'
                    f'{cliente.cnpj};'
                    f';'
                    f'{cliente.nome_fantasia};'
                    f'{cliente.razao_social};'
                    f';'
                    f'{cliente.endereco}\n'
                )
            cad_clientes.append(dados_cliente)
            for conta in cliente.contas:
                identificador_conta = f'{conta.agencia:04d}-{conta.numero:04d}'
                dados_conta = (
                    f'{len(cad_contas) + 1};'
                    f'{conta.tipo_conta};'
                    f'{conta.agencia};'
                    f'{conta.numero};'
                    f'{cadastro_cliente}\n'
                )
                cad_contas.append(dados_conta)
                for transacao in conta.historico.transacoes:
                    dados_transacao = (
                        f'{len(cad_transacoes) + 1};'
                        f'{transacao.tipo};'
                        f'{transacao.valor};'
                        f'{identificador_conta}\n'
                    )
                    cad_transacoes.append(dados_transacao)

        with open(self.NOME_ARQUIVO, 'w+', encoding='utf-8') as arquivo:
            arquivo.write('clientes\n')
            for cliente in cad_clientes:
                arquivo.write(cliente)
            arquivo.write('contas\n')
            for conta in cad_contas:
                arquivo.write(conta)
            arquivo.write('transacoes\n')
            for transacao in cad_transacoes:
                arquivo.write(transacao)

    def localizar_conta(
            self,
            agencia_numero: str
    ) -> ContaCorrente | ContaPoupanca | ContaSalario:
        """
        Varre as contas de cada objeto Cliente no objeto BancoDeDados
        e retorna a conta desejada.

        :param agencia_numero: Agência e número da conta no formato
        "0000-0000"
        :return Conta: O objeto Conta que possui a agência e conta
        correspondente à variável `agencia_numero`
        """
        for cliente in self.clientes:
            for conta in cliente.contas:
                agencia_numero_atual = (
                    f'{conta.agencia:04d}-{conta.numero:04d}')
                if agencia_numero == agencia_numero_atual:
                    return conta

    def localizar_cliente(
            self,
            cadastro_cliente: str
    ) -> PessoaFisica | PessoaJuridica:
        """
        Varre os clientes no objeto BancoDeDados e retorna o cliente
        desejado.

        :param cadastro_cliente: CPF ou CNPJ do cliente com os
        caracteres divisores
        :return Cliente: O objeto Cliente que possui o cadastro
        correspondente à variável `cadastro_cliente^
        """
        for cliente in self.clientes:
            if cliente.tipo_cadastro == 'cpf':
                cadastro_cliente_atual = cliente.cpf
            elif cliente.tipo_cadastro == 'cnpj':
                cadastro_cliente_atual = cliente.cnpj
            else:
                cadastro_cliente_atual = False

            if cadastro_cliente_atual == cadastro_cliente:
                return cliente

        raise TypeError

    def acessar_cliente(
            self
    ) -> PessoaFisica | PessoaJuridica | bool:
        """
        Verifica a existência e retorna o objeto Cliente solicitado
        via inserção de dados pelo usuário.
        """
        while True:
            passe = False
            tipo_cadastro = str(input(
                'Preciso do tipo de cadastro do cliente:\n'
                '\t[pf] - Pessoa Física;\n'
                '\t[pj] - Pessoa Jurídica; ou\n'
                '\t[q]  - Para sair desta ação.\n'
                'Digite aqui =>'
            ))
            if tipo_cadastro == 'pf':
                tipo_cadastro = 'cpf'
                passe = True
            elif tipo_cadastro == 'pj':
                tipo_cadastro = 'cnpj'
                passe = True
            elif tipo_cadastro == 'q':
                print('Voltando ao menu do sistema.')
                return False

            if passe:
                cadastro_cliente = str(input(
                    f'Preciso do número de {tipo_cadastro.upper()} (com os '
                    f'caracteres divisores)  do cliente.\nDigite aqui =>'
                ))
                for cliente in self.clientes:
                    if cliente.tipo_cadastro == tipo_cadastro and tipo_cadastro == 'cpf':
                        if cliente.cpf == cadastro_cliente:
                            return cliente

                    elif cliente.tipo_cadastro == tipo_cadastro and tipo_cadastro == 'cnpj':
                        if cliente.cnpj == cadastro_cliente:
                            return cliente

                print(
                    f'@@@ Operação falhou!           Não foi encontrado um '
                    f'cliente com o número de {tipo_cadastro.upper()} '
                    f'passado. Tente novamente. @@@'
                )

    @staticmethod
    def _validacao_calculada_de_cpf(combinacao: str) -> bool:
        """
        Validação de duas etapas para confirmar a validade da
        combinação de números como um CPF.

        :param combinacao: O potencial CPF a ser validado.
        """
        calculo_digito_A = 0
        calculo_digito_B = int(combinacao[0]) * 11
        multiplicador = 10
        for indice_digito in range(9):
            calculo_digito_A += (
                    int(combinacao[indice_digito]) * multiplicador
            )
            calculo_digito_B += (
                    int(combinacao[indice_digito + 1]) * multiplicador
            )
            multiplicador -= 1

        calculo_digito_A = calculo_digito_A % 11
        if calculo_digito_A <= 2:
            ver_digito_A = int(combinacao[9]) == 0
        else:
            ver_digito_A = int(combinacao[9]) == 11 - calculo_digito_A

        calculo_digito_B = calculo_digito_B % 11
        if calculo_digito_B <= 2:
            ver_digito_B = int(combinacao[10]) == 0
        else:
            ver_digito_B = int(combinacao[10]) == 11 - calculo_digito_B

        return ver_digito_A and ver_digito_B

    def validar_cpf(self, cpf_cliente: str) -> str:
        """
        Verifica se o valor satisfaz as diretrizes do sistema para um CPF
        válido.

        :param cpf_cliente: A combinação de números que representa o cpf

        :return falha: Error
        :return sucesso: O CPF formatado com pontos após o terceiro e
        sexto números, e o traço do dígito
        """
        if not cpf_cliente.isnumeric():
            print('@@@ Operação falhou!            A combinação passada '
                  'contém um ou mais caracteres não permitidos. @@@')

        elif len(cpf_cliente) != 11:
            print('@@@ Operação falhou!           Operação Inválida! A '
                  'combinação passada não tem o comprimento normal de um CPF '
                  '(11 caractéres). @@@')

        else:
            novo_cpf_f = (
                f'{cpf_cliente[:3]}.'
                f'{cpf_cliente[3:6]}.'
                f'{cpf_cliente[6:9]}-'
                f'{cpf_cliente[9:]}'
            )
            if not self._validacao_calculada_de_cpf(cpf_cliente):
                print('@@@ Operação falhou!           Operação inválida! A '
                      'combinação passada não é um CPF válido. @@@')

            elif not self.cadastro_e_unico(novo_cpf_f):
                print('@@@ Operação falhou!           O CPF passado já conta'
                      ' em nossa base de dados. @@@')

            else:
                return novo_cpf_f

        return 'error'

    @staticmethod
    def _validacao_calculada_de_cnpj(combinacao: str) -> bool:
        """
        Validação de duas etapas para confirmar a validade da
        combinação de números como um CNPJ.

        :param combinacao: O potencial CNPJ a ser validado.
        """
        calculo_digito_A = 0
        calculo_digito_B = int(combinacao[0]) * 6
        multiplicador = 5
        for indice_digito in range(12):
            calculo_digito_A += int(combinacao[indice_digito]) * multiplicador
            calculo_digito_B += int(combinacao[indice_digito + 1]) * multiplicador
            if multiplicador == 2:
                multiplicador = 9
            else:
                multiplicador -= 1

        calculo_digito_A = calculo_digito_A % 11
        if calculo_digito_A <= 2:
            ver_digito_A = int(combinacao[12]) == 0
        else:
            ver_digito_A = int(combinacao[12]) == 11 - calculo_digito_A

        calculo_digito_B = calculo_digito_B % 11
        if calculo_digito_B <= 2:
            ver_digito_B = int(combinacao[13]) == 0
        else:
            ver_digito_B = int(combinacao[13]) == 11 - calculo_digito_B

        return ver_digito_A and ver_digito_B

    def validar_cnpj(self, cnpj_cliente) -> str:
        """
        Verifica se o valor satisfaz as diretrizes do sistema para um CPF
        válido.

        :param cnpj_cliente: A combinação de números que representa o cpf

        :return falha: Error
        :return sucesso: O CNPJ formatado com pontos após o segundo e
        quinto números, barra após o oitavo e o traço do dígito
        """
        if not cnpj_cliente.isnumeric():
            print('@@@ Operação falhou!           A combinação passada contém'
                  ' um ou mais caracteres não permitidos. @@@')

        elif len(cnpj_cliente) != 14:
            print('@@@ Operação falhou!           A combinação passada não '
                  'tem o comprimento normal de um CNPJ (14 caractéres).')

        else:
            novo_cnpj_f = (
                f'{cnpj_cliente[:2]}.'
                f'{cnpj_cliente[2:5]}.'
                f'{cnpj_cliente[5:8]}/'
                f'{cnpj_cliente[8:12]}-'
                f'{cnpj_cliente[12:]}'
            )
            if not self._validacao_calculada_de_cnpj(cnpj_cliente):
                print('@@@ Operação falhou!           A combinação passada '
                      'não é um CNPJ válido. @@@')

            elif not self.cadastro_e_unico(novo_cnpj_f):
                print('@@@ Operação falhou!           Este CNPJ já conta em '
                      'nossa base de dados. @@@')

            else:
                return novo_cnpj_f

        return 'error'


def sessao_sistema() -> None:
    """
    Lida com o acesso do usuário ao sistema bancário, valida ações
    superficiais e invoca os métodos necessários.
    """
    MENSAGEM_MENU_SISTEMA = (
        "<__________________MENU_SISTEMA__________________>\n"
        "\tEscolha a operação da lista abaixo:\n"
        "\t\t[c] Cadastrar novo cliente;\n"
        "\t\t[a] Acessar cliente; ou\n"
        "\t\t[q] Sair do sistema.\n"
        "Operação => "
    )
    banco_de_dados = BancoDeDados()
    while True:
        operacao_sistema = str(input(MENSAGEM_MENU_SISTEMA))
        print('\n\n\n')
        if operacao_sistema == 'c' or operacao_sistema == 'a':
            if operacao_sistema == 'c':
                cliente = cadastrar_novo_cliente(banco_de_dados)
                banco_de_dados.clientes.append(cliente)

            else:
                cliente = banco_de_dados.acessar_cliente()

            if cliente:
                sessao_cliente(banco_de_dados, cliente)

        elif operacao_sistema == 'q':
            print("Encerrando sistema! ... ")
            banco_de_dados.salvar_dados()
            break

        else:
            print("@@@ Operação falhou!           Por favor, tente "
                  "novamente. @@@")


def cadastrar_novo_cliente(
        banco_dados: BancoDeDados
) -> PessoaFisica | PessoaJuridica | bool:
    """
    Inicia a criação de um objeto Cliente, solicitando a natureza e
    validando o cadastro antes de instanciar o objeto.

    :param banco_dados: Objeto BancoDeDados para validar a operação
    """
    while True:
        natureza = str(input(
            "Qual é a natureza do cliente?\n"
            "\t[pf] - Pessoa Física;\n"
            "\t[pj] - Pessoa Jurídica; ou\n"
            "\t[q]  - Sair."
            "Digite =>"
        ))
        if natureza == 'pf':
            while True:
                entrada = str(input(
                    'Preciso que me informe um CPF válido.\nDigite aqui =>'
                ))
                novo_cpf = banco_dados.validar_cpf(entrada)
                if novo_cpf != 'error':
                    break
            return PessoaFisica(True, novo_cpf)
        elif natureza == 'pj':
            while True:
                entrada = str(input(
                    'Preciso que me informe um CNPJ válido.\nDigite aqui =>'
                ))
                novo_cnpj = banco_dados.validar_cnpj(entrada)
                if novo_cnpj != 'error':
                    break
            return PessoaJuridica(True, novo_cnpj)
        elif natureza == 'q':
            return False
        else:
            print("~~~ Operação não identificada! Não compreendi o que você "
                  "deseja, tente novamente ~~~")


def sessao_cliente(
        banco_dados: BancoDeDados,
        cliente: PessoaFisica | PessoaJuridica
) -> None:
    """
    Lida com as operações permitidas ao cliente.

    :param banco_dados: Objeto BancoDeDados que será utilizado para
    resgatar o próximo número de conta para a criação da mesma
    :param cliente: Objeto Cliente que irá lidar com a autenticação do
    cliente e as operações da classe
    """
    tipo_cadastro = cliente.tipo_cadastro
    if tipo_cadastro == 'cpf':
        identificador = cliente.cpf
    else:
        identificador = cliente.cnpj
    print(
        f"!!! Operação bem sucedida!     Você está em sessão e identificado "
        f"como o cliente de {tipo_cadastro.upper()} nº {identificador}. !!!"
    )
    MENSAGEM_MENU_CLIENTE = (
        "\tO que deseja fazer?\n"
        "\t\t[n] - Abrir uma nova conta;\n"
        "\t\t[l] - Listar as contas do cliente;\n"
        "\t\t[a] - Acessar uma conta;\n"
        "\t\t[q] - Sair do cliente\n"
        "Digite =>"
    )
    while True:
        operacao_cliente = str(input(MENSAGEM_MENU_CLIENTE))
        print('\n\n\n')
        if operacao_cliente == 'n':
            if abrir_nova_conta(cliente, banco_dados.proximo_numero_conta):
                print("!!! Operação bem sucedida!     Nova conta aberta com "
                      "sucesso! !!!")

        elif operacao_cliente == 'l':
            cliente.listar_contas()
        elif operacao_cliente == 'a':
            conta = acessar_conta(cliente)
            if conta:
                sessao_conta(conta)

        elif operacao_cliente == 'q':
            print('Saindo do menu do cliente.')
            break
        else:
            print("~~~ Operação não identificada! Tente novamente ~~~")


def validar_conta(
        cliente: PessoaFisica | PessoaJuridica,
        agenc_num_conta: str
) -> tuple:
    """
    Busca na lista de contas do objeto Cliente se existe a conta
    desejada.

    :param cliente: Objeto Cliente que possivelmente possui a
    conta desejada
    :param agenc_num_conta: Agência e número da conta no formato
    "0000-0000"
    """
    for n in range(len(cliente.contas)):
        agenc_num_conta_atual = (
            f'{cliente.contas[n].agencia:04d}-'
            f'{cliente.contas[n].numero:04d}'
        )
        if agenc_num_conta == agenc_num_conta_atual:
            return True, n
    return False, -1


def acessar_conta(
        cliente: PessoaFisica | PessoaJuridica
) -> ContaCorrente | ContaPoupanca | ContaSalario | bool:
    """
    Valida a identidade do cliente e retorna o objeto correspondente.

    :param cliente: Objeto Cliente que se deseja acessar.
    """
    MENSAGEM_AG_NUM = (
        'Me diga o número da agência e da conta (formato, "0000-0000"); ou\n'
        'digite "q" para voltar ao menu do usuário.\n'
        'Operação =>'
    )
    MENSAGEM_LIBERAR_ACESSO = (
        'Agora preciso do {} (com os caracteres separadores) do cliente para '
        'liberar o acesso à conta.\nDigite aqui =>'
    )
    while True:
        agencia_e_numero_conta = str(input(MENSAGEM_AG_NUM))
        verificador, indice_conta = validar_conta(cliente, agencia_e_numero_conta)
        if agencia_e_numero_conta == 'q':
            print("Voltando ao menu do cliente.")
            return False
        elif verificador:
            tipo_cadastro = cliente.tipo_cadastro.upper()
            cadastro = str(input(MENSAGEM_LIBERAR_ACESSO.format(tipo_cadastro)))
            if tipo_cadastro == 'CPF':
                if cliente.cpf == cadastro:
                    return cliente.contas[indice_conta]
            elif tipo_cadastro == 'CNPJ':
                if cliente.cnpj == cadastro:
                    return cliente.contas[indice_conta]
            print(f'@@@ Operação falhou!           {tipo_cadastro} não '
                  f'validado! Tente novamente. @@@')
        else:
            print(
                '@@@ Operação falhou!           O valor passado não '
                'corresponde com nenhuma conta deste cliente. @@@'
            )


def sessao_conta(
        conta: ContaCorrente | ContaPoupanca | ContaSalario
) -> None:
    """
    Lida com as operações pertinentes à conta.
    """
    MENSAGEM_MENU_CONTA = (
        'Operando em conta nº{}\n'
        '\t[d] - Depositar em Conta\n'
        '\t[s] - Sacar da Conta\n'
        '\t[e] - Exibir Extrato\n'
        '\t[q] - Sair da Conta\n'
        'Operação =>'
    )
    while True:
        operacao_conta = str(input(MENSAGEM_MENU_CONTA.format(conta.numero)))
        print('\n\n\n')
        if operacao_conta == 'd':
            valor_deposito = float(input('Quanto você deseja depositar?'))
            if conta.historico.novo_deposito(conta, valor_deposito):
                print('!!! Operação bem sucedida!     Depósito efetuado com '
                      'sucesso. !!!')

            else:
                if conta.tipo_conta == 'CS':
                    print('@@@ Operação falhou!           Essa conta não '
                          'permite depósitos. @@@')
                else:
                    print('@@@ Operação falhou!           Não foi possível '
                          'realizar o depósito. Verifique e tente novamente. '
                          '@@@')

        elif operacao_conta == 's':
            valor_saque = float(input("Quanto você deseja sacar?"))
            if conta.historico.novo_saque(conta, valor_saque):
                print('!!! Operação bem sucedida!     Saque efetuado com '
                      'sucesso. !!!')
            else:
                print('@@@ Operação falhou!           Não foi possível '
                      'realizar o saque. @@@')
        elif operacao_conta == 'e':
            print(conta.historico)
        elif operacao_conta == 'q':
            print('Saindo do acesso a conta e voltando ao menu do cliente.')
            break
        else:
            print('~~~ Operação não identificada! Não entendi o que você '
                  'deseja, tente novamente. ~~~')


def abrir_nova_conta(
        cliente: PessoaFisica | PessoaJuridica,
        numero_nova_conta: int
) -> bool:
    """
    Valida a possibilidade e cria um novo objeto Conta.

    :param cliente:  Objeto Cliente que está em sessão
    :param numero_nova_conta: Inteiro resultante do incremento em 1 do
    maior número de conta encontrado no objeto BandoDeDados.
    """
    while True:
        tipo_conta = str(input(
            'Qual é o tipo de conta que o cliente deseja abrir?\n'
            '\t[cc] - Conta Corrente;\n'
            '\t[cs] - Conta Salário\t\t(somente para pessoas físicas);\n'
            '\t[cp] - Conta Poupança\t\t(somente para pessoas físicas); ou\n'
            '\t[q]  - Voltar ao menu do cliente.\n'
            'Digite =>'
        ))
        if tipo_conta == 'cc':
            cliente.contas.append(ContaCorrente(cliente, numero_nova_conta))
            return True
        elif tipo_conta == 'cs' and cliente.tipo_cadastro == 'cpf':
            cliente.contas.append(ContaSalario(cliente, numero_nova_conta))
            return True
        elif tipo_conta == 'cp' and cliente.tipo_cadastro == 'cpf':
            cliente.contas.append(ContaPoupanca(cliente, numero_nova_conta))
            return True
        elif tipo_conta == 'q':
            return False
        elif (
                (tipo_conta == 'cs' or tipo_conta == 'cp') and
                (cliente.tipo_cadastro != 'cpf')
        ):
            print("@@@ Operação falhou!           Esta conta não é permitida"
                  " para o cliente em sessão. @@@")

        else:
            print("~~~ Operação não identificada! Tente novamente. ~~~")


if __name__ == '__main__':

    sessao_sistema()
