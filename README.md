# 🛫 The World's Best Airline Miles Calculator

The most comprehensive airline miles calculator with worldwide coverage, accurate calculations, and professional design.

## 🌟 Features

### ✈️ **Comprehensive Coverage**
- **179 International Airports** worldwide from Wikipedia's comprehensive database
- **69 Airlines** across all major alliances (Star Alliance, Oneworld, SkyTeam) plus unallianced carriers
- **63 Loyalty Programs** with airline-specific tier names and earning rates
- **1,638 Earning Rate Combinations** for accurate, program-specific calculations

### 🎯 **Accurate Calculations**
- **Different programs earn different miles** for the same flight (industry-accurate)
- **Separate airline vs loyalty program selection** (fly Cathay Pacific, credit to Qantas)
- **Elite status bonuses** with airline-specific tier names
- **Minimum miles rules** (500 miles per segment)
- **Booking class variations** (Y, J, C, F with different earning rates)

### 🎨 **Professional Design**
- **Modern, Apple-inspired interface** with clean card-based layout
- **No overlap issues** - proper z-index management for all dropdowns
- **Responsive design** that works on all screen sizes
- **Intuitive workflow** with clear visual hierarchy

### 🔧 **Technical Excellence**
- **Flask backend** with SQLite database
- **React frontend** with modern UI components
- **RESTful API** for all data operations
- **Production-ready** with proper error handling

## 🚀 Quick Deploy to Render.com

1. **Extract** this archive to your repository
2. **Push** to GitHub (or your Git provider)
3. **Connect** to Render.com - it will automatically detect the `render.yaml`
4. **Deploy** - Render will build and start automatically

## 🛠️ Local Development

### Backend Setup
```bash
cd airline-miles-calculator-ULTIMATE
pip install -r requirements.txt
python3 src/ultimate_seeder.py  # Populate database
python3 src/main.py             # Start server
```

### Frontend Development
The production-built frontend is included in `src/static/`. For development:
```bash
# Frontend source is in the original project
npm install
npm run dev
```

## 📊 Database Statistics

- **179 Airports**: All major international airports worldwide
- **69 Airlines**: Complete coverage of global carriers
- **63 Loyalty Programs**: Every major frequent flyer program
- **4 Fare Classes**: Economy, Premium Economy, Business, First
- **26 Booking Classes**: Complete IATA booking class coverage
- **1,638 Earning Rates**: Program-specific earning variations

## 🌍 Alliance Coverage

### Star Alliance (21 Programs)
United MileagePlus, Lufthansa Miles & More, Singapore KrisFlyer, ANA Mileage Club, Air Canada Aeroplan, and more.

### Oneworld (14 Programs)  
American AAdvantage, British Airways Executive Club, Cathay Pacific Asia Miles, Qantas Frequent Flyer, JAL Mileage Bank, and more.

### SkyTeam (15 Programs)
Delta SkyMiles, Air France-KLM Flying Blue, Korean Air SKYPASS, Aeroflot Bonus, China Southern Sky Pearl Club, and more.

### Unallianced (13 Programs)
Emirates Skywards, Etihad Guest, JetBlue TrueBlue, Southwest Rapid Rewards, and more.

## 🎯 Key Differentiators

1. **Separate Operating Airline vs Loyalty Program**: Accurately reflects real-world crediting scenarios
2. **Program-Specific Earning Rates**: Different loyalty programs earn different miles for the same flight
3. **Comprehensive Airport Database**: 179 international airports from Wikipedia's authoritative list
4. **Professional UI/UX**: No overlap issues, modern design, intuitive workflow
5. **Industry-Accurate Calculations**: Proper elite bonuses, minimum miles, booking class variations

## 📈 Example Calculation

**Route**: Shanghai (PVG) → Singapore (SIN), Cathay Pacific Business Class J

**Different Programs, Different Miles**:
- American AAdvantage: 4,059 miles (175% earning rate)
- British Airways Executive Club: 3,353 miles (142.5% earning rate)  
- Qantas Frequent Flyer: 3,000 miles (127.5% earning rate)

*Same flight, different programs = different miles earned!*

## 🏆 The World's Best

This airline miles calculator sets the industry standard with comprehensive data coverage, accurate calculations, and professional design. Whether you're a frequent flyer optimizing your earning strategy or a travel enthusiast planning your next adventure, this calculator provides the most accurate and comprehensive miles calculations available.

---

**Built with ❤️ for the global travel community**
