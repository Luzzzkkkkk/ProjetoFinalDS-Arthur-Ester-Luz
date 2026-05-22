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
            else: 
                break
        except ValueError:
            print('Erro, tente novamente!')
                
def estudante():
    
    nome = input('Digite seu nome: ')
    nome_correto = "".join ([c for c in nome if c.isalpha() or c.isspace()])
    print(nome_correto)
    matrícula = (input('Digite o número da matrícula: ')).isdigit()
    senha = input('Coloque sua senha: ').replace(" ","")


cadastro()