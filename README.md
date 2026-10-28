# Hapa Live

A full-stack starter for discovering live music around Kenya. The web app uses **React + TypeScript + Vite**. The API uses **Python + FastAPI + SQLAlchemy** with SQLite for local development. SQLite is simple to run locally; PostgreSQL is a straightforward next step when deploying for multiple users.

## What is in this version

- **Home page:** colorful event discovery, search, city filter, date sorting, dark and light themes, and direct links to organiser or ticket pages.
- **Sign up and login:** password validation, Argon2 password hashing, and a seven-day HttpOnly session cookie.
- **My plans:** account-specific wishlists and a personal record of bookings.
- **Booking record:** after paying on the event organiser’s website, a signed-in user can mark an event as booked and save ticket quantity plus a personal note. This is a reminder only: Hapa Live does not process payments or verify tickets.
- **Sample concerts:** a small starter set sourced from published event pages. The seed script adds new examples and refreshes the sample event details when the API starts.
- **Event artwork:** event cards use a poster or photo from the event/ticket page when one is available, with a genre image as a fallback. These images load from the source site, so they need an internet connection; check image reuse terms before a public launch.

## Run locally (Windows PowerShell)

Open two terminals from this folder.

### Terminal 1: Python API

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:HAPA_SECRET_KEY = 'replace-with-a-long-random-local-secret'
uvicorn app.main:app --reload --port 8000
```

The API is at `http://127.0.0.1:8000`; interactive endpoint docs are at `http://127.0.0.1:8000/docs`. The SQLite file `hapa_live.db` is created in `backend/` the first time the API runs.

### Terminal 2: React app

```powershell
cd frontend
npm install
npm run dev
```

Open the local address Vite prints (usually `http://localhost:5173`). Vite forwards `/api` requests to the Python API.

## Publish this project on GitHub

This folder is the complete source project. After creating an empty repository on GitHub, connect and push it from this folder:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

The `.gitignore` keeps local dependencies, build output, environment secrets, and the SQLite database out of the repository. Do not commit real passwords or secret keys.

## Learn the code in this order

1. `frontend/src/types.ts` — the shared shape of a user, event, and booking.
2. `frontend/src/pages/Home.tsx` — event search, city filtering, and the wishlist interaction.
3. `frontend/src/components/EventCard.tsx` — the reusable concert card and organiser link.
4. `frontend/src/pages/Auth.tsx` — signup and login forms.
5. `frontend/src/pages/Dashboard.tsx` — the signed-in wishlist and booking record.
6. `frontend/src/api.ts` — browser requests to the API, including cookie credentials.
7. `backend/app/models.py` — database tables and links between users, events, wishlists, and booking records.
8. `backend/app/routes.py` — the API actions; account-only routes get the user from the signed session cookie.
9. `frontend/src/styles.css` — layout, responsive rules, and light/dark color tokens.

A good first customization is adding a county or city to the seed data, then tracing it through the database model, TypeScript type, and city filter.

## Pair-programming path

- **You pick the product detail.** For example: which counties, genres, ticket details, or accessibility information would help someone choose an event?
- **Trace one feature end to end.** We can add a county filter together by changing the event model, seed, API response, frontend type, and home-page control.
- **You make the next edit.** I can explain the relevant files, suggest a small change, and review what you add before we move on.
- **Keep the boundaries clear.** Organisers own checkout and tickets; Hapa Live owns discovery, wishlists, and the user’s personal plans.

## Security and deployment notes

This is a learning starter, not a production authentication service. Before deployment, use a long random `HAPA_SECRET_KEY`, HTTPS, `HAPA_COOKIE_SECURE=true`, PostgreSQL, schema migrations, email verification, password reset, login rate limiting, and a reviewable event-import workflow. Keep event sources and ticket links visible, recheck listings, and respect each source’s terms. Never scrape a site that disallows it.

## Project layout

```text
hapa-live/
├── frontend/                 React + TypeScript UI
│   └── src/
│       ├── App.tsx           Routes and sign-in gate
│       ├── pages/            Home, authentication, and My Plans screens
│       ├── components/       Shared navigation, event cards, and dialogs
│       ├── api.ts            Typed API requests
│       ├── auth.tsx          Current account state
│       ├── styles.css        Colors, components, responsive layout
│       └── types.ts          Frontend data types
└── backend/                  FastAPI service
    └── app/
        ├── main.py           App startup and database seeding
        ├── models.py         SQLAlchemy tables
        ├── routes.py         Auth, events, wishlist, bookings
        ├── schemas.py        Request and response validation
        ├── security.py       Password hashes and signed sessions
        └── seed.py           Starter event listings
```

## Event data note

The starter seed includes a small set of sample listings. Regional examples were checked against their linked event pages on 28 October 2026; organisers can change dates, venues, and prices, so open the source link before making plans. The Mombasa entry links to the live SoldOutAfrica calendar because its current listing is on that calendar.

