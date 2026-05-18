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
    while True:
        try:
            cargo = input("Digite seu cargo: ")
            if cargo == "1":
                input('Digite seu nome: ')
                input('Digite sua matrícula: ')
                input('Coloque sua senha: ')
            elif cargo == "2":
                input('Digite seu nome: ')
                input('Digite seu ID: ')
            else: 
                print('Erro, tente novamente!')


