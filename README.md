# Airline Miles Calculator

A comprehensive airline miles calculator with worldwide airport coverage, accurate calculations, and modern UI/UX design.

## Features

- **20 major international airports** (CDG, LHR, JFK, etc.)
- **20 airlines** across all alliances (Star Alliance, Oneworld, SkyTeam, Unallianced)
- **Alliance-based airline selection** with dynamic filtering
- **Airline-specific elite tier names** (e.g., "Premier Gold" for United)
- **Dual airport selection**: Search + scrollable dropdown
- **Industry-accurate calculations** with proper elite bonuses
- **Modern Apple-inspired UI/UX design**

## Quick Deploy on Render.com

1. Upload this repository to GitHub
2. Connect to Render.com
3. Render will automatically detect the `render.yaml` and deploy

## Local Development

### Setup
```bash
pip install -r requirements.txt
python src/simple_seeder.py  # Populate database
python src/main.py           # Start server on port 5000
```

### Access
- Application: http://localhost:5000
- API: http://localhost:5000/api

## API Endpoints

- `GET /api/airports` - Airport search and listing
- `GET /api/alliances` - Alliance information  
- `GET /api/airlines` - Airline listing with alliance filtering
- `POST /api/calculate-miles` - Miles calculation engine

## Database

Uses SQLite with the following tables:
- `airports` - 20 major international airports
- `airlines` - 20 airlines across all alliances
- `loyalty_programs` - Airline-specific program details
- `earning_rates` - Comprehensive earning rules

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: React (built and served as static files)
- **Database**: SQLite
- **Deployment**: Render.com ready

## Status

✅ Production ready with comprehensive testing completed
