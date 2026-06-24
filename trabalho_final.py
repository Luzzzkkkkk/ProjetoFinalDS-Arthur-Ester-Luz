import mysql.connector
from mysql.connector import Error
import secrets
import string

#conexão

def conexão():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',       
            password='Senac2026',      
            database='sistema_escolar'
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def obter_texto_valido(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if entrada:
            return entrada
        print("Erro: Este campo não pode ficar vazio.")

def obter_inteiro_valido(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: Digite um número inteiro válido.")

def obter_nota_valida(mensagem):
    while True:
        try:
            nota = float(input(mensagem))
            if 0.0 <= nota <= 10.0:
                return nota
            print("Erro: A nota deve ser entre 0 e 10.")
        except ValueError:
            print("Erro: Digite um número decimal válido.")

def obter_nome_valido(mensagem):
    """Garante que o nome contenha apenas letras e espaços, sem números ou símbolos."""
    while True:
        nome = input(mensagem).strip()

#tira espaço em branco 
        if nome.replace(" ", "").isalpha():
            return nome
        print("Erro: O nome não pode conter números ou caracteres especiais. Digite novamente.")

def gerar_senha_aleatoria(tamanho=8):
    """Gera uma senha segura com letras e números."""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

def calcular_media_e_situacao(notas):
    if not notas:
        return 0.0, "Reprovado"
    
    soma = 0.0
    for n in notas:
        soma += n
    media = round(soma / len(notas), 2)
    
    if media >= 7.0:
        situacao = "Aprovado"
    elif media >= 5.0:
        situacao = "Recuperacao"
    else:
        situacao = "Reprovado"
        
    return media, situacao

def atualizar_media_banco(conexao, matricula):
    cursor = conexao.cursor()
    cursor.execute("SELECT nota FROM notas_alunos WHERE matricula_FK = %s AND nota IS NOT NULL", (matricula,))
    resultados = cursor.fetchall()
    
    notas = []
    for r in resultados:
        notas.append(float(r[0]))
        
    media, situacao = calcular_media_e_situacao(notas)
    
    cursor.execute("""
        UPDATE notas_alunos 
        SET media = %s, situacao = %s 
        WHERE matricula_FK = %s
    """, (media, situacao, matricula))
    conexao.commit()

#professores

def cadastrar_professor(conexao):
    print("\n--- CADASTRO DE PROFESSOR ---")
    nome = obter_nome_valido("Nome do Professor: ")
    materia = obter_texto_valido("Matéria/Disciplina: ")
    
    senha_provisoria = gerar_senha_aleatoria()
    
    cursor = conexao.cursor()
    comando = "INSERT INTO professores (nome, materia, senha) VALUES (%s, %s, %s)"
    cursor.execute(comando, (nome, materia, senha_provisoria))
    conexao.commit()
    
    id_prof = cursor.lastrowid
    print(f"Professor cadastrado com sucesso! ID gerado: {id_prof}")
    print(f"SENHA GERADA: {senha_provisoria} (Anote e passe para o professor)")

def listar_professores(conexao):
    print("\n--- LISTA DE PROFESSORES ---")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, materia FROM professores")
    professores = cursor.fetchall()
    
    if not professores:
        print("Nenhum professor cadastrado.")
        return
        
    for prof in professores:
        print(f"ID: {prof[0]} | Nome: {prof[1]} | Matéria: {prof[2]}")

def editar_professor(conexao):
    print("\n--- EDITAR PROFESSOR ---")
    id_prof = obter_inteiro_valido("Digite o ID do professor para editar: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM professores WHERE id = %s", (id_prof,))
    if not cursor.fetchone():
        print("Professor não encontrado.")
        return
        
    novo_nome = obter_nome_valido("Novo Nome: ")
    nova_materia = obter_texto_valido("Nova Matéria: ")
    
    cursor.execute("""
        UPDATE professores 
        SET nome = %s, materia = %s 
        WHERE id = %s
    """, (novo_nome, nova_materia, id_prof))
    conexao.commit()
    print("Dados do professor atualizados com sucesso!")

def remover_professor(conexao):
    print("\n--- REMOVER PROFESSOR ---")
    id_prof = obter_inteiro_valido("Digite o ID do professor para remover: ")
    
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM professores WHERE id = %s", (id_prof,))
    conexao.commit()
    print("Professor removido com sucesso.")

#aluno e nota

def cadastrar_aluno(conexao):
    print("\n--- CADASTRO DE ALUNO ---")
    nome = obter_nome_valido("Nome do Aluno: ")
    idade = obter_inteiro_valido("Idade: ")
    turma = obter_texto_valido("Turma: ")
    
    cursor = conexao.cursor()
    comando = "INSERT INTO alunos (nome, idade, turma) VALUES (%s, %s, %s)"
    cursor.execute(comando, (nome, idade, turma))
    conexao.commit()
    
    matricula = cursor.lastrowid
    print(f"Aluno cadastrado com sucesso! Matrícula gerada: {matricula}")

def listar_alunos(conexao):
    print("\n--- LISTA DE ALUNOS ---")
    cursor = conexao.cursor()
    cursor.execute("SELECT matricula, nome, idade, turma FROM alunos")
    alunos = cursor.fetchall()
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
        
    for aluno in alunos:
        print(f"Matrícula: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | Turma: {aluno[3]}")

def editar_aluno(conexao):
    print("\n--- EDITAR ALUNO ---")
    matricula = obter_inteiro_valido("Digite a matrícula do aluno para editar: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM alunos WHERE matricula = %s", (matricula,))
    if not cursor.fetchone():
        print("Aluno não encontrado.")
        return
        
    novo_nome = obter_nome_valido("Novo Nome: ")
    nova_idade = obter_inteiro_valido("Nova Idade: ")
    nova_turma = obter_texto_valido("Nova Turma: ")
    
    cursor.execute("""
        UPDATE alunos SET nome = %s, idade = %s, turma = %s WHERE matricula = %s
    """, (novo_nome, nova_idade, nova_turma, matricula))
    conexao.commit()
    print("Dados do aluno atualizados com sucesso!")

def remover_aluno(conexao):
    print("\n--- REMOVER ALUNO ---")
    matricula = obter_inteiro_valido("Digite a matrícula do aluno para remover: ")
    
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM notas_alunos WHERE matricula_FK = %s", (matricula,))
    cursor.execute("DELETE FROM alunos WHERE matricula = %s", (matricula,))
    conexao.commit()
    print("Aluno e suas respectivas notas foram removidos.")

def buscar_aluno_por_nome(conexao):
    print("\n--- BUSCAR ALUNO ---")
    nome_busca = obter_texto_valido("Digite o nome ou parte do nome: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT matricula, nome, turma FROM alunos WHERE nome LIKE %s", (f"%{nome_busca}%",))
    resultados = cursor.fetchall()
    
    if not resultados:
        print("Nenhum aluno encontrado.")
        return
        
    for r in resultados:
        print(f"Matrícula: {r[0]} | Nome: {r[1]} | Turma: {r[2]}")

def gerenciar_notas_turma(conexao):
    print("\n--- LANÇAMENTO DE NOTAS POR TURMA ---")
    turma = obter_texto_valido("Digite a turma que deseja buscar: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT matricula, nome FROM alunos WHERE turma = %s", (turma,))
    alunos = cursor.fetchall()
    
    if not alunos:
        print("Nenhum aluno encontrado nesta turma.")
        return
        
    print(f"\nAlunos da Turma {turma}:")
    for a in alunos:
        print(f"ID/Matrícula: {a[0]} - Nome: {a[1]}")
        
    matricula = obter_inteiro_valido("\nDigite a matrícula do aluno para gerenciar as notas: ")

    cursor.execute("SELECT nome FROM alunos WHERE matricula = %s AND turma = %s", (matricula, turma))
    aluno_encontrado = cursor.fetchone()
    
    if not aluno_encontrado:
        print("Erro: Este aluno não pertence a esta turma ou não existe.")
        return

    print(f"\n1 - Adicionar Nota\n2 - Remover Notas Existentes\n0 - Voltar Menu")
    while True:
        opcao = obter_inteiro_valido("Escolha uma opção: ")
        
        if opcao == 1:
            nota = obter_nota_valida("Digite a nota (0.0 a 10.0): ")
            cursor.execute("INSERT INTO notas_alunos (matricula_FK, nota) VALUES (%s, %s)", (matricula, nota))
            conexao.commit()
            atualizar_media_banco(conexao, matricula)
            print("Nota registrada!")
            print("\n1 - Adicionar Nota\n2 - Remover Notas Existentes\n0 - Voltar Menu")
            
        elif opcao == 2:
            cursor.execute("DELETE FROM notas_alunos WHERE matricula_FK = %s", (matricula,))
            conexao.commit()
            atualizar_media_banco(conexao, matricula)
            print("Notas removidas e médias resetadas.")
            print("\n1 - Adicionar Nota\n2 - Remover Notas Existentes\n0 - Voltar Menu")
            
        elif opcao == 0:
            print("Voltando ao menu anterior...")
            break
        else:
            print("Essa opção não é válida, tente novamente.")

#login aluno/professor

def painel_aluno(conexao):
    print("\n--- PAINEL DO ALUNO ---")

def painel_aluno(conexao):
    print("\n--- PAINEL DO ALUNO ---")
    matricula = obter_inteiro_valido("Digite sua matrícula para acessar suas notas: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, turma FROM alunos WHERE matricula = %s", (matricula,))
    aluno = cursor.fetchone()
    
    if not aluno:
        print("Matrícula não cadastrada.")
        return
        
    print(f"\nBem-vindo(a), {aluno[0]} | Turma: {aluno[1]}")
    
    cursor.execute("SELECT nota FROM notas_alunos WHERE matricula_FK = %s AND nota IS NOT NULL", (matricula,))
    linhas_notas = cursor.fetchall()
    
    if not linhas_notas:
        print("Nenhuma nota lançada para você ainda.")
        return
        
    print("Suas Notas: ", end="")
    notas_lista = []
    for ln in linhas_notas:
        notas_lista.append(str(ln[0]))
    print(", ".join(notas_lista))
    
    cursor.execute("SELECT DISTINCT media, situacao FROM notas_alunos WHERE matricula_FK = %s", (matricula,))
    resultado_final = cursor.fetchone()
    
    if resultado_final:
        print(f"Sua Média Atual: {resultado_final[0]}")
        print(f"Situação: {resultado_final[1]}")


def login_professor(conexao):
    print("\n--- ACESSO DO PROFESSOR ---")
    id_prof = obter_inteiro_valido("Digite seu ID de Professor: ")
    senha = obter_texto_valido("Digite sua senha: ")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM professores WHERE id = %s AND senha = %s", (id_prof, senha))
    professor = cursor.fetchone()
    
    if not professor:
        print("Erro: ID ou Senha incorretos.")
        return
        
    print(f"\nBem-vindo(a), Prof. {professor[0]}!")
    while True:
        print("\n--- MENU PROFESSOR ---")
        print("1. Pesquisar Sala e Lançar/Remover Notas")
        print("0. Voltar")
        
        sub_opcao = obter_inteiro_valido("Opção: ")
        
        if sub_opcao == 1:
            gerenciar_notas_turma(conexao)
        elif sub_opcao == 0:
            break

def cadastrar_professor(conexao):
    print("\n--- CADASTRO DE PROFESSOR ---")
    nome = obter_nome_valido("Nome do Professor: ")
    materia = obter_texto_valido("Matéria/Disciplina: ")
    
    senha_provisoria = gerar_senha_aleatoria()
    
    cursor = conexao.cursor()
    comando = "INSERT INTO professores (nome, materia, senha) VALUES (%s, %s, %s)"
    cursor.execute(comando, (nome, materia, senha_provisoria))
    conexao.commit()
    
    id_prof = cursor.lastrowid
    print(f"Professor cadastrado com sucesso! ID gerado: {id_prof}")
    print(f"SENHA GERADA: {senha_provisoria} (Anote e passe para o professor)")


#menu

def menu():
    conexao = conexão()
    if not conexao:
        return

    while True:
        print("\n===============================")
        print("    SISTEMA ESCOLAR PYTHON     ")
        print("===============================")
        print("1. Entrar como Secretário Escolar")
        print("2. Entrar como Professor")
        print("3. Entrar como Aluno")
        print("0. Sair")
        
        opcao = obter_inteiro_valido("Escolha seu perfil: ")
        
        if opcao == 1:
            while True:
                print("\n--- MENU SECRETÁRIO ---")
                print("1. Cadastrar Aluno")
                print("2. Listar Alunos")
                print("3. Editar Aluno")
                print("4. Remover Aluno")
                print("5. Buscar Aluno por Nome")
                print("6. Cadastrar Professor")
                print("7. Listar Professores")
                print("8. Editar Professor")
                print("9. Remover Professor")
                print("0. Voltar")
                
                sub_opcao = obter_inteiro_valido("Opção: ")
                
                if sub_opcao == 1: cadastrar_aluno(conexao)
                elif sub_opcao == 2: listar_alunos(conexao)
                elif sub_opcao == 3: editar_aluno(conexao)
                elif sub_opcao == 4: remover_aluno(conexao)
                elif sub_opcao == 5: buscar_aluno_por_nome(conexao)
                elif sub_opcao == 6: cadastrar_professor(conexao)
                elif sub_opcao == 7: listar_professores(conexao)
                elif sub_opcao == 8: editar_professor(conexao)
                elif sub_opcao == 9: remover_professor(conexao)
                elif sub_opcao == 0: break
        
        elif opcao == 2:
            login_professor(conexao)
                
        elif opcao == 3:
            painel_aluno(conexao)
            
        elif opcao == 0:
            print("Encerrando o sistema...")
            conexao.close()
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()

# CREATE DATABASE IF NOT EXISTS sistema_escolar;

# USE sistema_escolar;

# CREATE TABLE IF NOT EXISTS alunos (
#     matricula INT AUTO_INCREMENT PRIMARY KEY,
#     nome VARCHAR(100) NOT NULL,
#     idade TINYINT UNSIGNED NOT NULL,
#     data_nascimento DATE,
#     turma VARCHAR(100) NOT NULL,
#     criacao_conta DATETIME DEFAULT CURRENT_TIMESTAMP
# );
# ALTER TABLE alunos MODIFY COLUMN turma VARCHAR(255);

# CREATE TABLE IF NOT EXISTS notas_alunos (
#     id_nota INT AUTO_INCREMENT PRIMARY KEY,
#     matricula_FK INT NOT NULL,
#     nota DECIMAL(4,2),
#     media DECIMAL(4,2) DEFAULT 0.00,
#     situacao ENUM('Aprovado', 'Recuperacao', 'Reprovado'),
#     FOREIGN KEY (matricula_FK) REFERENCES alunos(matricula)
# );

# CREATE TABLE IF NOT EXISTS professores (
#     id INT AUTO_INCREMENT PRIMARY KEY,          
#     nome VARCHAR(100) NOT NULL,
#     idade TINYINT UNSIGNED NULL,                 
#     data_nascimento DATE NULL,                  
#     materia VARCHAR(50) NOT NULL,                
#     senha VARCHAR(255) NOT NULL 
# );
# USE sistema_escolar;

# ALTER TABLE professores ADD COLUMN senha VARCHAR(255) NOT NULL;

# CREATE TABLE IF NOT EXISTS secretario (
#    id_secretario INT NOT NULL,
#    nome VARCHAR(100),
#    idade TINYINT UNSIGNED NOT NULL,
#    data_nascimento DATE
# );

# SELECT * FROM alunos;
# SELECT * FROM notas_alunos;
# SELECT * FROM professores;
# SELECT * FROM secretario;
