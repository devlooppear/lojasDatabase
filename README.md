# lojasDatabase

Este projeto é uma aplicação Python que gera e atualiza dados de teste em um banco de dados MySQL chamado "Lojas". Ele inclui tabelas para representar informações sobre estados, municípios, clientes, faturas de venda e contas a receber. O objetivo é criar um ambiente de teste para desenvolvimento e depuração de aplicações que utilizem esse banco de dados. Eu fiz porque tinham que fazer na facul esse banco de dados, mas eu quiz fazer um código de testes pra ter certeza que tava tudo certo.

Você pode encontrar este projeto no GitHub em: [lojasDatabase](https://github.com/devlooppear/lojasDatabase.git)

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- MySQL Server
- Bibliotecas Python: mysql.connector, Faker

Você pode instalar as bibliotecas Python necessárias executando o seguinte comando:

```
pip install -r requirements.txt
```

## Configuração
- Clone o repositório para o seu sistema local usando o seguinte comando:
```
git clone https://github.com/devlooppear/lojasDatabase.git
```

Acesse o diretório do projeto:
```
cd lojasDatabase
```

Certifique-se de ter um servidor MySQL em execução e ajuste as configurações de conexão no arquivo .env conforme necessário. inclusive crie um arquivo env, baseado com o que eu coloquei em `.env.example`:

```python
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_db_name
```

Importe a estrutura do banco de dados executando o seguinte comando no MySQL:

```sql
source table_lojas.sql;
```

Este comando irá criar as tabelas necessárias no seu banco de dados.

## Uso
Para gerar e atualizar dados de teste no banco de dados, execute o seguinte comando:

```
python main.py
```

Isso irá preencher as tabelas do banco de dados com dados de teste aleatórios.