from sqlalchemy import (
    create_engine,
    select, 
    func
)
from sqlalchemy.orm import Session
from tabelas import Base
from tabelas import (
    TipoCliente, 
    Cliente, 
    Conta, 
    TipoTransacao, 
    Transacao
)


def main():
    # Iniciando a máquina 
    engine = create_engine('sqlite://', echo=False)
    # Criando as tabelas em Base
    Base.metadata.create_all(engine)
    # Iniciando a sessão
    with Session(engine) as session:
        persistir(session)
        consultas(session)


def consultas(session):
    print("\n\nConsulta de Clientes que sejam `Pessoa Física`:")
    #   SELECT c.nome
    #   FROM cad_Cliente c
    #   WHERE c.id_tipo = 1;
    stmt = select(Cliente.nome).where(Cliente.id_tipo.is_(1))
    for row in session.scalars(stmt):
        print(row)

    print("\n\nConsulta da concatenação de Agência e Número de conta e Nome do cliente:")
    #   SELECT 
    #       cta.agencia & cta.numero,
    #       cli.nome
    #   FROM 
    #       cad_Cliente cli,
    #       cad_Conta cta JOIN cli
    #           ON cta.id_cliente = cli.id;
    resultados = {}
    stmt_contas = select(Conta)
    for row in session.scalars(stmt_contas):
        resultados[row.id] = {
            "agencia_e_conta": f'{row.agencia:04d} - {row.numero:04d}',
            "id_cliente": row.id_cliente
        }
    stmt_clientes = select(Cliente)
    for row in session.scalars(stmt_clientes):
        for conta in resultados:
            if row.id == resultados[conta]['id_cliente']:
                resultados[conta]['nome_cliente'] = row.nome
    print("_AGENCIA_E_CONTA_|_NOME_CLIENTE_")
    for resultado in resultados:
        print(f" {resultados[resultado]['agencia_e_conta']:>15} | {resultados[resultado]['nome_cliente']}")
    
    print("\n\nConsulta de contágem de contas agrupados por cliente:")
    #   SELECT 
    #       cli.nome, 
    #       count(cnt.id)
    #   FROM 
    #       cad_Cliente cli, 
    #       cad_Conta cnt JOIN cli
    #           ON (cli.id = cnt.id_cliente)
    #   GROUP BY cli.nome;
    dicionario_clientes = {}
    stmt_clientes = select(Cliente)
    for row in session.scalars(stmt_clientes):
        dicionario_clientes[row.id] = row.nome
    contagem_de_contas = {}
    stmt_contas = select(Conta)
    for row in session.scalars(stmt_contas):
        try:
            contagem_de_contas[dicionario_clientes[row.id_cliente]] += 1
        except KeyError:
            contagem_de_contas[dicionario_clientes[row.id_cliente]] = 1
    print("_NOME_CLIENTE____________|_QUANT._CONTAS")
    for cliente in contagem_de_contas:
        print(f' {cliente:<23} | {contagem_de_contas[cliente]}')


    print("\n\nConsulta de todas as contas cadastradas, seus saldos e o nome do cliente:")
    #   SELECT 
    #       cta.id as main_id,
    #       SUM(sub_query_saldo.subQ_valor),
    #       cli.nome
    #   FROM 
    #       cad_Conta cta,
    #       cad_Cliente cli JOIN cta
    #           ON cli.id = cta.id_cliente,
    #       (SELECT 
    #           cta.id as subQ_id
    #           (trs.valor * tpo.multiplicador) as subQ_valor
    #        FROM 
    #           rel_Transacao trs,
    #           lst_Tipo_Transacao tpo JOIN trs
    #               ON tpo.id = trs.id_tipo
    #       ) sub_query_saldo LEFT JOIN cta
    #           ON cta.id = sub_query_saldo.subQ_id;
    saldos_contas = {}
    stmt_contas = select(Conta)
    for row in session.scalars(stmt_contas):
        saldos_contas[row.id] = {
            'id_cliente': row.id_cliente,
            'nome_cliente': "",
            'saldo_positivo': 0,
            'saldo_negativo': 0
        }

    stmt_clientes = select(Cliente)
    for row in session.scalars(stmt_clientes):
        for conta in saldos_contas:
            if row.id == saldos_contas[conta]['id_cliente']:
                saldos_contas[conta]['nome_cliente'] = row.nome

    stmt_transacoes = select(Transacao)
    for row in session.scalars(stmt_transacoes):
        if row.id_tipo == 1:
            saldos_contas[row.id_conta]['saldo_positivo'] += row.valor
        else:
            saldos_contas[row.id_conta]['saldo_negativo'] += row.valor

    print("_ID_CONTA_|_________SALDO_|_NOME_CLIENTE_")
    for id_conta in saldos_contas:
        f_id = f'{id_conta:04d}'
        saldo = saldos_contas[id_conta]['saldo_positivo'] \
              - saldos_contas[id_conta]['saldo_negativo']
        f_saldo = f'{saldo:.2f}'
        print(f" {f_id:>8} |"
              f" R$ {f_saldo:>10} |"
              f" {saldos_contas[id_conta]['nome_cliente']}")
def persistir(session):
    # Inserção de dados base
    session.add_all(
        [
            TipoCliente(descricao="Pessoa Física", cadastro="CPF"),
            TipoCliente(descricao="Pessoa Jurídica", cadastro="CNPJ"),
            TipoTransacao(descricao="Deposito", multiplicador=1),
            TipoTransacao(descricao="Saque", multiplicador=-1)
        ]
    )
    # Inserção de dados teste para Cliente
    session.add_all(
        [
            Cliente(nome="Alex Bastos", 
                endereco="R. Tenente-Coronel Cardoso, 1 - 28035-042 - Centro, Campos dos Goytacazes/RJ", 
                numero_cadastro="84032987149", 
                id_tipo=1
                ),
            Cliente(nome="Carlos Dantas", 
                endereco="R. Barão de Vitória, 2 - 09961-660 - Casa Grande, Diadema/SP", 
                numero_cadastro="55723206257", 
                id_tipo=1
                ),
            Cliente(nome="Empreendimentos Ferdan",
                endereco="R. Arlindo Nogueira, 3 - 64000-290 - Centro, Teresina/PI",
                numero_cadastro="39571455000100",
                id_tipo=2
                ),
            Cliente(nome="Gustavo Holanda",
                endereco="Tv. Antônio Ferreira, 4 - 68700-216 - Igrejinha, Capanema/PA",
                numero_cadastro="25611449336",
                id_tipo=1
                ),
            Cliente(nome="Imobiliária Junqueira",
                endereco="Av. Afonso Pena, 5 - 30130-005 - Boa Viagem, Belo Horizonte/MG",
                numero_cadastro="71867318000112",
                id_tipo=2
                ),
            Cliente(nome="Kero-kero Rações",
                endereco="Av. São João, 6 - 13216-000 - Vila Joana, Jundiaí/SP",
                numero_cadastro="82275575000181",
                id_tipo=2
                ),
            Cliente(nome="Lavínia Motta",
                endereco="Av. Governador José Malcher, 7 - 66055-260 - Nazaré, Belém/PA",
                numero_cadastro="71564508838",
                id_tipo=1
                ),
            Cliente(nome="Negócio Urbano",
                endereco="R. Pereira Estéfano, 8 - 04144-070 - Vila da Saúde, São Paulo/SP",
                numero_cadastro="16790162000100",
                id_tipo=2
                ),
            Cliente(nome="Otavio Pires",
                endereco="R. da Imprensa, 9 - 79002-290 - Monte Castelo, Campo Grande/MS",
                numero_cadastro="02213828440",
                id_tipo=1
                ),
            Cliente(nome="Queima-Peças",
                endereco="QE 11 Área Especial C - 71020-631 - Guará I, Brasília/DF",
                numero_cadastro="84132321000130",
                id_tipo=2
                )
        ]
    )
    # Inserção de dados teste para Conta
    session.add_all(
        [
            Conta(agencia=1, numero=1, id_cliente=1),
            Conta(agencia=1, numero=2, id_cliente=2),
            Conta(agencia=2, numero=3, id_cliente=1),
            Conta(agencia=3, numero=4, id_cliente=3),
            Conta(agencia=1, numero=5, id_cliente=4),
            Conta(agencia=2, numero=6, id_cliente=5),
            Conta(agencia=4, numero=7, id_cliente=3),
            Conta(agencia=2, numero=8, id_cliente=7),
            Conta(agencia=1, numero=9, id_cliente=3),
            Conta(agencia=5, numero=10, id_cliente=8),
            Conta(agencia=3, numero=11, id_cliente=9),
            Conta(agencia=4, numero=12, id_cliente=10)
        ]
    )
    # Inserção de dados teste para Transacao
    session.add_all(
        [
            Transacao(valor=200000, id_tipo=1, id_conta=3),
            Transacao(valor=1000, id_tipo=1, id_conta=1),
            Transacao(valor=500, id_tipo=2, id_conta=1),
            Transacao(valor=225, id_tipo=1, id_conta=5),
            Transacao(valor=385, id_tipo=1, id_conta=8),
            Transacao(valor=140233.3, id_tipo=1, id_conta=9),
            Transacao(valor=215, id_tipo=2, id_conta=2),
            Transacao(valor=334, id_tipo=1, id_conta=6),
            Transacao(valor=2334.6, id_tipo=2, id_conta=4),
            Transacao(valor=44567, id_tipo=1, id_conta=11),
            Transacao(valor=4567, id_tipo=2, id_conta=11),
            Transacao(valor=234355.2, id_tipo=1, id_conta=12),
            Transacao(valor=244, id_tipo=1, id_conta=2),
            Transacao(valor=46788.3, id_tipo=2, id_conta=12)
        ]
    )
    session.commit()


main()