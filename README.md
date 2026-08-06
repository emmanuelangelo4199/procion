# Porcion

**A behavioral weight management platform built around emotion-aware food tracking and peer accountability.**

![Python](https://img.shields.io/badge/python-3.13-blue)
![Framework](https://img.shields.io/badge/framework-Django-0C4B33)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

Porcion helps people build healthier relationships with food by pairing emotion-aware tracking with small, supportive peer circles — real accountability, not just calorie counting.

<!-- picture of porcion -->

<!-- ![Porcion dashboard](screenshots/dashboard.png) -->
<!-- <img src="screenshots/dashboard.png" alt="Porcion dashboard" width="600"> -->

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Project Status](#project-status)
- [Academic Context](#academic-context)
- [Author](#author)
- [License](#license)

## Features

- **Emotion-food tracking** — log meals alongside emotional state and see progress insights over time
- **Peer accountability circles** — small groups of 4–6 members for mutual support, with automatic waitlist backfill when a spot opens up
- **Real-time group chat** — WebSocket-based messaging within each circle, powered by Django Channels
- **Email-based accounts** — custom user model with Google OAuth 2.0 sign-in
- **Progress dashboard** — a central view of tracking history and circle activity

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django |
| Real-time | Django Channels 4.x + Daphne (ASGI) |
| Frontend | HTML5, Tailwind CSS |
| Database | MySQL (production), SQLite (local development) |
| Auth | Custom email-based user model, Google OAuth 2.0 |
| Version Control | Git / GitHub |

## Project Structure

Porcion is organized into five Django apps:

| App | Responsibility |
|---|---|
| `user` | Authentication (email-based login + Google OAuth), account management |
| `tracking` | Emotion-food logging and progress insights |
| `circle` | Peer accountability circles, membership limits, and waitlist backfill |
| `dashboard` | Central view of a user's tracking history and circle activity |
| `home` (`app`) | Landing pages and shared base templates |

## Getting Started

### Prerequisites

- Python 3.13
- MySQL (for a production-like setup — SQLite is used automatically for local development)
- Redis, if your channel layer is configured to use `channels_redis` (check `settings.py`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/emmanuelangelo4199/procion.git
   cd procion
   ```

2. **Create and activate a virtual environment**
   ```powershell
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```
   ```bash
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   GOOGLE_OAUTH_CLIENT_ID=your-client-id
   GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

   # Only needed outside local dev — SQLite is used by default
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=your-db-host
   DB_PORT=3306
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   Channels handles WebSocket connections through `runserver` in development. For a production-like run, serve through Daphne instead:
   ```bash
   daphne project.asgi:application
   ```

## Project Status

🚧 **Active development** — targeting a September 2026 submission.

Currently in the frontend and URL-mapping phase. Completed so far:

- Custom email-based `User` model with Google OAuth 2.0
- Circle membership logic with member caps and waitlist backfill
- Django Channels + Daphne wired for real-time chat

## Academic Context

Porcion began as a formal research proposal for the BSc ICT program at the University of Education, Winneba (UEW), and is being developed as the Level 400 capstone project.

## Author

**Angelo**
Full-stack developer based in Accra, Ghana

- GitHub: [@emmanuelangelo4199](https://github.com/emmanuelangelo4199)
- Building in public on X: [@mrangelo4199](https://x.com/mrangelo4199)

## License

No license has been added yet. MIT is a common default for portfolio/capstone projects if you'd like to add one.