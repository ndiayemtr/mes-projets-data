# Network Quality Prediction & Decision Dashboard

## Contexte

Dans les réseaux télécom, la qualité de service est un enjeu critique.  
Les opérateurs doivent **détecter rapidement les dégradations réseau** pour améliorer l’expérience utilisateur et réduire le churn.

 Ce projet propose un **système intelligent de monitoring et de prédiction de la qualité réseau** basé sur la Data Science.

---

## Objectif

Construire un modèle capable de :

- Prédire la qualité réseau (**Good / Medium / Poor**)
- Détecter efficacement les cas critiques (**Poor**)  
- Fournir un **outil d’aide à la décision** via un dashboard interactif  

---

## Approche Data Science

### Data Engineering
- Simulation d’un dataset réaliste (>50 000 lignes)
- Injection de valeurs manquantes et nettoyage
- Feature engineering avancé :
  - `speed_efficiency`
  - `location_risk`
  - `weather_impact`
  - `peak_usage`

---

### Feature Selection (niveau pro)

- Suppression des variables non pertinentes (IDs, timestamps)
- Détection et suppression du **data leakage**
- Sélection basée sur :
  - importance des variables (Random Forest)
  - logique métier télécom

---

### Modélisation

- Modèle principal : **XGBoost**
- Gestion du déséquilibre via **sample_weight**
- Optimisation orientée métier :
  - priorité au **recall des cas "Poor"**

---

## 📊 Résultats

| Classe | Recall |
|-------|--------|
| 🔴 Poor | **52%** |
| 🟠 Medium | 39% |
| 🟢 Good | 76% |

 Le modèle privilégie la détection des problèmes réseau,  
ce qui est **crucial en production**.

---

## Insights métier

- 📉 La qualité réseau se dégrade fortement en **heures de pointe**
- 🌧️ Les conditions météo impactent les performances
- 📍 Certaines zones présentent un risque plus élevé
- 📶 Le type de réseau influence directement la qualité perçue

---

## 🖥️ Dashboard (Streamlit)

Application interactive :

- 📊 KPI globaux (qualité réseau, usage, performance)
- 🎛️ Filtres dynamiques (réseau, zone, heure)
- 📈 Visualisation des tendances
- 🔮 Simulation de scénarios en temps réel

 Objectif :
> **Aider les opérateurs à anticiper et corriger les problèmes réseau**

---

## 🛠️ Stack technique

- Python
- Pandas / NumPy
- Scikit-learn
- XGBoost
- Streamlit

---

## 📁 Structure du projet
qualite_de_service/
├── app.py # Dashboard Streamlit
├── model.pkl # Modèle entraîné
├── data.csv # Dataset utilisé
├── utils.py # Fonctions de prédiction
├── requirements.txt
└── README.md
└── qualite_de_service.ipynb


---

## 🚀 Démo

👉 [Lien vers l'application Streamlit] *(à ajouter)*

---

## Valeur ajoutée

✔ Projet orienté **problème réel télécom**  
✔ Approche **end-to-end** (data → modèle → dashboard)  
✔ Optimisation basée sur **enjeux métier (recall critique)**  
✔ Projet directement **exploitable en production**

---

## Contact

N’hésite pas à me contacter pour échanger sur ce projet ou des opportunités.

Ingénieur en transition vers la Data Science, je développe des solutions basées sur les données pour résoudre des problématiques concrètes dans les systèmes complexes (télécom, logistique, transport).

--> Ouvert à des opportunités à fort impact.