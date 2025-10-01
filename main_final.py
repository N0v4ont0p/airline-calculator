#!/usr/bin/env python3
"""
Airline Miles Calculator - Complete Production Version
Comprehensive miles calculator with 1475+ international airports
"""

import os
import csv
import math
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from geopy.distance import geodesic

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///airline_calculator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Alliance(db.Model):
    __tablename__ = 'alliances'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    airlines = db.relationship('Airline', backref='alliance_ref', lazy=True)
    loyalty_programs = db.relationship('LoyaltyProgram', backref='alliance_ref', lazy=True)

class Airline(db.Model):
    __tablename__ = 'airlines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    country = db.Column(db.String(100), nullable=False)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliances.id'), nullable=True)
    
    loyalty_programs = db.relationship('LoyaltyProgram', backref='airline_ref', lazy=True)

class LoyaltyProgram(db.Model):
    __tablename__ = 'loyalty_programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    airline = db.Column(db.String(200), nullable=False)
    currency_name = db.Column(db.String(100), nullable=False)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliances.id'), nullable=True)
    
    elite_tiers = db.relationship('EliteTier', backref='program', lazy=True)

class EliteTier(db.Model):
    __tablename__ = 'elite_tiers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bonus_percentage = db.Column(db.Integer, default=0)
    loyalty_program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)

class BookingClass(db.Model):
    __tablename__ = 'booking_classes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cabin_class = db.Column(db.String(50), nullable=False)
    earning_percentage = db.Column(db.Integer, default=100)

class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100))
    latitude = db.Column(db.Float, default=0.0)
    longitude = db.Column(db.Float, default=0.0)

# API Routes
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'airports': Airport.query.count(),
        'airlines': Airline.query.count(),
        'programs': LoyaltyProgram.query.count()
    })

@app.route('/api/airports')
def search_airports():
    search_term = request.args.get('search', '').strip()
    if len(search_term) < 2:
        return jsonify([])
    
    airports = Airport.query.filter(
        db.or_(
            Airport.code.ilike(f'%{search_term}%'),
            Airport.name.ilike(f'%{search_term}%'),
            Airport.city.ilike(f'%{search_term}%'),
            Airport.country.ilike(f'%{search_term}%')
        )
    ).limit(20).all()
    
    return jsonify([{
        'id': airport.id,
        'name': airport.name,
        'code': airport.code,
        'city': airport.city,
        'country': airport.country,
        'region': airport.region,
        'latitude': airport.latitude,
        'longitude': airport.longitude
    } for airport in airports])

@app.route('/api/alliances')
def get_alliances():
    alliances = Alliance.query.all()
    return jsonify([{
        'id': alliance.id,
        'name': alliance.name,
        'description': alliance.description
    } for alliance in alliances])

@app.route('/api/airlines')
def get_airlines():
    alliance_id = request.args.get('alliance_id')
    
    query = Airline.query
    if alliance_id and alliance_id != '-1':
        query = query.filter_by(alliance_id=alliance_id)
    elif alliance_id == '-1':
        query = query.filter_by(alliance_id=None)
    
    airlines = query.all()
    return jsonify([{
        'id': airline.id,
        'name': airline.name,
        'code': airline.code,
        'country': airline.country,
        'alliance_id': airline.alliance_id,
        'alliance': airline.alliance_ref.name if airline.alliance_ref else 'Unallianced'
    } for airline in airlines])

@app.route('/api/loyalty-programs')
def get_loyalty_programs():
    alliance_id = request.args.get('alliance_id')
    
    query = LoyaltyProgram.query
    if alliance_id and alliance_id != '-1':
        query = query.filter_by(alliance_id=alliance_id)
    elif alliance_id == '-1':
        query = query.filter_by(alliance_id=None)
    
    programs = query.all()
    return jsonify([{
        'id': program.id,
        'name': program.name,
        'airline': program.airline,
        'currency_name': program.currency_name,
        'alliance_id': program.alliance_id
    } for program in programs])

@app.route('/api/booking-classes')
def get_booking_classes():
    classes = BookingClass.query.all()
    return jsonify([{
        'id': cls.id,
        'code': cls.code,
        'name': cls.name,
        'cabin_class': cls.cabin_class,
        'earning_percentage': cls.earning_percentage
    } for cls in classes])

@app.route('/api/elite-tiers/<int:program_id>')
def get_elite_tiers(program_id):
    tiers = EliteTier.query.filter_by(loyalty_program_id=program_id).all()
    return jsonify([{
        'id': tier.id,
        'name': tier.name,
        'bonus_percentage': tier.bonus_percentage
    } for tier in tiers])

@app.route('/api/calculate', methods=['POST'])
def calculate_miles():
    try:
        data = request.get_json()
        
        # Get airports
        origin = Airport.query.filter_by(code=data['origin_code']).first()
        destination = Airport.query.filter_by(code=data['destination_code']).first()
        
        if not origin or not destination:
            return jsonify({'error': 'Invalid airport codes'}), 400
        
        # Calculate distance
        origin_coords = (origin.latitude, origin.longitude)
        destination_coords = (destination.latitude, destination.longitude)
        distance_km = geodesic(origin_coords, destination_coords).kilometers
        distance_miles = distance_km * 0.621371
        
        # Get other entities
        operating_airline = Airline.query.get(data['operating_airline_id'])
        loyalty_program = LoyaltyProgram.query.get(data['loyalty_program_id'])
        booking_class = BookingClass.query.get(data['booking_class_id'])
        elite_tier = None
        if data.get('elite_tier_id'):
            elite_tier = EliteTier.query.get(data['elite_tier_id'])
        
        if not all([operating_airline, loyalty_program, booking_class]):
            return jsonify({'error': 'Invalid selection'}), 400
        
        # Calculate earning percentage
        base_earning = booking_class.earning_percentage
        
        # Alliance relationship bonus/penalty
        earning_percentage = base_earning
        if operating_airline.alliance_id != loyalty_program.alliance_id:
            if operating_airline.alliance_id is None or loyalty_program.alliance_id is None:
                earning_percentage = int(base_earning * 0.5)  # 50% for unallianced
            else:
                earning_percentage = int(base_earning * 0.25)  # 25% for different alliance
        
        # Calculate base miles
        base_miles = max(500, int(distance_miles * earning_percentage / 100))
        
        # Elite bonus
        elite_bonus_miles = 0
        if elite_tier:
            elite_bonus_miles = int(base_miles * elite_tier.bonus_percentage / 100)
        
        total_miles = base_miles + elite_bonus_miles
        
        return jsonify({
            'origin': {
                'code': origin.code,
                'name': origin.name,
                'city': origin.city
            },
            'destination': {
                'code': destination.code,
                'name': destination.name,
                'city': destination.city
            },
            'distance_miles': int(distance_miles),
            'operating_airline': {
                'name': operating_airline.name,
                'code': operating_airline.code
            },
            'loyalty_program': {
                'name': loyalty_program.name,
                'currency_name': loyalty_program.currency_name
            },
            'booking_class': {
                'code': booking_class.code,
                'name': booking_class.name,
                'cabin_class': booking_class.cabin_class
            },
            'elite_tier': {
                'name': elite_tier.name,
                'bonus_percentage': elite_tier.bonus_percentage
            } if elite_tier else None,
            'earning_percentage': earning_percentage,
            'base_miles': base_miles,
            'elite_bonus_miles': elite_bonus_miles,
            'total_miles': total_miles
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def seed_database():
    """Seed the database with comprehensive data"""
    
    # Check if already seeded
    if Airport.query.count() > 100:
        print("Database already seeded, skipping...")
        return
    
    print("Seeding database with comprehensive data...")
    
    # Create alliances
    alliances_data = [
        {'id': 1, 'name': 'Star Alliance', 'description': 'The world\'s largest global airline alliance'},
        {'id': 2, 'name': 'Oneworld', 'description': 'Premier global airline alliance'},
        {'id': 3, 'name': 'SkyTeam', 'description': 'Global airline alliance providing worldwide coverage'},
        {'id': -1, 'name': 'Unallianced', 'description': 'Airlines not in any alliance'}
    ]
    
    for alliance_data in alliances_data:
        if not Alliance.query.filter_by(name=alliance_data['name']).first():
            alliance = Alliance(**alliance_data)
            db.session.add(alliance)
    
    db.session.commit()
    
    # Load airports from CSV
    csv_path = '/home/ubuntu/all_international_airports.csv'
    if os.path.exists(csv_path):
        print("Loading ALL international airports...")
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not Airport.query.filter_by(code=row['code']).first():
                    airport = Airport(
                        name=row['name'],
                        code=row['code'],
                        city=row['city'],
                        country=row['country'],
                        region=row.get('region', ''),
                        latitude=float(row.get('latitude', 0.0)),
                        longitude=float(row.get('longitude', 0.0))
                    )
                    db.session.add(airport)
                    count += 1
                    
                    if count % 100 == 0:
                        db.session.commit()
                        print(f"Loaded {count} airports...")
        
        db.session.commit()
        print(f"Loaded {count} international airports!")
    
    # Airlines data
    airlines_data = [
        # Star Alliance
        {'name': 'United Airlines', 'code': 'UA', 'country': 'United States', 'alliance_id': 1},
        {'name': 'Lufthansa', 'code': 'LH', 'country': 'Germany', 'alliance_id': 1},
        {'name': 'Singapore Airlines', 'code': 'SQ', 'country': 'Singapore', 'alliance_id': 1},
        {'name': 'ANA', 'code': 'NH', 'country': 'Japan', 'alliance_id': 1},
        {'name': 'Air Canada', 'code': 'AC', 'country': 'Canada', 'alliance_id': 1},
        {'name': 'Swiss International Air Lines', 'code': 'LX', 'country': 'Switzerland', 'alliance_id': 1},
        {'name': 'Austrian Airlines', 'code': 'OS', 'country': 'Austria', 'alliance_id': 1},
        {'name': 'Turkish Airlines', 'code': 'TK', 'country': 'Turkey', 'alliance_id': 1},
        {'name': 'Thai Airways', 'code': 'TG', 'country': 'Thailand', 'alliance_id': 1},
        {'name': 'Scandinavian Airlines', 'code': 'SK', 'country': 'Sweden', 'alliance_id': 1},
        {'name': 'TAP Air Portugal', 'code': 'TP', 'country': 'Portugal', 'alliance_id': 1},
        {'name': 'LOT Polish Airlines', 'code': 'LO', 'country': 'Poland', 'alliance_id': 1},
        {'name': 'Brussels Airlines', 'code': 'SN', 'country': 'Belgium', 'alliance_id': 1},
        {'name': 'Copa Airlines', 'code': 'CM', 'country': 'Panama', 'alliance_id': 1},
        {'name': 'Avianca', 'code': 'AV', 'country': 'Colombia', 'alliance_id': 1},
        {'name': 'Ethiopian Airlines', 'code': 'ET', 'country': 'Ethiopia', 'alliance_id': 1},
        {'name': 'South African Airways', 'code': 'SA', 'country': 'South Africa', 'alliance_id': 1},
        {'name': 'EVA Air', 'code': 'BR', 'country': 'Taiwan', 'alliance_id': 1},
        {'name': 'Asiana Airlines', 'code': 'OZ', 'country': 'South Korea', 'alliance_id': 1},
        {'name': 'Air China', 'code': 'CA', 'country': 'China', 'alliance_id': 1},
        
        # Oneworld
        {'name': 'American Airlines', 'code': 'AA', 'country': 'United States', 'alliance_id': 2},
        {'name': 'British Airways', 'code': 'BA', 'country': 'United Kingdom', 'alliance_id': 2},
        {'name': 'Cathay Pacific', 'code': 'CX', 'country': 'Hong Kong', 'alliance_id': 2},
        {'name': 'Qantas', 'code': 'QF', 'country': 'Australia', 'alliance_id': 2},
        {'name': 'Japan Airlines', 'code': 'JL', 'country': 'Japan', 'alliance_id': 2},
        {'name': 'Iberia', 'code': 'IB', 'country': 'Spain', 'alliance_id': 2},
        {'name': 'Finnair', 'code': 'AY', 'country': 'Finland', 'alliance_id': 2},
        {'name': 'Qatar Airways', 'code': 'QR', 'country': 'Qatar', 'alliance_id': 2},
        {'name': 'Royal Jordanian', 'code': 'RJ', 'country': 'Jordan', 'alliance_id': 2},
        {'name': 'S7 Airlines', 'code': 'S7', 'country': 'Russia', 'alliance_id': 2},
        {'name': 'SriLankan Airlines', 'code': 'UL', 'country': 'Sri Lanka', 'alliance_id': 2},
        {'name': 'Malaysia Airlines', 'code': 'MH', 'country': 'Malaysia', 'alliance_id': 2},
        {'name': 'Royal Air Maroc', 'code': 'AT', 'country': 'Morocco', 'alliance_id': 2},
        {'name': 'Alaska Airlines', 'code': 'AS', 'country': 'United States', 'alliance_id': 2},
        
        # SkyTeam
        {'name': 'Delta Air Lines', 'code': 'DL', 'country': 'United States', 'alliance_id': 3},
        {'name': 'Air France', 'code': 'AF', 'country': 'France', 'alliance_id': 3},
        {'name': 'KLM', 'code': 'KL', 'country': 'Netherlands', 'alliance_id': 3},
        {'name': 'Alitalia', 'code': 'AZ', 'country': 'Italy', 'alliance_id': 3},
        {'name': 'Korean Air', 'code': 'KE', 'country': 'South Korea', 'alliance_id': 3},
        {'name': 'China Eastern', 'code': 'MU', 'country': 'China', 'alliance_id': 3},
        {'name': 'China Southern', 'code': 'CZ', 'country': 'China', 'alliance_id': 3},
        {'name': 'Aeroflot', 'code': 'SU', 'country': 'Russia', 'alliance_id': 3},
        {'name': 'Air Europa', 'code': 'UX', 'country': 'Spain', 'alliance_id': 3},
        {'name': 'Czech Airlines', 'code': 'OK', 'country': 'Czech Republic', 'alliance_id': 3},
        {'name': 'Garuda Indonesia', 'code': 'GA', 'country': 'Indonesia', 'alliance_id': 3},
        {'name': 'Kenya Airways', 'code': 'KQ', 'country': 'Kenya', 'alliance_id': 3},
        {'name': 'Middle East Airlines', 'code': 'ME', 'country': 'Lebanon', 'alliance_id': 3},
        {'name': 'Saudia', 'code': 'SV', 'country': 'Saudi Arabia', 'alliance_id': 3},
        {'name': 'TAROM', 'code': 'RO', 'country': 'Romania', 'alliance_id': 3},
        {'name': 'Vietnam Airlines', 'code': 'VN', 'country': 'Vietnam', 'alliance_id': 3},
        {'name': 'Xiamen Airlines', 'code': 'MF', 'country': 'China', 'alliance_id': 3},
        
        # Unallianced
        {'name': 'Emirates', 'code': 'EK', 'country': 'UAE', 'alliance_id': None},
        {'name': 'Etihad Airways', 'code': 'EY', 'country': 'UAE', 'alliance_id': None},
        {'name': 'JetBlue Airways', 'code': 'B6', 'country': 'United States', 'alliance_id': None},
        {'name': 'Southwest Airlines', 'code': 'WN', 'country': 'United States', 'alliance_id': None},
        {'name': 'Virgin Atlantic', 'code': 'VS', 'country': 'United Kingdom', 'alliance_id': None},
        {'name': 'Virgin Australia', 'code': 'VA', 'country': 'Australia', 'alliance_id': None},
        {'name': 'Air India', 'code': 'AI', 'country': 'India', 'alliance_id': None},
        {'name': 'IndiGo', 'code': '6E', 'country': 'India', 'alliance_id': None},
        {'name': 'Ryanair', 'code': 'FR', 'country': 'Ireland', 'alliance_id': None},
        {'name': 'easyJet', 'code': 'U2', 'country': 'United Kingdom', 'alliance_id': None},
        {'name': 'Norwegian Air', 'code': 'DY', 'country': 'Norway', 'alliance_id': None},
        {'name': 'Wizz Air', 'code': 'W6', 'country': 'Hungary', 'alliance_id': None}
    ]
    
    for airline_data in airlines_data:
        if not Airline.query.filter_by(code=airline_data['code']).first():
            airline = Airline(**airline_data)
            db.session.add(airline)
    
    db.session.commit()
    
    # Loyalty programs (matching airlines)
    for airline_data in airlines_data:
        airline = Airline.query.filter_by(code=airline_data['code']).first()
        if airline and not LoyaltyProgram.query.filter_by(airline=airline.name).first():
            # Create loyalty program names
            program_names = {
                'United Airlines': 'MileagePlus',
                'American Airlines': 'AAdvantage',
                'Delta Air Lines': 'SkyMiles',
                'British Airways': 'Executive Club',
                'Lufthansa': 'Miles & More',
                'Air France': 'Flying Blue',
                'Singapore Airlines': 'KrisFlyer',
                'Cathay Pacific': 'Asia Miles',
                'Emirates': 'Skywards',
                'Qantas': 'Frequent Flyer'
            }
            
            program_name = program_names.get(airline.name, f"{airline.name} Rewards")
            
            program = LoyaltyProgram(
                name=program_name,
                airline=airline.name,
                currency_name='Miles',
                alliance_id=airline.alliance_id
            )
            db.session.add(program)
    
    db.session.commit()
    
    # Elite tiers for each program
    programs = LoyaltyProgram.query.all()
    for program in programs:
        if not EliteTier.query.filter_by(loyalty_program_id=program.id).first():
            tiers = [
                {'name': 'Base', 'bonus_percentage': 0},
                {'name': 'Silver', 'bonus_percentage': 25},
                {'name': 'Gold', 'bonus_percentage': 50},
                {'name': 'Platinum', 'bonus_percentage': 100}
            ]
            
            for tier_data in tiers:
                tier = EliteTier(
                    name=tier_data['name'],
                    bonus_percentage=tier_data['bonus_percentage'],
                    loyalty_program_id=program.id
                )
                db.session.add(tier)
    
    db.session.commit()
    
    # Booking classes
    booking_classes_data = [
        # Economy
        {'code': 'Y', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 100},
        {'code': 'B', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 100},
        {'code': 'M', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 100},
        {'code': 'H', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 50},
        {'code': 'Q', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 50},
        {'code': 'V', 'name': 'Economy', 'cabin_class': 'Economy', 'earning_percentage': 25},
        
        # Premium Economy
        {'code': 'W', 'name': 'Premium Economy', 'cabin_class': 'Premium Economy', 'earning_percentage': 125},
        {'code': 'S', 'name': 'Premium Economy', 'cabin_class': 'Premium Economy', 'earning_percentage': 125},
        
        # Business
        {'code': 'J', 'name': 'Business', 'cabin_class': 'Business', 'earning_percentage': 150},
        {'code': 'C', 'name': 'Business', 'cabin_class': 'Business', 'earning_percentage': 150},
        {'code': 'D', 'name': 'Business', 'cabin_class': 'Business', 'earning_percentage': 125},
        {'code': 'I', 'name': 'Business', 'cabin_class': 'Business', 'earning_percentage': 125},
        
        # First
        {'code': 'F', 'name': 'First', 'cabin_class': 'First', 'earning_percentage': 200},
        {'code': 'A', 'name': 'First', 'cabin_class': 'First', 'earning_percentage': 200},
        {'code': 'P', 'name': 'First', 'cabin_class': 'First', 'earning_percentage': 150}
    ]
    
    for class_data in booking_classes_data:
        if not BookingClass.query.filter_by(code=class_data['code']).first():
            booking_class = BookingClass(**class_data)
            db.session.add(booking_class)
    
    db.session.commit()
    print("Database seeding completed!")

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        seed_database()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Airline Miles Calculator on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
