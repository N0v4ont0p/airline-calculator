# Airline Miles Calculator

The world's most comprehensive airline miles calculator with 1,475+ international airports, 66 airlines across all major alliances, and accurate cross-alliance crediting calculations.

## Features

### ✈️ **Comprehensive Coverage**
- **1,475+ International Airports** worldwide with accurate coordinates
- **66 Airlines** across Star Alliance, Oneworld, SkyTeam, and unallianced carriers
- **66 Loyalty Programs** with proper program names and currency types
- **15 Booking Classes** with accurate earning percentages
- **Elite Status Tiers** with bonus calculations

### 🌍 **Dynamic Alliance System**
- Select from Star Alliance, Oneworld, SkyTeam, or Unallianced
- Airlines and loyalty programs filter dynamically based on alliance selection
- Cross-alliance crediting with accurate earning rate adjustments
- Proper handling of airline partnerships and relationships

### 🎯 **Accurate Calculations**
- Geodesic distance calculations using real airport coordinates
- Industry-standard minimum miles rules (500 miles minimum)
- Booking class multipliers (Economy 25-100%, Business 125-150%, First 150-200%)
- Elite status bonuses (Silver +25%, Gold +50%, Platinum +100%)
- Alliance relationship penalties for cross-crediting

### 💻 **Professional Interface**
- Modern React frontend with Tailwind CSS and shadcn/ui components
- Responsive design that works on all devices
- Real-time search with autocomplete for airports, airlines, and programs
- No overlapping dropdowns or UI issues
- Smooth animations and professional styling

## Deployment on Render.com

### Quick Deploy
1. **Upload** this entire folder to your Git repository (GitHub, GitLab, or Bitbucket)
2. **Connect** your repository to Render.com
3. **Create** a new Web Service
4. **Deploy** - Render will automatically detect the configuration

### Manual Configuration (if needed)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main_final.py`
- **Environment**: Python 3.11

### Environment Variables
The application automatically handles:
- SQLite for development
- PostgreSQL for production (when DATABASE_URL is provided)
- Port configuration (uses PORT environment variable)

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main_final.py
```

The application will:
1. Create database tables automatically
2. Seed with all airport and airline data
3. Start the Flask server on port 5000
4. Serve the React frontend at http://localhost:5000

### Database
- **Development**: SQLite (airline_calculator.db)
- **Production**: PostgreSQL (automatically configured on Render)
- **Auto-seeding**: All data is loaded automatically on first run

## Technical Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing
- **geopy** - Geographic distance calculations
- **psycopg2** - PostgreSQL adapter

### Frontend
- **React** - UI framework
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Lucide React** - Icons
- **Vite** - Build tool

### Database Schema
- **Airports** - Name, code, city, country, coordinates
- **Airlines** - Name, code, country, alliance
- **Loyalty Programs** - Name, airline, currency, alliance
- **Elite Tiers** - Name, bonus percentage, program
- **Booking Classes** - Code, name, cabin class, earning percentage
- **Alliances** - Name, description

## API Endpoints

- `GET /api/stats` - Application statistics
- `GET /api/airports?search=<term>` - Search airports
- `GET /api/alliances` - List all alliances
- `GET /api/airlines?alliance_id=<id>` - List airlines (filtered by alliance)
- `GET /api/loyalty-programs?alliance_id=<id>` - List programs (filtered by alliance)
- `GET /api/booking-classes` - List booking classes
- `GET /api/elite-tiers/<program_id>` - List elite tiers for program
- `POST /api/calculate` - Calculate miles for route

## Data Sources

### Airports
Comprehensive list of international airports from multiple sources including:
- IATA airport codes and names
- City and country information
- Geographic coordinates for distance calculations
- Regional classifications

### Airlines & Programs
- All major Star Alliance members (United, Lufthansa, Singapore Airlines, etc.)
- Complete Oneworld alliance (American, British Airways, Cathay Pacific, etc.)
- Full SkyTeam coverage (Delta, Air France, KLM, etc.)
- Major unallianced carriers (Emirates, Etihad, JetBlue, etc.)
- Accurate loyalty program names and currencies

## License

This project is provided as-is for educational and personal use.
