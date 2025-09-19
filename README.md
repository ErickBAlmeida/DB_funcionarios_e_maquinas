# DB_funcionarios_e_maquinas

Este projeto tem como objetivo gerenciar colaboradores e máquinas de uma empresas, utilizando Python e SQLite para armazenamento dos dados. O sistema permite inserir, atualizar e remover informações de funcionários e equipamentos.

## Funcionalidades
- Cadastro de colaboradores
- Cadastro de máquinas
- Atualização e remoção de registros

## Estrutura do Projeto
- `banco.py`: Lógica de acesso ao banco de dados e manipulação dos registros
- `dicts.py`: Dicionários e listas auxiliares
- `UI.py`: Interface do usuário (arquivo de execução)

## Requisitos
- Python 3.11+
- SQLite3
- openpyxl (para manipulação de arquivos Excel)

## Como executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o arquivo principal:
   ```bash
   python UI.py
   ```

## Autor
Erick B Almeida