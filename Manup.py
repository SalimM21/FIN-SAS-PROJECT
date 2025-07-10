import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('DataSet.csv', encoding='utf-8')
# Afficher les 5 premières lignes du DataFrame
# print(df.head( n=5))

# Afficher la taille (dimensions) du dataset (lignes, colonnes)
print(df.shape)

# Lister les colonnes disponibles dans le dataset
print(df.columns)

# Créer un sous-ensemble du jeu de données contenant uniquement les colonnes suivantes :
# ['SEQN','SMQ020', 'RIAGENDR', 'RIDAGEYR','DMDEDUC2','BMXWT', 'BMXHT', 'BMXBMI']

df = df[['SEQN','SMQ020', 'RIAGENDR', 'RIDAGEYR','DMDEDUC2','BMXWT', 'BMXHT', 'BMXBMI']]
# Afficher les 5 premières lignes du DataFrame
print(df.head(5))

# Afficher les informations générales (.info()) sur ce sous-ensemble
print(df.info())

# Renommer les colonnes avec des noms plus explicites :
# ['seqn','smoking','gender', 'age','education','weight','height','bmi']
df = df.rename(columns={'SEQN' : 'seqn','SMQ020' :'smoking','RIAGENDR' :'gender', 'RIDAGEYR' :'age','DMDEDUC2' : 'education','BMXWT' : 'weight','BMXHT' : 'height','BMXBMI' : 'bmi'})

print(df.head(5))

# Vérifier la présence de doublons dans le dataset
print(df.duplicated().sum())

# Supprimer les doublons si nécessaire
df.drop_duplicates(inplace=True)

# Supprimer la colonne 'seqn', considérée comme un identifiant inutile pour l’analyse
df.drop('seqn', axis=1, inplace=True)

# Identifier les valeurs manquantes (NaN) dans les colonnes.
print(df.isnull().sum())

# Remplacer les valeurs manquantes :

# education : remplacer par la médiane
df['education'].fillna(df['education'].median(), inplace=True)
# weight, height, bmi : remplacer par la moyenne
df['weight'].fillna(df['weight'].mean(), inplace=True)

# Afficher les statistiques descriptives (moyenne, écart-type, min, max, etc.) du dataset
print(df.describe())

# Détecter les valeurs aberrantes (outliers) à l’aide de méthodes statistiques
# (Q1, Q2 , Q3)

Q1 = df['bmi'].quantile(0.25)  # 25ème centile
Q2 = df['bmi'].quantile(0.50)  # Médiane
Q3 = df['bmi'].quantile(0.75)  # 75ème centile

print(f"Q1 = {Q1}, Q2 (Médiane) = {Q2}, Q3 = {Q3}")

# Supprimer les outliers pour améliorer la qualité des données
# Définir les seuils corrects
IQR = Q3-Q1
# Filtrer les données
df_clean = df[(df['bmi'] >= Q1 - 1.5 * IQR) & (df['bmi'] <= Q3 + 1.5 * IQR)]
print("Données nettoyées (sans outliers) :\n", df_clean)

# Remplacer les codes numériques par des labels explicites dans trois colonnes :
# smoking : {1: 'yes', 2: 'no', 7: nan, 8: nan}
# gender : {1: 'male', 2: 'female'}
# education : {1: '<9th grade', 2: '9-11th grade', 3: 'HS or GED', 4: 'Some college / AA', 5: 'College or above', 7: 'Other', 8: 'Other'}

smoking_mapping = {
    1: 'yes',
    2: 'no',
    7: np.nan,  
    8: np.nan  
}

# Appliquer le mapping à la colonne
df['smoking'] = df['smoking'].map(smoking_mapping)

print(df)
 
# gender : {1: 'male', 2: 'female'}
gender_mapping = {
    1: 'male',
    2: 'female'
    }

df['gender'] = df['gender'].map(gender_mapping)
print(df)

# education : {1: '<9th grade', 2: '9-11th grade', 3: 'HS or GED', 4: 'Some college / AA', 5: 'College or above', 7: 'Other', 8: 'Other'}
education_mapping = {
    1: '<9th grade',
    2: '9-11th grade',
    3: 'HS or GED',
    4: 'Some college / AA',
    5: 'College or above', 
    7: 'Other', 
    8: 'Other'
    }
df['education'] = df['education'].map(education_mapping)
print(df)

# Analyser les relations entre variables :
# Utiliser Seaborn Pairplot pour visualiser les relations entre toutes les variables
sns.pairplot(df)
plt.show()

# Créer des graphiques individuels pour observer la distribution ou la corrélation de chaque attribut.
# Calculer la matrice de corrélation sur les colonnes numériques
corr_matrix = df.select_dtypes(include=[np.number]).corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Matrice de Corrélation')
plt.show()

# Sauvegarder le dataset nettoyé au format CSV
df.to_csv('data_cleaned.csv', index=False)



