# Airlines Calculator

A comprehensive web application for comparing miles earned through different airline loyalty programs. This tool helps travelers make informed decisions about which loyalty programs offer the best value for their specific routes.

## Features

- **Route Selection**: Choose from major international airports
- **Alliance Comparison**: Compare programs across SkyTeam, Oneworld, and Star Alliance
- **Miles Calculation**: Calculate exact miles earned based on route distance and fare class
- **Program Comparison**: Side-by-side comparison of multiple loyalty programs
- **Apple-Inspired Design**: Clean, modern interface with smooth animations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database for storing airline and airport data
- **Flask-CORS**: Cross-origin resource sharing support

### Frontend
- **React**: Modern JavaScript framework
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality React components
- **Lucide Icons**: Beautiful icon library

## Project Structure

```
airlines-calculator/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── airline.py       # Airline, Airport, LoyaltyProgram models
│   ├── routes/
│   │   ├── user.py          # User routes (template)
│   │   └── airlines.py      # Airlines API routes
│   ├── static/              # Built frontend files
│   ├── database/
│   │   └── app.db          # SQLite database
│   ├── main.py             # Flask application entry point
│   └── data_seeder.py      # Database seeding script
├── venv/                   # Python virtual environment
└── requirements.txt        # Python dependencies
```

## Database Schema

### Airlines
- ID, Name, IATA Code, Alliance, Loyalty Program

### Airports
- ID, Name, IATA Code, City, Country, Latitude, Longitude

### Loyalty Programs
- ID, Name, Airline ID, Alliance, Base Earning Rate

### Earning Rates
- ID, Loyalty Program ID, Fare Class, Booking Class, Earning Percentage, Elite Bonus

## API Endpoints

### GET /api/airlines
Returns all airlines in the database.

### GET /api/airlines/{alliance}
Returns airlines filtered by alliance (SkyTeam, Oneworld, Star Alliance).

### GET /api/airports
Returns all airports. Supports search parameter for filtering.

### GET /api/loyalty-programs
Returns all loyalty programs. Supports alliance parameter for filtering.

### POST /api/calculate-miles
Calculates miles earned for a specific route and loyalty program.

**Request Body:**
```json
{
  "origin": "JFK",
  "destination": "LAX",
  "loyalty_program_id": 1,
  "fare_class": "Economy",
  "booking_class": "Y"
}
```

### POST /api/compare-miles
Compares miles earned across different loyalty programs for the same route.

**Request Body:**
```json
{
  "origin": "JFK",
  "destination": "LAX",
  "alliance": "Star Alliance",
  "fare_class": "Economy",
  "booking_class": "Y"
}
```

## Installation and Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- pnpm (for frontend dependencies)

### Backend Setup
1. Navigate to the project directory:
   ```bash
   cd airlines-calculator
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Seed the database:
   ```bash
   python src/data_seeder.py
   ```

5. Run the Flask application:
   ```bash
   python src/main.py
   ```

### Frontend Development Setup
1. Navigate to the frontend directory:
   ```bash
   cd airlines-calculator-frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm run dev
   ```

### Production Build
1. Build the frontend:
   ```bash
   cd airlines-calculator-frontend
   pnpm run build
   ```

2. Copy built files to Flask static directory:
   ```bash
   cp -r dist/* ../airlines-calculator/src/static/
   ```

3. Run the integrated Flask application:
   ```bash
   cd airlines-calculator
   source venv/bin/activate
   python src/main.py
   ```

## Data Sources

The application includes comprehensive data for:

### Airlines (18 major carriers)
- **SkyTeam**: Air France, KLM, Delta, Korean Air, China Eastern, Virgin Atlantic
- **Oneworld**: American Airlines, British Airways, Cathay Pacific, JAL, Qantas, Qatar Airways
- **Star Alliance**: United, Singapore Airlines, Lufthansa, Air Canada, Turkish Airlines, Thai Airways

### Airports (16 major international hubs)
- **North America**: JFK, LAX, ORD, YYZ
- **Europe**: LHR, CDG, AMS, FRA
- **Asia**: HND, SIN, HKG, ICN
- **Middle East**: DXB, DOH
- **Australia**: SYD, MEL

### Earning Rates
- Comprehensive fare class and booking class combinations
- Elite status bonuses for each alliance
- Distance-based and revenue-based earning models

## Key Features Explained

### Miles Calculation
The application uses the Haversine formula to calculate great circle distances between airports, then applies loyalty program-specific earning rates based on:
- Fare class (First, Business, Premium Economy, Economy)
- Booking class (specific letter codes like Y, B, M, etc.)
- Elite status bonuses

### Alliance Comparison
Users can compare all loyalty programs within a specific alliance for the same route, helping identify which program offers the best earning potential.

### Responsive Design
The interface adapts seamlessly to different screen sizes using Tailwind CSS responsive utilities and modern CSS Grid/Flexbox layouts.

## Deployment

The application is designed for easy deployment on platforms like Render.com:

1. Ensure `requirements.txt` is up to date
2. Frontend is built and copied to Flask static directory
3. Database is seeded with initial data
4. Flask serves both API and frontend from a single application

## Future Enhancements

- **Route Maps**: Visual representation of flight routes
- **Real-time Data**: Integration with airline APIs for current earning rates
- **Elite Status Tracking**: Account for different elite status levels
- **Award Redemption**: Calculate award ticket costs and availability
- **Mobile App**: Native mobile applications for iOS and Android
- **User Accounts**: Save favorite routes and loyalty programs

## Contributing

This project was developed as a comprehensive demonstration of full-stack web development capabilities, including:
- Modern React frontend with TypeScript
- RESTful API design with Flask
- Database modeling and relationships
- Responsive UI/UX design
- Production deployment preparation

## License

This project is for demonstration purposes and includes publicly available airline and airport information.

