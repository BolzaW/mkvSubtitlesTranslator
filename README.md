# 🎬 MKV Subtitles Translator

Ce projet permet de **traduire automatiquement les sous-titres** d'une ou plusieurs vidéos `.mkv` en utilisant l'API DeepL et les outils mkvtoolnix et mkvtoolnix-gui

## 🚀 Fonctionnalités
- Extraction des sous-titres intégrés aux fichiers `.mkv`
- Traduction automatique via l'API DeepL
- Réinjection des sous-titres traduits dans les vidéos
- Nettoyage optionnel des sous-titres (paroles de chansons, etc.)
- Gestion de plusieurs clés API (fallback)
- Mode simulation (`dry-run`)

## 📁 Structure attendue

Les fichiers `.mkv` à traiter doivent être placés dans le volume **`/data`** (sur l’hôte).
Ils doivent disposer d'une piste de sous-titre intégrée

### Exemple :
```bash
/mnt/mes_videos/
├── film1.mkv
├── film2.mkv
└── ...
```

## 🐳 Utilisation

### 📦 Pré-Requis

Le projet est une image docker contenant un script python ainsi que les utilitaires mkvtoolnix mkvtoolnix-gui
Je ne souhaite pas à ce stade du projet publier l'image sur docker hub, il faut donc build l'image docker en local

Docker et Docker Compose installés.

Executer la commande suivante à la racine du projet :
```bash
docker build -t mkv-subtitles-translator:latest .
```

#### Note :
Si vous voulez déplacer le container sur une autre machine
Vous pouvez créer une archive portable grâce à la commande :
```bash
docker save -o mkv-subtitles-translator.tar mkv-subtiles-translator:latest
```
Puis copier l'archive sur une autre machine et utiliser la commande :
```bash
docker load -i mkv-subtitles-translator.tar
```

### 🌐 Obtenir une clé API de DeepL

Ce projet est basé sur l'API de DeepL pour traduire du texte
Une clé API est nécessaire pour la faire fonctionnée, DeepL propose une clé API gratuite avec une limitation de 500 000 caractères par mois.
Pour l'obtenir il faut se créér un compte et renseigner ses identifiants bancaires (même si c'est gratuit)

ça se passe ici :
[DeepL](https://www.deepl.com/fr/signup)

### ⚙️ Configuration

A ce stade l'image docker est disponible sur votre environnement.
La méthode recommandée pour exécuter le container est d'utiliser un fichier docker-compose.yml :

Vous retrouverez un exemple de configuration dans samples/ du projet
Copier ces fichiers de configuration dans un répertoire de votre choix
Modifier le fichier .env avec votre clé API
```bash
DEEPL_API_KEYS=<API_KEY_FROM_DEEPL>
```
Modifier le fichier docker-compose.yml en renseignant le path vers vos videos à traduire
```bash
volumes:
      - /mnt/mes_videos:/data
```
Modifier les variables d'environnement au besoin (cf ci dessous)
Lancer le container avec la commande
```bash
docker-compose up
```

### ⚙️ Variables d'environnements et options du logiciel

Ce projet est paramètrables via les variables d'environnement :

- **DRY_RUN** permet de ne pas appeler l'API DeepL, le script python peut alors fonctionner sans clé API et sans consommer de caractères.
⚠️ Cependant celà empèche également la traduction il faut donc mettre cette variable à `false` une fois votre configuration testé
```bash
DRY_RUN=true
```
- **OVERWRITE_FILES** permet de supprimer le fichier mkv source une fois la traduction terminée et le fichier mkv traduit créé.
⚠️ Dans certains scénarios, vos données pourraient être perdu sans possibilité de les récupérer.
Il est recommandé de laisser l'option à false et de faire le nettoyage manuellement une fois les fichiers traduits testés
```bash
OVERWRITE_FILES=false
```

- **KEEP_SRT_FILES** permet de conserver les fichier srt (original et traduit) en plus du fichier mkv les contenant
```bash
KEEP_SRT_FILES=false
```

- **CLEANUP_SUBTITLES** permet de 'nettoyer' les sous-titres avant de les envoyer à DeepL.
Cela supprime tous les sous-titres d'audio description et sous-titres sans texte
```bash
CLEANUP_SUBTITLES=true
```

- **CLEANUP_SONGS_SUBTITLES** permet de 'nettoyer' les sous-titres avant de les envoyer à DeepL.
Cela supprime tous les sous-titres de chanson en les identifiants avec le caractère ♪.
Note : Cette option ne fait rien si `CLEANUP_SUBTITLES=false`
```bash
CLEANUP_SONGS_SUBTITLES=true
```

- **ORIGIN_LANG** Spécifie la langue d'origine des sous-titres à traduire
```bash
ORIGIN_LANG=EN
```

- **TARGET_LANG** Spécifie la langue désirée pour la traduction
```bash
```bash
TARGET_LANG=FR
```









