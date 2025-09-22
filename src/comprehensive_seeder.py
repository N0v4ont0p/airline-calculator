#!/usr/bin/env python3
"""
Comprehensive data seeder for the airline miles calculator using the full OurAirports dataset.
"""

import os
import sys
import csv
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

def seed_comprehensive_airports():
    """Seed comprehensive airport data from the processed OurAirports dataset"""
    print("Seeding comprehensive airport data...")
    
    airports_file = '/home/ubuntu/comprehensive_airports.csv'
    if not os.path.exists(airports_file):
        print(f"Error: {airports_file} not found! Please run process_comprehensive_airports.py first.")
        return
    
    airports_added = 0
    
    with open(airports_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Skip if airport already exists
            existing = Airport.query.filter_by(code=row['code']).first()
            if existing:
                continue
            
            airport = Airport(
                code=row['code'],
                name=row['name'],
                city=row['city'],
                state=row['state'] if row['state'] else None,
                country=row['country'],
                latitude=float(row['latitude']),
                longitude=float(row['longitude'])
            )
            
            db.session.add(airport)
            airports_added += 1
            
            # Commit in batches to avoid memory issues
            if airports_added % 1000 == 0:
                db.session.commit()
                print(f"Added {airports_added} airports...")
    
    db.session.commit()
    print(f"Successfully added {airports_added} airports to the database")

def seed_comprehensive_airlines():
    """Seed comprehensive airline data with major international carriers"""
    print("Seeding comprehensive airline data...")
    
    # Comprehensive airline data including major international carriers
    airlines_data = [
        # Star Alliance (Major carriers)
        ('UA', 'United Airlines', 'Star Alliance', 'MileagePlus', 'US'),
        ('LH', 'Lufthansa', 'Star Alliance', 'Miles & More', 'DE'),
        ('AC', 'Air Canada', 'Star Alliance', 'Aeroplan', 'CA'),
        ('SQ', 'Singapore Airlines', 'Star Alliance', 'KrisFlyer', 'SG'),
        ('NH', 'All Nippon Airways', 'Star Alliance', 'ANA Mileage Club', 'JP'),
        ('TK', 'Turkish Airlines', 'Star Alliance', 'Miles&Smiles', 'TR'),
        ('LX', 'Swiss International Air Lines', 'Star Alliance', 'Miles & More', 'CH'),
        ('OS', 'Austrian Airlines', 'Star Alliance', 'Miles & More', 'AT'),
        ('SN', 'Brussels Airlines', 'Star Alliance', 'Miles & More', 'BE'),
        ('TP', 'TAP Air Portugal', 'Star Alliance', 'TAP Miles&Go', 'PT'),
        ('SK', 'Scandinavian Airlines', 'Star Alliance', 'EuroBonus', 'SE'),
        ('TG', 'Thai Airways', 'Star Alliance', 'Royal Orchid Plus', 'TH'),
        ('EV', 'EVA Air', 'Star Alliance', 'Infinity MileageLands', 'TW'),
        ('OZ', 'Asiana Airlines', 'Star Alliance', 'Asiana Club', 'KR'),
        ('CA', 'Air China', 'Star Alliance', 'PhoenixMiles', 'CN'),
        
        # Oneworld (Major carriers)
        ('AA', 'American Airlines', 'Oneworld', 'AAdvantage', 'US'),
        ('BA', 'British Airways', 'Oneworld', 'Executive Club', 'GB'),
        ('CX', 'Cathay Pacific', 'Oneworld', 'Asia Miles', 'HK'),
        ('QF', 'Qantas', 'Oneworld', 'Frequent Flyer', 'AU'),
        ('JL', 'Japan Airlines', 'Oneworld', 'JAL Mileage Bank', 'JP'),
        ('IB', 'Iberia', 'Oneworld', 'Iberia Plus', 'ES'),
        ('AY', 'Finnair', 'Oneworld', 'Finnair Plus', 'FI'),
        ('QR', 'Qatar Airways', 'Oneworld', 'Privilege Club', 'QA'),
        ('RJ', 'Royal Jordanian', 'Oneworld', 'Royal Club', 'JO'),
        ('S7', 'S7 Airlines', 'Oneworld', 'S7 Priority', 'RU'),
        ('MH', 'Malaysia Airlines', 'Oneworld', 'Enrich', 'MY'),
        ('WF', 'Widerøe', 'Oneworld', 'Widerøe Club', 'NO'),
        ('AT', 'Royal Air Maroc', 'Oneworld', 'Safar Flyer', 'MA'),
        ('OW', 'Oman Air', 'Oneworld', 'Sindbad', 'OM'),
        
        # SkyTeam (Major carriers)
        ('DL', 'Delta Air Lines', 'SkyTeam', 'SkyMiles', 'US'),
        ('AF', 'Air France', 'SkyTeam', 'Flying Blue', 'FR'),
        ('KL', 'KLM Royal Dutch Airlines', 'SkyTeam', 'Flying Blue', 'NL'),
        ('KE', 'Korean Air', 'SkyTeam', 'SKYPASS', 'KR'),
        ('MU', 'China Eastern Airlines', 'SkyTeam', 'Eastern Miles', 'CN'),
        ('VN', 'Vietnam Airlines', 'SkyTeam', 'Lotusmiles', 'VN'),
        ('AZ', 'ITA Airways', 'SkyTeam', 'Volare', 'IT'),
        ('SU', 'Aeroflot', 'SkyTeam', 'Aeroflot Bonus', 'RU'),
        ('AM', 'Aeroméxico', 'SkyTeam', 'Club Premier', 'MX'),
        ('AR', 'Aerolíneas Argentinas', 'SkyTeam', 'Aerolíneas Plus', 'AR'),
        ('UX', 'Air Europa', 'SkyTeam', 'SUMA', 'ES'),
        ('CI', 'China Airlines', 'SkyTeam', 'Dynasty Flyer', 'TW'),
        ('CZ', 'China Southern Airlines', 'SkyTeam', 'Sky Pearl Club', 'CN'),
        ('OK', 'Czech Airlines', 'SkyTeam', 'OK Plus', 'CZ'),
        ('RO', 'TAROM', 'SkyTeam', 'Flying Blue', 'RO'),
        
        # Major Unallianced carriers
        ('EK', 'Emirates', None, 'Skywards', 'AE'),
        ('EY', 'Etihad Airways', None, 'Etihad Guest', 'AE'),
        ('B6', 'JetBlue Airways', None, 'TrueBlue', 'US'),
        ('WN', 'Southwest Airlines', None, 'Rapid Rewards', 'US'),
        ('FR', 'Ryanair', None, 'myRyanair', 'IE'),
        ('U2', 'easyJet', None, 'easyJet Plus', 'GB'),
        ('F9', 'Frontier Airlines', None, 'FRONTIER Miles', 'US'),
        ('NK', 'Spirit Airlines', None, 'Free Spirit', 'US'),
        ('G4', 'Allegiant Air', None, 'myAllegiant', 'US'),
        ('AS', 'Alaska Airlines', None, 'Mileage Plan', 'US'),
        ('HA', 'Hawaiian Airlines', None, 'HawaiianMiles', 'US'),
        ('VS', 'Virgin Atlantic', None, 'Flying Club', 'GB'),
        ('VA', 'Virgin Australia', None, 'Velocity', 'AU'),
        ('JQ', 'Jetstar Airways', None, 'Jetstar Club', 'AU'),
        ('3K', 'Jetstar Asia', None, 'Jetstar Club', 'SG'),
        ('TR', 'Scoot', None, 'Scoot Rewards', 'SG'),
        ('FZ', 'flydubai', None, 'OPEN', 'AE'),
        ('PC', 'Pegasus Airlines', None, 'Pegasus Plus', 'TR'),
        ('W6', 'Wizz Air', None, 'Wizz Priority', 'HU'),
        ('VY', 'Vueling', None, 'Vueling Club', 'ES')
    ]
    
    airlines_added = 0
    for code, name, alliance, loyalty_program, country in airlines_data:
        # Skip if airline already exists
        existing = Airline.query.filter_by(code=code).first()
        if existing:
            continue
            
        airline = Airline(
            code=code,
            name=name,
            alliance=alliance,
            loyalty_program=loyalty_program,
            country=country
        )
        db.session.add(airline)
        airlines_added += 1
    
    db.session.commit()
    print(f"Successfully added {airlines_added} airlines to the database")

def seed_fare_and_booking_classes():
    """Seed fare classes and booking classes"""
    print("Seeding fare and booking classes...")
    
    # Fare classes
    fare_classes_data = [
        ('Economy', 'Standard economy class'),
        ('Premium Economy', 'Enhanced economy with extra legroom and amenities'),
        ('Business', 'Business class with lie-flat seats and premium service'),
        ('First', 'First class with private suites and luxury amenities')
    ]
    
    for name, description in fare_classes_data:
        existing = FareClass.query.filter_by(name=name).first()
        if not existing:
            fare_class = FareClass(name=name, description=description)
            db.session.add(fare_class)
    
    db.session.commit()
    
    # Get fare classes for booking classes
    economy = FareClass.query.filter_by(name='Economy').first()
    premium_economy = FareClass.query.filter_by(name='Premium Economy').first()
    business = FareClass.query.filter_by(name='Business').first()
    first = FareClass.query.filter_by(name='First').first()
    
    # Booking classes with more comprehensive coverage
    booking_classes_data = [
        # Economy booking classes
        ('Y', economy.id, 'Full fare economy'),
        ('B', economy.id, 'Economy discount'),
        ('M', economy.id, 'Economy discount'),
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
        
        # Add earning rates for this loyalty program
        earning_rates_data = [
            # Economy rates
            ('Economy', 'Y', 1.0, 500),
            ('Economy', 'B', 0.75, 500),
            ('Economy', 'M', 0.75, 500),
            ('Economy', 'H', 0.50, 500),
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
            ('Economy', 'E', 0.25, 500),
            
            # Premium Economy rates
            ('Premium Economy', 'W', 1.25, 500),
            ('Premium Economy', 'S', 1.0, 500),
            ('Premium Economy', 'A', 1.0, 500),
            
            # Business rates
            ('Business', 'J', 1.5, 500),
            ('Business', 'C', 1.5, 500),
            ('Business', 'D', 1.25, 500),
            ('Business', 'I', 1.25, 500),
            ('Business', 'Z', 1.0, 500),
            
            # First class rates
            ('First', 'F', 2.0, 500),
            ('First', 'A', 1.75, 500),
            ('First', 'P', 1.5, 500)
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

def get_silver_tier_name(airline_code):
    """Get airline-specific silver tier names"""
    tier_names = {
        'AA': 'Gold', 'DL': 'Silver Medallion', 'UA': 'Premier Silver',
        'BA': 'Bronze', 'AF': 'Silver', 'LH': 'Senator',
        'SQ': 'Elite Silver', 'CX': 'Silver', 'QF': 'Silver',
        'EK': 'Silver', 'TK': 'Elite', 'AC': 'Elite 25K',
        'JL': 'Crystal', 'QR': 'Silver', 'KE': 'Silver',
        'NH': 'Bronze', 'EY': 'Silver', 'AS': 'MVP'
    }
    return tier_names.get(airline_code, 'Silver')

def get_gold_tier_name(airline_code):
    """Get airline-specific gold tier names"""
    tier_names = {
        'AA': 'Platinum', 'DL': 'Gold Medallion', 'UA': 'Premier Gold',
        'BA': 'Silver', 'AF': 'Gold', 'LH': 'Senator',
        'SQ': 'Elite Gold', 'CX': 'Gold', 'QF': 'Gold',
        'EK': 'Gold', 'TK': 'Elite Plus', 'AC': 'Elite 50K',
        'JL': 'Sapphire', 'QR': 'Gold', 'KE': 'Gold',
        'NH': 'Platinum', 'EY': 'Gold', 'AS': 'MVP Gold'
    }
    return tier_names.get(airline_code, 'Gold')

def get_platinum_tier_name(airline_code):
    """Get airline-specific platinum tier names"""
    tier_names = {
        'AA': 'Platinum Pro', 'DL': 'Platinum Medallion', 'UA': 'Premier Platinum',
        'BA': 'Gold', 'AF': 'Platinum', 'LH': 'HON Circle',
        'SQ': 'PPS Club', 'CX': 'Diamond', 'QF': 'Platinum',
        'EK': 'Platinum', 'TK': 'Elite Plus', 'AC': 'Elite 75K',
        'JL': 'Emerald', 'QR': 'Platinum', 'KE': 'Platinum',
        'NH': 'Diamond', 'EY': 'Platinum', 'AS': 'MVP Gold 75K'
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
        
        # Seed comprehensive data
        seed_comprehensive_airports()
        seed_comprehensive_airlines()
        seed_fare_and_booking_classes()
        seed_loyalty_programs_and_earning_rates()
        
        # Print final statistics
        print("\n" + "="*50)
        print("COMPREHENSIVE DATA SEEDING COMPLETED!")
        print("="*50)
        print(f"Total airports: {Airport.query.count():,}")
        print(f"Total airlines: {Airline.query.count():,}")
        print(f"Total loyalty programs: {LoyaltyProgram.query.count():,}")
        print(f"Total earning rates: {EarningRate.query.count():,}")
        print(f"Total fare classes: {FareClass.query.count():,}")
        print(f"Total booking classes: {BookingClass.query.count():,}")
        print("="*50)

if __name__ == '__main__':
    main()
