#!/usr/bin/env python3
"""
Production data seeder for Airline Miles Calculator
Optimized for PostgreSQL deployment on Render.com
"""

import os
import sys
from main import app, db, Airport, Airline, LoyaltyProgram, FareClass, BookingClass, EarningRate

def seed_basic_data():
    """Seed essential data for production deployment"""
    print("Starting production data seeding...")
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        EarningRate.query.delete()
        BookingClass.query.delete()
        FareClass.query.delete()
        LoyaltyProgram.query.delete()
        Airline.query.delete()
        Airport.query.delete()
        db.session.commit()
        
        # Seed major international airports
        print("Seeding major international airports...")
        airports_data = [
            {'code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'US', 'lat': 40.6413, 'lon': -73.7781},
            {'code': 'LHR', 'name': 'London Heathrow Airport', 'city': 'London', 'country': 'GB', 'lat': 51.4700, 'lon': -0.4543},
            {'code': 'CDG', 'name': 'Charles de Gaulle Airport', 'city': 'Paris', 'country': 'FR', 'lat': 49.0097, 'lon': 2.5479},
            {'code': 'NRT', 'name': 'Narita International Airport', 'city': 'Tokyo', 'country': 'JP', 'lat': 35.7720, 'lon': 140.3929},
            {'code': 'SIN', 'name': 'Singapore Changi Airport', 'city': 'Singapore', 'country': 'SG', 'lat': 1.3644, 'lon': 103.9915},
            {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'AE', 'lat': 25.2532, 'lon': 55.3657},
            {'code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'US', 'lat': 33.9425, 'lon': -118.4081},
            {'code': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'DE', 'lat': 50.0379, 'lon': 8.5622},
            {'code': 'HKG', 'name': 'Hong Kong International Airport', 'city': 'Hong Kong', 'country': 'HK', 'lat': 22.3080, 'lon': 113.9185},
            {'code': 'SYD', 'name': 'Sydney Kingsford Smith Airport', 'city': 'Sydney', 'country': 'AU', 'lat': -33.9399, 'lon': 151.1753},
            {'code': 'ICN', 'name': 'Incheon International Airport', 'city': 'Seoul', 'country': 'KR', 'lat': 37.4602, 'lon': 126.4407},
            {'code': 'AMS', 'name': 'Amsterdam Airport Schiphol', 'city': 'Amsterdam', 'country': 'NL', 'lat': 52.3105, 'lon': 4.7683},
            {'code': 'YYZ', 'name': 'Toronto Pearson International Airport', 'city': 'Toronto', 'country': 'CA', 'lat': 43.6777, 'lon': -79.6248},
            {'code': 'DOH', 'name': 'Hamad International Airport', 'city': 'Doha', 'country': 'QA', 'lat': 25.2731, 'lon': 51.6080},
            {'code': 'IST', 'name': 'Istanbul Airport', 'city': 'Istanbul', 'country': 'TR', 'lat': 41.2753, 'lon': 28.7519},
            {'code': 'PVG', 'name': 'Shanghai Pudong International Airport', 'city': 'Shanghai', 'country': 'CN', 'lat': 31.1443, 'lon': 121.8083},
            {'code': 'BKK', 'name': 'Suvarnabhumi Airport', 'city': 'Bangkok', 'country': 'TH', 'lat': 13.6900, 'lon': 100.7501},
            {'code': 'MUC', 'name': 'Munich Airport', 'city': 'Munich', 'country': 'DE', 'lat': 48.3537, 'lon': 11.7750},
            {'code': 'ZUR', 'name': 'Zurich Airport', 'city': 'Zurich', 'country': 'CH', 'lat': 47.4647, 'lon': 8.5492},
            {'code': 'ORD', 'name': 'Chicago O\'Hare International Airport', 'city': 'Chicago', 'country': 'US', 'lat': 41.9742, 'lon': -87.9073},
        ]
        
        for airport_data in airports_data:
            airport = Airport(
                code=airport_data['code'],
                name=airport_data['name'],
                city=airport_data['city'],
                state='',
                country=airport_data['country'],
                latitude=airport_data['lat'],
                longitude=airport_data['lon']
            )
            db.session.add(airport)
        
        # Seed major airlines
        print("Seeding major airlines...")
        airlines_data = [
            {'code': 'UA', 'name': 'United Airlines', 'country': 'US', 'alliance': 'Star Alliance', 'program': 'MileagePlus'},
            {'code': 'AA', 'name': 'American Airlines', 'country': 'US', 'alliance': 'Oneworld', 'program': 'AAdvantage'},
            {'code': 'DL', 'name': 'Delta Air Lines', 'country': 'US', 'alliance': 'SkyTeam', 'program': 'SkyMiles'},
            {'code': 'BA', 'name': 'British Airways', 'country': 'GB', 'alliance': 'Oneworld', 'program': 'Executive Club'},
            {'code': 'LH', 'name': 'Lufthansa', 'country': 'DE', 'alliance': 'Star Alliance', 'program': 'Miles & More'},
            {'code': 'AF', 'name': 'Air France', 'country': 'FR', 'alliance': 'SkyTeam', 'program': 'Flying Blue'},
            {'code': 'SQ', 'name': 'Singapore Airlines', 'country': 'SG', 'alliance': 'Star Alliance', 'program': 'KrisFlyer'},
            {'code': 'CX', 'name': 'Cathay Pacific', 'country': 'HK', 'alliance': 'Oneworld', 'program': 'Asia Miles'},
            {'code': 'QF', 'name': 'Qantas', 'country': 'AU', 'alliance': 'Oneworld', 'program': 'Frequent Flyer'},
            {'code': 'EK', 'name': 'Emirates', 'country': 'AE', 'alliance': None, 'program': 'Skywards'},
        ]
        
        for airline_data in airlines_data:
            airline = Airline(
                code=airline_data['code'],
                name=airline_data['name'],
                country=airline_data['country'],
                alliance=airline_data['alliance'],
                loyalty_program=airline_data['program']
            )
            db.session.add(airline)
        
        db.session.commit()
        
        # Seed loyalty programs
        print("Seeding loyalty programs...")
        loyalty_programs_data = [
            {'airline_code': 'UA', 'name': 'MileagePlus', 'alliance': 'Star Alliance', 'silver': 'Premier Silver', 'gold': 'Premier Gold', 'platinum': 'Premier Platinum'},
            {'airline_code': 'AA', 'name': 'AAdvantage', 'alliance': 'Oneworld', 'silver': 'Gold', 'gold': 'Platinum', 'platinum': 'Platinum Pro'},
            {'airline_code': 'DL', 'name': 'SkyMiles', 'alliance': 'SkyTeam', 'silver': 'Silver Medallion', 'gold': 'Gold Medallion', 'platinum': 'Diamond Medallion'},
            {'airline_code': 'BA', 'name': 'Executive Club', 'alliance': 'Oneworld', 'silver': 'Executive Club Silver', 'gold': 'Executive Club Gold', 'platinum': 'Executive Club Platinum'},
            {'airline_code': 'LH', 'name': 'Miles & More', 'alliance': 'Star Alliance', 'silver': 'Frequent Traveller', 'gold': 'Senator', 'platinum': 'HON Circle'},
            {'airline_code': 'AF', 'name': 'Flying Blue', 'alliance': 'SkyTeam', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
            {'airline_code': 'SQ', 'name': 'KrisFlyer', 'alliance': 'Star Alliance', 'silver': 'KrisFlyer Elite Silver', 'gold': 'KrisFlyer Elite Gold', 'platinum': 'PPS Club'},
            {'airline_code': 'CX', 'name': 'Asia Miles', 'alliance': 'Oneworld', 'silver': 'Marco Polo Silver', 'gold': 'Marco Polo Gold', 'platinum': 'Marco Polo Diamond'},
            {'airline_code': 'QF', 'name': 'Frequent Flyer', 'alliance': 'Oneworld', 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
            {'airline_code': 'EK', 'name': 'Skywards', 'alliance': None, 'silver': 'Silver', 'gold': 'Gold', 'platinum': 'Platinum'},
        ]
        
        for program_data in loyalty_programs_data:
            airline = Airline.query.filter_by(code=program_data['airline_code']).first()
            if airline:
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
        
        # Seed fare classes
        print("Seeding fare classes...")
        fare_classes_data = [
            {'name': 'Economy', 'description': 'Economy class'},
            {'name': 'Premium Economy', 'description': 'Premium economy class'},
            {'name': 'Business', 'description': 'Business class'},
            {'name': 'First', 'description': 'First class'}
        ]
        
        for fare_class_data in fare_classes_data:
            fare_class = FareClass(
                name=fare_class_data['name'],
                description=fare_class_data['description']
            )
            db.session.add(fare_class)
        
        db.session.commit()
        
        # Seed booking classes
        print("Seeding booking classes...")
        booking_classes_data = [
            # Economy
            {'code': 'Y', 'description': 'Full fare economy', 'fare_class': 'Economy'},
            {'code': 'B', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'M', 'description': 'Economy discount', 'fare_class': 'Economy'},
            {'code': 'H', 'description': 'Economy discount', 'fare_class': 'Economy'},
            # Premium Economy
            {'code': 'W', 'description': 'Premium economy full fare', 'fare_class': 'Premium Economy'},
            {'code': 'E', 'description': 'Premium economy discount', 'fare_class': 'Premium Economy'},
            # Business
            {'code': 'J', 'description': 'Business full fare', 'fare_class': 'Business'},
            {'code': 'C', 'description': 'Business full fare', 'fare_class': 'Business'},
            {'code': 'D', 'description': 'Business discount', 'fare_class': 'Business'},
            {'code': 'I', 'description': 'Business discount', 'fare_class': 'Business'},
            # First
            {'code': 'F', 'description': 'First class full fare', 'fare_class': 'First'},
            {'code': 'A', 'description': 'First class discount', 'fare_class': 'First'},
        ]
        
        for booking_class_data in booking_classes_data:
            fare_class = FareClass.query.filter_by(name=booking_class_data['fare_class']).first()
            if fare_class:
                booking_class = BookingClass(
                    code=booking_class_data['code'],
                    description=booking_class_data['description'],
                    fare_class_id=fare_class.id
                )
                db.session.add(booking_class)
        
        db.session.commit()
        
        # Seed earning rates with program-specific variations
        print("Seeding earning rates...")
        loyalty_programs = LoyaltyProgram.query.all()
        booking_classes = BookingClass.query.all()
        
        # Program-specific earning multipliers
        program_multipliers = {
            'MileagePlus': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
            'AAdvantage': {'Y': 1.0, 'B': 0.5, 'J': 1.75, 'C': 1.75, 'F': 2.0},  # Higher business earning
            'SkyMiles': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 1.5},
            'Executive Club': {'Y': 1.0, 'B': 0.5, 'J': 1.425, 'C': 1.425, 'F': 1.5},  # Tier points focus
            'Miles & More': {'Y': 1.0, 'B': 0.5, 'J': 1.25, 'C': 1.25, 'F': 1.5},
            'Flying Blue': {'Y': 1.0, 'B': 0.5, 'J': 1.25, 'C': 1.25, 'F': 1.5},
            'KrisFlyer': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
            'Asia Miles': {'Y': 1.0, 'B': 0.5, 'J': 1.65, 'C': 1.65, 'F': 1.8},
            'Frequent Flyer': {'Y': 1.0, 'B': 0.5, 'J': 1.275, 'C': 1.275, 'F': 1.5},  # Lower business earning
            'Skywards': {'Y': 1.0, 'B': 0.5, 'J': 1.5, 'C': 1.5, 'F': 2.0},
        }
        
        for program in loyalty_programs:
            for booking_class in booking_classes:
                # Get program-specific earning multiplier
                multipliers = program_multipliers.get(program.name, {'Y': 1.0, 'B': 0.5, 'J': 1.4, 'C': 1.4, 'F': 1.6})
                earning_percentage = multipliers.get(booking_class.code, 1.0)
                
                earning_rate = EarningRate(
                    loyalty_program_id=program.id,
                    fare_class=booking_class.fare_class.name,
                    booking_class=booking_class.code,
                    earning_percentage=earning_percentage,
                    minimum_miles=500,
                    elite_bonus_silver=0.25,
                    elite_bonus_gold=0.50,
                    elite_bonus_platinum=1.00
                )
                db.session.add(earning_rate)
        
        db.session.commit()
        
        # Print final statistics
        airport_count = Airport.query.count()
        airline_count = Airline.query.count()
        program_count = LoyaltyProgram.query.count()
        earning_rate_count = EarningRate.query.count()
        
        print("==================================================")
        print("PRODUCTION DATA SEEDING COMPLETED!")
        print("==================================================")
        print(f"Total airports: {airport_count}")
        print(f"Total airlines: {airline_count}")
        print(f"Total loyalty programs: {program_count}")
        print(f"Total earning rates: {earning_rate_count}")
        print("==================================================")
        print("🎉 AIRLINE MILES CALCULATOR IS READY!")
        print("==================================================")

if __name__ == "__main__":
    seed_basic_data()
