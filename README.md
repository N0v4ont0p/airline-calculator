# Ultimate Airline Miles Calculator

A comprehensive, professional airline miles calculator with worldwide airport coverage, alliance-specific loyalty programs, and accurate mileage calculations.

## Features

### ✈️ **Comprehensive Coverage**
- **60+ Major International Airports** worldwide with accurate coordinates
- **40 Airlines** across all major alliances (Star Alliance, Oneworld, SkyTeam) plus unallianced carriers
- **40 Loyalty Programs** with accurate program names and earning rates
- **16 Booking Classes** with proper fare code coverage (F, J, C, Y, etc.)
- **4 Elite Status Tiers** with appropriate bonus percentages

### 🎯 **Advanced Functionality**
- **Cross-Alliance Crediting**: Fly one airline, credit to another loyalty program
- **Dynamic Alliance Filtering**: Select alliance to see only relevant airlines and programs
- **Accurate Distance Calculation**: Uses geodesic calculations with real airport coordinates
- **Industry-Standard Rules**: Minimum miles rules, booking class multipliers, elite bonuses
- **Professional Algorithm**: Considers all factors that affect miles earning

### 🎨 **Exceptional User Experience**
- **Beautiful Modern Interface**: Built with React, Tailwind CSS, and shadcn/ui components
- **Step-by-Step Workflow**: Guided process with progress tracking
- **Real-Time Search**: Instant airport search with autocomplete
- **Responsive Design**: Works perfectly on desktop and mobile
- **Professional Styling**: Clean, intuitive interface with proper visual feedback

## Quick Start

### Deploy to Render.com (Recommended)

1. **Upload to Git Repository**
   - Extract this package to your Git repository
   - Commit and push all files

2. **Connect to Render.com**
   - Create a new Web Service on Render.com
   - Connect your Git repository
   - Render will automatically detect the configuration

3. **Deploy**
   - Render will build and deploy automatically
   - The application handles database setup and seeding

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

3. **Access the Calculator**
   - Open http://localhost:5000 in your browser

## Technical Details

### Backend
- **Framework**: Flask with SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **APIs**: RESTful endpoints for airports, airlines, alliances, and calculations
- **Distance Calculation**: Geopy library for accurate geodesic distance

### Frontend
- **Framework**: React with modern hooks
- **Styling**: Tailwind CSS with shadcn/ui components
- **Icons**: Lucide React icons
- **Animations**: Framer Motion for smooth transitions

## File Structure

```
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── render.yaml            # Render.com deployment configuration
├── static/                # Built React frontend
│   ├── index.html
│   └── assets/
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## API Endpoints

- `GET /api/stats` - Application statistics
- `GET /api/airports?search={query}` - Search airports
- `GET /api/alliances` - Get all alliances
- `GET /api/airlines/{alliance_id}` - Get airlines by alliance
- `GET /api/booking-classes` - Get all booking classes
- `GET /api/elite-tiers` - Get all elite tiers
- `POST /api/calculate` - Calculate miles for a route

## Deployment Configuration

The application is configured for seamless deployment on Render.com:

- **Automatic Build**: Dependencies installed via requirements.txt
- **Database Setup**: Automatic table creation and data seeding
- **Static Files**: React frontend served by Flask
- **Environment Variables**: Supports PostgreSQL via DATABASE_URL

## Support

This is a complete, production-ready application that requires no additional configuration. The database is automatically seeded with comprehensive data on first run.
