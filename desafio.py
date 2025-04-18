from datetime import datetime, date

# Variáveis globais
saldo = 0
limite = 500
extrato = []
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACOES_DIARIAS = 10

clientes = []
contas = []
AGENCIA_PADRAO = "0001"

transacoes_por_dia = {}  # {'2025-04-18': 5}
saques_por_dia = {}      # {'2025-04-18': 2}

menu = """================ MENU ================

[c] Cadastrar cliente
[n] Nova conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def encontrar_cliente(cpf):
    return next((cliente for cliente in clientes if cliente["cpf"] == cpf), None)

def cadastrar_cliente():
    cpf = input("Informe o CPF (somente números): ")
    if encontrar_cliente(cpf):
        print("❌ CPF já cadastrado.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (rua, número - bairro - cidade/estado): ")

    cliente = {"nome": nome, "cpf": cpf, "nascimento": nascimento, "endereco": endereco}
    clientes.append(cliente)
    print("✅ Cliente cadastrado com sucesso!")

def criar_conta():
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf)
    if not cliente:
        print("❌ Cliente não encontrado. Cadastre o cliente primeiro.")
        return

    numero_conta = len(contas) + 1
    conta = {"agencia": AGENCIA_PADRAO, "numero": numero_conta, "cpf": cpf}
    contas.append(conta)
    print(f"✅ Conta criada com sucesso! Agência: {AGENCIA_PADRAO}, Número: {numero_conta}")

def hoje():
    return date.today().isoformat()

def pode_transacionar():
    return transacoes_por_dia.get(hoje(), 0) < LIMITE_TRANSACOES_DIARIAS

def pode_sacar():
    return saques_por_dia.get(hoje(), 0) < LIMITE_SAQUES_DIARIOS

def registrar_transacao(tipo, valor):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    extrato.append(f"{agora} - {tipo}: R$ {valor:.2f}")
    data_hoje = hoje()
    transacoes_por_dia[data_hoje] = transacoes_por_dia.get(data_hoje, 0) + 1

def registrar_saque():
    data_hoje = hoje()
    saques_por_dia[data_hoje] = saques_por_dia.get(data_hoje, 0) + 1

def depositar():
    global saldo
    if not pode_transacionar():
        print("❌ Limite de 10 transações diárias atingido.")
        return

    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        registrar_transacao("Depósito", valor)
    else:
        print("❌ Valor inválido.")

def sacar():
    global saldo
    if not pode_transacionar():
        print("❌ Limite de 10 transações diárias atingido.")
        return
    if not pode_sacar():
        print("❌ Limite de 3 saques diários atingido.")
        return

    valor = float(input("Informe o valor do saque: "))
    if valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print("❌ Valor excede o limite por saque.")
    elif valor > 0:
        saldo -= valor
        registrar_transacao("Saque", valor)
        registrar_saque()
    else:
        print("❌ Valor inválido.")

def exibir_extrato():
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for linha in extrato:
            print(linha)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==========================================")

# Loop principal
while True:
    opcao = input(menu)

    if opcao == "c":
        cadastrar_cliente()
    elif opcao == "n":
        criar_conta()
    elif opcao == "d":
        depositar()
    elif opcao == "s":
        sacar()
    elif opcao == "e":
        exibir_extrato()
    elif opcao == "q":
        break
    else:
        print("❌ Opção inválida. Tente novamente.")
