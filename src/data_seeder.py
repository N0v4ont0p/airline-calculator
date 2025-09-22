import os
import sys
import pandas as pd
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

def seed_airports():
    """Seed airports from the processed international airports CSV"""
    print("Seeding airports...")
    
    # Read the processed international airports CSV
    airports_df = pd.read_csv('/home/ubuntu/international_airports.csv')
    
    for _, row in airports_df.iterrows():
        airport = Airport(
            name=row['name'],
            code=row['iata_code'],
            city=row['city'],
            country=row['country_code'],
            latitude=row['latitude_deg'],
            longitude=row['longitude_deg']
        )
        db.session.add(airport)
    
    db.session.commit()
    print(f"Seeded {len(airports_df)} airports")

def seed_airlines():
    """Seed airlines with comprehensive alliance data"""
    print("Seeding airlines...")
    
    # SkyTeam Airlines
    skyteam_airlines = [
        ('AR', 'Aerolíneas Argentinas', 'Argentina', 'Aerolíneas Plus'),
        ('AM', 'Aeromexico', 'Mexico', 'Club Premier'),
        ('UX', 'Air Europa', 'Spain', 'SUMA'),
        ('AF', 'Air France', 'France', 'Flying Blue'),
        ('CI', 'China Airlines', 'Taiwan', 'Dynasty Flyer'),
        ('MU', 'China Eastern Airlines', 'China', 'Eastern Miles'),
        ('DL', 'Delta Air Lines', 'United States', 'SkyMiles'),
        ('GA', 'Garuda Indonesia', 'Indonesia', 'GarudaMiles'),
        ('KQ', 'Kenya Airways', 'Kenya', 'Flying Blue'),
        ('KE', 'Korean Air', 'South Korea', 'SKYPASS'),
        ('ME', 'Middle East Airlines', 'Lebanon', 'Cedar Miles'),
        ('SV', 'Saudia', 'Saudi Arabia', 'Alfursan'),
        ('RO', 'TAROM', 'Romania', 'Flying Blue'),
        ('VN', 'Vietnam Airlines', 'Vietnam', 'Lotusmiles'),
        ('VS', 'Virgin Atlantic', 'United Kingdom', 'Flying Club'),
        ('MF', 'Xiamen Air', 'China', 'Egret Miles')
    ]
    
    # Oneworld Airlines
    oneworld_airlines = [
        ('AS', 'Alaska Airlines', 'United States', 'Mileage Plan'),
        ('AA', 'American Airlines', 'United States', 'AAdvantage'),
        ('BA', 'British Airways', 'United Kingdom', 'Executive Club'),
        ('CX', 'Cathay Pacific', 'Hong Kong', 'Asia Miles'),
        ('FJ', 'Fiji Airways', 'Fiji', 'Tabua Club'),
        ('AY', 'Finnair', 'Finland', 'Finnair Plus'),
        ('IB', 'Iberia', 'Spain', 'Iberia Plus'),
        ('JL', 'Japan Airlines', 'Japan', 'JAL Mileage Bank'),
        ('MH', 'Malaysia Airlines', 'Malaysia', 'Enrich'),
        ('QF', 'Qantas', 'Australia', 'Frequent Flyer'),
        ('QR', 'Qatar Airways', 'Qatar', 'Privilege Club'),
        ('AT', 'Royal Air Maroc', 'Morocco', 'Safar Flyer'),
        ('RJ', 'Royal Jordanian', 'Jordan', 'Royal Club'),
        ('UL', 'SriLankan Airlines', 'Sri Lanka', 'FlySmiLes')
    ]
    
    # Star Alliance Airlines
    star_alliance_airlines = [
        ('A3', 'Aegean Airlines', 'Greece', 'Miles+Bonus'),
        ('AC', 'Air Canada', 'Canada', 'Aeroplan'),
        ('CA', 'Air China', 'China', 'PhoenixMiles'),
        ('AI', 'Air India', 'India', 'Flying Returns'),
        ('NZ', 'Air New Zealand', 'New Zealand', 'Airpoints'),
        ('NH', 'All Nippon Airways', 'Japan', 'ANA Mileage Club'),
        ('OZ', 'Asiana Airlines', 'South Korea', 'Asiana Club'),
        ('OS', 'Austrian Airlines', 'Austria', 'Miles & More'),
        ('AV', 'Avianca', 'Colombia', 'LifeMiles'),
        ('SN', 'Brussels Airlines', 'Belgium', 'Miles & More'),
        ('CM', 'Copa Airlines', 'Panama', 'ConnectMiles'),
        ('OU', 'Croatia Airlines', 'Croatia', 'Miles & More'),
        ('MS', 'EgyptAir', 'Egypt', 'EgyptAir Plus'),
        ('ET', 'Ethiopian Airlines', 'Ethiopia', 'ShebaMiles'),
        ('BR', 'EVA Air', 'Taiwan', 'Infinity MileageLands'),
        ('LO', 'LOT Polish Airlines', 'Poland', 'Miles & More'),
        ('LH', 'Lufthansa', 'Germany', 'Miles & More'),
        ('SK', 'Scandinavian Airlines', 'Sweden', 'EuroBonus'),
        ('ZH', 'Shenzhen Airlines', 'China', 'Phoenix Miles'),
        ('SQ', 'Singapore Airlines', 'Singapore', 'KrisFlyer'),
        ('SA', 'South African Airways', 'South Africa', 'Voyager'),
        ('LX', 'SWISS', 'Switzerland', 'Miles & More'),
        ('TP', 'TAP Air Portugal', 'Portugal', 'TAP Miles&Go'),
        ('TG', 'Thai Airways', 'Thailand', 'Royal Orchid Plus'),
        ('TK', 'Turkish Airlines', 'Turkey', 'Miles&Smiles'),
        ('UA', 'United Airlines', 'United States', 'MileagePlus')
    ]
    
    # Unallianced Airlines
    unallianced_airlines = [
        ('EK', 'Emirates', 'United Arab Emirates', 'Skywards'),
        ('EY', 'Etihad Airways', 'United Arab Emirates', 'Etihad Guest'),
        ('HA', 'Hawaiian Airlines', 'United States', 'HawaiianMiles'),
        ('9Y', 'Juneyao Air', 'China', 'Juneyao Rewards'),
        ('LA', 'LATAM Airlines', 'Chile', 'LATAM Pass'),
        ('WN', 'Southwest Airlines', 'United States', 'Rapid Rewards'),
        ('G4', 'Allegiant Air', 'United States', 'myAllegiant Rewards'),
        ('F9', 'Frontier Airlines', 'United States', 'FRONTIER Miles'),
        ('NK', 'Spirit Airlines', 'United States', 'Free Spirit'),
        ('B6', 'JetBlue Airways', 'United States', 'TrueBlue'),
        ('FR', 'Ryanair', 'Ireland', 'myRyanair'),
        ('U2', 'EasyJet', 'United Kingdom', 'easyJet Plus'),
        ('DY', 'Norwegian Air', 'Norway', 'Norwegian Reward'),
        ('WS', 'WestJet', 'Canada', 'WestJet Rewards'),
        ('G3', 'GOL', 'Brazil', 'Smiles'),
        ('AD', 'Azul', 'Brazil', 'TudoAzul'),
        ('AK', 'AirAsia', 'Malaysia', 'BIG Loyalty'),
        ('JT', 'Lion Air', 'Indonesia', 'Lion Parcel'),
        ('6E', 'IndiGo', 'India', '6E Rewards'),
        ('SG', 'SpiceJet', 'India', 'SpiceClub'),
        ('VB', 'Viva Aerobus', 'Mexico', 'Viva Points'),
        ('Y4', 'Volaris', 'Mexico', 'v.club'),
        ('W6', 'Wizz Air', 'Hungary', 'Wizz Priority'),
        ('PC', 'Pegasus Airlines', 'Turkey', 'Pegasus BolBol')
    ]
    
    # Add all airlines
    for alliance, airlines in [
        ('SkyTeam', skyteam_airlines),
        ('Oneworld', oneworld_airlines),
        ('Star Alliance', star_alliance_airlines),
        (None, unallianced_airlines)
    ]:
        for code, name, country, loyalty_program in airlines:
            airline = Airline(
                code=code,
                name=name,
                alliance=alliance,
                country=country,
                loyalty_program=loyalty_program
            )
            db.session.add(airline)
    
    db.session.commit()
    print(f"Seeded {len(skyteam_airlines) + len(oneworld_airlines) + len(star_alliance_airlines) + len(unallianced_airlines)} airlines")

def seed_fare_classes():
    """Seed fare classes"""
    print("Seeding fare classes...")
    
    fare_classes = [
        ('Economy', 'Standard economy class'),
        ('Premium Economy', 'Enhanced economy with extra legroom and amenities'),
        ('Business', 'Business class with lie-flat seats and premium service'),
        ('First', 'First class with private suites and luxury amenities')
    ]
    
    for name, description in fare_classes:
        fare_class = FareClass(name=name, description=description)
        db.session.add(fare_class)
    
    db.session.commit()
    print(f"Seeded {len(fare_classes)} fare classes")

def seed_booking_classes():
    """Seed booking classes"""
    print("Seeding booking classes...")
    
    # Get fare classes
    economy = FareClass.query.filter_by(name='Economy').first()
    premium_economy = FareClass.query.filter_by(name='Premium Economy').first()
    business = FareClass.query.filter_by(name='Business').first()
    first = FareClass.query.filter_by(name='First').first()
    
    booking_classes = [
        # Economy
        ('Y', economy.id, 'Full fare economy'),
        ('B', economy.id, 'Economy discount'),
        ('M', economy.id, 'Economy discount'),
        ('U', economy.id, 'Economy discount'),
        ('H', economy.id, 'Economy deep discount'),
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
        ('X', economy.id, 'Economy deep discount'),
        ('E', economy.id, 'Economy deep discount'),
        
        # Premium Economy
        ('W', premium_economy.id, 'Premium economy full fare'),
        ('S', premium_economy.id, 'Premium economy discount'),
        ('A', premium_economy.id, 'Premium economy discount'),
        
        # Business
        ('J', business.id, 'Business full fare'),
        ('C', business.id, 'Business full fare'),
        ('D', business.id, 'Business discount'),
        ('I', business.id, 'Business discount'),
        ('Z', business.id, 'Business discount'),
        
        # First
        ('F', first.id, 'First class full fare'),
        ('A', first.id, 'First class discount'),
        ('P', first.id, 'First class discount')
    ]
    
    for code, fare_class_id, description in booking_classes:
        booking_class = BookingClass(
            code=code,
            fare_class_id=fare_class_id,
            description=description
        )
        db.session.add(booking_class)
    
    db.session.commit()
    print(f"Seeded {len(booking_classes)} booking classes")

def seed_loyalty_programs():
    """Seed loyalty programs with realistic earning rates"""
    print("Seeding loyalty programs...")
    
    airlines = Airline.query.all()
    
    for airline in airlines:
        # Create loyalty program
        loyalty_program = LoyaltyProgram(
            name=airline.loyalty_program,
            airline_id=airline.id,
            alliance=airline.alliance,
            earning_model='distance',  # Most programs are distance-based
            base_earning_rate=1.0,  # 1 mile per mile flown as base
            silver_tier_name=get_silver_tier_name(airline.code),
            gold_tier_name=get_gold_tier_name(airline.code),
            platinum_tier_name=get_platinum_tier_name(airline.code),
            silver_bonus=0.25,  # 25% bonus
            gold_bonus=0.50,    # 50% bonus
            platinum_bonus=1.0  # 100% bonus
        )
        db.session.add(loyalty_program)
        db.session.flush()  # Get the ID
        
        # Add earning rates for different fare/booking classes
        earning_rates = [
            # Economy classes
            ('Economy', 'Y', 1.0, 500),  # Full fare economy
            ('Economy', 'B', 0.75, 500), # Economy discount
            ('Economy', 'M', 0.75, 500),
            ('Economy', 'U', 0.50, 500), # Economy discount
            ('Economy', 'H', 0.50, 500), # Economy deep discount
            ('Economy', 'Q', 0.25, 500),
            ('Economy', 'V', 0.25, 500),
            ('Economy', 'W', 0.25, 500),
            ('Economy', 'S', 0.25, 500),
            ('Economy', 'T', 0.25, 500),
            ('Economy', 'L', 0.25, 500),
            ('Economy', 'K', 0.25, 500),
            ('Economy', 'G', 0.25, 500),
            ('Economy', 'N', 0.25, 500),
            ('Economy', 'R', 0.25, 500),
            ('Economy', 'X', 0.25, 500),
            ('Economy', 'E', 0.25, 500),
            
            # Premium Economy
            ('Premium Economy', 'W', 1.25, 500),
            ('Premium Economy', 'S', 1.0, 500),
            ('Premium Economy', 'A', 1.0, 500),
            
            # Business
            ('Business', 'J', 1.5, 500),
            ('Business', 'C', 1.5, 500),
            ('Business', 'D', 1.25, 500),
            ('Business', 'I', 1.25, 500),
            ('Business', 'Z', 1.0, 500),
            
            # First
            ('First', 'F', 2.0, 500),
            ('First', 'A', 1.75, 500),
            ('First', 'P', 1.5, 500)
        ]
        
        for fare_class, booking_class, earning_percentage, minimum_miles in earning_rates:
            earning_rate = EarningRate(
                loyalty_program_id=loyalty_program.id,
                fare_class=fare_class,
                booking_class=booking_class,
                earning_percentage=earning_percentage,
                minimum_miles=minimum_miles,
                elite_bonus_silver=0.0,  # Use program defaults
                elite_bonus_gold=0.0,
                elite_bonus_platinum=0.0
            )
            db.session.add(earning_rate)
    
    db.session.commit()
    print(f"Seeded loyalty programs for {len(airlines)} airlines")

def get_silver_tier_name(airline_code):
    """Get airline-specific silver tier names"""
    tier_names = {
        'AA': 'Gold',
        'DL': 'Silver Medallion',
        'UA': 'Premier Silver',
        'BA': 'Bronze',
        'AF': 'Silver',
        'LH': 'Senator',
        'SQ': 'Elite Silver',
        'CX': 'Silver',
        'QF': 'Silver',
        'EK': 'Silver',
        'TK': 'Elite',
        'AC': 'Elite 25K'
    }
    return tier_names.get(airline_code, 'Silver')

def get_gold_tier_name(airline_code):
    """Get airline-specific gold tier names"""
    tier_names = {
        'AA': 'Platinum',
        'DL': 'Gold Medallion',
        'UA': 'Premier Gold',
        'BA': 'Silver',
        'AF': 'Gold',
        'LH': 'Senator',
        'SQ': 'Elite Gold',
        'CX': 'Gold',
        'QF': 'Gold',
        'EK': 'Gold',
        'TK': 'Elite Plus',
        'AC': 'Elite 50K'
    }
    return tier_names.get(airline_code, 'Gold')

def get_platinum_tier_name(airline_code):
    """Get airline-specific platinum tier names"""
    tier_names = {
        'AA': 'Platinum Pro',
        'DL': 'Platinum Medallion',
        'UA': 'Premier Platinum',
        'BA': 'Gold',
        'AF': 'Platinum',
        'LH': 'HON Circle',
        'SQ': 'PPS Club',
        'CX': 'Diamond',
        'QF': 'Platinum',
        'EK': 'Platinum',
        'TK': 'Elite Plus',
        'AC': 'Elite 75K'
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
        
        # Seed data
        seed_airports()
        seed_airlines()
        seed_fare_classes()
        seed_booking_classes()
        seed_loyalty_programs()
        
        print("Data seeding completed successfully!")

if __name__ == '__main__':
    main()

