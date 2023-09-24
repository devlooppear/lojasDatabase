import mysql.connector
from mysql.connector import errorcode
from faker import Faker
import random
from datetime import date
import os
from dotenv import load_dotenv

# Connect to your MySQL server
try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Access denied. Check your MySQL username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist.")
    else:
        print("Error:", err)
    exit(1)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Initialize Faker for generating random data
fake = Faker()

# Function to execute SQL queries with error handling
def execute_query(query, data=None):
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        connection.rollback()

# Define functions to generate and refresh test data for each table

def generate_and_refresh_estado_data():
    # Generate data for the Estado table
    for _ in range(5):
        estado_row = (
            fake.state(),
            fake.state_abbr()
        )
        execute_query("INSERT INTO Estado (Nome, UF) VALUES (%s, %s)", estado_row)

def generate_and_refresh_municipio_data():
    # Generate data for the Municipio table
    for _ in range(10):
        municipio_row = (
            fake.city(),
            fake.state_abbr(),
            fake.random_int(10, 99)
        )
        execute_query("INSERT INTO Municipio (Nome, UF, DDD) VALUES (%s, %s, %s)", municipio_row)

def generate_and_refresh_cliente_data(estado_ids, municipio_ids):
    # Generate data for the Cliente table using the retrieved IDs
    for _ in range(10):
        cliente_row = (
            fake.name(),
            fake.unique.random_number(digits=11),
            fake.phone_number(),
            random.choice(municipio_ids),
            random.choice(estado_ids),
            fake.date_of_birth(minimum_age=18, maximum_age=80),
            fake.street_address(),
            fake.building_number(),
            fake.street_name(),
            fake.city(),
            fake.zipcode(),
            fake.phone_number(),
            fake.email()
        )
        execute_query("""
            INSERT INTO Cliente (Nome, CPF, Celular, Municipio_ID, Estado_ID, DataNascimento, 
            EndLogradouro, EndNumero, EndBairro, EndCidade, EndCEP, Telefone, Email) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, cliente_row)

def generate_and_refresh_faturavenda_data(cliente_ids):
    # Generate data for the FaturaVenda table using the retrieved Cliente IDs
    for _ in range(10):
        faturavenda_row = (
            random.choice(cliente_ids),
            fake.date_between(start_date="-1y", end_date="today"),
            round(random.uniform(10.0, 1000.0), 2)
        )
        execute_query("""
            INSERT INTO FaturaVenda (Cliente_ID, DataFatura, ValorTotal)
            VALUES (%s, %s, %s)
        """, faturavenda_row)

def generate_and_refresh_contareceber_data(cliente_ids, faturavenda_ids):
    # Generate data for the ContaReceber table using retrieved Cliente and FaturaVenda IDs
    for _ in range(20):
        contareceber_row = (
            random.choice(cliente_ids),
            random.choice(faturavenda_ids),
            fake.date_between(start_date="-1y", end_date="today"),
            fake.date_between(start_date="today", end_date="+90d"),
            round(random.uniform(10.0, 500.0), 2),
            random.choice(['Aberto', 'Pago', 'Cancelado']),
            fake.unique.random_number(digits=20)
        )
        execute_query("""
            INSERT INTO ContaReceber (Cliente_ID, FaturaVendaID, DataConta, DataVencimento, Valor, Situação, NúmeroDocumento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, contareceber_row)

def refresh_data():
    # Delete all existing data from tables
    execute_query("DELETE FROM ContaReceber")
    execute_query("DELETE FROM FaturaVenda")
    execute_query("DELETE FROM Cliente")
    execute_query("DELETE FROM Municipio")
    execute_query("DELETE FROM Estado")

# Refresh data by deleting existing records
refresh_data()

# Generate and refresh data for all tables
generate_and_refresh_estado_data()
generate_and_refresh_municipio_data()

# Retrieve the IDs created for Estado and Municipio
cursor.execute("SELECT ID FROM Estado")
estado_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ID FROM Municipio")
municipio_ids = [row[0] for row in cursor.fetchall()]

generate_and_refresh_cliente_data(estado_ids, municipio_ids)

# Retrieve the IDs created for Cliente
cursor.execute("SELECT ID FROM Cliente")
cliente_ids = [row[0] for row in cursor.fetchall()]

generate_and_refresh_faturavenda_data(cliente_ids)

# Retrieve the IDs created for FaturaVenda
cursor.execute("SELECT ID FROM FaturaVenda")
faturavenda_ids = [row[0] for row in cursor.fetchall()]

generate_and_refresh_contareceber_data(cliente_ids, faturavenda_ids)

# Close the cursor and the database connection
cursor.close()
connection.close()
