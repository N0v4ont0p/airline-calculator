# Airline Miles Calculator

A comprehensive airline miles calculator with worldwide airport coverage, alliance-specific loyalty programs, and accurate mileage calculations.

## Features

- **Comprehensive Coverage**: 100+ airports worldwide with accurate coordinates
- **Alliance Support**: Star Alliance, Oneworld, SkyTeam, and unallianced airlines
- **Dynamic Selection**: Airlines and loyalty programs filter by alliance
- **Accurate Calculations**: Distance-based calculations with elite status bonuses
- **Professional Interface**: Modern, responsive design with smooth interactions
- **Cross-Alliance Crediting**: Calculate miles when flying one airline but crediting to another

## Technical Stack

- **Backend**: Flask with SQLAlchemy
- **Frontend**: React with Tailwind CSS and shadcn/ui components
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Render.com compatible

## Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Access the Application**:
   Open http://localhost:5000 in your browser

### Render.com Deployment

1. **Create a new Web Service** on Render.com
2. **Connect your Git repository**
3. **Use these settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Environment**: Python 3.11

The application will automatically:
- Create database tables
- Seed comprehensive airport and airline data
- Start the Flask server
- Serve the React frontend

## Database Schema

### Core Models

- **Airport**: Name, IATA code, city, country, coordinates
- **Alliance**: Star Alliance, Oneworld, SkyTeam
- **Airline**: Name, IATA code, country, alliance membership
- **LoyaltyProgram**: Program name, airline, currency type
- **EliteTier**: Status levels with bonus percentages
- **BookingClass**: Fare codes (Y, J, F, etc.) with cabin classifications
- **EarningRate**: Miles earning rates by program, airline, and class

### Key Features

- **Dynamic Filtering**: Airlines and programs filter by alliance selection
- **Cross-Alliance Crediting**: Fly one airline, credit to another program
- **Elite Status Bonuses**: Automatic calculation of status bonuses
- **Minimum Miles**: Industry-standard 500-mile minimum per segment
- **Partner Reductions**: Reduced earning rates for partner airlines

## API Endpoints

- `GET /api/airports?search=<term>` - Search airports
- `GET /api/alliances` - Get all alliances
- `GET /api/airlines?alliance_id=<id>` - Get airlines by alliance
- `GET /api/loyalty-programs?alliance_id=<id>` - Get programs by alliance
- `GET /api/booking-classes` - Get all booking classes
- `GET /api/elite-tiers/<program_id>` - Get elite tiers for program
- `POST /api/calculate` - Calculate miles for a trip

## Calculation Algorithm

The miles calculation considers:

1. **Base Distance**: Great circle distance between airports
2. **Earning Rate**: Varies by booking class and airline relationship
3. **Alliance Factors**: Same airline (100%), alliance partner (85%), non-alliance (75%)
4. **Cabin Class Multipliers**: Economy (100%), Premium Economy (125%), Business (150%), First (200%)
5. **Elite Status Bonus**: Additional percentage based on status level
6. **Minimum Miles**: 500-mile minimum per segment

## Data Coverage

- **100+ Major Airports**: Worldwide coverage including all major hubs
- **38 Airlines**: Across all three major alliances plus unallianced carriers
- **38 Loyalty Programs**: One per airline with accurate program names
- **15 Booking Classes**: Complete fare code coverage
- **Elite Tiers**: 4 levels per program (Base, Silver, Gold, Platinum)

## Deployment Files

- `main.py` - Complete Flask application with all models and routes
- `seed_data.py` - Additional airport data seeding
- `requirements.txt` - Python dependencies
- `Procfile` - Render.com process definition
- `render.yaml` - Render.com service configuration
- `static/` - Built React frontend

## License

MIT License - Feel free to use and modify as needed.
