import os
import sys
import csv
import math
from geopy.distance import geodesic

from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'ultimate-airline-calculator-2024'
CORS(app)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///airline_calculator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

class Alliance(db.Model):
    __tablename__ = 'alliances'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(50))

class Airline(db.Model):
    __tablename__ = 'airlines'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(200), nullable=False)
    alliance_id = db.Column(db.String(20), db.ForeignKey('alliances.id'))
    
    alliance = db.relationship('Alliance', backref='airlines')

class BookingClass(db.Model):
    __tablename__ = 'booking_classes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    cabin = db.Column(db.String(50), nullable=False)
    multiplier = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))

class EliteTier(db.Model):
    __tablename__ = 'elite_tiers'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bonus = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))

# API Routes
@app.route('/api/airports')
def get_airports():
    search = request.args.get('search', '').strip()
    if len(search) < 2:
        return jsonify([])
    
    airports = Airport.query.filter(
        db.or_(
            Airport.code.ilike(f'%{search}%'),
            Airport.name.ilike(f'%{search}%'),
            Airport.city.ilike(f'%{search}%'),
            Airport.country.ilike(f'%{search}%')
        )
    ).limit(20).all()
    
    return jsonify([{
        'code': airport.code,
        'name': airport.name,
        'city': airport.city,
        'country': airport.country,
        'region': airport.region,
        'lat': airport.latitude,
        'lng': airport.longitude
    } for airport in airports])

@app.route('/api/alliances')
def get_alliances():
    alliances = Alliance.query.all()
    return jsonify([{
        'id': alliance.id,
        'name': alliance.name,
        'description': alliance.description,
        'color': alliance.color
    } for alliance in alliances])

@app.route('/api/airlines/<alliance_id>')
def get_airlines(alliance_id):
    if alliance_id == 'unallianced':
        airlines = Airline.query.filter_by(alliance_id=None).all()
    else:
        airlines = Airline.query.filter_by(alliance_id=alliance_id).all()
    
    return jsonify([{
        'id': airline.id,
        'name': airline.name,
        'code': airline.code,
        'country': airline.country,
        'program': airline.program
    } for airline in airlines])

@app.route('/api/booking-classes')
def get_booking_classes():
    classes = BookingClass.query.all()
    return jsonify([{
        'code': cls.code,
        'name': cls.name,
        'cabin': cls.cabin,
        'multiplier': cls.multiplier,
        'color': cls.color
    } for cls in classes])

@app.route('/api/elite-tiers')
def get_elite_tiers():
    tiers = EliteTier.query.all()
    return jsonify([{
        'id': tier.id,
        'name': tier.name,
        'bonus': tier.bonus,
        'color': tier.color
    } for tier in tiers])

@app.route('/api/calculate', methods=['POST'])
def calculate_miles():
    try:
        data = request.get_json()
        
        # Get airports
        origin = Airport.query.filter_by(code=data['origin']).first()
        destination = Airport.query.filter_by(code=data['destination']).first()
        
        if not origin or not destination:
            return jsonify({'error': 'Invalid airport codes'}), 400
        
        # Calculate distance
        distance = geodesic(
            (origin.latitude, origin.longitude),
            (destination.latitude, destination.longitude)
        ).miles
        
        # Get booking class
        booking_class = BookingClass.query.filter_by(code=data['booking_class']).first()
        if not booking_class:
            return jsonify({'error': 'Invalid booking class'}), 400
        
        # Get elite tier
        elite_tier = EliteTier.query.filter_by(id=data['elite_tier']).first()
        if not elite_tier:
            return jsonify({'error': 'Invalid elite tier'}), 400
        
        # Calculate base miles
        base_miles = max(500, int(distance * (booking_class.multiplier / 100)))
        
        # Alliance relationship factor
        alliance_multiplier = 1.0
        if data['operating_airline'] != data['loyalty_program']:
            alliance_multiplier = 0.5  # 50% for cross-crediting
        
        base_miles = int(base_miles * alliance_multiplier)
        
        # Elite bonus
        elite_bonus = int(base_miles * (elite_tier.bonus / 100))
        total_miles = base_miles + elite_bonus
        
        return jsonify({
            'distance': int(distance),
            'base_miles': base_miles,
            'elite_bonus': elite_bonus,
            'total_miles': total_miles,
            'alliance_multiplier': alliance_multiplier
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'airports': Airport.query.count(),
        'airlines': Airline.query.count(),
        'alliances': Alliance.query.count(),
        'booking_classes': BookingClass.query.count()
    })

def seed_database():
    """Seed the database with comprehensive data"""
    
    if Airport.query.count() > 0:
        print("Database already seeded")
        return
    
    print("Seeding database with comprehensive data...")
    
    # Seed Alliances
    alliances = [
        {'id': 'star', 'name': 'Star Alliance', 'description': 'The world\'s largest airline alliance', 'color': 'bg-blue-500'},
        {'id': 'oneworld', 'name': 'Oneworld', 'description': 'Premium global airline alliance', 'color': 'bg-red-500'},
        {'id': 'skyteam', 'name': 'SkyTeam', 'description': 'Global airline alliance', 'color': 'bg-green-500'},
        {'id': 'unallianced', 'name': 'Unallianced', 'description': 'Independent airlines', 'color': 'bg-gray-500'}
    ]
    
    for alliance_data in alliances:
        alliance = Alliance(**alliance_data)
        db.session.add(alliance)
    
    # Comprehensive airport data - Major international airports worldwide
    airports = [
        # Major US Hubs
        {'code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'United States', 'region': 'North America', 'latitude': 33.9425, 'longitude': -118.4081},
        {'code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'United States', 'region': 'North America', 'latitude': 40.6413, 'longitude': -73.7781},
        {'code': 'ORD', 'name': 'O\'Hare International Airport', 'city': 'Chicago', 'country': 'United States', 'region': 'North America', 'latitude': 41.9742, 'longitude': -87.9073},
        {'code': 'DFW', 'name': 'Dallas/Fort Worth International Airport', 'city': 'Dallas', 'country': 'United States', 'region': 'North America', 'latitude': 32.8998, 'longitude': -97.0403},
        {'code': 'ATL', 'name': 'Hartsfield-Jackson Atlanta International Airport', 'city': 'Atlanta', 'country': 'United States', 'region': 'North America', 'latitude': 33.6407, 'longitude': -84.4277},
        {'code': 'SFO', 'name': 'San Francisco International Airport', 'city': 'San Francisco', 'country': 'United States', 'region': 'North America', 'latitude': 37.6213, 'longitude': -122.3790},
        {'code': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami', 'country': 'United States', 'region': 'North America', 'latitude': 25.7959, 'longitude': -80.2870},
        {'code': 'SEA', 'name': 'Seattle-Tacoma International Airport', 'city': 'Seattle', 'country': 'United States', 'region': 'North America', 'latitude': 47.4502, 'longitude': -122.3088},
        {'code': 'LAS', 'name': 'McCarran International Airport', 'city': 'Las Vegas', 'country': 'United States', 'region': 'North America', 'latitude': 36.0840, 'longitude': -115.1537},
        {'code': 'BOS', 'name': 'Logan International Airport', 'city': 'Boston', 'country': 'United States', 'region': 'North America', 'latitude': 42.3656, 'longitude': -71.0096},
        {'code': 'DEN', 'name': 'Denver International Airport', 'city': 'Denver', 'country': 'United States', 'region': 'North America', 'latitude': 39.8617, 'longitude': -104.6731},
        {'code': 'PHX', 'name': 'Phoenix Sky Harbor International Airport', 'city': 'Phoenix', 'country': 'United States', 'region': 'North America', 'latitude': 33.4343, 'longitude': -112.0116},
        {'code': 'IAH', 'name': 'George Bush Intercontinental Airport', 'city': 'Houston', 'country': 'United States', 'region': 'North America', 'latitude': 29.9902, 'longitude': -95.3368},
        {'code': 'MSP', 'name': 'Minneapolis-Saint Paul International Airport', 'city': 'Minneapolis', 'country': 'United States', 'region': 'North America', 'latitude': 44.8848, 'longitude': -93.2223},
        {'code': 'DTW', 'name': 'Detroit Metropolitan Wayne County Airport', 'city': 'Detroit', 'country': 'United States', 'region': 'North America', 'latitude': 42.2124, 'longitude': -83.3534},
        
        # Major European Hubs
        {'code': 'LHR', 'name': 'Heathrow Airport', 'city': 'London', 'country': 'United Kingdom', 'region': 'Europe', 'latitude': 51.4700, 'longitude': -0.4543},
        {'code': 'CDG', 'name': 'Charles de Gaulle Airport', 'city': 'Paris', 'country': 'France', 'region': 'Europe', 'latitude': 49.0097, 'longitude': 2.5479},
        {'code': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'Germany', 'region': 'Europe', 'latitude': 50.0379, 'longitude': 8.5622},
        {'code': 'AMS', 'name': 'Amsterdam Airport Schiphol', 'city': 'Amsterdam', 'country': 'Netherlands', 'region': 'Europe', 'latitude': 52.3105, 'longitude': 4.7683},
        {'code': 'MAD', 'name': 'Madrid-Barajas Airport', 'city': 'Madrid', 'country': 'Spain', 'region': 'Europe', 'latitude': 40.4839, 'longitude': -3.5680},
        {'code': 'FCO', 'name': 'Leonardo da Vinci International Airport', 'city': 'Rome', 'country': 'Italy', 'region': 'Europe', 'latitude': 41.8003, 'longitude': 12.2389},
        {'code': 'MUC', 'name': 'Munich Airport', 'city': 'Munich', 'country': 'Germany', 'region': 'Europe', 'latitude': 48.3537, 'longitude': 11.7750},
        {'code': 'ZUR', 'name': 'Zurich Airport', 'city': 'Zurich', 'country': 'Switzerland', 'region': 'Europe', 'latitude': 47.4647, 'longitude': 8.5492},
        {'code': 'VIE', 'name': 'Vienna International Airport', 'city': 'Vienna', 'country': 'Austria', 'region': 'Europe', 'latitude': 48.1103, 'longitude': 16.5697},
        {'code': 'ARN', 'name': 'Stockholm Arlanda Airport', 'city': 'Stockholm', 'country': 'Sweden', 'region': 'Europe', 'latitude': 59.6519, 'longitude': 17.9186},
        {'code': 'CPH', 'name': 'Copenhagen Airport', 'city': 'Copenhagen', 'country': 'Denmark', 'region': 'Europe', 'latitude': 55.6181, 'longitude': 12.6561},
        {'code': 'OSL', 'name': 'Oslo Airport', 'city': 'Oslo', 'country': 'Norway', 'region': 'Europe', 'latitude': 60.1939, 'longitude': 11.1004},
        {'code': 'HEL', 'name': 'Helsinki Airport', 'city': 'Helsinki', 'country': 'Finland', 'region': 'Europe', 'latitude': 60.3172, 'longitude': 24.9633},
        {'code': 'LGW', 'name': 'Gatwick Airport', 'city': 'London', 'country': 'United Kingdom', 'region': 'Europe', 'latitude': 51.1481, 'longitude': -0.1903},
        {'code': 'MAN', 'name': 'Manchester Airport', 'city': 'Manchester', 'country': 'United Kingdom', 'region': 'Europe', 'latitude': 53.3537, 'longitude': -2.2750},
        
        # Major Asian Hubs
        {'code': 'NRT', 'name': 'Narita International Airport', 'city': 'Tokyo', 'country': 'Japan', 'region': 'Asia', 'latitude': 35.7720, 'longitude': 140.3929},
        {'code': 'HND', 'name': 'Haneda Airport', 'city': 'Tokyo', 'country': 'Japan', 'region': 'Asia', 'latitude': 35.5494, 'longitude': 139.7798},
        {'code': 'ICN', 'name': 'Incheon International Airport', 'city': 'Seoul', 'country': 'South Korea', 'region': 'Asia', 'latitude': 37.4602, 'longitude': 126.4407},
        {'code': 'SIN', 'name': 'Singapore Changi Airport', 'city': 'Singapore', 'country': 'Singapore', 'region': 'Asia', 'latitude': 1.3644, 'longitude': 103.9915},
        {'code': 'HKG', 'name': 'Hong Kong International Airport', 'city': 'Hong Kong', 'country': 'Hong Kong', 'region': 'Asia', 'latitude': 22.3080, 'longitude': 113.9185},
        {'code': 'PEK', 'name': 'Beijing Capital International Airport', 'city': 'Beijing', 'country': 'China', 'region': 'Asia', 'latitude': 40.0799, 'longitude': 116.6031},
        {'code': 'PVG', 'name': 'Shanghai Pudong International Airport', 'city': 'Shanghai', 'country': 'China', 'region': 'Asia', 'latitude': 31.1443, 'longitude': 121.8083},
        {'code': 'BKK', 'name': 'Suvarnabhumi Airport', 'city': 'Bangkok', 'country': 'Thailand', 'region': 'Asia', 'latitude': 13.6900, 'longitude': 100.7501},
        {'code': 'KUL', 'name': 'Kuala Lumpur International Airport', 'city': 'Kuala Lumpur', 'country': 'Malaysia', 'region': 'Asia', 'latitude': 2.7456, 'longitude': 101.7072},
        {'code': 'DEL', 'name': 'Indira Gandhi International Airport', 'city': 'New Delhi', 'country': 'India', 'region': 'Asia', 'latitude': 28.5562, 'longitude': 77.1000},
        {'code': 'BOM', 'name': 'Chhatrapati Shivaji Maharaj International Airport', 'city': 'Mumbai', 'country': 'India', 'region': 'Asia', 'latitude': 19.0896, 'longitude': 72.8656},
        {'code': 'CGK', 'name': 'Soekarno-Hatta International Airport', 'city': 'Jakarta', 'country': 'Indonesia', 'region': 'Asia', 'latitude': -6.1256, 'longitude': 106.6559},
        {'code': 'MNL', 'name': 'Ninoy Aquino International Airport', 'city': 'Manila', 'country': 'Philippines', 'region': 'Asia', 'latitude': 14.5086, 'longitude': 121.0194},
        {'code': 'TPE', 'name': 'Taiwan Taoyuan International Airport', 'city': 'Taipei', 'country': 'Taiwan', 'region': 'Asia', 'latitude': 25.0797, 'longitude': 121.2342},
        {'code': 'KIX', 'name': 'Kansai International Airport', 'city': 'Osaka', 'country': 'Japan', 'region': 'Asia', 'latitude': 34.4347, 'longitude': 135.2441},
        
        # Middle East & Africa
        {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'UAE', 'region': 'Middle East', 'latitude': 25.2532, 'longitude': 55.3657},
        {'code': 'DOH', 'name': 'Hamad International Airport', 'city': 'Doha', 'country': 'Qatar', 'region': 'Middle East', 'latitude': 25.2731, 'longitude': 51.6080},
        {'code': 'AUH', 'name': 'Abu Dhabi International Airport', 'city': 'Abu Dhabi', 'country': 'UAE', 'region': 'Middle East', 'latitude': 24.4330, 'longitude': 54.6511},
        {'code': 'CAI', 'name': 'Cairo International Airport', 'city': 'Cairo', 'country': 'Egypt', 'region': 'Africa', 'latitude': 30.1219, 'longitude': 31.4056},
        {'code': 'JNB', 'name': 'O.R. Tambo International Airport', 'city': 'Johannesburg', 'country': 'South Africa', 'region': 'Africa', 'latitude': -26.1367, 'longitude': 28.2411},
        {'code': 'ADD', 'name': 'Addis Ababa Bole International Airport', 'city': 'Addis Ababa', 'country': 'Ethiopia', 'region': 'Africa', 'latitude': 8.9806, 'longitude': 38.7992},
        {'code': 'CPT', 'name': 'Cape Town International Airport', 'city': 'Cape Town', 'country': 'South Africa', 'region': 'Africa', 'latitude': -33.9649, 'longitude': 18.6017},
        {'code': 'LOS', 'name': 'Murtala Muhammed International Airport', 'city': 'Lagos', 'country': 'Nigeria', 'region': 'Africa', 'latitude': 6.5774, 'longitude': 3.3212},
        {'code': 'CMN', 'name': 'Mohammed V International Airport', 'city': 'Casablanca', 'country': 'Morocco', 'region': 'Africa', 'latitude': 33.3675, 'longitude': -7.5898},
        {'code': 'TLV', 'name': 'Ben Gurion Airport', 'city': 'Tel Aviv', 'country': 'Israel', 'region': 'Middle East', 'latitude': 32.0114, 'longitude': 34.8867},
        
        # Oceania
        {'code': 'SYD', 'name': 'Sydney Kingsford Smith Airport', 'city': 'Sydney', 'country': 'Australia', 'region': 'Oceania', 'latitude': -33.9399, 'longitude': 151.1753},
        {'code': 'MEL', 'name': 'Melbourne Airport', 'city': 'Melbourne', 'country': 'Australia', 'region': 'Oceania', 'latitude': -37.6690, 'longitude': 144.8410},
        {'code': 'AKL', 'name': 'Auckland Airport', 'city': 'Auckland', 'country': 'New Zealand', 'region': 'Oceania', 'latitude': -37.0082, 'longitude': 174.7850},
        {'code': 'BNE', 'name': 'Brisbane Airport', 'city': 'Brisbane', 'country': 'Australia', 'region': 'Oceania', 'latitude': -27.3942, 'longitude': 153.1218},
        {'code': 'PER', 'name': 'Perth Airport', 'city': 'Perth', 'country': 'Australia', 'region': 'Oceania', 'latitude': -31.9403, 'longitude': 115.9669},
        {'code': 'CHC', 'name': 'Christchurch Airport', 'city': 'Christchurch', 'country': 'New Zealand', 'region': 'Oceania', 'latitude': -43.4894, 'longitude': 172.5320},
        
        # South America
        {'code': 'GRU', 'name': 'São Paulo/Guarulhos International Airport', 'city': 'São Paulo', 'country': 'Brazil', 'region': 'South America', 'latitude': -23.4356, 'longitude': -46.4731},
        {'code': 'EZE', 'name': 'Ezeiza International Airport', 'city': 'Buenos Aires', 'country': 'Argentina', 'region': 'South America', 'latitude': -34.8222, 'longitude': -58.5358},
        {'code': 'SCL', 'name': 'Santiago International Airport', 'city': 'Santiago', 'country': 'Chile', 'region': 'South America', 'latitude': -33.3927, 'longitude': -70.7854},
        {'code': 'LIM', 'name': 'Jorge Chávez International Airport', 'city': 'Lima', 'country': 'Peru', 'region': 'South America', 'latitude': -12.0219, 'longitude': -77.1143},
        {'code': 'BOG', 'name': 'El Dorado International Airport', 'city': 'Bogotá', 'country': 'Colombia', 'region': 'South America', 'latitude': 4.7016, 'longitude': -74.1469},
        {'code': 'GIG', 'name': 'Rio de Janeiro/Galeão International Airport', 'city': 'Rio de Janeiro', 'country': 'Brazil', 'region': 'South America', 'latitude': -22.8099, 'longitude': -43.2505},
        
        # Canada
        {'code': 'YYZ', 'name': 'Toronto Pearson International Airport', 'city': 'Toronto', 'country': 'Canada', 'region': 'North America', 'latitude': 43.6777, 'longitude': -79.6248},
        {'code': 'YVR', 'name': 'Vancouver International Airport', 'city': 'Vancouver', 'country': 'Canada', 'region': 'North America', 'latitude': 49.1939, 'longitude': -123.1844},
        {'code': 'YUL', 'name': 'Montreal-Pierre Elliott Trudeau International Airport', 'city': 'Montreal', 'country': 'Canada', 'region': 'North America', 'latitude': 45.4706, 'longitude': -73.7408},
        {'code': 'YYC', 'name': 'Calgary International Airport', 'city': 'Calgary', 'country': 'Canada', 'region': 'North America', 'latitude': 51.1315, 'longitude': -114.0106}
    ]
    
    for airport_data in airports:
        airport = Airport(**airport_data)
        db.session.add(airport)
    
    # Seed Airlines
    airlines = [
        # Star Alliance
        {'id': 'ua', 'name': 'United Airlines', 'code': 'UA', 'country': 'United States', 'program': 'MileagePlus', 'alliance_id': 'star'},
        {'id': 'lh', 'name': 'Lufthansa', 'code': 'LH', 'country': 'Germany', 'program': 'Miles & More', 'alliance_id': 'star'},
        {'id': 'sq', 'name': 'Singapore Airlines', 'code': 'SQ', 'country': 'Singapore', 'program': 'KrisFlyer', 'alliance_id': 'star'},
        {'id': 'nh', 'name': 'ANA', 'code': 'NH', 'country': 'Japan', 'program': 'ANA Mileage Club', 'alliance_id': 'star'},
        {'id': 'ac', 'name': 'Air Canada', 'code': 'AC', 'country': 'Canada', 'program': 'Aeroplan', 'alliance_id': 'star'},
        {'id': 'lx', 'name': 'Swiss International Air Lines', 'code': 'LX', 'country': 'Switzerland', 'program': 'Miles & More', 'alliance_id': 'star'},
        {'id': 'os', 'name': 'Austrian Airlines', 'code': 'OS', 'country': 'Austria', 'program': 'Miles & More', 'alliance_id': 'star'},
        {'id': 'tk', 'name': 'Turkish Airlines', 'code': 'TK', 'country': 'Turkey', 'program': 'Miles&Smiles', 'alliance_id': 'star'},
        {'id': 'tg', 'name': 'Thai Airways', 'code': 'TG', 'country': 'Thailand', 'program': 'Royal Orchid Plus', 'alliance_id': 'star'},
        {'id': 'sk', 'name': 'Scandinavian Airlines', 'code': 'SK', 'country': 'Sweden', 'program': 'EuroBonus', 'alliance_id': 'star'},
        
        # Oneworld
        {'id': 'aa', 'name': 'American Airlines', 'code': 'AA', 'country': 'United States', 'program': 'AAdvantage', 'alliance_id': 'oneworld'},
        {'id': 'ba', 'name': 'British Airways', 'code': 'BA', 'country': 'United Kingdom', 'program': 'Executive Club', 'alliance_id': 'oneworld'},
        {'id': 'cx', 'name': 'Cathay Pacific', 'code': 'CX', 'country': 'Hong Kong', 'program': 'Asia Miles', 'alliance_id': 'oneworld'},
        {'id': 'qf', 'name': 'Qantas', 'code': 'QF', 'country': 'Australia', 'program': 'Frequent Flyer', 'alliance_id': 'oneworld'},
        {'id': 'jl', 'name': 'Japan Airlines', 'code': 'JL', 'country': 'Japan', 'program': 'JAL Mileage Bank', 'alliance_id': 'oneworld'},
        {'id': 'ib', 'name': 'Iberia', 'code': 'IB', 'country': 'Spain', 'program': 'Iberia Plus', 'alliance_id': 'oneworld'},
        {'id': 'ay', 'name': 'Finnair', 'code': 'AY', 'country': 'Finland', 'program': 'Finnair Plus', 'alliance_id': 'oneworld'},
        {'id': 'qr', 'name': 'Qatar Airways', 'code': 'QR', 'country': 'Qatar', 'program': 'Privilege Club', 'alliance_id': 'oneworld'},
        {'id': 'rj', 'name': 'Royal Jordanian', 'code': 'RJ', 'country': 'Jordan', 'program': 'Royal Plus', 'alliance_id': 'oneworld'},
        {'id': 'mh', 'name': 'Malaysia Airlines', 'code': 'MH', 'country': 'Malaysia', 'program': 'Enrich', 'alliance_id': 'oneworld'},
        
        # SkyTeam
        {'id': 'dl', 'name': 'Delta Air Lines', 'code': 'DL', 'country': 'United States', 'program': 'SkyMiles', 'alliance_id': 'skyteam'},
        {'id': 'af', 'name': 'Air France', 'code': 'AF', 'country': 'France', 'program': 'Flying Blue', 'alliance_id': 'skyteam'},
        {'id': 'kl', 'name': 'KLM', 'code': 'KL', 'country': 'Netherlands', 'program': 'Flying Blue', 'alliance_id': 'skyteam'},
        {'id': 'ke', 'name': 'Korean Air', 'code': 'KE', 'country': 'South Korea', 'program': 'SKYPASS', 'alliance_id': 'skyteam'},
        {'id': 'mu', 'name': 'China Eastern', 'code': 'MU', 'country': 'China', 'program': 'Eastern Miles', 'alliance_id': 'skyteam'},
        {'id': 'cz', 'name': 'China Southern', 'code': 'CZ', 'country': 'China', 'program': 'Sky Pearl Club', 'alliance_id': 'skyteam'},
        {'id': 'su', 'name': 'Aeroflot', 'code': 'SU', 'country': 'Russia', 'program': 'Aeroflot Bonus', 'alliance_id': 'skyteam'},
        {'id': 'ga', 'name': 'Garuda Indonesia', 'code': 'GA', 'country': 'Indonesia', 'program': 'GarudaMiles', 'alliance_id': 'skyteam'},
        {'id': 'kq', 'name': 'Kenya Airways', 'code': 'KQ', 'country': 'Kenya', 'program': 'Flying Blue', 'alliance_id': 'skyteam'},
        {'id': 'vn', 'name': 'Vietnam Airlines', 'code': 'VN', 'country': 'Vietnam', 'program': 'Golden Lotus Plus', 'alliance_id': 'skyteam'},
        
        # Unallianced
        {'id': 'ek', 'name': 'Emirates', 'code': 'EK', 'country': 'UAE', 'program': 'Skywards', 'alliance_id': None},
        {'id': 'ey', 'name': 'Etihad Airways', 'code': 'EY', 'country': 'UAE', 'program': 'Etihad Guest', 'alliance_id': None},
        {'id': 'b6', 'name': 'JetBlue Airways', 'code': 'B6', 'country': 'United States', 'program': 'TrueBlue', 'alliance_id': None},
        {'id': 'wn', 'name': 'Southwest Airlines', 'code': 'WN', 'country': 'United States', 'program': 'Rapid Rewards', 'alliance_id': None},
        {'id': 'vs', 'name': 'Virgin Atlantic', 'code': 'VS', 'country': 'United Kingdom', 'program': 'Flying Club', 'alliance_id': None},
        {'id': 'va', 'name': 'Virgin Australia', 'code': 'VA', 'country': 'Australia', 'program': 'Velocity', 'alliance_id': None},
        {'id': 'ai', 'name': 'Air India', 'code': 'AI', 'country': 'India', 'program': 'Flying Returns', 'alliance_id': None},
        {'id': 'fr', 'name': 'Ryanair', 'code': 'FR', 'country': 'Ireland', 'program': 'myRyanair', 'alliance_id': None},
        {'id': 'u2', 'name': 'easyJet', 'code': 'U2', 'country': 'United Kingdom', 'program': 'easyJet Plus', 'alliance_id': None},
        {'id': 'dy', 'name': 'Norwegian Air', 'code': 'DY', 'country': 'Norway', 'program': 'Norwegian Reward', 'alliance_id': None}
    ]
    
    for airline_data in airlines:
        airline = Airline(**airline_data)
        db.session.add(airline)
    
    # Seed Booking Classes
    booking_classes = [
        {'code': 'F', 'name': 'First Class', 'cabin': 'First', 'multiplier': 200, 'color': 'bg-purple-500'},
        {'code': 'A', 'name': 'First Class', 'cabin': 'First', 'multiplier': 200, 'color': 'bg-purple-500'},
        {'code': 'P', 'name': 'First Class (Discounted)', 'cabin': 'First', 'multiplier': 150, 'color': 'bg-purple-400'},
        {'code': 'J', 'name': 'Business Class', 'cabin': 'Business', 'multiplier': 150, 'color': 'bg-blue-500'},
        {'code': 'C', 'name': 'Business Class', 'cabin': 'Business', 'multiplier': 150, 'color': 'bg-blue-500'},
        {'code': 'D', 'name': 'Business Class (Discounted)', 'cabin': 'Business', 'multiplier': 125, 'color': 'bg-blue-400'},
        {'code': 'I', 'name': 'Business Class (Discounted)', 'cabin': 'Business', 'multiplier': 125, 'color': 'bg-blue-400'},
        {'code': 'W', 'name': 'Premium Economy', 'cabin': 'Premium Economy', 'multiplier': 125, 'color': 'bg-green-500'},
        {'code': 'S', 'name': 'Premium Economy', 'cabin': 'Premium Economy', 'multiplier': 125, 'color': 'bg-green-500'},
        {'code': 'Y', 'name': 'Economy Class', 'cabin': 'Economy', 'multiplier': 100, 'color': 'bg-yellow-500'},
        {'code': 'B', 'name': 'Economy Class', 'cabin': 'Economy', 'multiplier': 100, 'color': 'bg-yellow-500'},
        {'code': 'M', 'name': 'Economy Class', 'cabin': 'Economy', 'multiplier': 100, 'color': 'bg-yellow-500'},
        {'code': 'H', 'name': 'Economy Class (Discounted)', 'cabin': 'Economy', 'multiplier': 50, 'color': 'bg-yellow-400'},
        {'code': 'Q', 'name': 'Economy Class (Discounted)', 'cabin': 'Economy', 'multiplier': 50, 'color': 'bg-yellow-400'},
        {'code': 'V', 'name': 'Economy Class (Deep Discount)', 'cabin': 'Economy', 'multiplier': 25, 'color': 'bg-yellow-300'},
        {'code': 'L', 'name': 'Economy Class (Deep Discount)', 'cabin': 'Economy', 'multiplier': 25, 'color': 'bg-yellow-300'}
    ]
    
    for class_data in booking_classes:
        booking_class = BookingClass(**class_data)
        db.session.add(booking_class)
    
    # Seed Elite Tiers
    elite_tiers = [
        {'id': 'base', 'name': 'Base Member', 'bonus': 0, 'color': 'bg-gray-400'},
        {'id': 'silver', 'name': 'Silver/Gold', 'bonus': 25, 'color': 'bg-gray-300'},
        {'id': 'gold', 'name': 'Gold/Platinum', 'bonus': 50, 'color': 'bg-yellow-400'},
        {'id': 'platinum', 'name': 'Platinum/Diamond', 'bonus': 100, 'color': 'bg-purple-400'}
    ]
    
    for tier_data in elite_tiers:
        tier = EliteTier(**tier_data)
        db.session.add(tier)
    
    db.session.commit()
    print("Database seeded successfully!")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
