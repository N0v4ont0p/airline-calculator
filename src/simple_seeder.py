import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
from src.models.user import db
from src.models.airline import (
    Airline, Airport, LoyaltyProgram, EarningRate, 
    FareClass, BookingClass, Route, calculate_distance
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/airline-calculator/database/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def seed_basic_data():
    """Seed basic data for testing"""
    print("Seeding basic data...")
    
    # Major international airports
    airports_data = [
        ('JFK', 'John F. Kennedy International Airport', 'New York', 'NY', 'US', 40.6413, -73.7781),
        ('LAX', 'Los Angeles International Airport', 'Los Angeles', 'CA', 'US', 33.9425, -118.4081),
        ('LHR', 'London Heathrow Airport', 'London', '', 'GB', 51.4700, -0.4543),
        ('CDG', 'Charles de Gaulle Airport', 'Paris', '', 'FR', 49.0097, 2.5479),
        ('NRT', 'Narita International Airport', 'Tokyo', '', 'JP', 35.7720, 140.3929),
        ('SIN', 'Singapore Changi Airport', 'Singapore', '', 'SG', 1.3644, 103.9915),
        ('DXB', 'Dubai International Airport', 'Dubai', '', 'AE', 25.2532, 55.3657),
        ('FRA', 'Frankfurt Airport', 'Frankfurt', '', 'DE', 50.0379, 8.5622),
        ('SYD', 'Sydney Kingsford Smith Airport', 'Sydney', 'NSW', 'AU', -33.9399, 151.1753),
        ('HKG', 'Hong Kong International Airport', 'Hong Kong', '', 'HK', 22.3080, 113.9185),
        ('ICN', 'Incheon International Airport', 'Seoul', '', 'KR', 37.4602, 126.4407),
        ('YYZ', 'Toronto Pearson International Airport', 'Toronto', 'ON', 'CA', 43.6777, -79.6248),
        ('PVG', 'Shanghai Pudong International Airport', 'Shanghai', '', 'CN', 31.1443, 121.8083),
        ('BKK', 'Suvarnabhumi Airport', 'Bangkok', '', 'TH', 13.6900, 100.7501),
        ('DEL', 'Indira Gandhi International Airport', 'New Delhi', '', 'IN', 28.5562, 77.1000),
        ('GRU', 'São Paulo–Guarulhos International Airport', 'São Paulo', 'SP', 'BR', -23.4356, -46.4731),
        ('MEX', 'Mexico City International Airport', 'Mexico City', '', 'MX', 19.4363, -99.0721),
        ('JNB', 'O.R. Tambo International Airport', 'Johannesburg', '', 'ZA', -26.1367, 28.2411),
        ('CAI', 'Cairo International Airport', 'Cairo', '', 'EG', 30.1219, 31.4056),
        ('IST', 'Istanbul Airport', 'Istanbul', '', 'TR', 41.2619, 28.7279)
    ]
    
    for code, name, city, state, country, lat, lon in airports_data:
        airport = Airport(
            code=code,
            name=name,
            city=city,
            state=state,
            country=country,
            latitude=lat,
            longitude=lon
        )
        db.session.add(airport)
    
    # Airlines
    airlines_data = [
        # Star Alliance
        ('UA', 'United Airlines', 'Star Alliance', 'MileagePlus', 'US'),
        ('LH', 'Lufthansa', 'Star Alliance', 'Miles & More', 'DE'),
        ('AC', 'Air Canada', 'Star Alliance', 'Aeroplan', 'CA'),
        ('SQ', 'Singapore Airlines', 'Star Alliance', 'KrisFlyer', 'SG'),
        ('NH', 'All Nippon Airways', 'Star Alliance', 'ANA Mileage Club', 'JP'),
        
        # Oneworld
        ('AA', 'American Airlines', 'Oneworld', 'AAdvantage', 'US'),
        ('BA', 'British Airways', 'Oneworld', 'Executive Club', 'GB'),
        ('CX', 'Cathay Pacific', 'Oneworld', 'Asia Miles', 'HK'),
        ('QF', 'Qantas', 'Oneworld', 'Frequent Flyer', 'AU'),
        ('JL', 'Japan Airlines', 'Oneworld', 'JAL Mileage Bank', 'JP'),
        
        # SkyTeam
        ('DL', 'Delta Air Lines', 'SkyTeam', 'SkyMiles', 'US'),
        ('AF', 'Air France', 'SkyTeam', 'Flying Blue', 'FR'),
        ('KE', 'Korean Air', 'SkyTeam', 'SKYPASS', 'KR'),
        ('MU', 'China Eastern Airlines', 'SkyTeam', 'Eastern Miles', 'CN'),
        ('VN', 'Vietnam Airlines', 'SkyTeam', 'Lotusmiles', 'VN'),
        
        # Unallianced
        ('EK', 'Emirates', None, 'Skywards', 'AE'),
        ('EY', 'Etihad Airways', None, 'Etihad Guest', 'AE'),
        ('B6', 'JetBlue Airways', None, 'TrueBlue', 'US'),
        ('WN', 'Southwest Airlines', None, 'Rapid Rewards', 'US'),
        ('FR', 'Ryanair', None, 'myRyanair', 'IE')
    ]
    
    for code, name, alliance, loyalty_program, country in airlines_data:
        airline = Airline(
            code=code,
            name=name,
            alliance=alliance,
            loyalty_program=loyalty_program,
            country=country
        )
        db.session.add(airline)
    
    # Fare classes
    fare_classes_data = [
        ('Economy', 'Standard economy class'),
        ('Premium Economy', 'Enhanced economy with extra legroom and amenities'),
        ('Business', 'Business class with lie-flat seats and premium service'),
        ('First', 'First class with private suites and luxury amenities')
    ]
    
    for name, description in fare_classes_data:
        fare_class = FareClass(name=name, description=description)
        db.session.add(fare_class)
    
    db.session.commit()
    
    # Get fare classes for booking classes
    economy = FareClass.query.filter_by(name='Economy').first()
    premium_economy = FareClass.query.filter_by(name='Premium Economy').first()
    business = FareClass.query.filter_by(name='Business').first()
    first = FareClass.query.filter_by(name='First').first()
    
    # Booking classes
    booking_classes_data = [
        ('Y', economy.id, 'Full fare economy'),
        ('B', economy.id, 'Economy discount'),
        ('M', economy.id, 'Economy discount'),
        ('H', economy.id, 'Economy deep discount'),
        ('Q', economy.id, 'Economy deep discount'),
        ('V', economy.id, 'Economy deep discount'),
        ('W', premium_economy.id, 'Premium economy'),
        ('S', premium_economy.id, 'Premium economy discount'),
        ('J', business.id, 'Business full fare'),
        ('C', business.id, 'Business full fare'),
        ('D', business.id, 'Business discount'),
        ('F', first.id, 'First class full fare'),
        ('A', first.id, 'First class discount')
    ]
    
    for code, fare_class_id, description in booking_classes_data:
        booking_class = BookingClass(
            code=code,
            fare_class_id=fare_class_id,
            description=description
        )
        db.session.add(booking_class)
    
    # Loyalty programs and earning rates
    airlines = Airline.query.all()
    for airline in airlines:
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
        
        # Add earning rates
        earning_rates_data = [
            ('Economy', 'Y', 1.0, 500),
            ('Economy', 'B', 0.75, 500),
            ('Economy', 'M', 0.75, 500),
            ('Economy', 'H', 0.50, 500),
            ('Economy', 'Q', 0.25, 500),
            ('Economy', 'V', 0.25, 500),
            ('Premium Economy', 'W', 1.25, 500),
            ('Premium Economy', 'S', 1.0, 500),
            ('Business', 'J', 1.5, 500),
            ('Business', 'C', 1.5, 500),
            ('Business', 'D', 1.25, 500),
            ('First', 'F', 2.0, 500),
            ('First', 'A', 1.75, 500)
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
    
    db.session.commit()
    print(f"Seeded {len(airports_data)} airports, {len(airlines_data)} airlines, and loyalty programs")

def get_silver_tier_name(airline_code):
    tier_names = {
        'AA': 'Gold', 'DL': 'Silver Medallion', 'UA': 'Premier Silver',
        'BA': 'Bronze', 'AF': 'Silver', 'LH': 'Senator',
        'SQ': 'Elite Silver', 'CX': 'Silver', 'QF': 'Silver',
        'EK': 'Silver', 'TK': 'Elite', 'AC': 'Elite 25K'
    }
    return tier_names.get(airline_code, 'Silver')

def get_gold_tier_name(airline_code):
    tier_names = {
        'AA': 'Platinum', 'DL': 'Gold Medallion', 'UA': 'Premier Gold',
        'BA': 'Silver', 'AF': 'Gold', 'LH': 'Senator',
        'SQ': 'Elite Gold', 'CX': 'Gold', 'QF': 'Gold',
        'EK': 'Gold', 'TK': 'Elite Plus', 'AC': 'Elite 50K'
    }
    return tier_names.get(airline_code, 'Gold')

def get_platinum_tier_name(airline_code):
    tier_names = {
        'AA': 'Platinum Pro', 'DL': 'Platinum Medallion', 'UA': 'Premier Platinum',
        'BA': 'Gold', 'AF': 'Platinum', 'LH': 'HON Circle',
        'SQ': 'PPS Club', 'CX': 'Diamond', 'QF': 'Platinum',
        'EK': 'Platinum', 'TK': 'Elite Plus', 'AC': 'Elite 75K'
    }
    return tier_names.get(airline_code, 'Platinum')

def main():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(EarningRate).delete()
        db.session.query(LoyaltyProgram).delete()
        db.session.query(BookingClass).delete()
        db.session.query(FareClass).delete()
        db.session.query(Route).delete()
        db.session.query(Airline).delete()
        db.session.query(Airport).delete()
        db.session.commit()
        
        # Seed basic data
        seed_basic_data()
        
        print("Basic data seeding completed successfully!")

if __name__ == '__main__':
    main()

