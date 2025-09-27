#!/usr/bin/env python3
"""
Complete Airline Miles Calculator - Production Ready
Includes all models, routes, and data seeding in a single file for easy deployment
"""

import os
import sys
import csv
import math
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from geopy.distance import geodesic

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'airline-miles-calculator-secret-key'

# Database configuration
if os.environ.get('DATABASE_URL'):
    # Production - PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Development - SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airline_calculator.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Airport(db.Model):
    __tablename__ = 'airports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False, default=0.0)
    longitude = db.Column(db.Float, nullable=False, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

class Alliance(db.Model):
    __tablename__ = 'alliances'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Airline(db.Model):
    __tablename__ = 'airlines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    country = db.Column(db.String(100), nullable=False)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliances.id'), nullable=True)
    
    alliance = db.relationship('Alliance', backref='airlines')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'alliance_id': self.alliance_id,
            'alliance': self.alliance.name if self.alliance else 'Unallianced'
        }

class LoyaltyProgram(db.Model):
    __tablename__ = 'loyalty_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    currency_name = db.Column(db.String(50), nullable=False, default='Miles')
    
    airline = db.relationship('Airline', backref='loyalty_programs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'airline_id': self.airline_id,
            'airline': self.airline.name if self.airline else 'Unknown',
            'currency_name': self.currency_name
        }

class EliteTier(db.Model):
    __tablename__ = 'elite_tiers'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    bonus_percentage = db.Column(db.Float, nullable=False, default=0.0)
    
    program = db.relationship('LoyaltyProgram', backref='elite_tiers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'name': self.name,
            'level': self.level,
            'bonus_percentage': self.bonus_percentage
        }

class BookingClass(db.Model):
    __tablename__ = 'booking_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(1), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    cabin_class = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'cabin_class': self.cabin_class
        }

class EarningRate(db.Model):
    __tablename__ = 'earning_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    operating_airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    booking_class_id = db.Column(db.Integer, db.ForeignKey('booking_classes.id'), nullable=False)
    earning_percentage = db.Column(db.Float, nullable=False)
    
    program = db.relationship('LoyaltyProgram')
    operating_airline = db.relationship('Airline')
    booking_class = db.relationship('BookingClass')

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/airports', methods=['GET'])
def get_airports():
    """Get airports with optional search"""
    search = request.args.get('search', '').strip()
    
    query = Airport.query
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Airport.name.ilike(search_term),
                Airport.code.ilike(search_term),
                Airport.city.ilike(search_term),
                Airport.country.ilike(search_term)
            )
        )
    
    airports = query.order_by(Airport.name).limit(100).all()
    return jsonify({'airports': [airport.to_dict() for airport in airports]})

@app.route('/api/alliances', methods=['GET'])
def get_alliances():
    """Get all airline alliances"""
    alliances = Alliance.query.order_by(Alliance.name).all()
    # Add unallianced option
    result = [{'id': -1, 'name': 'Unallianced', 'description': 'Airlines not in any alliance'}]
    result.extend([alliance.to_dict() for alliance in alliances])
    return jsonify(result)

@app.route('/api/airlines', methods=['GET'])
def get_airlines():
    """Get airlines, optionally filtered by alliance"""
    alliance_id = request.args.get('alliance_id', type=int)
    
    query = Airline.query
    
    if alliance_id is not None:
        if alliance_id == -1:  # Unallianced
            query = query.filter(Airline.alliance_id.is_(None))
        else:
            query = query.filter(Airline.alliance_id == alliance_id)
    
    airlines = query.order_by(Airline.name).all()
    return jsonify([airline.to_dict() for airline in airlines])

@app.route('/api/loyalty-programs', methods=['GET'])
def get_loyalty_programs():
    """Get loyalty programs, optionally filtered by alliance"""
    alliance_id = request.args.get('alliance_id', type=int)
    
    query = LoyaltyProgram.query.join(Airline)
    
    if alliance_id is not None:
        if alliance_id == -1:  # Unallianced
            query = query.filter(Airline.alliance_id.is_(None))
        else:
            query = query.filter(Airline.alliance_id == alliance_id)
    
    programs = query.order_by(LoyaltyProgram.name).all()
    return jsonify([program.to_dict() for program in programs])

@app.route('/api/elite-tiers/<int:program_id>', methods=['GET'])
def get_elite_tiers(program_id):
    """Get elite tiers for a specific loyalty program"""
    tiers = EliteTier.query.filter_by(program_id=program_id).order_by(EliteTier.level).all()
    return jsonify([tier.to_dict() for tier in tiers])

@app.route('/api/booking-classes', methods=['GET'])
def get_booking_classes():
    """Get all booking classes"""
    classes = BookingClass.query.order_by(BookingClass.cabin_class, BookingClass.code).all()
    return jsonify([cls.to_dict() for cls in classes])

@app.route('/api/calculate', methods=['POST'])
def calculate_miles():
    """Calculate miles for a trip"""
    data = request.get_json()
    
    # Extract parameters
    origin_code = data.get('origin_code')
    destination_code = data.get('destination_code')
    operating_airline_id = data.get('operating_airline_id')
    loyalty_program_id = data.get('loyalty_program_id')
    booking_class_id = data.get('booking_class_id')
    elite_tier_id = data.get('elite_tier_id')
    
    # Validate required parameters
    if not all([origin_code, destination_code, operating_airline_id, loyalty_program_id, booking_class_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Get airports
    origin = Airport.query.filter_by(code=origin_code).first()
    destination = Airport.query.filter_by(code=destination_code).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Calculate distance using geodesic
    distance_miles = geodesic(
        (origin.latitude, origin.longitude),
        (destination.latitude, destination.longitude)
    ).miles
    
    # Get models
    operating_airline = Airline.query.get(operating_airline_id)
    loyalty_program = LoyaltyProgram.query.get(loyalty_program_id)
    booking_class = BookingClass.query.get(booking_class_id)
    elite_tier = EliteTier.query.get(elite_tier_id) if elite_tier_id else None
    
    if not all([operating_airline, loyalty_program, booking_class]):
        return jsonify({'error': 'Invalid airline, program, or booking class'}), 400
    
    # Get earning rate
    earning_rate = EarningRate.query.filter_by(
        program_id=loyalty_program_id,
        operating_airline_id=operating_airline_id,
        booking_class_id=booking_class_id
    ).first()
    
    # Calculate earning percentage
    if earning_rate:
        earning_percentage = earning_rate.earning_percentage
    else:
        # Default earning rates based on cabin class and airline relationship
        base_rate = 100.0
        
        if booking_class.cabin_class == 'First':
            base_rate = 200.0
        elif booking_class.cabin_class == 'Business':
            base_rate = 150.0
        elif booking_class.cabin_class == 'Premium Economy':
            base_rate = 125.0
        
        # Check if same airline vs partner
        is_partner = operating_airline.id != loyalty_program.airline_id
        if is_partner:
            # Check if same alliance
            if (operating_airline.alliance_id and 
                loyalty_program.airline.alliance_id and 
                operating_airline.alliance_id == loyalty_program.airline.alliance_id):
                base_rate *= 0.85  # 15% reduction for alliance partners
            else:
                base_rate *= 0.75  # 25% reduction for non-alliance partners
        
        earning_percentage = base_rate
    
    # Calculate base miles
    base_miles = distance_miles * (earning_percentage / 100.0)
    
    # Apply minimum miles rule (500 miles minimum per segment)
    if base_miles < 500:
        base_miles = 500
    
    # Calculate elite bonus
    elite_bonus_miles = 0
    elite_bonus_percentage = 0
    
    if elite_tier:
        elite_bonus_percentage = elite_tier.bonus_percentage
        elite_bonus_miles = base_miles * (elite_bonus_percentage / 100.0)
    
    # Calculate total miles
    total_miles = base_miles + elite_bonus_miles
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance_miles),
        'operating_airline': operating_airline.to_dict(),
        'loyalty_program': loyalty_program.to_dict(),
        'booking_class': booking_class.to_dict(),
        'elite_tier': elite_tier.to_dict() if elite_tier else None,
        'earning_percentage': earning_percentage,
        'elite_bonus_percentage': elite_bonus_percentage,
        'base_miles': int(base_miles),
        'elite_bonus_miles': int(elite_bonus_miles),
        'total_miles': int(total_miles)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    return jsonify({
        'airports': Airport.query.count(),
        'airlines': Airline.query.count(),
        'programs': LoyaltyProgram.query.count()
    })

# ============================================================================
# STATIC FILE SERVING
# ============================================================================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files and SPA routing"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({'message': 'Airline Miles Calculator API', 'version': '1.0'}), 200

# ============================================================================
# DATA SEEDING
# ============================================================================

def seed_database():
    """Seed the database with comprehensive data"""
    print("Creating database tables...")
    db.create_all()
    
    # Check if data already exists
    if Airport.query.count() > 0:
        print("Database already seeded, skipping...")
        return
    
    print("Seeding database...")
    
    # Seed alliances
    alliances_data = [
        {'name': 'Star Alliance', 'description': 'The world\'s largest global airline alliance'},
        {'name': 'Oneworld', 'description': 'Premier global airline alliance'},
        {'name': 'SkyTeam', 'description': 'Global airline alliance providing worldwide coverage'},
    ]
    
    for alliance_data in alliances_data:
        alliance = Alliance(**alliance_data)
        db.session.add(alliance)
    
    db.session.commit()
    
    # Get alliances
    star_alliance = Alliance.query.filter_by(name='Star Alliance').first()
    oneworld = Alliance.query.filter_by(name='Oneworld').first()
    skyteam = Alliance.query.filter_by(name='SkyTeam').first()
    
    # Seed airlines
    airlines_data = [
        # Star Alliance
        {'name': 'United Airlines', 'code': 'UA', 'country': 'United States', 'alliance_id': star_alliance.id},
        {'name': 'Lufthansa', 'code': 'LH', 'country': 'Germany', 'alliance_id': star_alliance.id},
        {'name': 'Singapore Airlines', 'code': 'SQ', 'country': 'Singapore', 'alliance_id': star_alliance.id},
        {'name': 'ANA', 'code': 'NH', 'country': 'Japan', 'alliance_id': star_alliance.id},
        {'name': 'Air Canada', 'code': 'AC', 'country': 'Canada', 'alliance_id': star_alliance.id},
        {'name': 'Swiss International Air Lines', 'code': 'LX', 'country': 'Switzerland', 'alliance_id': star_alliance.id},
        {'name': 'Austrian Airlines', 'code': 'OS', 'country': 'Austria', 'alliance_id': star_alliance.id},
        {'name': 'Turkish Airlines', 'code': 'TK', 'country': 'Turkey', 'alliance_id': star_alliance.id},
        {'name': 'Thai Airways', 'code': 'TG', 'country': 'Thailand', 'alliance_id': star_alliance.id},
        {'name': 'Scandinavian Airlines', 'code': 'SK', 'country': 'Sweden', 'alliance_id': star_alliance.id},
        
        # Oneworld
        {'name': 'American Airlines', 'code': 'AA', 'country': 'United States', 'alliance_id': oneworld.id},
        {'name': 'British Airways', 'code': 'BA', 'country': 'United Kingdom', 'alliance_id': oneworld.id},
        {'name': 'Cathay Pacific', 'code': 'CX', 'country': 'Hong Kong', 'alliance_id': oneworld.id},
        {'name': 'Qantas', 'code': 'QF', 'country': 'Australia', 'alliance_id': oneworld.id},
        {'name': 'Japan Airlines', 'code': 'JL', 'country': 'Japan', 'alliance_id': oneworld.id},
        {'name': 'Finnair', 'code': 'AY', 'country': 'Finland', 'alliance_id': oneworld.id},
        {'name': 'Iberia', 'code': 'IB', 'country': 'Spain', 'alliance_id': oneworld.id},
        {'name': 'Malaysia Airlines', 'code': 'MH', 'country': 'Malaysia', 'alliance_id': oneworld.id},
        {'name': 'Qatar Airways', 'code': 'QR', 'country': 'Qatar', 'alliance_id': oneworld.id},
        {'name': 'Alaska Airlines', 'code': 'AS', 'country': 'United States', 'alliance_id': oneworld.id},
        
        # SkyTeam
        {'name': 'Delta Air Lines', 'code': 'DL', 'country': 'United States', 'alliance_id': skyteam.id},
        {'name': 'Air France', 'code': 'AF', 'country': 'France', 'alliance_id': skyteam.id},
        {'name': 'KLM', 'code': 'KL', 'country': 'Netherlands', 'alliance_id': skyteam.id},
        {'name': 'Korean Air', 'code': 'KE', 'country': 'South Korea', 'alliance_id': skyteam.id},
        {'name': 'China Southern Airlines', 'code': 'CZ', 'country': 'China', 'alliance_id': skyteam.id},
        {'name': 'China Eastern Airlines', 'code': 'MU', 'country': 'China', 'alliance_id': skyteam.id},
        {'name': 'Aeroflot', 'code': 'SU', 'country': 'Russia', 'alliance_id': skyteam.id},
        {'name': 'Alitalia', 'code': 'AZ', 'country': 'Italy', 'alliance_id': skyteam.id},
        {'name': 'Garuda Indonesia', 'code': 'GA', 'country': 'Indonesia', 'alliance_id': skyteam.id},
        {'name': 'Vietnam Airlines', 'code': 'VN', 'country': 'Vietnam', 'alliance_id': skyteam.id},
        
        # Unallianced
        {'name': 'Emirates', 'code': 'EK', 'country': 'UAE', 'alliance_id': None},
        {'name': 'Etihad Airways', 'code': 'EY', 'country': 'UAE', 'alliance_id': None},
        {'name': 'JetBlue Airways', 'code': 'B6', 'country': 'United States', 'alliance_id': None},
        {'name': 'Southwest Airlines', 'code': 'WN', 'country': 'United States', 'alliance_id': None},
        {'name': 'Virgin Atlantic', 'code': 'VS', 'country': 'United Kingdom', 'alliance_id': None},
        {'name': 'Virgin Australia', 'code': 'VA', 'country': 'Australia', 'alliance_id': None},
        {'name': 'Air Asia', 'code': 'AK', 'country': 'Malaysia', 'alliance_id': None},
        {'name': 'Hawaiian Airlines', 'code': 'HA', 'country': 'United States', 'alliance_id': None},
    ]
    
    for airline_data in airlines_data:
        airline = Airline(**airline_data)
        db.session.add(airline)
    
    db.session.commit()
    
    # Seed booking classes
    booking_classes_data = [
        {'code': 'Y', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'B', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'M', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'H', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'Q', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'V', 'name': 'Economy', 'cabin_class': 'Economy'},
        {'code': 'W', 'name': 'Premium Economy', 'cabin_class': 'Premium Economy'},
        {'code': 'S', 'name': 'Premium Economy', 'cabin_class': 'Premium Economy'},
        {'code': 'J', 'name': 'Business', 'cabin_class': 'Business'},
        {'code': 'C', 'name': 'Business', 'cabin_class': 'Business'},
        {'code': 'D', 'name': 'Business', 'cabin_class': 'Business'},
        {'code': 'I', 'name': 'Business', 'cabin_class': 'Business'},
        {'code': 'F', 'name': 'First', 'cabin_class': 'First'},
        {'code': 'A', 'name': 'First', 'cabin_class': 'First'},
        {'code': 'P', 'name': 'First', 'cabin_class': 'First'},
    ]
    
    for class_data in booking_classes_data:
        booking_class = BookingClass(**class_data)
        db.session.add(booking_class)
    
    db.session.commit()
    
    # Seed loyalty programs
    airlines = Airline.query.all()
    program_data = {
        'UA': {'name': 'MileagePlus', 'currency': 'Miles'},
        'LH': {'name': 'Miles & More', 'currency': 'Miles'},
        'SQ': {'name': 'KrisFlyer', 'currency': 'Miles'},
        'NH': {'name': 'Mileage Club', 'currency': 'Miles'},
        'AC': {'name': 'Aeroplan', 'currency': 'Points'},
        'AA': {'name': 'AAdvantage', 'currency': 'Miles'},
        'BA': {'name': 'Executive Club', 'currency': 'Avios'},
        'CX': {'name': 'Asia Miles', 'currency': 'Miles'},
        'QF': {'name': 'Frequent Flyer', 'currency': 'Points'},
        'JL': {'name': 'Mileage Bank', 'currency': 'Miles'},
        'DL': {'name': 'SkyMiles', 'currency': 'Miles'},
        'AF': {'name': 'Flying Blue', 'currency': 'Miles'},
        'KL': {'name': 'Flying Blue', 'currency': 'Miles'},
        'KE': {'name': 'SKYPASS', 'currency': 'Miles'},
        'EK': {'name': 'Skywards', 'currency': 'Miles'},
        'EY': {'name': 'Guest', 'currency': 'Miles'},
        'B6': {'name': 'TrueBlue', 'currency': 'Points'},
        'WN': {'name': 'Rapid Rewards', 'currency': 'Points'},
    }
    
    for airline in airlines:
        program_info = program_data.get(airline.code, {
            'name': f'{airline.name} Rewards',
            'currency': 'Miles'
        })
        
        program = LoyaltyProgram(
            name=program_info['name'],
            airline_id=airline.id,
            currency_name=program_info['currency']
        )
        db.session.add(program)
    
    db.session.commit()
    
    # Seed elite tiers
    programs = LoyaltyProgram.query.all()
    for program in programs:
        tiers = [
            {'name': 'Base', 'level': 1, 'bonus_percentage': 0.0},
            {'name': 'Silver', 'level': 2, 'bonus_percentage': 25.0},
            {'name': 'Gold', 'level': 3, 'bonus_percentage': 50.0},
            {'name': 'Platinum', 'level': 4, 'bonus_percentage': 75.0},
        ]
        
        for tier_data in tiers:
            tier = EliteTier(
                program_id=program.id,
                name=tier_data['name'],
                level=tier_data['level'],
                bonus_percentage=tier_data['bonus_percentage']
            )
            db.session.add(tier)
    
    db.session.commit()
    
    # Seed major airports
    major_airports = [
        {'name': 'Los Angeles International Airport', 'code': 'LAX', 'city': 'Los Angeles', 'state': 'CA', 'country': 'United States', 'latitude': 33.9425, 'longitude': -118.4081},
        {'name': 'John F. Kennedy International Airport', 'code': 'JFK', 'city': 'New York', 'state': 'NY', 'country': 'United States', 'latitude': 40.6413, 'longitude': -73.7781},
        {'name': 'London Heathrow Airport', 'code': 'LHR', 'city': 'London', 'state': None, 'country': 'United Kingdom', 'latitude': 51.4700, 'longitude': -0.4543},
        {'name': 'Tokyo Haneda Airport', 'code': 'HND', 'city': 'Tokyo', 'state': None, 'country': 'Japan', 'latitude': 35.5494, 'longitude': 139.7798},
        {'name': 'Singapore Changi Airport', 'code': 'SIN', 'city': 'Singapore', 'state': None, 'country': 'Singapore', 'latitude': 1.3644, 'longitude': 103.9915},
        {'name': 'Dubai International Airport', 'code': 'DXB', 'city': 'Dubai', 'state': None, 'country': 'UAE', 'latitude': 25.2532, 'longitude': 55.3657},
        {'name': 'Frankfurt Airport', 'code': 'FRA', 'city': 'Frankfurt', 'state': None, 'country': 'Germany', 'latitude': 50.0379, 'longitude': 8.5622},
        {'name': 'Charles de Gaulle Airport', 'code': 'CDG', 'city': 'Paris', 'state': None, 'country': 'France', 'latitude': 49.0097, 'longitude': 2.5479},
        {'name': 'Amsterdam Airport Schiphol', 'code': 'AMS', 'city': 'Amsterdam', 'state': None, 'country': 'Netherlands', 'latitude': 52.3105, 'longitude': 4.7683},
        {'name': 'Hong Kong International Airport', 'code': 'HKG', 'city': 'Hong Kong', 'state': None, 'country': 'Hong Kong', 'latitude': 22.3080, 'longitude': 113.9185},
        {'name': 'Sydney Kingsford Smith Airport', 'code': 'SYD', 'city': 'Sydney', 'state': 'NSW', 'country': 'Australia', 'latitude': -33.9399, 'longitude': 151.1753},
        {'name': 'Toronto Pearson International Airport', 'code': 'YYZ', 'city': 'Toronto', 'state': 'ON', 'country': 'Canada', 'latitude': 43.6777, 'longitude': -79.6248},
        {'name': 'O\'Hare International Airport', 'code': 'ORD', 'city': 'Chicago', 'state': 'IL', 'country': 'United States', 'latitude': 41.9742, 'longitude': -87.9073},
        {'name': 'San Francisco International Airport', 'code': 'SFO', 'city': 'San Francisco', 'state': 'CA', 'country': 'United States', 'latitude': 37.6213, 'longitude': -122.3790},
        {'name': 'Miami International Airport', 'code': 'MIA', 'city': 'Miami', 'state': 'FL', 'country': 'United States', 'latitude': 25.7959, 'longitude': -80.2870},
        {'name': 'Incheon International Airport', 'code': 'ICN', 'city': 'Seoul', 'state': None, 'country': 'South Korea', 'latitude': 37.4602, 'longitude': 126.4407},
        {'name': 'Beijing Capital International Airport', 'code': 'PEK', 'city': 'Beijing', 'state': None, 'country': 'China', 'latitude': 40.0799, 'longitude': 116.6031},
        {'name': 'Shanghai Pudong International Airport', 'code': 'PVG', 'city': 'Shanghai', 'state': None, 'country': 'China', 'latitude': 31.1443, 'longitude': 121.8083},
        {'name': 'Munich Airport', 'code': 'MUC', 'city': 'Munich', 'state': None, 'country': 'Germany', 'latitude': 48.3537, 'longitude': 11.7750},
        {'name': 'Zurich Airport', 'code': 'ZUR', 'city': 'Zurich', 'state': None, 'country': 'Switzerland', 'latitude': 47.4647, 'longitude': 8.5492},
    ]
    
    for airport_data in major_airports:
        airport = Airport(**airport_data)
        db.session.add(airport)
    
    db.session.commit()
    
    print("Database seeding completed!")
    print(f"Seeded {Airport.query.count()} airports")
    print(f"Seeded {Airline.query.count()} airlines")
    print(f"Seeded {LoyaltyProgram.query.count()} loyalty programs")

# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        seed_database()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Airline Miles Calculator on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
