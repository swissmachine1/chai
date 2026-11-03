# Carnet de chai

Une petite app pour téléphone qui sert de carnet de cave. On y suit chaque cuve et chaque barrique : état du vin, opérations faites (soutirage, remontage, ouillage, SO₂...), notes et transferts. Tout le monde qui a le code voit les mêmes données, même hors ligne.

L'app tourne gratuitement sur **Cloudflare**, un service qui héberge des petits programmes en ligne. Ce guide explique comment installer ta propre copie. Compte environ **20 minutes**, sans rien payer.

Ce qu'il te faut : un **Mac** (le script d'installation ne marche pas tel quel sur Windows) et une adresse email.

---

## 1. Créer le compte Cloudflare (5 min)

1. Va sur [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) et crée un compte avec ton email et un mot de passe.
2. Ouvre l'email de Cloudflare et clique sur le lien de confirmation. Sans cette étape, l'installation échoue.
3. Le plan **Free** (gratuit) suffit. Pas besoin de carte bancaire.
4. Dans le menu de gauche, clique sur **Workers & Pages** (parfois appelé **Compute (Workers)**). Si Cloudflare te demande de choisir un **sous-domaine workers.dev**, choisis un nom simple, par exemple le nom de ton domaine viticole. Il apparaîtra dans l'adresse de ton app.

## 2. Récupérer deux informations sur Cloudflare (5 min)

**L'identifiant du compte (Account ID)**
Une fois connecté, regarde l'adresse de la page dans ton navigateur : `dash.cloudflare.com/` suivi d'une suite de **32 lettres et chiffres**. C'est ton identifiant. Copie-le.

**Le jeton (Token), qui autorise le script à installer l'app**
1. Va sur [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens).
2. Clique sur **Créer un jeton** (Create Token).
3. Sur la ligne **Modifier les Cloudflare Workers** (Edit Cloudflare Workers), clique sur **Utiliser le modèle**.
4. Dans **Ressources du compte**, choisis ton compte. Dans **Ressources de zone**, choisis **Toutes les zones**.
5. Clique sur **Continuer vers le résumé**, puis **Créer le jeton**.
6. Copie le jeton tout de suite : Cloudflare ne le montre **qu'une seule fois**.

## 3. Télécharger l'app (2 min)

1. Sur cette page GitHub, clique sur le bouton vert **Code**, puis **Download ZIP**.
2. Ouvre le fichier téléchargé : un dossier **chai-main** apparaît. Range-le où tu veux, par exemple dans Documents.

## 4. Remplir le fichier de réglages (3 min)

1. Ouvre l'app **Terminal** : appuie sur `Cmd + Espace`, tape `Terminal`, puis `Entrée`.
2. Tape `cd ` (avec un espace à la fin), **glisse le dossier chai-main** dans la fenêtre du Terminal, puis appuie sur `Entrée`.
3. Copie-colle cette ligne et appuie sur `Entrée` :
   ```
   cp env.example .env && open -e .env
   ```
4. Le fichier `.env` s'ouvre dans TextEdit. Colle tes informations après chaque `=`, sans espace :
   ```
   CLOUDFLARE_ACCOUNT_ID=ton identifiant de 32 caractères
   CLOUDFLARE_WORKERS_TOKEN=ton jeton
   CHAI_PIN=un code d'au moins 6 chiffres
   ```
5. Enregistre (`Cmd + S`) et ferme TextEdit.

Ce fichier contient tes clés. **Ne l'envoie à personne et ne le mets jamais sur GitHub.**

## 5. Installer l'app en ligne (2 min)

Dans le même Terminal, tape :
```
zsh deploy.sh
```
Si le Mac propose d'installer les **outils de développement en ligne de commande**, accepte, attends la fin, puis relance la même commande.

Quand tout marche, les dernières lignes ressemblent à ça :
```
deploy True []
cron True
URL: https://carnet-chai.ton-nom.workers.dev
test code: 200 (200 attendu)
```
L'adresse affichée après `URL:` est celle de ton app.

## 6. Mettre l'app sur le téléphone (1 min)

1. Ouvre l'adresse de l'app sur le téléphone.
2. **iPhone (Safari)** : bouton Partager, puis **Sur l'écran d'accueil**. **Android (Chrome)** : menu ⋮, puis **Ajouter à l'écran d'accueil**.
3. Tape le code (`CHAI_PIN`). Le téléphone le garde en mémoire, il ne faut le taper qu'une fois.

Donne l'adresse et le code aux personnes qui travaillent avec toi au chai. Tout le monde voit les mêmes cuves.

---

## Adapter l'app à ton chai

Le plan livré est celui d'un chai précis (zones, cuves, barriques, volumes). Pour mettre le tien :

1. Ouvre `app.html` dans TextEdit et cherche `const ZONES`.
2. Chaque zone a un nom (`nom`), une description (`desc`) et une liste de cuves. Chaque cuve s'écrit `L('Nom de la cuve', volume en litres, 'l')`. Le `'l'` ou `'r'` place la cuve à gauche ou à droite du plan.
3. Cherche aussi `Demande le code à Gus` et remplace « Gus » par ton prénom.
4. Enregistre, puis relance `zsh deploy.sh` dans le Terminal.

Tu peux relancer `zsh deploy.sh` autant de fois que tu veux : **les données saisies ne sont jamais effacées**, elles sont stockées à part chez Cloudflare.

## Bon à savoir

- **Sauvegardes** : l'app fait une copie de toutes les données chaque nuit et garde les 30 derniers jours. On peut restaurer une copie depuis l'app.
- **Hors ligne** : sans réseau, l'app continue de marcher et enregistre sur le téléphone. Elle envoie tout dès que le réseau revient.
- **Sécurité** : après 30 codes faux en 24 h, l'app bloque tout accès pendant 24 h. Les saisies restent sur les téléphones et repartent ensuite. Un code plus long rend l'app plus sûre.
- **Coût** : le plan gratuit de Cloudflare permet 100 000 visites et 1 000 enregistrements par jour. C'est largement assez pour un chai.

## Si ça ne marche pas

| Message dans le Terminal | Solution |
|---|---|
| `Remplis CLOUDFLARE_WORKERS_TOKEN et CHAI_PIN dans .env` | Le fichier `.env` est vide ou mal nommé. Refais l'étape 4. |
| Une erreur avec `Traceback`, ou `deploy False` avec `Authentication error` | Le jeton ou l'identifiant est faux. Vérifie qu'il n'y a pas d'espace après le `=`. Sinon, recrée le jeton (étape 2). |
| `Pas encore de sous-domaine workers.dev` | Ouvre **Workers & Pages** sur Cloudflare, choisis un nom, puis relance `zsh deploy.sh`. |
| L'app affiche « code faux » | Le code tapé n'est pas celui de `CHAI_PIN`. Après 30 erreurs, attends 24 h. |

## Les fichiers

| Fichier | Rôle |
|---|---|
| `app.html` | L'app elle-même (écrans, plan du chai, opérations). |
| `deploy.sh` | Le script qui installe ou met à jour l'app sur Cloudflare. |
| `build.py` | Assemble les fichiers en un seul programme pour Cloudflare (lancé par `deploy.sh`). |
| `sw.js`, `manifest.json`, `icon.svg` | Permettent d'installer l'app sur l'écran d'accueil et de l'utiliser hors ligne. |
| `env.example` | Modèle du fichier de réglages, à copier en `.env`. |
| `index.html` | Ancienne version, plus utilisée. |
