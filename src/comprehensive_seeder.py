import os
import sys
import csv
from math import radians, cos, sin, asin, sqrt

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.airline import Airport, Airline, LoyaltyProgram, EarningRate, FareClass, BookingClass

def get_program_multiplier(airline_code):
    """
    Get program-specific multiplier to create different earning rates for different programs.
    This ensures that the same Cathay Pacific flight credited to different Oneworld programs
    will earn different amounts of miles.
    """
    multipliers = {
        # Star Alliance - varying rates
        'UA': 1.0,    # United - baseline
        'LH': 1.1,    # Lufthansa - slightly higher
        'SQ': 1.2,    # Singapore Airlines - premium rates
        'AC': 0.9,    # Air Canada - slightly lower
        'NH': 1.05,   # ANA - moderate premium
        
        # Oneworld - varying rates
        'AA': 1.15,   # American - good rates
        'BA': 0.95,   # British Airways - lower rates (Avios system)
        'CX': 1.1,    # Cathay Pacific - good rates
        'QF': 0.85,   # Qantas - lower rates (different point system)
        'JL': 1.0,    # JAL - baseline
        
        # SkyTeam - varying rates
        'DL': 1.05,   # Delta - moderate rates
        'AF': 1.0,    # Air France - baseline
        'KL': 1.0,    # KLM - baseline
        'KE': 1.1,    # Korean Air - good rates
        'AZ': 0.9,    # Alitalia - lower rates
        
        # Unallianced - varying rates
        'EK': 1.3,    # Emirates - premium rates
        'EY': 1.25,   # Etihad - high rates
        'B6': 0.8,    # JetBlue - lower rates (TrueBlue points)
        'WN': 0.7,    # Southwest - much lower (Rapid Rewards points)
        'AS': 1.0,    # Alaska - baseline
    }
    
    # Default multiplier for airlines not specifically listed
    return multipliers.get(airline_code, 1.0)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on earth (specified in decimal degrees)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    
    return c * r

def get_silver_tier_name(airline_code):
    """Get airline-specific silver tier name"""
    tier_names = {
        'UA': 'Premier Silver',
        'AA': 'Gold',
        'DL': 'Silver Medallion',
        'BA': 'Executive Club Silver',
        'LH': 'Senator',
        'AF': 'Silver',
        'KL': 'Silver',
        'SQ': 'PPS Club',
        'CX': 'Marco Polo Silver',
        'QF': 'Silver',
        'JL': 'Crystal',
        'NH': 'Bronze',
        'AC': 'Elite 25K',
        'EK': 'Silver',
        'EY': 'Silver',
        'KE': 'Morning Calm Club Silver',
        'AZ': 'MilleMiglia Silver',
        'B6': 'Mosaic',
        'WN': 'A-List',
        'AS': 'MVP'
    }
    return tier_names.get(airline_code, 'Silver')

def get_gold_tier_name(airline_code):
    """Get airline-specific gold tier name"""
    tier_names = {
        'UA': 'Premier Gold',
        'AA': 'Platinum',
        'DL': 'Gold Medallion',
        'BA': 'Executive Club Gold',
        'LH': 'HON Circle',
        'AF': 'Gold',
        'KL': 'Gold',
        'SQ': 'KrisFlyer Elite Gold',
        'CX': 'Marco Polo Gold',
        'QF': 'Gold',
        'JL': 'Sapphire',
        'NH': 'Platinum',
        'AC': 'Elite 50K',
        'EK': 'Gold',
        'EY': 'Gold',
        'KE': 'Morning Calm Club Gold',
        'AZ': 'MilleMiglia Gold',
        'B6': 'Mosaic+',
        'WN': 'A-List Preferred',
        'AS': 'MVP Gold'
    }
    return tier_names.get(airline_code, 'Gold')

def get_platinum_tier_name(airline_code):
    """Get airline-specific platinum tier name"""
    tier_names = {
        'UA': 'Premier Platinum',
        'AA': 'Platinum Pro',
        'DL': 'Platinum Medallion',
        'BA': 'Executive Club Platinum',
        'LH': 'HON Circle Member',
        'AF': 'Platinum',
        'KL': 'Platinum',
        'SQ': 'PPS Club',
        'CX': 'Marco Polo Diamond',
        'QF': 'Platinum',
        'JL': 'Diamond',
        'NH': 'Diamond',
        'AC': 'Elite 75K',
        'EK': 'Platinum',
        'EY': 'Platinum',
        'KE': 'Morning Calm Club Platinum',
        'AZ': 'MilleMiglia Platinum',
        'B6': 'Mint',
        'WN': 'Companion Pass',
        'AS': 'MVP Gold 75K'
    }
    return tier_names.get(airline_code, 'Platinum')

def clear_existing_data():
    """Clear existing data from all tables"""
    print("Clearing existing data...")
    
    # Delete in reverse order of dependencies
    EarningRate.query.delete()
    BookingClass.query.delete()
    FareClass.query.delete()
    LoyaltyProgram.query.delete()
    Airline.query.delete()
    Airport.query.delete()
    
    db.session.commit()

def seed_airports():
    """Seed comprehensive airport data from international_airports.csv"""
    print("Seeding comprehensive airport data...")
    
    csv_file_path = '/home/ubuntu/international_airports.csv'
    
    if not os.path.exists(csv_file_path):
        print(f"Error: {csv_file_path} not found!")
        return
    
    airports_added = 0
    batch_size = 1000
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        airports_batch = []
        
        for row in reader:
            # Skip if airport already exists
            existing = Airport.query.filter_by(code=row['iata_code']).first()
            if existing:
                continue
                
            airport = Airport(
                code=row['iata_code'],
                name=row['name'],
                city=row['city'],
                state='',  # Not available in this CSV format
                country=row['country_code'],
                latitude=float(row['latitude_deg']),
                longitude=float(row['longitude_deg'])
            )
            airports_batch.append(airport)
            
            # Commit in batches for better performance
            if len(airports_batch) >= batch_size:
                db.session.add_all(airports_batch)
                db.session.commit()
                airports_added += len(airports_batch)
                print(f"Added {airports_added} airports...")
                airports_batch = []
        
        # Add remaining airports
        if airports_batch:
            db.session.add_all(airports_batch)
            db.session.commit()
            airports_added += len(airports_batch)
    
    print(f"Successfully added {airports_added} airports to the database")

def seed_airlines():
    """Seed comprehensive airline data"""
    print("Seeding comprehensive airline data...")
    
    airlines_data = [
        # Star Alliance
        ('UA', 'United Airlines', 'US', 'Star Alliance', 'MileagePlus'),
        ('LH', 'Lufthansa', 'DE', 'Star Alliance', 'Miles & More'),
        ('SQ', 'Singapore Airlines', 'SG', 'Star Alliance', 'KrisFlyer'),
        ('AC', 'Air Canada', 'CA', 'Star Alliance', 'Aeroplan'),
        ('NH', 'All Nippon Airways', 'JP', 'Star Alliance', 'ANA Mileage Club'),
        ('OS', 'Austrian Airlines', 'AT', 'Star Alliance', 'Miles & More'),
        ('SN', 'Brussels Airlines', 'BE', 'Star Alliance', 'Miles & More'),
        ('CA', 'Air China', 'CN', 'Star Alliance', 'PhoenixMiles'),
        ('HR', 'Croatia Airlines', 'HR', 'Star Alliance', 'Miles & More'),
        ('MS', 'EgyptAir', 'EG', 'Star Alliance', 'EgyptAir Plus'),
        ('ET', 'Ethiopian Airlines', 'ET', 'Star Alliance', 'ShebaMiles'),
        ('EW', 'Eurowings', 'DE', 'Star Alliance', 'Miles & More'),
        ('LO', 'LOT Polish Airlines', 'PL', 'Star Alliance', 'Miles & More'),
        ('SK', 'SAS', 'SE', 'Star Alliance', 'EuroBonus'),
        ('ZH', 'Shenzhen Airlines', 'CN', 'Star Alliance', 'Phoenix Miles'),
        ('CM', 'Copa Airlines', 'PA', 'Star Alliance', 'ConnectMiles'),
        ('OU', 'Croatia Airlines', 'HR', 'Star Alliance', 'Miles & More'),
        ('TG', 'Thai Airways', 'TH', 'Star Alliance', 'Royal Orchid Plus'),
        ('TP', 'TAP Air Portugal', 'PT', 'Star Alliance', 'TAP Miles&Go'),
        ('TK', 'Turkish Airlines', 'TR', 'Star Alliance', 'Miles&Smiles'),
        ('SA', 'South African Airways', 'ZA', 'Star Alliance', 'Voyager'),
        
        # Oneworld
        ('AA', 'American Airlines', 'US', 'Oneworld', 'AAdvantage'),
        ('BA', 'British Airways', 'GB', 'Oneworld', 'Executive Club'),
        ('CX', 'Cathay Pacific', 'HK', 'Oneworld', 'Asia Miles'),
        ('QF', 'Qantas', 'AU', 'Oneworld', 'Frequent Flyer'),
        ('JL', 'Japan Airlines', 'JP', 'Oneworld', 'JAL Mileage Bank'),
        ('IB', 'Iberia', 'ES', 'Oneworld', 'Iberia Plus'),
        ('AY', 'Finnair', 'FI', 'Oneworld', 'Finnair Plus'),
        ('QR', 'Qatar Airways', 'QA', 'Oneworld', 'Privilege Club'),
        ('RJ', 'Royal Jordanian', 'JO', 'Oneworld', 'Royal Club'),
        ('S7', 'S7 Airlines', 'RU', 'Oneworld', 'S7 Priority'),
        ('LA', 'LATAM Airlines', 'CL', 'Oneworld', 'LATAM Pass'),
        ('MH', 'Malaysia Airlines', 'MY', 'Oneworld', 'Enrich'),
        ('WF', 'Fiji Airways', 'FJ', 'Oneworld', 'Tabua Club'),
        ('AS', 'Alaska Airlines', 'US', 'Oneworld', 'Mileage Plan'),
        
        # SkyTeam
        ('DL', 'Delta Air Lines', 'US', 'SkyTeam', 'SkyMiles'),
        ('AF', 'Air France', 'FR', 'SkyTeam', 'Flying Blue'),
        ('KL', 'KLM', 'NL', 'SkyTeam', 'Flying Blue'),
        ('KE', 'Korean Air', 'KR', 'SkyTeam', 'SKYPASS'),
        ('AZ', 'ITA Airways', 'IT', 'SkyTeam', 'Volare'),
        ('AM', 'Aeromexico', 'MX', 'SkyTeam', 'Club Premier'),
        ('AR', 'Aerolineas Argentinas', 'AR', 'SkyTeam', 'Aerolineas Plus'),
        ('SU', 'Aeroflot', 'RU', 'SkyTeam', 'Aeroflot Bonus'),
        ('UX', 'Air Europa', 'ES', 'SkyTeam', 'SUMA'),
        ('MF', 'Xiamen Airlines', 'CN', 'SkyTeam', 'Egret Miles'),
        ('CZ', 'China Southern', 'CN', 'SkyTeam', 'Sky Pearl Club'),
        ('MU', 'China Eastern', 'CN', 'SkyTeam', 'Eastern Miles'),
        ('OK', 'Czech Airlines', 'CZ', 'SkyTeam', 'OK Plus'),
        ('RO', 'TAROM', 'RO', 'SkyTeam', 'Flying Blue'),
        ('VN', 'Vietnam Airlines', 'VN', 'SkyTeam', 'Lotusmiles'),
        
        # Unallianced
        ('EK', 'Emirates', 'AE', None, 'Skywards'),
        ('EY', 'Etihad Airways', 'AE', None, 'Etihad Guest'),
        ('B6', 'JetBlue Airways', 'US', None, 'TrueBlue'),
        ('WN', 'Southwest Airlines', 'US', None, 'Rapid Rewards'),
        ('F9', 'Frontier Airlines', 'US', None, 'FRONTIER Miles'),
        ('NK', 'Spirit Airlines', 'US', None, 'Free Spirit'),
        ('G4', 'Allegiant Air', 'US', None, 'myAllegiant Rewards'),
        ('SY', 'Sun Country Airlines', 'US', None, 'Ufly Rewards'),
        ('HA', 'Hawaiian Airlines', 'US', None, 'HawaiianMiles'),
    ]
    
    airlines_added = 0
    for code, name, country, alliance, loyalty_program in airlines_data:
        # Skip if airline already exists
        existing = Airline.query.filter_by(code=code).first()
        if existing:
            continue
            
        airline = Airline(
            code=code,
            name=name,
            country=country,
            alliance=alliance,
            loyalty_program=loyalty_program
        )
        db.session.add(airline)
        airlines_added += 1
    
    db.session.commit()
    print(f"Successfully added {airlines_added} airlines to the database")

def seed_fare_and_booking_classes():
    """Seed fare classes and booking classes"""
    print("Seeding fare and booking classes...")
    
    # Add fare classes
    fare_classes_data = [
        ('Economy', 'Economy class'),
        ('Premium Economy', 'Premium economy class'),
        ('Business', 'Business class'),
        ('First', 'First class')
    ]
    
    for name, description in fare_classes_data:
        existing = FareClass.query.filter_by(name=name).first()
        if not existing:
            fare_class = FareClass(name=name, description=description)
            db.session.add(fare_class)
    
    db.session.commit()
    
    # Get fare class objects
    economy = FareClass.query.filter_by(name='Economy').first()
    premium_economy = FareClass.query.filter_by(name='Premium Economy').first()
    business = FareClass.query.filter_by(name='Business').first()
    first = FareClass.query.filter_by(name='First').first()
    
    # Add booking classes
    booking_classes_data = [
        # Economy booking classes
        ('Y', economy.id, 'Full fare economy'),
        ('B', economy.id, 'Economy discount'),
        ('M', economy.id, 'Economy discount'),
        ('H', economy.id, 'Economy discount'),
        ('Q', economy.id, 'Economy deep discount'),
        ('V', economy.id, 'Economy deep discount'),
        ('W', economy.id, 'Economy deep discount'),
        ('S', economy.id, 'Economy deep discount'),
        ('T', economy.id, 'Economy deep discount'),
        ('L', economy.id, 'Economy deep discount'),
        ('K', economy.id, 'Economy deep discount'),
        ('G', economy.id, 'Economy deep discount'),
        ('N', economy.id, 'Economy deep discount'),
        ('R', economy.id, 'Economy deep discount'),
        ('E', economy.id, 'Economy deep discount'),
        
        # Premium Economy booking classes
        ('W', premium_economy.id, 'Premium economy full fare'),
        ('S', premium_economy.id, 'Premium economy discount'),
        ('A', premium_economy.id, 'Premium economy discount'),
        
        # Business booking classes
        ('J', business.id, 'Business full fare'),
        ('C', business.id, 'Business full fare'),
        ('D', business.id, 'Business discount'),
        ('I', business.id, 'Business discount'),
        ('Z', business.id, 'Business discount'),
        
        # First class booking classes
        ('F', first.id, 'First class full fare'),
        ('A', first.id, 'First class discount'),
        ('P', first.id, 'First class discount')
    ]
    
    booking_classes_added = 0
    for code, fare_class_id, description in booking_classes_data:
        # Check if this combination already exists
        existing = BookingClass.query.filter_by(code=code, fare_class_id=fare_class_id).first()
        if not existing:
            booking_class = BookingClass(
                code=code,
                fare_class_id=fare_class_id,
                description=description
            )
            db.session.add(booking_class)
            booking_classes_added += 1
    
    db.session.commit()
    print(f"Successfully added {booking_classes_added} booking classes to the database")

def seed_loyalty_programs_and_earning_rates():
    """Seed loyalty programs and earning rates for all airlines"""
    print("Seeding loyalty programs and earning rates...")
    
    airlines = Airline.query.all()
    programs_added = 0
    rates_added = 0
    
    for airline in airlines:
        # Skip if loyalty program already exists
        existing_program = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
        if existing_program:
            continue
            
        # Create loyalty program
        loyalty_program = LoyaltyProgram(
            name=airline.loyalty_program,
            airline_id=airline.id,
            alliance=airline.alliance,
            earning_model='distance',
            base_earning_rate=1.0,
            silver_tier_name=get_silver_tier_name(airline.code),
            gold_tier_name=get_gold_tier_name(airline.code),
            platinum_tier_name=get_platinum_tier_name(airline.code),
            silver_bonus=0.25,
            gold_bonus=0.50,
            platinum_bonus=1.0
        )
        db.session.add(loyalty_program)
        db.session.flush()
        programs_added += 1
        
        # Add earning rates for this loyalty program - DIFFERENT RATES FOR DIFFERENT PROGRAMS
        # Each airline/program has different earning rates for the same booking class
        base_multiplier = get_program_multiplier(airline.code)
        
        earning_rates_data = [
            # Economy rates (vary by program)
            ('Economy', 'Y', 1.0 * base_multiplier, 500),
            ('Economy', 'B', 0.75 * base_multiplier, 500),
            ('Economy', 'M', 0.75 * base_multiplier, 500),
            ('Economy', 'H', 0.50 * base_multiplier, 500),
            ('Economy', 'Q', 0.25 * base_multiplier, 500),
            ('Economy', 'V', 0.25 * base_multiplier, 500),
            ('Economy', 'W', 0.25 * base_multiplier, 500),
            ('Economy', 'S', 0.25 * base_multiplier, 500),
            ('Economy', 'T', 0.25 * base_multiplier, 500),
            ('Economy', 'L', 0.25 * base_multiplier, 500),
            ('Economy', 'K', 0.25 * base_multiplier, 500),
            ('Economy', 'G', 0.25 * base_multiplier, 500),
            ('Economy', 'N', 0.25 * base_multiplier, 500),
            ('Economy', 'R', 0.25 * base_multiplier, 500),
            ('Economy', 'E', 0.25 * base_multiplier, 500),
            
            # Premium Economy rates (vary by program)
            ('Premium Economy', 'W', 1.25 * base_multiplier, 500),
            ('Premium Economy', 'S', 1.0 * base_multiplier, 500),
            ('Premium Economy', 'A', 1.0 * base_multiplier, 500),
            
            # Business rates (vary by program)
            ('Business', 'J', 1.5 * base_multiplier, 500),
            ('Business', 'C', 1.5 * base_multiplier, 500),
            ('Business', 'D', 1.25 * base_multiplier, 500),
            ('Business', 'I', 1.25 * base_multiplier, 500),
            ('Business', 'Z', 1.0 * base_multiplier, 500),
            
            # First class rates (vary by program)
            ('First', 'F', 2.0 * base_multiplier, 500),
            ('First', 'A', 1.75 * base_multiplier, 500),
            ('First', 'P', 1.5 * base_multiplier, 500)
        ]
        
        for fare_class, booking_class, earning_percentage, minimum_miles in earning_rates_data:
            earning_rate = EarningRate(
                loyalty_program_id=loyalty_program.id,
                fare_class=fare_class,
                booking_class=booking_class,
                earning_percentage=earning_percentage,
                minimum_miles=minimum_miles
            )
            db.session.add(earning_rate)
            rates_added += 1
    
    db.session.commit()
    print(f"Successfully added {programs_added} loyalty programs and {rates_added} earning rates")

def main():
    """Main seeding function"""
    from src.models.user import db
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        clear_existing_data()
        seed_airports()
        seed_airlines()
        seed_fare_and_booking_classes()
        seed_loyalty_programs_and_earning_rates()
        
        print("=" * 50)
        print("COMPREHENSIVE DATA SEEDING COMPLETED!")
        print("=" * 50)
        print(f"Total airports: {Airport.query.count():,}")
        print(f"Total airlines: {Airline.query.count()}")
        print(f"Total loyalty programs: {LoyaltyProgram.query.count()}")
        print(f"Total earning rates: {EarningRate.query.count():,}")
        print(f"Total fare classes: {FareClass.query.count()}")
        print(f"Total booking classes: {BookingClass.query.count()}")
        print("=" * 50)

if __name__ == '__main__':
    main()
