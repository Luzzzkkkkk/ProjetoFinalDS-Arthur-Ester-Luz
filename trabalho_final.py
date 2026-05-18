import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Senac2026",
        database="trabalhoadsfinal"
    )
<<<<<<< HEAD

=======
             
>>>>>>> 9d9c6b18368e666e510e7969d253a0aa542208ff
def cadastro():
    print("=-=-=-=-=-=-=-Cadastro-=-=-=-=-=-=-=-")
    print("1 - Estudante")
    print("2 - Professor")
<<<<<<< HEAD
    print("0 - Sair")
=======
>>>>>>> 9d9c6b18368e666e510e7969d253a0aa542208ff
    
    while True:
        try:
            cargo = input("Digite seu cargo: ")
            if cargo == "1":
                nome = input('Digite seu nome: ')
                matrícula = int(input('Digite o número da matrícula: '))
                senha = input('Coloque sua senha: ')
            elif cargo == "2":
                nome = input('Digite seu nome: ')
                id = int(input('Digite seu ID: '))
                senha = input('Coloque sua senha: ')
            else: 
                break
        except ValueError:
            print('Erro, tente novamente!')


def validarDados   