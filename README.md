# Hapa Live

**Discover live music and upcoming events around Kenya.**

Hapa Live is a full-stack event discovery project. Browse concerts, open the organiser’s ticket page, and keep track of events you want to attend.

> Hapa Live helps you discover events. Ticket purchases happen on the organiser’s or ticket seller’s website.

## Features

- Browse and search event listings
- Filter events by city
- Switch between light and dark themes
- Open the organiser’s or ticket seller’s page for event and ticket details
- Create an account and save events to a wishlist
- Keep personal booking notes in **My Plans**

Event listings are starter examples. Check the linked event page for current dates, venues, and ticket details. Hapa Live does not process payments or verify tickets.

## Built with

- **Frontend:** React, TypeScript, and Vite
- **Backend:** Python, FastAPI, and SQLAlchemy
- **Local database:** SQLite
- **Hosted database:** PostgreSQL

## Run locally on Windows

Install Python and Node.js, then open two terminals in the project folder.

### Start the API

In the first terminal, run:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:HAPA_SECRET_KEY = 'replace-with-a-long-random-local-secret'
uvicorn app.main:app --reload --port 8000
```

The API runs at `http://127.0.0.1:8000`. Its interactive documentation is at `http://127.0.0.1:8000/docs`.

### Start the website

In the second terminal, run:

```powershell
cd frontend
npm install
npm run dev
```

Open the address Vite displays, usually `http://localhost:5173`.

## Deploy

The project includes a `Dockerfile` that builds the React website and serves it from the FastAPI app. Both use the same web address, including the sign-in session.

1. Push the project to GitHub.
2. Create a PostgreSQL database, for example on Neon, and copy its connection URL.
3. In Render, create a **Web Service** connected to the GitHub repository. Select the **Docker** runtime and use the repository’s `Dockerfile`.
4. Add these environment variables to the Render service:
   - `HAPA_DATABASE_URL` — your PostgreSQL connection URL
   - `HAPA_SECRET_KEY` — a long, randomly generated secret
   - `HAPA_ENVIRONMENT` — `production`
   - `HAPA_COOKIE_SECURE` — `true`
   - `HAPA_CLOUDFLARE_TOKEN` — the token from your Cloudflare Web Analytics snippet
5. Deploy, then open the service URL. The health endpoint is `/api/health`.

To create the analytics token, add your deployed hostname in **Web Analytics** in Cloudflare, then copy the token value from its JavaScript snippet. Add it to Render as `HAPA_CLOUDFLARE_TOKEN` and redeploy. The dashboard will start collecting visits after the snippet is active.

Keep database URLs and secret keys private. Do not commit them to GitHub. Review your hosting providers’ current limits and costs before choosing a plan.

## Project structure

```text
hapa-live/
├── frontend/       React and TypeScript website
├── backend/        FastAPI service and database models
├── Dockerfile      Production build and startup instructions
└── .dockerignore   Keeps local files out of the Docker build
```

A good place to start exploring is `frontend/src/pages/Home.tsx` for event discovery and `backend/app/routes.py` for API routes.

## Event images and links

Event links take users to the organiser or ticket seller. Images load from their source websites when available and require an internet connection. Check each source’s terms before reusing images in a public launch.

## Project status

Hapa Live is a learning project under active development. The listings are examples and may change. Review the authentication and deployment setup before using the project publicly.
