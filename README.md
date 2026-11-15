# Yuraylik Bot

Yuraylik Bot is a Telegram bot that helps users build a walking habit. Users can
record their daily walking time, track streaks, view personal statistics and
rankings, and configure daily reminders.

The bot's user-facing messages are currently written in Uzbek.

## Features

- Record daily walking time in minutes
- Automatically accumulate daily activity and walking streaks
- View total minutes, current/highest streaks, and user ranking
- Display a top-20 leaderboard
- Choose whether to appear in the leaderboard
- Configure daily walking reminders
- Persist data in PostgreSQL
- Apply database migrations automatically when started with Docker Compose

## Tech stack

- Python 3.11
- [aiogram](https://docs.aiogram.dev/) 3
- aiohttp webhook server
- SQLAlchemy asyncio
- PostgreSQL
- Alembic
- Docker and Docker Compose

## Requirements

- Python 3.11 or newer
- PostgreSQL 15 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A publicly reachable HTTPS URL for the webhook

Docker Compose is recommended because it starts PostgreSQL and runs migrations
automatically.

## Configuration

Create a local environment file:

```bash
cp .env.example .env
```

Set the following values in `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://admin:admin@db:5432/yuraylik
DATABASE_ECHO=false
WEBHOOK_URL=https://your-public-domain.example
```

`WEBHOOK_URL` must be the public base URL of the bot without the `/webhook`
path. The application registers the webhook at:

```text
{WEBHOOK_URL}/webhook
```

When running the bot outside Docker, replace `db` in `DATABASE_URL` with
`localhost` or the hostname of your PostgreSQL server.

## Run with Docker Compose

```bash
cp .env.example .env
# Edit .env and provide BOT_TOKEN and WEBHOOK_URL
docker compose up --build
```

The bot listens on port `8000`, and PostgreSQL is exposed on port `5432`.
Alembic migrations run before the bot starts.

To stop the services:

```bash
docker compose down
```

To stop the services and remove the database volume:

```bash
docker compose down -v
```

## Run locally

Create and activate a virtual environment, then install dependencies:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure PostgreSQL is running and configure `.env` with a local database
connection, for example:

```env
DATABASE_URL=postgresql+asyncpg://admin:admin@localhost:5432/yuraylik
```

Apply migrations and start the bot:

```bash
alembic upgrade head
python main.py
```

Because the bot uses Telegram webhooks, `WEBHOOK_URL` must point to an HTTPS
endpoint that can reach the application on port `8000`. For local development,
use a tunneling service such as ngrok or Cloudflare Tunnel.

## Database migrations

Create a new migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Apply pending migrations:

```bash
alembic upgrade head
```

## Project structure

```text
.
├── core/                 # Application configuration
├── db/                   # SQLAlchemy models, database, and CRUD operations
├── handlers/             # Telegram commands, messages, and callback handlers
├── keyboards/            # Reply and inline keyboards
├── middlewares/          # Database and user initialization middleware
├── migrations/           # Alembic migration scripts
├── services/             # Background services, including notifications
├── main.py               # Application entry point and webhook server
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Health and ports

The application exposes the webhook server on `0.0.0.0:8000`. Telegram
requests are handled at `/webhook`.
