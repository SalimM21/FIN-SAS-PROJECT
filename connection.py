from numpy import insert
import pandas as pd
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine, text
from dotenv import load_dotenv
import urllib.parse
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL1 = os.getenv("DATABASE_URL")
# Créer la chaîne de connexion PostgreSQL
DATABASE_URL1 = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL1)
print(DATABASE_URL1)

# Tester la connexion en exécutant une requête simple
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        print(" Connexion réussie !")
        print("Version PostgreSQL :", version)
except Exception as e:
    print(" Erreur de connexion :", e)

metadata = MetaData()

IndiceSante = Table(
    "IndiceSante",
    metadata,
    Column("seqn", Integer, primary_key=True, autoincrement=True),
    Column("smoking", String(50), nullable=False),
    Column("gender", String(100), nullable=False),
    Column("age", Integer, nullable=False),
    Column("education", String(20), nullable=True),
    Column("weight", Float, nullable=True),
    Column("height", Float, nullable=True),
    Column("bmi", Float, nullable=True)
)

# print(" Table 'IndiceSante' créée avec succès.")
metadata.create_all(engine)

# --- 5. Charger le fichier CSV dans un DataFrame pandas ---
# `delimiter` ou `sep` : Spécifie le séparateur (virgule par défaut pour read_csv)
# `header` : 0 si la première ligne est l'en-tête, None si pas d'en-tête

import pandas as pd

# print("\nAperçu des données lues du CSV :")
df = pd.read_csv('DataSet.csv' ,encoding='utf-8')
df = pd.DataFrame(df)
print(df)

# Renommez les colonnes du DataFrame si elles ne correspondent pas exactement aux noms de la table SQL
df = df.rename(columns={'seqn': 'seqn' ,'smoking':'smoking','gender':'gender','age':'age','education': 'education','weight':'weight','height':'height','bmi':'bmi'})

# Conversion des types pour correspondre à la table PostgreSQL
df['age'] = df['age'].astype(int)
df['smoking'] = df['smoking'].astype(str)
df['gender'] = df['gender'].astype(str)
df['education'] = df['education'].astype(str)
df['weight'] = df['weight'].astype(float)
df['height'] = df['height'].astype(float)
df['bmi'] = df['bmi'].astype(float)

print("\nAperçu des données après nettoyage et préparation :")
print(df.head())
print("\nInformations sur le DataFrame après nettoyage :")
print(df.info())

# --- 7. Insertion du DataFrame dans la table PostgreSQL ---
df.to_sql(name=IndiceSante, con=engine, if_exists='append', index=False)

print(f"\nDonnées du fichier CSV est insérées avec succès dans la table IndiceSante.")

with engine.begin() as connection:
    connection.execute(insert(IndiceSante), [
        {"smoking": "yes", "gender": "male", "age": 62, "education": "College or above", "weight": 94.8, "height": 184.5, "bmi": 27.8},
        {"smoking": "yes", "gender": "male", "age": 53, "education": "HS or GED", "weight": 90.4, "height": 171.4, "bmi": 30.8},
        {"smoking": "yes", "gender": "male", "age": 78, "education": "HS or GED", "weight": 83.4, "height": 170.1, "bmi": 28.8},
        {"smoking": "no",  "gender": "female", "age": 56, "education": "College or above", "weight": 109.8, "height": 160.9, "bmi": 42.4},
        {"smoking": "no",  "gender": "female", "age": 42, "education": "Some college / AA", "weight": 55.2, "height": 164.9, "bmi": 20.3},
        {"smoking": "no",  "gender": "female", "age": 72, "education": "9-11th grade", "weight": 64.4, "height": 150.0, "bmi": 28.6},
        {"smoking": "yes", "gender": "male", "age": 22, "education": "Some college / AA", "weight": 76.6, "height": 165.4, "bmi": 28.0},
        {"smoking": "no",  "gender": "female", "age": 32, "education": "Some college / AA", "weight": 64.5, "height": 151.3, "bmi": 28.2},
        {"smoking": "no",  "gender": "male", "age": 18, "education": "Some college / AA", "weight": 72.4, "height": 166.1, "bmi": 26.2}
    ])
    print("✅ Données insérées dans la table IndiceSante.")

# =============================================================
import csv
import psycopg2

conn = psycopg2.connect(
    dbname="healthDataCleaned",
    user="postgresql",
    password="123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS IndiceSante (
    id SERIAL PRIMARY KEY,
    smoking TEXT,
    gender TEXT,
    age INTEGER,
    education TEXT,
    weight REAL,
    height REAL,
    bmi REAL
)
""")

with open('data_cleaned.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
            INSERT INTO IndiceSante (smoking, gender, age, education, weight, height, bmi)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['smoking'],
            row['gender'],
            int(row['age']),
            row['education'],
            float(row['weight']),
            float(row['height']),
            float(row['bmi'])
        ))

conn.commit()
conn.close()
print("✅ Données insérées avec succès dans PostgreSQL.")

df.to_sql('health_data_cleaned', con=engine, if_exists='replace', index=False)