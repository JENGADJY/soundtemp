# 🎧 SoundTemp

**SoundTemp** est une application qui associe la météo locale à vos goûts musicaux pour vous recommander des cocktails et des playlists adaptées à votre ambiance du moment.

---

## 🚀 Fonctionnalités

- 🔥 Recommandations musicales personnalisées via Spotify
- 🌤️ Analyse de la météo locale avec WeatherStack
- 🍹 Suggestions de cocktails en fonction du temps
- 🤖 Intégration IA (Mistral) à venir pour améliorer l’expérience utilisateur

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/JENGADJY/soundtemp.git
cd soundtemp
```

### 2. Installer les dépendances

#### Backend

```bash
cd backend
npm install
```

#### Frontend

```bash
cd ../frontend
npm install
```

### 3. Ajouter le fichier `.env`

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```env
SPOTIFY_CLIENT=
SPOTIFY_CLIENT_SECRET=
WEATHER_API=

MISTRAL_KEY=
MISTRAL_AGENT=

REDIRECT_URI=http://127.0.0.1:8000/spotify/callback/


## ▶️ Démarrage

### Backend

```bash
cd backend
npm run dev
```

### Frontend

```bash
cd ../frontend
npm start
```

---

## 🧠 Fonctionnalités IA (en cours)

L’agent **Mistral** sera intégré pour proposer une expérience intelligente et assistée sur les routes suivantes :

- `/accueil`
- `/register`
- `/login`
- `/profile`
- `/dashboard`

---

## 🛠️ Problèmes connus

- Si votre **token Spotify** expire : reconnectez votre compte via le bouton de connexion.
- Assurez-vous que toutes les clés API sont valides dans le `.env`.

---

## 📄 Licence

Projet réalisé à des fins pédagogiques. Tous droits réservés © JENGADJY

---

## 🤝 Contribuer

Les contributions sont les bienvenues !  
Forkez le projet, créez une branche, proposez une pull request.