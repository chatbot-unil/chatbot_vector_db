# Base de données vectorisée du projet chatbot

## Introduction

Ce git contient le code de la base de données vectorisée du projet chatbot. Il fait partie de mon projet de bachelor. Le but de ce projet est de créer un chatbot qui permet de répondre à des questions sur des données statistiques. Le chatbot sera capable de répondre à des questions sur des données statistiques provenant de l'annuaire statistique de l'Université de Lausanne ainsi que de faire des graphiques.

## Technologies utilisées

La base de données vectorisée sera contenue dans un conteneur Docker. La base de données vectorisée sera chromadb. Chromadb est une base de données vectorisée open-source qui permet de stocker des vecteurs. Ce répertoire contient tout le nécessaire pour lancer la base de données vectorisée. Elle sera utilisée pour stocker les vecteurs des données statistiques de l'annuaire statistique de l'Université de Lausanne. Et accessible via le backend du projet chatbot.

## Installation

La base de données vectorisée est contenue dans un conteneur Docker. Pour que cela sois pratique j'ai mis en place un Dockerfile et un docker-compose.yml. Pour lancer la base de données vectorisée il suffit de lancer la commande suivante :

```bash
docker-compose up
```

link docker hub : [chromadb](https://hub.docker.com/r/chromadb/chroma)
