from flask import Blueprint, jsonify, request
from src.models.airline import (
    Airline, Airport, LoyaltyProgram, EarningRate, Route, 
    FareClass, BookingClass, db, calculate_distance, calculate_miles_earned
)
from sqlalchemy import or_, func

airlines_bp = Blueprint('airlines', __name__)

@airlines_bp.route('/alliances', methods=['GET'])
def get_alliances():
    """Get all available alliances including unallianced option"""
    alliances = db.session.query(Airline.alliance).distinct().filter(
        Airline.alliance.isnot(None)
    ).order_by(Airline.alliance).all()
    
    alliance_list = [alliance[0] for alliance in alliances]
    alliance_list.append('Unallianced')  # Add unallianced option
    
    return jsonify(sorted(alliance_list))

@airlines_bp.route('/airlines', methods=['GET'])
def get_airlines():
    """Get airlines with optional alliance filter and search"""
    alliance = request.args.get('alliance')
    search = request.args.get('search', '')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = Airline.query
    
    # Filter by alliance
    if alliance:
        if alliance.lower() == 'unallianced':
            query = query.filter(Airline.alliance.is_(None))
        else:
            query = query.filter_by(alliance=alliance)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Airline.name.ilike(search_term),
                Airline.code.ilike(search_term),
                Airline.loyalty_program.ilike(search_term),
                Airline.country.ilike(search_term)
            )
        )
    
    # Order by relevance: exact code match first, then name
    if search:
        query = query.order_by(
            Airline.code.ilike(f"{search.upper()}%").desc(),
            Airline.name.ilike(f"{search}%").desc(),
            Airline.name
        )
    else:
        query = query.order_by(Airline.name)
    
    airlines = query.offset(offset).limit(limit).all()
    total_count = query.count()
    
    return jsonify({
        'airlines': [airline.to_dict() for airline in airlines],
        'total_count': total_count,
        'limit': limit,
        'offset': offset
    })

@airlines_bp.route('/airports', methods=['GET'])
def get_airports():
    """Get airports with comprehensive search and pagination"""
    search = request.args.get('search', '')
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    country = request.args.get('country')
    
    query = Airport.query
    
    # Filter by country if specified
    if country:
        query = query.filter_by(country=country)
    
    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Airport.name.ilike(search_term),
                Airport.code.ilike(search_term),
                Airport.city.ilike(search_term),
                Airport.country.ilike(search_term)
            )
        )
        
        # Order by relevance for search
        query = query.order_by(
            Airport.code.ilike(f"{search.upper()}%").desc(),
            Airport.name.ilike(f"{search}%").desc(),
            Airport.city.ilike(f"{search}%").desc(),
            Airport.name
        )
    else:
        query = query.order_by(Airport.name)
    
    airports = query.offset(offset).limit(limit).all()
    total_count = query.count()
    
    return jsonify({
        'airports': [airport.to_dict() for airport in airports],
        'total_count': total_count,
        'limit': limit,
        'offset': offset
    })

@airlines_bp.route('/airports/search', methods=['GET'])
def search_airports():
    """Quick airport search for autocomplete functionality"""
    search = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not search or len(search) < 2:
        return jsonify({'airports': []})
    
    search_term = f"%{search}%"
    airports = Airport.query.filter(
        or_(
            Airport.name.ilike(search_term),
            Airport.code.ilike(search_term),
            Airport.city.ilike(search_term)
        )
    ).order_by(
        Airport.code.ilike(f"{search.upper()}%").desc(),
        Airport.name.ilike(f"{search}%").desc(),
        Airport.city.ilike(f"{search}%").desc(),
        Airport.name
    ).limit(limit).all()
    
    return jsonify({
        'airports': [airport.to_dict() for airport in airports]
    })

@airlines_bp.route('/loyalty-programs', methods=['GET'])
def get_loyalty_programs():
    """Get loyalty programs with filtering options"""
    alliance = request.args.get('alliance')
    airline_id = request.args.get('airline_id', type=int)
    airline_code = request.args.get('airline_code')
    
    query = LoyaltyProgram.query.join(Airline)
    
    # Filter by alliance
    if alliance:
        if alliance.lower() == 'unallianced':
            query = query.filter(LoyaltyProgram.alliance.is_(None))
        else:
            query = query.filter(LoyaltyProgram.alliance == alliance)
    
    # Filter by airline
    if airline_id:
        query = query.filter(LoyaltyProgram.airline_id == airline_id)
    elif airline_code:
        query = query.filter(Airline.code == airline_code.upper())
    
    programs = query.order_by(LoyaltyProgram.name).all()
    return jsonify([program.to_dict() for program in programs])

@airlines_bp.route('/fare-classes', methods=['GET'])
def get_fare_classes():
    """Get all fare classes"""
    fare_classes = FareClass.query.order_by(FareClass.name).all()
    return jsonify([fc.to_dict() for fc in fare_classes])

@airlines_bp.route('/booking-classes', methods=['GET'])
def get_booking_classes():
    """Get booking classes with optional fare class filter"""
    fare_class_id = request.args.get('fare_class_id', type=int)
    fare_class_name = request.args.get('fare_class_name')
    
    query = BookingClass.query.join(FareClass)
    
    if fare_class_id:
        query = query.filter(BookingClass.fare_class_id == fare_class_id)
    elif fare_class_name:
        query = query.filter(FareClass.name == fare_class_name)
    
    booking_classes = query.order_by(BookingClass.code).all()
    return jsonify([bc.to_dict() for bc in booking_classes])

@airlines_bp.route('/elite-status-tiers', methods=['GET'])
def get_elite_status_tiers():
    """Get elite status tier names for a specific airline or loyalty program"""
    airline_code = request.args.get('airline_code')
    loyalty_program_id = request.args.get('loyalty_program_id', type=int)
    
    if loyalty_program_id:
        program = LoyaltyProgram.query.get(loyalty_program_id)
    elif airline_code:
        airline = Airline.query.filter_by(code=airline_code.upper()).first()
        if airline:
            program = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
        else:
            program = None
    else:
        return jsonify({'error': 'airline_code or loyalty_program_id required'}), 400
    
    if not program:
        return jsonify({'error': 'Loyalty program not found'}), 404
    
    return jsonify({
        'none': 'General Member',
        'silver': program.silver_tier_name or 'Silver',
        'gold': program.gold_tier_name or 'Gold',
        'platinum': program.platinum_tier_name or 'Platinum'
    })

@airlines_bp.route('/earning-rates', methods=['GET'])
def get_earning_rates():
    """Get earning rates for a specific loyalty program"""
    loyalty_program_id = request.args.get('loyalty_program_id', type=int)
    fare_class = request.args.get('fare_class')
    
    if not loyalty_program_id:
        return jsonify({'error': 'loyalty_program_id required'}), 400
    
    query = EarningRate.query.filter_by(loyalty_program_id=loyalty_program_id)
    
    if fare_class:
        query = query.filter_by(fare_class=fare_class)
    
    earning_rates = query.order_by(EarningRate.fare_class, EarningRate.booking_class).all()
    
    # Group by fare class
    grouped_rates = {}
    for rate in earning_rates:
        if rate.fare_class not in grouped_rates:
            grouped_rates[rate.fare_class] = []
        grouped_rates[rate.fare_class].append(rate.to_dict())
    
    return jsonify(grouped_rates)

@airlines_bp.route('/calculate-miles', methods=['POST'])
def calculate_miles():
    """Calculate miles earned for a specific route and loyalty program"""
    data = request.get_json()
    
    origin_code = data.get('origin')
    destination_code = data.get('destination')
    airline_code = data.get('airline_code')
    fare_class = data.get('fare_class', 'Economy')
    booking_class = data.get('booking_class', 'Y')
    elite_status = data.get('elite_status', 'none')
    
    # Validate required fields
    if not all([origin_code, destination_code, airline_code]):
        return jsonify({'error': 'origin, destination, and airline_code are required'}), 400
    
    # Get airports
    origin = Airport.query.filter_by(code=origin_code.upper()).first()
    destination = Airport.query.filter_by(code=destination_code.upper()).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Get airline and loyalty program
    airline = Airline.query.filter_by(code=airline_code.upper()).first()
    if not airline:
        return jsonify({'error': 'Invalid airline code'}), 400
    
    loyalty_program = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
    if not loyalty_program:
        return jsonify({'error': 'No loyalty program found for this airline'}), 400
    
    # Calculate distance
    distance = calculate_distance(origin.latitude, origin.longitude, 
                                destination.latitude, destination.longitude)
    
    # Get earning rate
    earning_rate = EarningRate.query.filter_by(
        loyalty_program_id=loyalty_program.id,
        fare_class=fare_class,
        booking_class=booking_class.upper()
    ).first()
    
    if not earning_rate:
        # Try to find a default earning rate for the fare class
        earning_rate = EarningRate.query.filter_by(
            loyalty_program_id=loyalty_program.id,
            fare_class=fare_class,
            booking_class='Y'
        ).first()
    
    if not earning_rate:
        return jsonify({'error': 'No earning rate found for this combination'}), 400
    
    # Calculate miles using the helper function
    miles_calculation = calculate_miles_earned(distance, earning_rate, elite_status)
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance, 2),
        'airline': airline.to_dict(),
        'loyalty_program': loyalty_program.to_dict(),
        'earning_rate': earning_rate.to_dict(),
        'fare_class': fare_class,
        'booking_class': booking_class.upper(),
        'elite_status': elite_status,
        'calculation': miles_calculation
    })

@airlines_bp.route('/compare-miles', methods=['POST'])
def compare_miles():
    """Compare miles earned across different airlines in the same alliance"""
    data = request.get_json()
    
    origin_code = data.get('origin')
    destination_code = data.get('destination')
    alliance = data.get('alliance')
    fare_class = data.get('fare_class', 'Economy')
    booking_class = data.get('booking_class', 'Y')
    elite_status = data.get('elite_status', 'none')
    
    # Validate required fields
    if not all([origin_code, destination_code, alliance]):
        return jsonify({'error': 'origin, destination, and alliance are required'}), 400
    
    # Get airports
    origin = Airport.query.filter_by(code=origin_code.upper()).first()
    destination = Airport.query.filter_by(code=destination_code.upper()).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    # Calculate distance
    distance = calculate_distance(origin.latitude, origin.longitude, 
                                destination.latitude, destination.longitude)
    
    # Get airlines from the specified alliance
    if alliance.lower() == 'unallianced':
        airlines = Airline.query.filter(Airline.alliance.is_(None)).all()
    else:
        airlines = Airline.query.filter_by(alliance=alliance).all()
    
    comparisons = []
    for airline in airlines:
        loyalty_program = LoyaltyProgram.query.filter_by(airline_id=airline.id).first()
        if not loyalty_program:
            continue
        
        # Get earning rate
        earning_rate = EarningRate.query.filter_by(
            loyalty_program_id=loyalty_program.id,
            fare_class=fare_class,
            booking_class=booking_class.upper()
        ).first()
        
        if not earning_rate:
            earning_rate = EarningRate.query.filter_by(
                loyalty_program_id=loyalty_program.id,
                fare_class=fare_class,
                booking_class='Y'
            ).first()
        
        if earning_rate:
            miles_calculation = calculate_miles_earned(distance, earning_rate, elite_status)
            
            comparisons.append({
                'airline': airline.to_dict(),
                'loyalty_program': loyalty_program.to_dict(),
                'earning_rate': earning_rate.to_dict(),
                'calculation': miles_calculation
            })
    
    # Sort by total miles (descending)
    comparisons.sort(key=lambda x: x['calculation']['total_miles'], reverse=True)
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance, 2),
        'alliance': alliance,
        'fare_class': fare_class,
        'booking_class': booking_class.upper(),
        'elite_status': elite_status,
        'comparisons': comparisons
    })

@airlines_bp.route('/route-distance', methods=['POST'])
def get_route_distance():
    """Get distance between two airports"""
    data = request.get_json()
    
    origin_code = data.get('origin')
    destination_code = data.get('destination')
    
    if not origin_code or not destination_code:
        return jsonify({'error': 'origin and destination codes are required'}), 400
    
    origin = Airport.query.filter_by(code=origin_code.upper()).first()
    destination = Airport.query.filter_by(code=destination_code.upper()).first()
    
    if not origin or not destination:
        return jsonify({'error': 'Invalid airport codes'}), 400
    
    distance_miles = calculate_distance(origin.latitude, origin.longitude, 
                                      destination.latitude, destination.longitude)
    distance_km = distance_miles * 1.60934
    
    return jsonify({
        'origin': origin.to_dict(),
        'destination': destination.to_dict(),
        'distance_miles': round(distance_miles, 2),
        'distance_km': round(distance_km, 2)
    })

@airlines_bp.route('/countries', methods=['GET'])
def get_countries():
    """Get list of countries with airports"""
    countries = db.session.query(Airport.country).distinct().order_by(Airport.country).all()
    return jsonify([country[0] for country in countries])

@airlines_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    stats = {
        'airports': Airport.query.count(),
        'airlines': Airline.query.count(),
        'loyalty_programs': LoyaltyProgram.query.count(),
        'alliances': {
            'SkyTeam': Airline.query.filter_by(alliance='SkyTeam').count(),
            'Oneworld': Airline.query.filter_by(alliance='Oneworld').count(),
            'Star Alliance': Airline.query.filter_by(alliance='Star Alliance').count(),
            'Unallianced': Airline.query.filter(Airline.alliance.is_(None)).count()
        }
    }
    return jsonify(stats)

