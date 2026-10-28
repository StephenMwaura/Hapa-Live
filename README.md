# Hapa Live

**Discover live music and upcoming events around Kenya.**

Hapa Live is a full-stack project for finding concerts, opening the organiser’s ticket page, and keeping track of events you want to attend.

> Hapa Live helps you discover events. Ticket purchases happen on the organiser’s or ticket seller’s website.

## Features

- Browse and search event listings
- Filter events by city
- Switch between light and dark themes
- Open the organiser’s or ticket seller’s page for event details and tickets
- Create an account and save events to a wishlist
- Keep personal booking notes in **My Plans**

Listings are starter examples, so check the linked event page for the latest dates, venues, and ticket details. Hapa Live does not process payments or verify tickets.

## Technology

- **Frontend:** React, TypeScript, and Vite
- **Backend:** Python, FastAPI, and SQLAlchemy
- **Database:** SQLite for local development





Project structure
hapa-live/
frontend/   React and TypeScript website
backend/    FastAPI service and database
A good place to start exploring is frontend/src/pages/Home.tsx for the event discovery page and backend/app/routes.py for the API routes.

Event images and links
Event links take users to the organiser or ticket seller. Event images load from their source websites when available and require an internet connection. 


Project status
Hapa Live is a learning project under active development. The event listings are examples and may change. Before using the project publicly, review the authentication and deployment setup, and keep secret keys out of GitHub.
