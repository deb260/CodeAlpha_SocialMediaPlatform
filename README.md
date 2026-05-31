# SocialAlpha — Social Media Platform
### CodeAlpha Full Stack Internship — Task 2

A mini social media web app built with **Django** and **HTML/CSS/JavaScript**.

---

## Features

- 👤 **User Profiles** — Avatar, bio, follower/following counts
- 📝 **Posts** — Create posts with optional images, delete your own
- ❤️ **Likes** — Like and unlike any post
- 💬 **Comments** — Comment on posts, delete your own comments
- 👥 **Follow System** — Follow/unfollow users, see their posts in your feed
- 📰 **Smart Feed** — See only posts from people you follow + your own
- 🔍 **Explore** — Search users and browse all posts
- ⚙️ **Edit Profile** — Update bio and profile photo

---

## Tech Stack

| Layer     | Technology            |
|-----------|-----------------------|
| Backend   | Python 3, Django 4.2  |
| Database  | SQLite (built-in)     |
| Frontend  | HTML, CSS, JavaScript |
| Auth      | Django built-in auth  |

---

## Setup Instructions

### 1. Clone & navigate
```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_SocialMediaPlatform
cd CodeAlpha_SocialMediaPlatform
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations social
python manage.py migrate
```

### 5. Create admin account
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

### 7. Visit the app
- **App:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin

---

## How to Test It

1. Register 2-3 different accounts
2. Follow each other
3. Create posts and comments
4. Like posts
5. Check how the feed changes based on who you follow

---

*Built for CodeAlpha Full Stack Development Internship*
