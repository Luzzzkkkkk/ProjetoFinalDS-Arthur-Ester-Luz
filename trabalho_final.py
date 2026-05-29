<<<<<<< HEAD
import _mysql_connector
import json
 
# =====================================================================
# CONFIGURAÇÃO E CRIAÇÃO DO BANCO DE DADOS (PERSISTÊNCIA & CRUD)
# =====================================================================
def inicializar_banco():
    conexao = _mysql_connector.connect("escola.db")
    cursor = conexao.cursor()
    # Tabela de Alunos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        turma TEXT NOT NULL,
        senha TEXT NOT NULL,
        notas TEXT DEFAULT '[]',
        media REAL DEFAULT 0.0,
        situacao TEXT DEFAULT 'Reprovado'
    )
    """)
    # Tabela de Professores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        turma TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    # Criar um Secretário Padrão (Admin) caso o banco esteja vazio
    cursor.execute("SELECT COUNT(*) FROM professores")
    if cursor.fetchone()[0] == 0:
        # Cadastros iniciais de teste
        cursor.execute("INSERT INTO professores (nome, idade, turma, senha) VALUES ('Admin Secretário', 40, 'ADMIN', '1234')")
        cursor.execute("INSERT INTO professores (nome, idade, turma, senha) VALUES ('Professor Reginaldo', 35, '9A', 'prof123')")
        cursor.execute("INSERT INTO alunos (nome, idade, turma, senha, notas, media, situacao) VALUES ('Lucas Silva', 15, '9A', 'aluno123', '[]', 0.0, 'Reprovado')")
        conexao.commit()
    conexao.close()
 
# =====================================================================
# FUNÇÕES DE VALIDAÇÃO DE CAMPOS
# =====================================================================
def ler_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < 0:
                print(" Erro: O valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print(" Erro: Digite um número inteiro válido.")
 
def ler_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0.0 or valor > 10.0:
                print(" Erro: A nota deve ser entre 0.0 e 10.0.")
                continue
            return valor
        except ValueError:
            print(" Erro: Digite um número decimal válido (use ponto).")
 
def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print(" Erro: Este campo não pode ficar vazio.")
            continue
        return valor
 
# =====================================================================
# REGRAS DE NEGÓCIO: CÁLCULOS E SITUAÇÃO
# =====================================================================
def calcular_situacao(notas_lista):
    if not notas_lista:
        return 0.0, "Reprovado"
    media = sum(notas_lista) / len(notas_lista)
    if media >= 7.0:
        situacao = "Aprovado"
    elif 5.0 <= media < 7.0:
        situacao = "Recuperacao"
    else:
        situacao = "Reprovado"
    return round(media, 2), situacao
 
# =====================================================================
# FUNÇÕES DO SECRETÁRIO (CRUD TOTAL)
# =====================================================================
def menu_secretario():
    while True:
        print("\n--- MENU DO SECRETÁRIO ---")
        print("1. Cadastrar Aluno")
        print("2. Listar Alunos")
        print("3. Editar Aluno")
        print("4. Remover Aluno")
        print("5. Cadastrar Professor")
        print("6. Listar Professores")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")
        conexao = _mysql_connector.connect("escola.db")
        cursor = conexao.cursor()
        if opcao == "1":
            print("\n[Cadastrar Aluno]")
            nome = ler_texto("Nome do Aluno: ")
            idade = ler_inteiro("Idade do Aluno: ")
            turma = ler_texto("Turma (ex: 9A): ")
            senha = ler_texto("Senha de Acesso: ")
            cursor.execute("INSERT INTO alunos (nome, idade, turma, senha) VALUES (?, ?, ?, ?)", (nome, idade, turma, senha))
            conexao.commit()
            print(f" Aluno cadastrado com sucesso! ID de matrícula: {cursor.lastrowid}")
        elif opcao == "2":
            print("\n[Lista de Alunos]")
            cursor.execute("SELECT id, nome, idade, turma, notas, media, situacao FROM alunos")
            alunos = cursor.fetchall()
            for alu in alunos:
                print(f"ID: {alu[0]} | Nome: {alu[1]} | Turma: {alu[3]} | Notas: {alu[4]} | Média: {alu[5]} | Status: {alu[6]}")
        elif opcao == "3":
            print("\n[Editar Aluno]")
            id_alu = ler_inteiro("Digite o ID do Aluno que deseja editar: ")
            cursor.execute("SELECT id FROM alunos WHERE id = ?", (id_alu,))
            if cursor.fetchone():
                novo_nome = ler_texto("Novo Nome: ")
                nova_idade = ler_inteiro("Nova Idade: ")
                nova_turma = ler_texto("Nova Turma: ")
                cursor.execute("UPDATE alunos SET nome = ?, idade = ?, turma = ? WHERE id = ?", (novo_nome, nova_idade, nova_turma, id_alu))
                conexao.commit()
                print(" Dados atualizados!")
            else:
                print(" Aluno não encontrado.")
        elif opcao == "4":
            print("\n[Remover Aluno]")
            id_alu = ler_inteiro("Digite o ID do Aluno a remover: ")
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_alu,))
            conexao.commit()
            print(" Aluno removido do sistema.")
        elif opcao == "5":
            print("\n[Cadastrar Professor]")
            nome = ler_texto("Nome do Professor: ")
            idade = ler_inteiro("Idade: ")
            turma = ler_texto("Turma de Ensino (ex: 9A): ")
            senha = ler_texto("Senha: ")
            cursor.execute("INSERT INTO profesores (nome, idade, turma, senha) VALUES (?, ?, ?, ?)", (nome, idade, turma, senha))
            conexao.commit()
            print(f" Professor cadastrado! ID de acesso: {cursor.lastrowid}")
        elif opcao == "6":
            print("\n[Lista de Professores]")
            cursor.execute("SELECT id, nome, turma FROM professores")
            for prof in cursor.fetchall():
                print(f"ID: {prof[0]} | Nome: {prof[1]} | Turma Alocada: {prof[2]}")
        elif opcao == "7":
            conexao.close()
            break
        else:
            print(" Opção Inválida.")
        conexao.close()
 
# =====================================================================
# FUNÇÕES DO PROFESSOR (Gerenciamento Acadêmico)
# =====================================================================
def menu_professor(prof_id, prof_turma):
    while True:
        print(f"\n--- PAINEL DO PROFESSOR (Turma: {prof_turma}) ---")
        print("1. Listar/Buscar Alunos da Sala")
        print("2. Lançar Nova Nota")
        print("3. Limpar/Remover Notas de Aluno")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")
        conexao = _mysql_connector.connect("escola.db")
        cursor = conexao.cursor()
        if opcao == "1":
            print(f"\n[Alunos da Turma {prof_turma}]")
            cursor.execute("SELECT id, nome, notas, media, situacao FROM alunos WHERE turma = ?", (prof_turma,))
            alunos = cursor.fetchall()
            if not alunos:
                print("Nenhum aluno matriculado nesta turma.")
            for alu in alunos:
                print(f"Matrícula: {alu[0]} | Aluno: {alu[1]} | Notas: {alu[2]} | Média: {alu[3]} | Situação: {alu[4]}")
        elif opcao == "2":
            print("\n[Lançar Nota]")
            id_alu = ler_inteiro("Digite a matrícula do Aluno: ")
            cursor.execute("SELECT notas, turma FROM alunos WHERE id = ?", (id_alu,))
            resultado = cursor.fetchone()
            if resultado:
                notas_atuais = json.loads(resultado[0])
                turma_alu = resultado[1]
                if turma_alu != prof_turma and prof_turma != "ADMIN":
                    print(" Você só pode lançar notas para alunos da sua própria turma.")
                    continue
                nova_nota = ler_float("Digite a nota a adicionar (0-10): ")
                notas_atuais.append(nova_nota)
                media, situacao = calcular_situacao(notas_atuais)
                notas_json = json.dumps(notas_atuais)
                cursor.execute("UPDATE alunos SET notas = ?, media = ?, situacao = ? WHERE id = ?", (notas_json, media, situacao, id_alu))
                conexao.commit()
                print(" Nota lançada e situação atualizada!")
            else:
                print("Aluno não encontrado.")
        elif opcao == "3":
            print("\n[Remover Notas]")
            id_alu = ler_inteiro("Digite a matrícula do Aluno: ")
            cursor.execute("SELECT turma FROM alunos WHERE id = ?", (id_alu,))
            resultado = cursor.fetchone()
            if resultado:
                if resultado[0] != prof_turma and prof_turma != "ADMIN":
                    print(" Permissão negada para esta turma.")
                    continue
                cursor.execute("UPDATE alunos SET notas = '[]', media = 0.0, situacao = 'Reprovado' WHERE id = ?", (id_alu,))
                conexao.commit()
                print(" Histórico de notas zerado para este aluno.")
            else:
                print(" Aluno não encontrado.")

=======
import mysql.connector
import time

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Senac2026",
        database="trabalhoadsfinal"
    )

def login():
    print("Bem vindo ao nosso sistema")
    time.sleep(1)
    print("Direcionando a login...")
    time.sleep(2) 
    print("=-=-=-=-=-=-=-login-=-=-=-=-=-=-=")
    time.sleep(2)
    print("escolha uma das opçoes")
    
    print("1 - Estudante")
    print("2 - Professor")
    print("0 - Sair")
    
    while True:
        try:
            cargo = input("Digite seu cargo: ")
            if cargo == "1":
                time.sleep(2)
                print("Bem-vindo à área do aluno!")
                estudante()
            elif cargo == "2":
                time.sleep(2)
                print("Bem-vindo à área do professor!")
                prof()
            else: 
                break
        except ValueError:
            print('Erro, tente novamente!')
                
def estudante():
    nome = input('Digite seu nome: ')
    
    if any(c.isdigit() for c in nome):
        print("⚠️ Alerta: O nome contém números. O nome será corrigido. ")
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

login()
>>>>>>> 1b3bb5c671fb265ea415fc99bd61870e645ff28e
