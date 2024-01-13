"""Código desenvolvido para obtenção de progresso na plataforma DIO, no 
curso Formação Python Developer."""
__author__ = "TDPessoa"
__email__ = "thiago.d.pessoa@gmail.com"
__github__ = "https://github.com/TDPessoa"


menu = ("""
[d] Deposito
[s] Sacar
[e] Extrato
[q] Sair
=>""")

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
while True:
    opcao = input(menu)
    if opcao == 'd':
        deposito = float(input("Quanto você deseja depositar:"))
        if deposito <= 0:
            print('Operação Inválida! O valor precisa ser positivo.')

        else:
            deposito_f = f'{deposito:.2f}'
            saldo += deposito
            extrato += f'  R$ + {deposito_f:>32}\n'

    elif opcao == 's':
        saque = float(input('Quanto você deseja sacar:'))
        if saque <= 0:
            print('Operação Inválida! O valor precisa ser positivo.')
        elif saque > saldo:
            print('Operação Inválida! O valor em conta não permite este'
		  ' saque.')
        elif saque > limite:
            print('Operação Inválida! O valor desejado ultrapassa o '
		  'limite permitido.')
        elif numero_saques == LIMITE_SAQUES:
            print('Operação Inválida! Vocâ já realizou o limite de '
		  'saques permitidos para o dia de hoje.')
        else:
            saque_f = f'{saque:.2f}'
            saldo -= saque
            extrato += f'  R$ - {saque_f:>32}\n'
            numero_saques += 1

    elif opcao == 'e':
        print('_'*20, 'EXTRATO', '_'*21)
        if len(extrato) == 0:
            print('Não houve movimentação.')
        else:
            print(extrato, end='\r')
        print('-'*50)
        print('  R$   {:>32}\t\tTOTAL'.format(f'{saldo:.2f}'))

    elif opcao == 'q':
        break

    else:
        print('Operação inválida, por favor selecione novamente a '
	      'operação desejada.')
