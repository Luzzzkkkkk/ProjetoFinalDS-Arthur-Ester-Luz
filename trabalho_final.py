import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Senac2026",
        database="trabalhoadsfinal"
    )

def cadastro():
    print("=-=-=-=-=-=-=-Cadastro-=-=-=-=-=-=-=-")
    print("1 - Estudante")
    print("2 - Professor")
    print("0 - Sair")
    
    while True:
        try:
            cargo = input("Digite seu cargo: ")
            if cargo == "1":
                print("Bem-vindo à área do aluno!")
                estudante()
            elif cargo == "2":
                print("Bem-vindo à área do professor!")
                prof()
            else: 
                break
        except ValueError:
            print('Erro, tente novamente!')
                
def estudante():
    nome = input('Digite seu nome: ')
    if any(c.isdigit() for c in nome):
        print("⚠️   Alerta: O nome contém números. O nome será corrigido.")
    nome_correto = "".join ([c for c in nome if c.isalpha() or c.isspace()])
    print(f"Correção do nome: { nome_correto }")
    while True:
        matrícula = (input('Digite o número da matrícula: '))
        if any(c.isalpha() for c in matrícula):
            print("Apenas números permitidos. Tente novamente.")
        else:
            print('Erro, tente novamente!')
            break
    
        senha = input('Coloque sua senha: ').replace(" ","")

def prof():
    ...

cadastro()