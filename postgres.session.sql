-- Insérer les données nettoyées dans une table PostgreSQL nommée, par exemple : health_data_cleaned

CREATE TABLE IndiceSante (
    seqn SERIAL PRIMARY KEY,
    smoking VARCHAR(50) NOT NULL,
    gender VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    education VARCHAR(20),
    weight FLOAT,
    height FLOAT,
    bmi FLOAT
);

INSERT INTO IndiceSante (smoking, gender, age, education, weight, height, bmi) VALUES
('yes', 'male', 62, 'College or above', 94.8, 184.5, 27.8),
('yes', 'male', 53, 'HS or GED', 90.4, 171.4, 30.8),
('yes', 'male', 78, 'HS or GED', 83.4, 170.1, 28.8),
('no', 'female', 56, 'College or above', 109.8, 160.9, 42.4),
('no', 'female', 42, 'Some college / AA', 55.2, 164.9, 20.3),
('no', 'female', 72, '9-11th grade', 64.4, 150.0, 28.6),
('yes', 'male', 22, 'Some college / AA', 76.6, 165.4, 28.0),
('no', 'female', 32, 'Some college / AA', 64.5, 151.3, 28.2),
('no', 'male', 18, 'Some college / AA', 72.4, 166.1, 26.2);

INSERT INTO IndiceSante (smoking, gender, age, education, weight, height, bmi) VALUES
('yes', 'female', 45, 'HS or GED', 78.6, 165.0, 28.9),
('no',  'male',   39, 'College or above', 88.2, 180.4, 27.1),
('yes', 'female', 29, 'Some college / AA', 60.3, 158.7, 24.0),
('no',  'male',   67, '9-11th grade', 70.1, 172.2, 23.6),
('yes', 'female', 51, 'College or above', 95.4, 168.3, 33.6);

COPY IndiceSante (smoking, gender, age, education, weight, height, bmi)
FROM 'C:\Users\PC\Desktop\Nouveau dossier\FIN-SAS-PROJECT\data_cleaned.csv'
WITH (FORMAT csv, HEADER true);

 
SELECT * FROM IndiceSante

-- Quelle est la répartition des individus par genre (gender)
SELECT
    gender,
    COUNT(*) AS nombre_individus
FROM
    IndiceSante
GROUP BY
    gender
ORDER BY
    nombre_individus DESC;

-- Quelle est la répartition des individus en fonction de leurs habitudes de tabagisme (smoking) ?
SELECT
    smoking,
    COUNT(*) AS nombre_individus
FROM
    IndiceSante
GROUP BY
    smoking
ORDER BY
    nombre_individus DESC;

-- Quelle est la moyenne de l'IMC (bmi) pour chaque genre (gender) ?
SELECT
    gender,
    AVG(bmi) AS moyenne_imc
FROM
    IndiceSante
GROUP BY
    gender;

-- Comment les individus se répartissent-ils en fonction de leur niveau d'éducation (education) ?
SELECT
    education,
    COUNT(*) AS nombre_individus
FROM
    IndiceSante
GROUP BY
    education
ORDER BY
    nombre_individus DESC;

-- Quelle est l'évolution de l'IMC moyen (bmi) en fonction des tranches d'âge (par exemple, 18-30, 31-50, 51+)
SELECT
    CASE
        WHEN age BETWEEN 0 AND 17 THEN '0-17 ans (Enfants/Ados)'
        WHEN age BETWEEN 18 AND 25 THEN '18-25 ans (Jeunes Adultes)'
        WHEN age BETWEEN 26 AND 35 THEN '26-35 ans (Adultes)'
        WHEN age BETWEEN 36 AND 50 THEN '36-50 ans (Adultes Murs)'
        WHEN age BETWEEN 51 AND 65 THEN '51-65 ans (Seniors)'
        ELSE '66+ ans (Aînés)'
    END AS tranche_age,
    AVG(bmi) AS moyenne_imc
FROM
    IndiceSante
WHERE
    bmi IS NOT NULL -- Exclure les lignes où l'IMC est NULL
GROUP BY
    tranche_age
ORDER BY
    MIN(age); -- Pour s'assurer que l'ordre des tranches d'âge est logique

-- Quelle est la moyenne d'âge (age) pour chaque catégorie de tabagisme (smoking) ?
SELECT
    smoking,
    AVG(age) AS moyenne_age
FROM
    IndiceSante
WHERE
    age IS NOT NULL -- Exclure les lignes où l'âge est NULL
GROUP BY
    smoking
ORDER BY
    smoking; -- Ou ORDER BY moyenne_age DESC; si vous préférez trier par l'âge moyen

