#!/usr/bin/env python3
"""
Ultimate comprehensive seeder for the airline miles calculator
- Uses comprehensive international airports database (180+ airports)
- Separates operating airlines from loyalty programs
- Creates realistic earning rates that differ between programs
- Includes all major international airports worldwide
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.airline import db, Airport, Airline, LoyaltyProgram, FareClass, BookingClass, EarningRate
from src.main import app
import csv
import random

def clear_existing_data():
    """Clear all existing data from the database"""
    print("Clearing existing data...")
    with app.app_context():
        EarningRate.query.delete()
        BookingClass.query.delete()
        FareClass.query.delete()
        LoyaltyProgram.query.delete()
        Airline.query.delete()
        Airport.query.delete()
        db.session.commit()

def seed_comprehensive_airports():
    """Seed comprehensive international airports from the CSV file"""
    print("Seeding comprehensive international airports...")
    
    airports_file = '/home/ubuntu/comprehensive_international_airports.csv'
    
    with app.app_context():
        airports_batch = []
        
        with open(airports_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Check if airport already exists
                existing = Airport.query.filter_by(code=row['iata_code']).first()
                if existing:
                    continue
                    
                airport = Airport(
                    code=row['iata_code'],
                    name=row['name'],
                    city=row['city'],
                    state='',  # Not available in this format
                    country=row['country'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude'])
                )
                airports_batch.append(airport)
                
                # Commit in batches for better performance
                if len(airports_batch) >= 50:
                    db.session.add_all(airports_batch)
                    db.session.commit()
                    print(f"Added {len(airports_batch)} airports...")
                    airports_batch = []
        
        # Commit remaining airports
        if airports_batch:
            db.session.add_all(airports_batch)
            db.session.commit()
            print(f"Added final {len(airports_batch)} airports...")
    
        total_airports = Airport.query.count()
        print(f"Successfully added {total_airports} airports to the database")

def seed_comprehensive_airlines():
    """Seed comprehensive airlines - operating carriers"""
    print("Seeding comprehensive airlines...")
    
    airlines_data = [
        # Star Alliance
        {'code': 'UA', 'name': 'United Airlines', 'country': 'US', 'alliance': 'Star Alliance'},
        {'code': 'LH', 'name': 'Lufthansa', 'country': 'DE', 'alliance': 'Star Alliance'},
        {'code': 'SQ', 'name': 'Singapore Airlines', 'country': 'SG', 'alliance': 'Star Alliance'},
        {'code': 'NH', 'name': 'All Nippon Airways', 'country': 'JP', 'alliance': 'Star Alliance'},
        {'code': 'AC', 'name': 'Air Canada', 'country': 'CA', 'alliance': 'Star Alliance'},
        {'code': 'LX', 'name': 'Swiss International Air Lines', 'country': 'CH', 'alliance': 'Star Alliance'},
        {'code': 'OS', 'name': 'Austrian Airlines', 'country': 'AT', 'alliance': 'Star Alliance'},
        {'code': 'SK', 'name': 'Scandinavian Airlines', 'country': 'SE', 'alliance': 'Star Alliance'},
        {'code': 'TK', 'name': 'Turkish Airlines', 'country': 'TR', 'alliance': 'Star Alliance'},
        {'code': 'TG', 'name': 'Thai Airways', 'country': 'TH', 'alliance': 'Star Alliance'},
        {'code': 'SA', 'name': 'South African Airways', 'country': 'ZA', 'alliance': 'Star Alliance'},
        {'code': 'ET', 'name': 'Ethiopian Airlines', 'country': 'ET', 'alliance': 'Star Alliance'},
        {'code': 'EK', 'name': 'Emirates', 'country': 'AE', 'alliance': 'Star Alliance'},  # Partner
        {'code': 'CA', 'name': 'Air China', 'country': 'CN', 'alliance': 'Star Alliance'},
        {'code': 'AI', 'name': 'Air India', 'country': 'IN', 'alliance': 'Star Alliance'},
        {'code': 'NZ', 'name': 'Air New Zealand', 'country': 'NZ', 'alliance': 'Star Alliance'},
        {'code': 'TP', 'name': 'TAP Air Portugal', 'country': 'PT', 'alliance': 'Star Alliance'},
        {'code': 'SN', 'name': 'Brussels Airlines', 'country': 'BE', 'alliance': 'Star Alliance'},
        {'code': 'LO', 'name': 'LOT Polish Airlines', 'country': 'PL', 'alliance': 'Star Alliance'},
        {'code': 'CM', 'name': 'Copa Airlines', 'country': 'PA', 'alliance': 'Star Alliance'},
        {'code': 'AV', 'name': 'Avianca', 'country': 'CO', 'alliance': 'Star Alliance'},
        
        # Oneworld
        {'code': 'AA', 'name': 'American Airlines', 'country': 'US', 'alliance': 'Oneworld'},
        {'code': 'BA', 'name': 'British Airways', 'country': 'GB', 'alliance': 'Oneworld'},
        {'code': 'CX', 'name': 'Cathay Pacific', 'country': 'HK', 'alliance': 'Oneworld'},
        {'code': 'QF', 'name': 'Qantas', 'country': 'AU', 'alliance': 'Oneworld'},
        {'code': 'JL', 'name': 'Japan Airlines', 'country': 'JP', 'alliance': 'Oneworld'},
        {'code': 'IB', 'name': 'Iberia', 'country': 'ES', 'alliance': 'Oneworld'},
        {'code': 'AY', 'name': 'Finnair', 'country': 'FI', 'alliance': 'Oneworld'},
        {'code': 'AS', 'name': 'Alaska Airlines', 'country': 'US', 'alliance': 'Oneworld'},
        {'code': 'QR', 'name': 'Qatar Airways', 'country': 'QA', 'alliance': 'Oneworld'},
        {'code': 'RJ', 'name': 'Royal Jordanian', 'country': 'JO', 'alliance': 'Oneworld'},
        {'code': 'S7', 'name': 'S7 Airlines', 'country': 'RU', 'alliance': 'Oneworld'},
        {'code': 'LA', 'name': 'LATAM Airlines', 'country': 'CL', 'alliance': 'Oneworld'},
        {'code': 'MH', 'name': 'Malaysia Airlines', 'country': 'MY', 'alliance': 'Oneworld'},
        {'code': 'WF', 'name': 'Fiji Airways', 'country': 'FJ', 'alliance': 'Oneworld'},
        
        # SkyTeam
        {'code': 'DL', 'name': 'Delta Air Lines', 'country': 'US', 'alliance': 'SkyTeam'},
        {'code': 'AF', 'name': 'Air France', 'country': 'FR', 'alliance': 'SkyTeam'},
        {'code': 'KL', 'name': 'KLM', 'country': 'NL', 'alliance': 'SkyTeam'},
        {'code': 'KE', 'name': 'Korean Air', 'country': 'KR', 'alliance': 'SkyTeam'},
        {'code': 'AZ', 'name': 'Alitalia', 'country': 'IT', 'alliance': 'SkyTeam'},
        {'code': 'SU', 'name': 'Aeroflot', 'country': 'RU', 'alliance': 'SkyTeam'},
        {'code': 'CZ', 'name': 'China Southern Airlines', 'country': 'CN', 'alliance': 'SkyTeam'},
        {'code': 'MU', 'name': 'China Eastern Airlines', 'country': 'CN', 'alliance': 'SkyTeam'},
        {'code': 'VN', 'name': 'Vietnam Airlines', 'country': 'VN', 'alliance': 'SkyTeam'},
        {'code': 'OK', 'name': 'Czech Airlines', 'country': 'CZ', 'alliance': 'SkyTeam'},
        {'code': 'RO', 'name': 'TAROM', 'country': 'RO', 'alliance': 'SkyTeam'},
        {'code': 'ME', 'name': 'Middle East Airlines', 'country': 'LB', 'alliance': 'SkyTeam'},
        {'code': 'AR', 'name': 'Aerolíneas Argentinas', 'country': 'AR', 'alliance': 'SkyTeam'},
        {'code': 'AM', 'name': 'Aeroméxico', 'country': 'MX', 'alliance': 'SkyTeam'},
        {'code': 'GA', 'name': 'Garuda Indonesia', 'country': 'ID', 'alliance': 'SkyTeam'},
        
        # Unallianced Major Carriers
        {'code': 'EK', 'name': 'Emirates', 'country': 'AE', 'alliance': None},
        {'code': 'EY', 'name': 'Etihad Airways', 'country': 'AE', 'alliance': None},
        {'code': 'B6', 'name': 'JetBlue Airways', 'country': 'US', 'alliance': None},
        {'code': 'WN', 'name': 'Southwest Airlines', 'country': 'US', 'alliance': None},
        {'code': 'F9', 'name': 'Frontier Airlines', 'country': 'US', 'alliance': None},
        {'code': 'NK', 'name': 'Spirit Airlines', 'country': 'US', 'alliance': None},
        {'code': 'G4', 'name': 'Allegiant Air', 'country': 'US', 'alliance': None},
        {'code': 'WS', 'name': 'WestJet', 'country': 'CA', 'alliance': None},
        {'code': 'VS', 'name': 'Virgin Atlantic', 'country': 'GB', 'alliance': None},
        {'code': 'EI', 'name': 'Aer Lingus', 'country': 'IE', 'alliance': None},
        {'code': 'FR', 'name': 'Ryanair', 'country': 'IE', 'alliance': None},
        {'code': 'U2', 'name': 'easyJet', 'country': 'GB', 'alliance': None},
        {'code': 'VY', 'name': 'Vueling', 'country': 'ES', 'alliance': None},
        {'code': 'W6', 'name': 'Wizz Air', 'country': 'HU', 'alliance': None},
        {'code': 'PC', 'name': 'Pegasus Airlines', 'country': 'TR', 'alliance': None},
        {'code': 'FZ', 'name': 'flydubai', 'country': 'AE', 'alliance': None},
        {'code': 'SV', 'name': 'Saudi Arabian Airlines', 'country': 'SA', 'alliance': None},
        {'code': 'MS', 'name': 'EgyptAir', 'country': 'EG', 'alliance': None},
        {'code': 'AT', 'name': 'Royal Air Maroc', 'country': 'MA', 'alliance': None},
        {'code': 'TU', 'name': 'Tunisair', 'country': 'TN', 'alliance': None},
    ]
    
    with app.app_context():
        for airline_data in airlines_data:
            existing = Airline.query.filter_by(code=airline_data['code']).first()
            if not existing:
                airline = Airline(
                    code=airline_data['code'],
                    name=airline_data['name'],
                    country=airline_data['country'],
                    alliance=airline_data['alliance'],
                    loyalty_program=airline_data.get('loyalty_program', 'Default Program')
                )
                db.session.add(airline)
        
        db.session.commit()
    
        total_airlines = Airline.query.count()
        print(f"Successfully added {total_airlines} airlines to the database")

def seed_loyalty_programs():
    """Seed loyalty programs - separate from operating airlines"""
    print("Seeding loyalty programs...")
    
    loyalty_programs_data = [
        # Star Alliance Programs
        {'airline_code': 'UA', 'name': 'MileagePlus', 'alliance': 'Star Alliance', 'silver': 'Premier Silver', 'gold': 'Premier Gold', 'platinum': 'Premier Platinum'},
        {'airline_code': 'LH', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
        {'airline_code': 'SQ', 'name': 'KrisFlyer', 'alliance': 'Star Alliance', 'silver': 'KrisFlyer Elite Silver', 'gold': 'KrisFlyer Elite Gold', 'platinum': 'PPS Club'},
        {'airline_code': 'NH', 'name': 'ANA Mileage Club', 'alliance': 'Star Alliance', 'silver': 'Bronze', 'gold': 'Platinum', 'platinum': 'Diamond'},
        {'airline_code': 'AC', 'name': 'Aeroplan', 'alliance': 'Star Alliance', 'silver': '25K', 'gold': '50K', 'platinum': '75K'},
        {'airline_code': 'LX', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
        {'airline_code': 'OS', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
        {'airline_code': 'SK', 'name': 'EuroBonus', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Diamond'},
        {'airline_code': 'TK', 'name': 'Miles&Smiles', 'alliance': 'Star Alliance', 'silver': 'Elite', 'gold': 'Elite Plus', 'platinum': 'Elite Plus'},
        {'airline_code': 'TG', 'name': 'Royal Orchid Plus', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'SA', 'name': 'Voyager', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'ET', 'name': 'ShebaMiles', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'CA', 'name': 'PhoenixMiles', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AI', 'name': 'Flying Returns', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'NZ', 'name': 'Airpoints', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Elite'},
        {'airline_code': 'TP', 'name': 'TAP Miles&Go', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'SN', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
        {'airline_code': 'LO', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
        {'airline_code': 'CM', 'name': 'ConnectMiles', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AV', 'name': 'LifeMiles', 'alliance': 'Star Alliance', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        
        # Oneworld Programs
        {'airline_code': 'AA', 'name': 'AAdvantage', 'alliance': 'Oneworld', 'silver': 'Gold', 'gold': 'Platinum', 'platinum': 'Platinum Pro'},
        {'airline_code': 'BA', 'name': 'Executive Club', 'alliance': 'Oneworld', 'silver': 'Executive Club Silver', 'gold': 'Executive Club Gold', 'platinum': 'Executive Club Platinum'},
        {'airline_code': 'CX', 'name': 'Asia Miles', 'alliance': 'Oneworld', 'silver': 'Marco Polo Silver', 'gold': 'Marco Polo Gold', 'platinum': 'Marco Polo Diamond'},
        {'airline_code': 'QF', 'name': 'Frequent Flyer', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'JL', 'name': 'JAL Mileage Bank', 'alliance': 'Oneworld', 'silver': 'Crystal', 'gold': 'Sapphire', 'platinum': 'Diamond'},
        {'airline_code': 'IB', 'name': 'Iberia Plus', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AY', 'name': 'Finnair Plus', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AS', 'name': 'Mileage Plan', 'alliance': 'Oneworld', 'silver': 'MVP', 'gold': 'MVP Gold', 'platinum': 'MVP Gold 75K'},
        {'airline_code': 'QR', 'name': 'Privilege Club', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'RJ', 'name': 'Royal Club', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'S7', 'name': 'S7 Priority', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'LA', 'name': 'LATAM Pass', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'MH', 'name': 'Enrich', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'WF', 'name': 'Tabua Club', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        
        # SkyTeam Programs
        {'airline_code': 'DL', 'name': 'SkyMiles', 'alliance': 'SkyTeam', 'silver': 'Silver Medallion', 'gold': 'Gold Medallion', 'platinum': 'Diamond Medallion'},
        {'airline_code': 'AF', 'name': 'Flying Blue', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'KL', 'name': 'Flying Blue', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'KE', 'name': 'SKYPASS', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Million Miler'},
        {'airline_code': 'AZ', 'name': 'MilleMiglia', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'SU', 'name': 'Bonus', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'CZ', 'name': 'Sky Pearl Club', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'MU', 'name': 'Eastern Miles', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'VN', 'name': 'Golden Lotus Plus', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'OK', 'name': 'OK Plus', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'RO', 'name': 'Smart Miles', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'ME', 'name': 'Cedar Miles', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AR', 'name': 'Aerolíneas Plus', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AM', 'name': 'Club Premier', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'GA', 'name': 'GarudaMiles', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        
        # Unallianced Programs
        {'airline_code': 'EK', 'name': 'Skywards', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'EY', 'name': 'Etihad Guest', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'B6', 'name': 'TrueBlue', 'alliance': None, 'silver': 'Mosaic', 'gold': 'Mosaic', 'platinum': 'Mosaic'},
        {'airline_code': 'WN', 'name': 'Rapid Rewards', 'alliance': None, 'silver': 'A-List', 'gold': 'A-List Preferred', 'platinum': 'Companion Pass'},
        {'airline_code': 'F9', 'name': 'FRONTIER Miles', 'alliance': None, 'silver': 'Elite 20K', 'gold': 'Elite 50K', 'platinum': 'Elite 100K'},
        {'airline_code': 'NK', 'name': 'Free Spirit', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'G4', 'name': 'myAllegiant', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'WS', 'name': 'WestJet Rewards', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'VS', 'name': 'Flying Club', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'EI', 'name': 'AerClub', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'SV', 'name': 'Alfursan', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'MS', 'name': 'EgyptAir Plus', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'AT', 'name': 'Safar Flyer', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        {'airline_code': 'TU', 'name': 'Fidelys', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
    ]
    
    with app.app_context():
        for program_data in loyalty_programs_data:
            airline = Airline.query.filter_by(code=program_data['airline_code']).first()
            if airline:
                existing = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
                if not existing:
                    program = LoyaltyProgram(
                        name=program_data['name'],
                        airline_id=airline.id,
                        alliance=program_data['alliance'],
                        base_earning_rate=1.0,
                        silver_bonus=0.25,
                        gold_bonus=0.50,
                        platinum_bonus=1.00,
                        silver_tier_name=program_data['silver'],
                        gold_tier_name=program_data['gold'],
                        platinum_tier_name=program_data['platinum'],
                        earning_model='distance',
                        currency='USD'
                    )
                    db.session.add(program)
        
        db.session.commit()
    
        total_programs = LoyaltyProgram.query.count()
        print(f"Successfully added {total_programs} loyalty programs to the database")

def seed_fare_and_booking_classes():
    """Seed fare classes and booking classes"""
    print("Seeding fare and booking classes...")
    
    with app.app_context():
        # Fare classes
        fare_classes_data = [
            {'name': 'Economy', 'description': 'Economy class'},
            {'name': 'Premium Economy', 'description': 'Premium economy class'},
            {'name': 'Business', 'description': 'Business class'},
            {'name': 'First', 'description': 'First class'}
        ]
        
        for fare_class_data in fare_classes_data:
            existing = FareClass.query.filter_by(name=fare_class_data['name']).first()
            if not existing:
                fare_class = FareClass(
                    name=fare_class_data['name'],
                    description=fare_class_data['description']
                )
                db.session.add(fare_class)
        
        # Booking classes
        booking_classes_data = [
            # Economy
            {'code': 'Y', 'description': 'Full fare economy', 'fare_class': 'Economy'},
            {'code': 'B', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'M', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'H', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'Q', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'V', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'W', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'S', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'T', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'L', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'K', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'G', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'N', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'R', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'E', 'description': 'Economy discount', 'fare_class': 'Economy'},
            
            # Premium Economy
            {'code': 'W', 'description': 'Premium economy full fare', 'fare_class': 'Premium Economy'},
            {'code': 'E', 'description': 'Premium economy discount', 'fare_class': 'Premium Economy'},
            {'code': 'T', 'description': 'Premium economy discount', 'fare_class': 'Premium Economy'},
            
            # Business
            {'code': 'J', 'description': 'Business full fare', 'fare_class': 'Business'},
            {'code': 'C', 'description': 'Business full fare', 'fare_class': 'Business'},
            {'code': 'D', 'description': 'Business discount', 'fare_class': 'Business'},
            {'code': 'I', 'description': 'Business discount', 'fare_class': 'Business'},
            {'code': 'Z', 'description': 'Business discount', 'fare_class': 'Business'},
            
            # First
            {'code': 'F', 'description': 'First class full fare', 'fare_class': 'First'},
            {'code': 'A', 'description': 'First class discount', 'fare_class': 'First'},
            {'code': 'P', 'description': 'First class discount', 'fare_class': 'First'}
        ]
        
        for booking_class_data in booking_classes_data:
            fare_class = FareClass.query.filter_by(name=booking_class_data['fare_class']).first()
            if fare_class:
                existing = BookingClass.query.filter_by(code=booking_class_data['code'], fare_class_id=fare_class.id).first()
                if not existing:
                    booking_class = BookingClass(
                        code=booking_class_data['code'],
                        description=booking_class_data['description'],
                        fare_class_id=fare_class.id
                    )
                    db.session.add(booking_class)
        
        db.session.commit()
    
        total_booking_classes = BookingClass.query.count()
        print(f"Successfully added {total_booking_classes} booking classes to the database")

def get_program_earning_multiplier(program_name, alliance, booking_class):
    """
    Get realistic earning multipliers for different programs
    This creates the variation that makes different programs earn different miles
    """
    base_multipliers = {
        # Star Alliance - generally higher earning rates
        'MileagePlus': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        'Miles & More': {'Y': 1.0, 'B': 0.5, 'J': 1.25, 'C': 1.25, 'F': 1.5},
        'KrisFlyer': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        'ANA Mileage Club': {'Y': 1.0, 'B': 0.5, 'J': 1.3, 'C': 1.3, 'F': 1.8},
        'Aeroplan': {'Y': 1.0, 'B': 0.25, 'J': 1.25, 'C': 1.25, 'F': 1.5},
        
        # Oneworld - varied earning rates
        'AAdvantage': {'Y': 1.0, 'B': 0.5, 'J': 1.75, 'C': 1.75, 'F': 2.0},  # Higher business earning
        'Executive Club': {'Y': 1.0, 'B': 0.5, 'J': 1.425, 'C': 1.425, 'F': 1.5},  # Tier points focus
        'Asia Miles': {'Y': 1.0, 'B': 0.5, 'J': 1.65, 'C': 1.65, 'F': 1.8},
        'Frequent Flyer': {'Y': 1.0, 'B': 0.5, 'J': 1.275, 'C': 1.275, 'F': 1.5},  # Lower business earning
        'JAL Mileage Bank': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        'Mileage Plan': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        
        # SkyTeam - moderate earning rates
        'SkyMiles': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 1.5},
        'Flying Blue': {'Y': 1.0, 'B': 0.5, 'J': 1.25, 'C': 1.25, 'F': 1.5},
        'SKYPASS': {'Y': 1.0, 'B': 0.5, 'J': 1.3, 'C': 1.3, 'F': 1.5},
        
        # Unallianced - varied strategies
        'Skywards': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        'Etihad Guest': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        'TrueBlue': {'Y': 1.0, 'B': 1.0, 'J': 1.0, 'C': 1.0, 'F': 1.0},  # Flat earning
    }
    
    # Get specific multiplier or use default based on alliance
    if program_name in base_multipliers:
        multipliers = base_multipliers[program_name]
    else:
        # Default multipliers based on alliance
        if alliance == 'Star Alliance':
            multipliers = {'Y': 1.0, 'B': 0.5, 'J': 1.4, 'C': 1.4, 'F': 1.8}
        elif alliance == 'Oneworld':
            multipliers = {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 1.8}
        elif alliance == 'SkyTeam':
            multipliers = {'Y': 1.0, 'B': 0.5, 'J': 1.3, 'C': 1.3, 'F': 1.5}
        else:  # Unallianced
            multipliers = {'Y': 1.0, 'B': 0.5, 'J': 1.4, 'C': 1.4, 'F': 1.6}
    
    return multipliers.get(booking_class, 1.0)

def seed_earning_rates():
    """Seed earning rates with realistic variations between programs"""
    print("Seeding earning rates with program-specific variations...")
    
    with app.app_context():
        loyalty_programs = LoyaltyProgram.query.all()
        booking_classes = BookingClass.query.all()
        
        earning_rates_batch = []
        
        for program in loyalty_programs:
            for booking_class in booking_classes:
                # Get program-specific earning multiplier
                earning_percentage = get_program_earning_multiplier(
                    program.name, 
                    program.alliance, 
                    booking_class.code
                )
                
                # Check if earning rate already exists
                existing = EarningRate.query.filter_by(
                    loyalty_program_id=program.id,
                    booking_class=booking_class.code,
                    fare_class=booking_class.fare_class.name
                ).first()
                
                if not existing:
                    earning_rate = EarningRate(
                        loyalty_program_id=program.id,
                        fare_class=booking_class.fare_class.name,
                        booking_class=booking_class.code,
                        earning_percentage=earning_percentage,
                        minimum_miles=500,  # Industry standard
                        elite_bonus_silver=0.25,
                        elite_bonus_gold=0.50,
                        elite_bonus_platinum=1.00
                    )
                    earning_rates_batch.append(earning_rate)
                    
                    # Commit in batches
                    if len(earning_rates_batch) >= 100:
                        db.session.add_all(earning_rates_batch)
                        db.session.commit()
                        print(f"Added {len(earning_rates_batch)} earning rates...")
                        earning_rates_batch = []
        
        # Commit remaining earning rates
        if earning_rates_batch:
            db.session.add_all(earning_rates_batch)
            db.session.commit()
            print(f"Added final {len(earning_rates_batch)} earning rates...")
    
        total_earning_rates = EarningRate.query.count()
        print(f"Successfully added {total_earning_rates} earning rates to the database")

def main():
    """Main seeding function"""
    print("==================================================")
    print("ULTIMATE COMPREHENSIVE DATA SEEDING STARTED!")
    print("==================================================")
    
    # Clear existing data
    clear_existing_data()
    
    # Seed all data
    seed_comprehensive_airports()
    seed_comprehensive_airlines()
    seed_loyalty_programs()
    seed_fare_and_booking_classes()
    seed_earning_rates()
    
    # Print final statistics
    with app.app_context():
        airport_count = Airport.query.count()
        airline_count = Airline.query.count()
        program_count = LoyaltyProgram.query.count()
        earning_rate_count = EarningRate.query.count()
        fare_class_count = FareClass.query.count()
        booking_class_count = BookingClass.query.count()
    
    print("==================================================")
    print("ULTIMATE COMPREHENSIVE DATA SEEDING COMPLETED!")
    print("==================================================")
    print(f"Total airports: {airport_count:,}")
    print(f"Total airlines: {airline_count}")
    print(f"Total loyalty programs: {program_count}")
    print(f"Total earning rates: {earning_rate_count:,}")
    print(f"Total fare classes: {fare_class_count}")
    print(f"Total booking classes: {booking_class_count}")
    print("==================================================")
    print("🎉 THE WORLD'S BEST AIRLINE MILES CALCULATOR IS READY!")
    print("==================================================")

if __name__ == "__main__":
    main()
