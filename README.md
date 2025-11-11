# ✈️ SkyMiles Calculator - World's Best Airline Miles Calculator

The most comprehensive and accurate airline miles calculator with **50+ loyalty programs**, **6,000+ airports**, and **Haversine formula** distance calculations.

![Lando Norris Aesthetic](https://img.shields.io/badge/Design-Lando%20Norris-D2FF00?style=for-the-badge)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38B2AC?style=for-the-badge&logo=tailwind-css)

---

## 🎯 Features

### Core Functionality
- ✅ **50+ Loyalty Programs** - United, Delta, American, British Airways, Singapore Airlines, and more
- ✅ **6,000+ Airports** - Complete OpenFlights database with IATA codes
- ✅ **Haversine Formula** - Accurate great-circle distance calculations
- ✅ **Distance-Based & Revenue-Based** - Support for both earning models
- ✅ **Fare Class Multipliers** - Accurate booking class percentages (F, J, Y, etc.)
- ✅ **Elite Status Bonuses** - Silver, Gold, Platinum, and Top Tier calculations
- ✅ **Minimum Miles Guarantee** - 500-mile minimum on most programs

### Advanced Features
- 🔍 **Smart Airport Search** - Autocomplete with IATA codes, city, and country
- 📊 **Visual Comparisons** - Bar charts and tables for easy comparison
- 💰 **Value Calculations** - Estimated value based on cents-per-mile
- 🏆 **Best Program Highlighting** - Automatic ranking by value
- 🌐 **Alliance Filters** - Star Alliance, SkyTeam, Oneworld quick filters
- 📈 **Top 10 Programs** - Pre-selected highest-value programs

### Export & Sharing
- 📄 **PDF Export** - Print-friendly reports with full details
- 📊 **CSV Export** - Spreadsheet-compatible data export
- 🔗 **Share Links** - Generate shareable URLs with parameters
- 💾 **Save Routes** - Store favorite routes in localStorage
- 📜 **Calculation History** - Track past calculations (last 50)

### Design
- 🎨 **Lando Norris Aesthetic** - Dark olive (#282C20) + Neon yellow (#D2FF00)
- ✨ **Neon Glow Effects** - Smooth 0.75s transitions
- 📱 **Fully Responsive** - Mobile-first design
- 🎭 **Glass Morphism** - Modern frosted glass UI elements
- 🌈 **Custom Animations** - Floating, shimmer, and fade effects

---

## 🚀 Quick Start

### Prerequisites
- Node.js 22.x
- pnpm (recommended) or npm

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd airline-miles-calculator

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
# Build the app
pnpm build

# Preview production build
pnpm preview
```

---

## 📊 Data Sources

### Airports Database
- **Source**: [OpenFlights Airport Database](https://openflights.org/data.html)
- **Count**: 6,054 airports with IATA codes
- **Fields**: IATA, ICAO, name, city, country, coordinates, timezone, region

### Airlines Database
- **Source**: [OpenFlights Airline Database](https://openflights.org/data.html)
- **Count**: 1,015 active airlines
- **Fields**: IATA, ICAO, name, country, alliance

### Loyalty Programs
- **Source**: Manually curated from official airline programs
- **Count**: 51 programs across all major alliances
- **Accuracy**: Updated as of 2025, verified against official earning charts

---

## 🧮 Calculation Methodology

### Distance Calculation (Haversine Formula)

```typescript
function calculateDistance(origin: Airport, destination: Airport): number {
  const R = 3440.065; // Earth's radius in nautical miles
  
  const lat1 = toRadians(origin.lat);
  const lat2 = toRadians(destination.lat);
  const deltaLat = toRadians(destination.lat - origin.lat);
  const deltaLon = toRadians(destination.lon - origin.lon);
  
  const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
            Math.cos(lat1) * Math.cos(lat2) *
            Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  
  return Math.round(R * c);
}
```

### Miles Earned Calculation

**Distance-Based Programs:**
```
Miles = (Distance × Fare Class Multiplier) + Elite Bonus
Elite Bonus = (Distance × Fare Class Multiplier) × Elite Bonus %
```

**Revenue-Based Programs:**
```
Miles = Ticket Price × Revenue Multiplier (varies by elite status)
```

### Fare Class Multipliers

| Cabin | Classes | Typical Multiplier |
|-------|---------|-------------------|
| First Class | F, A, P | 150% - 300% |
| Business Class | J, C, D, I | 125% - 200% |
| Premium Economy | W, E | 100% - 125% |
| Full Economy | Y, B, M, H | 100% |
| Discount Economy | Q, V, K, L, S, T | 50% - 75% |
| Deep Discount | N, O, G, U, X | 25% - 50% |

### Elite Status Bonuses

| Status | Typical Bonus |
|--------|--------------|
| None | 0% |
| Silver | 25% |
| Gold | 50% |
| Platinum | 75% |
| Top Tier | 100% |

---

## 🎨 Design System

### Color Palette (Lando Norris Theme)

```css
/* Primary Colors */
--background: oklch(0.20 0.02 80);      /* Dark Olive #282C20 */
--foreground: oklch(0.95 0.01 80);      /* Off-White #F4F4ED */
--primary: oklch(0.95 0.25 110);        /* Neon Yellow #D2FF00 */

/* Accent Colors */
--cyan: oklch(0.75 0.15 210);           /* #00D9FF */
--pink: oklch(0.60 0.25 340);           /* #FF006E */
--orange: oklch(0.70 0.20 40);          /* #FF6B35 */
--purple: oklch(0.65 0.20 290);         /* #9D4EDD */
```

### Typography

- **Headings**: Playfair Display (800 weight, uppercase)
- **Body**: Inter (300-900 weight range)
- **Monospace**: System monospace for numbers

### Animations

- **Transitions**: 0.75s cubic-bezier(0.65, 0.05, 0, 1)
- **Neon Glow**: Multi-layer box-shadow with primary color
- **Float**: 6s ease-in-out infinite
- **Shimmer**: 2s linear infinite

---

## 📁 Project Structure

```
airline-miles-calculator/
├── client/
│   ├── public/
│   │   ├── airports.json          # 6,054 airports
│   │   ├── airlines.json          # 1,015 airlines
│   │   └── programs.json          # 51 loyalty programs
│   ├── src/
│   │   ├── components/
│   │   │   ├── AirportSearch.tsx  # Autocomplete search
│   │   │   ├── ResultsDisplay.tsx # Results table & charts
│   │   │   └── ui/                # shadcn/ui components
│   │   ├── lib/
│   │   │   ├── calculator.ts      # Core calculation engine
│   │   │   └── export.ts          # Export utilities
│   │   ├── pages/
│   │   │   └── Calculator.tsx     # Main calculator page
│   │   ├── App.tsx
│   │   └── index.css              # Global styles
│   └── index.html
├── data/
│   ├── airports.csv               # Raw airport data
│   ├── airlines.csv               # Raw airline data
│   └── process_data.py            # Data processing script
├── test-calculations.mjs          # Calculation tests
├── package.json
└── README.md
```

---

## 🧪 Testing

Run the calculation accuracy tests:

```bash
node test-calculations.mjs
```

**Test Coverage:**
- ✅ Haversine distance formula accuracy
- ✅ Minimum miles guarantee (500 miles)
- ✅ Fare class multipliers (F, J, Y, T classes)
- ✅ Elite status bonuses (Gold 50%)
- ✅ Distance-based vs revenue-based programs

---

## 🌐 Deployment

### Render.com (Recommended)

1. **Create a new Static Site** on Render
2. **Connect your GitHub repository**
3. **Build settings:**
   - Build Command: `pnpm install && pnpm build`
   - Publish Directory: `client/dist`
4. **Deploy!**

### Manual Deployment

```bash
# Build the project
pnpm build

# The built files will be in client/dist/
# Upload to any static hosting service
```

### Supported Platforms
- ✅ Render.com
- ✅ Vercel
- ✅ Netlify
- ✅ GitHub Pages
- ✅ AWS S3 + CloudFront
- ✅ Any static hosting service

---

## 📚 Loyalty Programs Included

### Star Alliance (17 programs)
United MileagePlus, Lufthansa Miles & More, Singapore Airlines KrisFlyer, Air Canada Aeroplan, ANA Mileage Club, Thai Royal Orchid Plus, Turkish Miles&Smiles, Air New Zealand Airpoints, Avianca LifeMiles, Copa ConnectMiles, Ethiopian ShebaMiles, EVA Infinity MileageLands, LOT Miles & More, South African Voyager, Swiss Miles & More, TAP Miles&Go, Aegean Miles+Bonus

### SkyTeam (12 programs)
Delta SkyMiles, Air France/KLM Flying Blue, Korean Air SKYPASS, China Eastern Eastern Miles, China Southern Sky Pearl Club, Aeroméxico Rewards, Aerolíneas Plus, Czech Airlines OK Plus, ITA Volare, Kenya Airways Asante Rewards, Middle East Airlines Cedar Miles, Vietnam Airlines Lotusmiles

### Oneworld (13 programs)
American AAdvantage, British Airways Executive Club, Cathay Pacific Asia Miles, Qantas Frequent Flyer, Alaska Mileage Plan, Japan Airlines Mileage Bank, Finnair Plus, Iberia Plus, Malaysia Airlines Enrich, Qatar Airways Privilege Club, Royal Air Maroc Safar Flyer, Royal Jordanian Royal Plus, SriLankan Airlines FlySmiLes

### Independent (9 programs)
Emirates Skywards, Etihad Guest, Southwest Rapid Rewards, JetBlue TrueBlue, Virgin Atlantic Flying Club, Air Asia BIG, Frontier Miles, Spirit Free Spirit, Allegiant Allways Rewards

---

## 🛠️ Tech Stack

- **Frontend**: React 19 + TypeScript
- **Styling**: Tailwind CSS 4 + shadcn/ui
- **Routing**: Wouter (lightweight React router)
- **Build Tool**: Vite
- **Package Manager**: pnpm
- **Fonts**: Google Fonts (Playfair Display + Inter)

---

## 📝 License

This project is open source and available for personal and commercial use.

**Data Attribution:**
- Airport and airline data from [OpenFlights](https://openflights.org/)
- Loyalty program data manually curated from official airline sources

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

**Areas for contribution:**
- Additional loyalty programs
- Updated earning rates
- New features (multi-leg trips, credit card bonuses, etc.)
- Bug fixes and optimizations

---

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

## 🎉 Acknowledgments

- **OpenFlights** for comprehensive airport and airline databases
- **shadcn/ui** for beautiful React components
- **Tailwind CSS** for utility-first styling
- **Lando Norris** for design inspiration 🏎️

---

**Built with ❤️ for aviation enthusiasts and miles & points collectors**

✈️ Happy flying and happy earning! 🎯
