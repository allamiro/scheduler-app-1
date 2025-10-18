# Duty Scheduler

A full-stack sample application that pairs a FastAPI backend with a Next.js 14 frontend. The interface embraces the glassmorphism and playful gradients of the Vite welcome page while focusing on managing radiology duty rosters.

## Project structure

```text
backend/   FastAPI app with SQLite persistence and REST endpoints for doctors, schedules, and assignments
frontend/  Next.js 14 application styled with Tailwind CSS and a Vite-inspired hero experience
```

## Backend

### Features

- Doctors with specialties and capacity limits
- Weekly schedules with per-day assignments
- Validation to avoid exceeding capacity or double-booking a doctor
- Seed script with example doctors and assignments

### Local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>. Adjust the port in the frontend `.env.local` file if you change it.

### Database seeding

The backend ships with a lightweight SQLite database. Populate it with demo data:

```bash
cd backend
python seed_data.py
```

## Frontend

### Features

- Hero section designed to mirror the Vite landing page aesthetics
- Live schedule preview panel pulling data from the FastAPI backend
- Responsive layout that keeps the preview sticky on desktop

### Local development

```bash
cd frontend
npm install
npm run dev
```

By default the frontend expects the API at `http://localhost:8001`. Create a `.env.local` file to override the value exposed to the browser:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Building for production

```bash
npm run build
npm run start
```

## Testing the integration

1. Start the backend with `uvicorn app.main:app --reload`
2. Seed the database with `python seed_data.py`
3. Run the frontend dev server and navigate to <http://localhost:3000>

You should see the Vite-inspired hero and a live preview of the seeded assignments on the right-hand panel.

## License

MIT
