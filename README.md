﻿# Application de QCM Informatique

## 👥 Auteurs

- IMANSOURA Ramy
- IZEM Mohammed Amine
- HAMMAMTI Mohammed Fares Yacine
- HADDAD Chahinez

## 📝 Description
Une application console interactive permettant de passer des QCM sur différentes thématiques informatiques. L'application gère le temps, les scores et l'historique des utilisateurs.

## 🎯 Fonctionnalités

- ✅ Système de connexion/création d'utilisateur
- ⏱️ Chronomètre de 30 secondes par question
- 📊 Suivi des scores et historique des parties
- 📁 Export des résultats en CSV
- 🔄 Gestion de plusieurs catégories de questions
- 💡 Explications des réponses correctes

## 🔧 Installation

1. Clonez le repot :
```bash
git clone [url-du-repo]
cd AP-QCM-Project
```

2. Assurez-vous d'avoir Python 3.x installé
3. Aucune dépendance externe n'est requise

## 🚀 Utilisation

Pour lancer l'application :
```bash
python main.py
```

### Menu Principal
1. Commencer un nouveau QCM
2. Voir mon historique
3. Exporter mes résultats
4. Changer d'utilisateur
5. Quitter

## 📁 Structure des données

### Format des questions (data/questions.json)
```json
{
    "Catégorie": [
        {
            "question": "Question posée ?",
            "options": {
                "a": "Réponse A",
                "b": "Réponse B",
                "c": "Réponse C"
            },
            "correct": "lettre_correcte",
            "explanation": "Explication de la réponse"
        }
    ]
}
```

### Format des données utilisateur (data/users.json)
```json
{
    "nom_utilisateur": {
        "history": [
            {
                "date": "YYYY-MM-DD HH:MM",
                "category": "nom_categorie",
                "score": X,
                "total": Y,
                "time_taken": Z
            }
        ]
    }
}
```

## ⚙️ Fonctionnement technique

- La classe `Timer` gère le chronométrage des questions
- La classe `QCMApp` gère la logique principale de l'application
- Les données sont persistantes grâce au stockage JSON
- L'historique peut être exporté en CSV

## 🔒 Gestion des erreurs

- Validation des entrées utilisateur
- Gestion du temps dépassé
- Sauvegarde automatique des données
- Création automatique des fichiers nécessaires
