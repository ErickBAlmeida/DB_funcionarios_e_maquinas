import os
import sqlite3

from dotenv import load_dotenv


load_dotenv()

class Banco:
    def __init__(self):
        self.banco = sqlite3.connect(os.getenv("caminho_bd"))
        self.cursor = self.banco.cursor()
    
    def inserir_dados(self, tabela, dados: dict):
        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["?" for _ in dados])
        valores = tuple(dados.values())

        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, valores)
            self.banco.commit()

            print(f"✅ {next(iter(dados.values()))} inserido na tabela '{tabela}' com sucesso!")

        except sqlite3.IntegrityError as e:
            print(f"❌ Algum dado único do(a) {dados['nome']} já está cadastrado na tabela '{tabela}'.")

        except sqlite3.Error as e:
            print(f"❌ ERRO GERAL DO SQLITE: {e}")

        except Exception as e:
            print(f"❌ Detalhes do erro: {e}")

    def remover_dados(self, tabela, valor):
        if tabela == "Maquinas":
            sql = f"DELETE FROM {tabela} WHERE Placa = {valor}"
        
        elif tabela == "Colaboradores": 
            sql = f"DELETE FROM {tabela} WHERE nome = '{valor}'"
        
        try:
            self.cursor.execute(sql)
            self.banco.commit()

            print(f"✅ {valor} removido com sucesso!")

        except sqlite3.Error as e:
            print(f"❌ ERRO GERAL DO SQLITE: {e}")

        except Exception as e:
            print(f"❌ Detalhes do erro: {e}")

    def fechar_banco(self):
        self.cursor.close()
        self.banco.close()

# banco = Banco()
# planilha = Planilha(banco)
# planilha.iterar_planilha()
# banco.fechar_banco()