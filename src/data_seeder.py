import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.airline import Airline, Airport, LoyaltyProgram, EarningRate, Route, db
from src.main import app

def seed_airlines():
    """Seed airlines data"""
    airlines_data = [
        # SkyTeam
        {'name': 'Air France', 'code': 'AF', 'alliance': 'SkyTeam', 'loyalty_program': 'Flying Blue'},
        {'name': 'KLM Royal Dutch Airlines', 'code': 'KL', 'alliance': 'SkyTeam', 'loyalty_program': 'Flying Blue'},
        {'name': 'Delta Air Lines', 'code': 'DL', 'alliance': 'SkyTeam', 'loyalty_program': 'SkyMiles'},
        {'name': 'Korean Air', 'code': 'KE', 'alliance': 'SkyTeam', 'loyalty_program': 'SKYPASS'},
        {'name': 'China Eastern Airlines', 'code': 'MU', 'alliance': 'SkyTeam', 'loyalty_program': 'Eastern Miles'},
        {'name': 'Virgin Atlantic', 'code': 'VS', 'alliance': 'SkyTeam', 'loyalty_program': 'Flying Club'},
        
        # Oneworld
        {'name': 'American Airlines', 'code': 'AA', 'alliance': 'Oneworld', 'loyalty_program': 'AAdvantage'},
        {'name': 'British Airways', 'code': 'BA', 'alliance': 'Oneworld', 'loyalty_program': 'Executive Club'},
        {'name': 'Cathay Pacific', 'code': 'CX', 'alliance': 'Oneworld', 'loyalty_program': 'Asia Miles'},
        {'name': 'Japan Airlines', 'code': 'JL', 'alliance': 'Oneworld', 'loyalty_program': 'JAL Mileage Bank'},
        {'name': 'Qantas', 'code': 'QF', 'alliance': 'Oneworld', 'loyalty_program': 'Qantas Frequent Flyer'},
        {'name': 'Qatar Airways', 'code': 'QR', 'alliance': 'Oneworld', 'loyalty_program': 'Privilege Club'},
        
        # Star Alliance
        {'name': 'United Airlines', 'code': 'UA', 'alliance': 'Star Alliance', 'loyalty_program': 'MileagePlus'},
        {'name': 'Singapore Airlines', 'code': 'SQ', 'alliance': 'Star Alliance', 'loyalty_program': 'KrisFlyer'},
        {'name': 'Lufthansa', 'code': 'LH', 'alliance': 'Star Alliance', 'loyalty_program': 'Miles & More'},
        {'name': 'Air Canada', 'code': 'AC', 'alliance': 'Star Alliance', 'loyalty_program': 'Aeroplan'},
        {'name': 'Turkish Airlines', 'code': 'TK', 'alliance': 'Star Alliance', 'loyalty_program': 'Miles&Smiles'},
        {'name': 'Thai Airways', 'code': 'TG', 'alliance': 'Star Alliance', 'loyalty_program': 'Royal Orchid Plus'},
    ]
    
    for airline_data in airlines_data:
        existing = Airline.query.filter_by(code=airline_data['code']).first()
        if not existing:
            airline = Airline(**airline_data)
            db.session.add(airline)
    
    db.session.commit()

def seed_airports():
    """Seed major airports data"""
    airports_data = [
        # North America
        {'name': 'John F. Kennedy International Airport', 'code': 'JFK', 'city': 'New York', 'country': 'United States', 'latitude': 40.6413, 'longitude': -73.7781},
        {'name': 'Los Angeles International Airport', 'code': 'LAX', 'city': 'Los Angeles', 'country': 'United States', 'latitude': 33.9425, 'longitude': -118.4081},
        {'name': 'Chicago O\'Hare International Airport', 'code': 'ORD', 'city': 'Chicago', 'country': 'United States', 'latitude': 41.9742, 'longitude': -87.9073},
        {'name': 'Toronto Pearson International Airport', 'code': 'YYZ', 'city': 'Toronto', 'country': 'Canada', 'latitude': 43.6777, 'longitude': -79.6248},
        
        # Europe
        {'name': 'London Heathrow Airport', 'code': 'LHR', 'city': 'London', 'country': 'United Kingdom', 'latitude': 51.4700, 'longitude': -0.4543},
        {'name': 'Charles de Gaulle Airport', 'code': 'CDG', 'city': 'Paris', 'country': 'France', 'latitude': 49.0097, 'longitude': 2.5479},
        {'name': 'Amsterdam Airport Schiphol', 'code': 'AMS', 'city': 'Amsterdam', 'country': 'Netherlands', 'latitude': 52.3105, 'longitude': 4.7683},
        {'name': 'Frankfurt Airport', 'code': 'FRA', 'city': 'Frankfurt', 'country': 'Germany', 'latitude': 50.0379, 'longitude': 8.5622},
        
        # Asia
        {'name': 'Tokyo Haneda Airport', 'code': 'HND', 'city': 'Tokyo', 'country': 'Japan', 'latitude': 35.5494, 'longitude': 139.7798},
        {'name': 'Singapore Changi Airport', 'code': 'SIN', 'city': 'Singapore', 'country': 'Singapore', 'latitude': 1.3644, 'longitude': 103.9915},
        {'name': 'Hong Kong International Airport', 'code': 'HKG', 'city': 'Hong Kong', 'country': 'Hong Kong', 'latitude': 22.3080, 'longitude': 113.9185},
        {'name': 'Seoul Incheon International Airport', 'code': 'ICN', 'city': 'Seoul', 'country': 'South Korea', 'latitude': 37.4602, 'longitude': 126.4407},
        
        # Middle East
        {'name': 'Dubai International Airport', 'code': 'DXB', 'city': 'Dubai', 'country': 'United Arab Emirates', 'latitude': 25.2532, 'longitude': 55.3657},
        {'name': 'Hamad International Airport', 'code': 'DOH', 'city': 'Doha', 'country': 'Qatar', 'latitude': 25.2731, 'longitude': 51.6080},
        
        # Australia
        {'name': 'Sydney Kingsford Smith Airport', 'code': 'SYD', 'city': 'Sydney', 'country': 'Australia', 'latitude': -33.9399, 'longitude': 151.1753},
        {'name': 'Melbourne Airport', 'code': 'MEL', 'city': 'Melbourne', 'country': 'Australia', 'latitude': -37.6690, 'longitude': 144.8410},
    ]
    
    for airport_data in airports_data:
        existing = Airport.query.filter_by(code=airport_data['code']).first()
        if not existing:
            airport = Airport(**airport_data)
            db.session.add(airport)
    
    db.session.commit()

def seed_loyalty_programs():
    """Seed loyalty programs data"""
    airlines = Airline.query.all()
    
    for airline in airlines:
        existing = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
        if not existing:
            # Set base earning rates based on typical program structures
            base_rates = {
                'Flying Blue': 4.0,  # 4 miles per euro for Explorer level
                'SkyMiles': 5.0,     # 5 miles per dollar
                'SKYPASS': 1.0,      # Distance-based
                'Eastern Miles': 1.0, # Distance-based
                'Flying Club': 1.0,   # Distance-based
                'AAdvantage': 5.0,    # 5 miles per dollar
                'Executive Club': 1.0, # Distance-based
                'Asia Miles': 1.0,    # Distance-based
                'JAL Mileage Bank': 1.0, # Distance-based
                'Qantas Frequent Flyer': 1.0, # Distance-based
                'Privilege Club': 1.0, # Distance-based
                'MileagePlus': 5.0,   # 5 miles per dollar
                'KrisFlyer': 1.0,     # Distance-based
                'Miles & More': 1.0,  # Distance-based
                'Aeroplan': 1.0,      # Distance-based
                'Miles&Smiles': 1.0,  # Distance-based
                'Royal Orchid Plus': 1.0, # Distance-based
            }
            
            program = LoyaltyProgram(
                name=airline.loyalty_program,
                airline_id=airline.id,
                alliance=airline.alliance,
                base_earning_rate=base_rates.get(airline.loyalty_program, 1.0)
            )
            db.session.add(program)
    
    db.session.commit()

def seed_earning_rates():
    """Seed earning rates for different fare classes"""
    programs = LoyaltyProgram.query.all()
    
    # Standard earning rates by fare class
    fare_class_rates = {
        'First': {'Y': 200, 'F': 200, 'A': 200},
        'Business': {'J': 150, 'C': 150, 'D': 125, 'I': 125, 'Z': 125},
        'Premium Economy': {'W': 125, 'S': 125, 'T': 100, 'L': 100, 'P': 100},
        'Economy': {'Y': 100, 'B': 100, 'M': 75, 'H': 75, 'Q': 50, 'V': 50, 'W': 50, 'G': 50, 'K': 50, 'N': 50}
    }
    
    for program in programs:
        for fare_class, booking_classes in fare_class_rates.items():
            for booking_class, earning_percentage in booking_classes.items():
                existing = EarningRate.query.filter_by(
                    loyalty_program_id=program.id,
                    fare_class=fare_class,
                    booking_class=booking_class
                ).first()
                
                if not existing:
                    # Add elite bonuses for some programs
                    elite_bonus = 0.0
                    if program.alliance == 'SkyTeam':
                        elite_bonus = 50.0  # 50% bonus for Silver members
                    elif program.alliance == 'Oneworld':
                        elite_bonus = 40.0  # 40% bonus for Gold members
                    elif program.alliance == 'Star Alliance':
                        elite_bonus = 75.0  # 75% bonus for Gold members
                    
                    earning_rate = EarningRate(
                        loyalty_program_id=program.id,
                        fare_class=fare_class,
                        booking_class=booking_class,
                        earning_percentage=earning_percentage,
                        elite_bonus=elite_bonus
                    )
                    db.session.add(earning_rate)
    
    db.session.commit()

def seed_all_data():
    """Seed all data"""
    with app.app_context():
        print("Seeding airlines...")
        seed_airlines()
        
        print("Seeding airports...")
        seed_airports()
        
        print("Seeding loyalty programs...")
        seed_loyalty_programs()
        
        print("Seeding earning rates...")
        seed_earning_rates()
        
        print("Data seeding completed!")

if __name__ == '__main__':
    seed_all_data()

