from os import getenv

import psycopg

def criar_banco():
    try:
        # Conectando ao banco de dados
        password = getenv('PG_PASSWORD')
        conn = psycopg.connect(f'postgresql://postgres:{password}@db:5432/postgres')
        cursor = conn.cursor()
        print("Conectado ao banco de dados 'banco.db'.")

        # Criando a tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id BIGSERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            municipio TEXT NOT NULL,
            cpf TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cnes TEXT NOT NULL,
            profissao TEXT,
            senha TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            ativo INTEGER DEFAULT 1,
            is_admin INTEGER DEFAULT 0,
            is_super_admin INTEGER DEFAULT 0,  -- Novo campo para perfil estadual
            role TEXT DEFAULT 'municipal'     -- Campo existente
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculos (
            id BIGSERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            codigo_ficha TEXT NOT NULL UNIQUE,
            nome_gestante TEXT NOT NULL,
            data_nasc TEXT NOT NULL,
            telefone TEXT NOT NULL,
            municipio TEXT NOT NULL,
            ubs TEXT NOT NULL,
            acs TEXT NOT NULL,
            periodo_gestacional TEXT NOT NULL,
            data_envio TEXT NOT NULL,
            pontuacao_total INTEGER NOT NULL,
            classificacao_risco TEXT NOT NULL,
            imc REAL,
            caracteristicas TEXT,
            avaliacao_nutricional TEXT,
            comorbidades TEXT,
            historia_obstetrica TEXT,
            condicoes_gestacionais TEXT,
            profissional TEXT NOT NULL,
            desfecho TEXT,
            data_desfecho TEXT,
            FOREIGN KEY (user_id) REFERENCES usuarios (id)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS acoes_administrativas (
            id BIGSERIAL PRIMARY KEY,
            admin_id INTEGER NOT NULL,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            data_acao TEXT NOT NULL,
            detalhes TEXT,
            FOREIGN KEY (admin_id) REFERENCES usuarios (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        print("Tabela 'usuarios' verificada/criada.")
        # Salvando e fechando a conexão
        conn.commit()
        print("Banco de dados e tabelas 'usuarios', 'calculos' e 'acoes_administrativas' inicializados com sucesso.")

    except psycopg.Error as e:
        print(f"Erro ao configurar o banco de dados: {str(e)}")
        raise
    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    criar_banco()
