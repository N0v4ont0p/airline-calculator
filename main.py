#!/usr/bin/env python3
"""
Production-ready Airline Miles Calculator
Optimized for Render.com deployment with PostgreSQL
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import math

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration for production
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Production: Use PostgreSQL
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    print(f"Using PostgreSQL database")
else:
    # Development/Fallback: Use SQLite
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'airline_calculator.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"Using SQLite database at {db_path}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Airport(db.Model):
    __tablename__ = 'airports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
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

class Airline(db.Model):
    __tablename__ = 'airlines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    alliance = db.Column(db.String(20), nullable=True)
    loyalty_program = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'alliance': self.alliance,
            'loyalty_program': self.loyalty_program,
            'country': self.country
        }

class LoyaltyProgram(db.Model):
    __tablename__ = 'loyalty_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    alliance = db.Column(db.String(20), nullable=True)
    base_earning_rate = db.Column(db.Float, default=1.0)
    silver_bonus = db.Column(db.Float, default=0.25)
    gold_bonus = db.Column(db.Float, default=0.50)
    platinum_bonus = db.Column(db.Float, default=1.00)
    silver_tier_name = db.Column(db.String(50), default='Silver')
    gold_tier_name = db.Column(db.String(50), default='Gold')
    platinum_tier_name = db.Column(db.String(50), default='Platinum')
    earning_model = db.Column(db.String(20), default='distance')
    currency = db.Column(db.String(10), default='USD')
    
    airline = db.relationship('Airline', backref='loyalty_programs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'airline_id': self.airline_id,
            'alliance': self.alliance,
            'base_earning_rate': self.base_earning_rate,
            'silver_bonus': self.silver_bonus,
            'gold_bonus': self.gold_bonus,
            'platinum_bonus': self.platinum_bonus,
            'silver_tier_name': self.silver_tier_name,
            'gold_tier_name': self.gold_tier_name,
            'platinum_tier_name': self.platinum_tier_name,
            'earning_model': self.earning_model,
            'currency': self.currency
        }

class FareClass(db.Model):
    __tablename__ = 'fare_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class BookingClass(db.Model):
    __tablename__ = 'booking_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(1), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    fare_class_id = db.Column(db.Integer, db.ForeignKey('fare_classes.id'), nullable=False)
    
    fare_class = db.relationship('FareClass', backref='booking_classes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'fare_class_id': self.fare_class_id,
            'fare_class_name': self.fare_class.name if self.fare_class else None
        }

class EarningRate(db.Model):
    __tablename__ = 'earning_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    loyalty_program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    fare_class = db.Column(db.String(50), nullable=False)
    booking_class = db.Column(db.String(1), nullable=False)
    earning_percentage = db.Column(db.Float, nullable=False, default=1.0)
    minimum_miles = db.Column(db.Integer, default=500)
    elite_bonus_silver = db.Column(db.Float, default=0.25)
    elite_bonus_gold = db.Column(db.Float, default=0.50)
    elite_bonus_platinum = db.Column(db.Float, default=1.00)
    
    loyalty_program = db.relationship('LoyaltyProgram', backref='earning_rates')
    
    def to_dict(self):
        return {
            'id': self.id,
            'loyalty_program_id': self.loyalty_program_id,
            'fare_class': self.fare_class,
            'booking_class': self.booking_class,
            'earning_percentage': self.earning_percentage,
            'minimum_miles': self.minimum_miles,
            'elite_bonus_silver': self.elite_bonus_silver,
            'elite_bonus_gold': self.elite_bonus_gold,
            'elite_bonus_platinum': self.elite_bonus_platinum
        }

# Utility Functions
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on Earth using Haversine formula"""
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def calculate_miles_earned(distance, loyalty_program, booking_class, elite_status='general'):
    """Calculate miles earned based on distance, program, booking class, and elite status"""
    
    # Get earning rate for this program and booking class
    earning_rate = EarningRate.query.filter_by(
        loyalty_program_id=loyalty_program.id,
        booking_class=booking_class
    ).first()
    
    if not earning_rate:
        # Default earning rate if not found
        earning_percentage = 1.0
        minimum_miles = 500
    else:
        earning_percentage = earning_rate.earning_percentage
        minimum_miles = earning_rate.minimum_miles
    
    # Calculate base miles
    base_miles = distance * earning_percentage
    
    # Apply minimum miles rule
    if base_miles < minimum_miles:
        base_miles = minimum_miles
        minimum_miles_applied = True
    else:
        minimum_miles_applied = False
    
    # Calculate elite bonus
    elite_bonus_miles = 0
    if elite_status == 'silver':
        elite_bonus_miles = base_miles * loyalty_program.silver_bonus
    elif elite_status == 'gold':
        elite_bonus_miles = base_miles * loyalty_program.gold_bonus
    elif elite_status == 'platinum':
        elite_bonus_miles = base_miles * loyalty_program.platinum_bonus
    
    total_miles = base_miles + elite_bonus_miles
    
    return {
        'base_miles': round(base_miles),
        'elite_bonus_miles': round(elite_bonus_miles),
        'total_miles': round(total_miles),
        'minimum_miles_applied': minimum_miles_applied,
        'calculation_details': {
            'distance_miles': distance,
            'earning_percentage': earning_percentage * 100,
            'minimum_miles_threshold': minimum_miles,
            'elite_status': elite_status,
            'loyalty_program': loyalty_program.name
        }
    }

# API Routes
@app.route('/api/airports')
def get_airports():
    search = request.args.get('search', '').strip()
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    query = Airport.query
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                Airport.code.ilike(search_pattern),
                Airport.name.ilike(search_pattern),
                Airport.city.ilike(search_pattern),
                Airport.country.ilike(search_pattern)
            )
        )
    
    total_count = query.count()
    airports = query.offset(offset).limit(limit).all()
    
    return jsonify({
        'airports': [airport.to_dict() for airport in airports],
        'total_count': total_count,
        'limit': limit,
        'offset': offset
    })

@app.route('/api/airlines')
def get_airlines():
    search = request.args.get('search', '').strip()
    alliance = request.args.get('alliance', '').strip()
    
    query = Airline.query
    
    if alliance:
        if alliance.lower() == 'unallianced':
            query = query.filter(Airline.alliance.is_(None))
        else:
            query = query.filter(Airline.alliance == alliance)
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                Airline.code.ilike(search_pattern),
                Airline.name.ilike(search_pattern)
            )
        )
    
    airlines = query.all()
    return jsonify([airline.to_dict() for airline in airlines])

@app.route('/api/loyalty-programs')
def get_loyalty_programs():
    search = request.args.get('search', '').strip()
    alliance = request.args.get('alliance', '').strip()
    
    query = LoyaltyProgram.query.join(Airline)
    
    if alliance:
        if alliance.lower() == 'unallianced':
            query = query.filter(LoyaltyProgram.alliance.is_(None))
        else:
            query = query.filter(LoyaltyProgram.alliance == alliance)
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                LoyaltyProgram.name.ilike(search_pattern),
                Airline.name.ilike(search_pattern),
                Airline.code.ilike(search_pattern)
            )
        )
    
    programs = query.all()
    result = []
    for program in programs:
        program_dict = program.to_dict()
        program_dict['airline_name'] = program.airline.name
        program_dict['airline_code'] = program.airline.code
        result.append(program_dict)
    
    return jsonify(result)

@app.route('/api/booking-classes')
def get_booking_classes():
    fare_class = request.args.get('fare_class', '')
    
    query = BookingClass.query.join(FareClass)
    
    if fare_class:
        query = query.filter(FareClass.name == fare_class)
    
    booking_classes = query.all()
    return jsonify([bc.to_dict() for bc in booking_classes])

@app.route('/api/calculate-miles', methods=['POST'])
def calculate_miles():
    data = request.get_json()
    
    # Get airports
    origin = Airport.query.filter_by(code=data['origin_code']).first()
    destination = Airport.query.filter_by(code=data['destination_code']).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Get loyalty program
    loyalty_program = LoyaltyProgram.query.get(data['loyalty_program_id'])
    if not loyalty_program:
        return jsonify({'error': 'Invalid loyalty program'}), 400
    
    # Calculate distance
    distance = calculate_distance(
        origin.latitude, origin.longitude,
        destination.latitude, destination.longitude
    )
    
    # Calculate miles
    result = calculate_miles_earned(
        distance,
        loyalty_program,
        data['booking_class'],
        data.get('elite_status', 'general')
    )
    
    result['route'] = {
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance, 2)
    }
    
    return jsonify(result)

@app.route('/api/stats')
def get_stats():
    """Get database statistics"""
    stats = {
        'airports': Airport.query.count(),
        'airlines': Airline.query.count(),
        'loyalty_programs': LoyaltyProgram.query.count(),
        'earning_rates': EarningRate.query.count()
    }
    return jsonify(stats)

# Serve static files (React frontend)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    if path and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Frontend not found", 404

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
