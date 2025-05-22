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
SPOTIFY_CLIENT=258f8c75fe3e4d719640d45514a4f671
SPOTIFY_CLIENT_SECRET=33ea66765034468ea51b9e48c3a440b1
WEATHER_API=6722b5548d6dc09f3cf4b811ebce42dd

MISTRAL_KEY=HjC9IvVEzAIeVWL65ZTvxFkMD8jEIf79
MISTRAL_AGENT=ag:753184c9:20250516:spotitemps:0c659620

REDIRECT_URI=http://127.0.0.1:8000/spotify/callback/
```

> 🔒 **Attention** : Ne publiez jamais ce fichier sur GitHub. Utilisez un fichier `.env.example` sans valeurs pour le versionner.

---

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