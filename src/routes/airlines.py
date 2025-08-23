from flask import Blueprint, jsonify, request
from src.models.airline import Airline, Airport, LoyaltyProgram, EarningRate, Route, db
import math

airlines_bp = Blueprint('airlines', __name__)

@airlines_bp.route('/airlines', methods=['GET'])
def get_airlines():
    """Get all airlines"""
    airlines = Airline.query.all()
    return jsonify([airline.to_dict() for airline in airlines])

@airlines_bp.route('/airlines/<alliance>', methods=['GET'])
def get_airlines_by_alliance(alliance):
    """Get airlines by alliance"""
    airlines = Airline.query.filter_by(alliance=alliance).all()
    return jsonify([airline.to_dict() for airline in airlines])

@airlines_bp.route('/airports', methods=['GET'])
def get_airports():
    """Get all airports"""
    search = request.args.get('search', '')
    if search:
        airports = Airport.query.filter(
            (Airport.name.contains(search)) |
            (Airport.code.contains(search.upper())) |
            (Airport.city.contains(search))
        ).limit(20).all()
    else:
        airports = Airport.query.limit(100).all()
    return jsonify([airport.to_dict() for airport in airports])

@airlines_bp.route('/loyalty-programs', methods=['GET'])
def get_loyalty_programs():
    """Get all loyalty programs"""
    alliance = request.args.get('alliance')
    if alliance:
        programs = LoyaltyProgram.query.filter_by(alliance=alliance).all()
    else:
        programs = LoyaltyProgram.query.all()
    return jsonify([program.to_dict() for program in programs])

@airlines_bp.route('/calculate-miles', methods=['POST'])
def calculate_miles():
    """Calculate miles earned for a specific route and loyalty program"""
    data = request.get_json()
    
    origin_code = data.get('origin')
    destination_code = data.get('destination')
    loyalty_program_id = data.get('loyalty_program_id')
    fare_class = data.get('fare_class', 'Economy')
    booking_class = data.get('booking_class', 'Y')
    
    # Get airports
    origin = Airport.query.filter_by(code=origin_code.upper()).first()
    destination = Airport.query.filter_by(code=destination_code.upper()).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Calculate distance using Haversine formula
    distance = calculate_distance(origin.latitude, origin.longitude, 
                                destination.latitude, destination.longitude)
    
    # Get loyalty program
    loyalty_program = LoyaltyProgram.query.get(loyalty_program_id)
    if not loyalty_program:
        return jsonify({'error': 'Invalid loyalty program'}), 400
    
    # Get earning rate for the specific fare class and booking class
    earning_rate = EarningRate.query.filter_by(
        loyalty_program_id=loyalty_program_id,
        fare_class=fare_class,
        booking_class=booking_class.upper()
    ).first()
    
    if not earning_rate:
        # Use default earning rate if specific one not found
        earning_rate = EarningRate.query.filter_by(
            loyalty_program_id=loyalty_program_id,
            fare_class=fare_class
        ).first()
    
    if not earning_rate:
        return jsonify({'error': 'No earning rate found for this combination'}), 400
    
    # Calculate miles earned
    base_miles = distance * (earning_rate.earning_percentage / 100)
    elite_bonus_miles = distance * (earning_rate.elite_bonus / 100)
    total_miles = base_miles + elite_bonus_miles
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance, 2),
        'loyalty_program': loyalty_program.to_dict(),
        'earning_rate': earning_rate.to_dict(),
        'base_miles': round(base_miles, 2),
        'elite_bonus_miles': round(elite_bonus_miles, 2),
        'total_miles': round(total_miles, 2)
    })

@airlines_bp.route('/compare-miles', methods=['POST'])
def compare_miles():
    """Compare miles earned across different loyalty programs for the same route"""
    data = request.get_json()
    
    origin_code = data.get('origin')
    destination_code = data.get('destination')
    alliance = data.get('alliance')
    fare_class = data.get('fare_class', 'Economy')
    booking_class = data.get('booking_class', 'Y')
    
    # Get airports
    origin = Airport.query.filter_by(code=origin_code.upper()).first()
    destination = Airport.query.filter_by(code=destination_code.upper()).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Calculate distance
    distance = calculate_distance(origin.latitude, origin.longitude, 
                                destination.latitude, destination.longitude)
    
    # Get loyalty programs from the same alliance
    loyalty_programs = LoyaltyProgram.query.filter_by(alliance=alliance).all()
    
    comparisons = []
    for program in loyalty_programs:
        # Get earning rate
        earning_rate = EarningRate.query.filter_by(
            loyalty_program_id=program.id,
            fare_class=fare_class,
            booking_class=booking_class.upper()
        ).first()
        
        if not earning_rate:
            earning_rate = EarningRate.query.filter_by(
                loyalty_program_id=program.id,
                fare_class=fare_class
            ).first()
        
        if earning_rate:
            base_miles = distance * (earning_rate.earning_percentage / 100)
            elite_bonus_miles = distance * (earning_rate.elite_bonus / 100)
            total_miles = base_miles + elite_bonus_miles
            
            comparisons.append({
                'loyalty_program': program.to_dict(),
                'earning_rate': earning_rate.to_dict(),
                'base_miles': round(base_miles, 2),
                'elite_bonus_miles': round(elite_bonus_miles, 2),
                'total_miles': round(total_miles, 2)
            })
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance, 2),
        'alliance': alliance,
        'comparisons': comparisons
    })

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3956
    
    return c * r

