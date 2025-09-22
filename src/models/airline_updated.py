import math
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airline(db.Model):
    __tablename__ = 'airlines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)
    country = db.Column(db.String(50), nullable=False)
    alliance = db.Column(db.String(50), nullable=True)  # Star Alliance, Oneworld, SkyTeam, or null for unallianced
    loyalty_program = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'alliance': self.alliance,
            'loyalty_program': self.loyalty_program
        }

class Airport(db.Model):
    __tablename__ = 'airports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(4), nullable=False)  # IATA code
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timezone = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'city': self.city,
            'country': self.country,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timezone': self.timezone
        }

class LoyaltyProgram(db.Model):
    __tablename__ = 'loyalty_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    alliance = db.Column(db.String(50), nullable=True)
    earning_model = db.Column(db.String(20), default='distance')  # 'distance' or 'revenue'
    base_earning_rate = db.Column(db.Float, default=1.0)  # For revenue-based programs
    
    # Elite tier names (airline-specific)
    silver_tier_name = db.Column(db.String(50), default='Silver')
    gold_tier_name = db.Column(db.String(50), default='Gold')
    platinum_tier_name = db.Column(db.String(50), default='Platinum')
    
    # Elite bonus rates (as multipliers, e.g., 0.25 for 25% bonus)
    silver_bonus = db.Column(db.Float, default=0.25)
    gold_bonus = db.Column(db.Float, default=0.50)
    platinum_bonus = db.Column(db.Float, default=1.00)
    
    # Relationships
    airline = db.relationship('Airline', backref=db.backref('loyalty_programs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'airline_id': self.airline_id,
            'name': self.name,
            'alliance': self.alliance,
            'earning_model': self.earning_model,
            'base_earning_rate': self.base_earning_rate,
            'silver_tier_name': self.silver_tier_name,
            'gold_tier_name': self.gold_tier_name,
            'platinum_tier_name': self.platinum_tier_name,
            'silver_bonus': self.silver_bonus,
            'gold_bonus': self.gold_bonus,
            'platinum_bonus': self.platinum_bonus,
            'airline': self.airline.to_dict() if self.airline else None
        }

class EarningRate(db.Model):
    __tablename__ = 'earning_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    loyalty_program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    fare_class = db.Column(db.String(20), nullable=False)  # Economy, Business, First, Premium Economy
    booking_class = db.Column(db.String(5), nullable=False)  # Y, B, M, etc.
    earning_percentage = db.Column(db.Float, nullable=False)  # 0.25 = 25%, 1.0 = 100%, 1.5 = 150%
    minimum_miles = db.Column(db.Integer, default=500)  # Minimum miles per segment
    maximum_miles = db.Column(db.Integer, nullable=True)  # Maximum miles per segment (rare)
    
    # Elite-specific bonuses (overrides program defaults if set)
    elite_bonus_silver = db.Column(db.Float, nullable=True)
    elite_bonus_gold = db.Column(db.Float, nullable=True)
    elite_bonus_platinum = db.Column(db.Float, nullable=True)
    
    # Relationships
    loyalty_program = db.relationship('LoyaltyProgram', backref=db.backref('earning_rates', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'loyalty_program_id': self.loyalty_program_id,
            'fare_class': self.fare_class,
            'booking_class': self.booking_class,
            'earning_percentage': self.earning_percentage,
            'minimum_miles': self.minimum_miles,
            'maximum_miles': self.maximum_miles,
            'elite_bonus_silver': self.elite_bonus_silver,
            'elite_bonus_gold': self.elite_bonus_gold,
            'elite_bonus_platinum': self.elite_bonus_platinum
        }

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    distance_miles = db.Column(db.Float, nullable=False)
    
    # Relationships
    origin = db.relationship('Airport', foreign_keys=[origin_id])
    destination = db.relationship('Airport', foreign_keys=[destination_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'origin_id': self.origin_id,
            'destination_id': self.destination_id,
            'distance_miles': self.distance_miles,
            'origin': self.origin.to_dict() if self.origin else None,
            'destination': self.destination.to_dict() if self.destination else None
        }

class FareClass(db.Model):
    __tablename__ = 'fare_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Economy, Business, First, Premium Economy
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
    code = db.Column(db.String(5), nullable=False)  # Y, B, M, etc.
    fare_class_id = db.Column(db.Integer, db.ForeignKey('fare_classes.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    # Relationship
    fare_class = db.relationship('FareClass', backref=db.backref('booking_classes', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'fare_class_id': self.fare_class_id,
            'description': self.description,
            'fare_class': self.fare_class.to_dict() if self.fare_class else None
        }

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) using the Haversine formula.
    Returns distance in miles.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in miles
    r = 3959
    
    return c * r

def calculate_miles_earned(distance, earning_rate, elite_status='none', ticket_price=None, is_partner=False):
    """
    Calculate miles earned based on distance, earning rate, and elite status.
    Supports both distance-based and revenue-based earning models with industry-standard improvements.
    
    Args:
        distance (float): Flight distance in miles
        earning_rate (EarningRate): EarningRate object with earning percentage and bonuses
        elite_status (str): 'none', 'silver', 'gold', 'platinum'
        ticket_price (float, optional): Ticket price for revenue-based calculations
        is_partner (bool): Whether this is a partner airline flight (affects earning rates)
    
    Returns:
        dict: Contains detailed breakdown of miles calculation
    """
    loyalty_program = earning_rate.loyalty_program
    
    # Determine base miles calculation method
    if loyalty_program.earning_model == 'revenue' and ticket_price:
        # Revenue-based earning: miles per dollar spent
        base_miles = ticket_price * loyalty_program.base_earning_rate * earning_rate.earning_percentage
    else:
        # Distance-based earning: miles per mile flown
        base_miles = distance * earning_rate.earning_percentage
    
    # Apply partner airline reduction if applicable
    if is_partner:
        partner_multiplier = 0.75  # 25% reduction for partner flights
        base_miles *= partner_multiplier
    
    # Apply minimum miles rule (industry standard: 500 miles minimum per segment)
    minimum_miles = earning_rate.minimum_miles or 500
    minimum_applied = False
    if base_miles < minimum_miles:
        base_miles = minimum_miles
        minimum_applied = True
    
    # Apply maximum miles rule if specified (rare, but some airlines have caps)
    maximum_applied = False
    if earning_rate.maximum_miles and base_miles > earning_rate.maximum_miles:
        base_miles = earning_rate.maximum_miles
        maximum_applied = True
    
    # Calculate elite bonus miles (FIXED: proper percentage calculation)
    elite_bonus_miles = 0
    elite_bonus_rate = 0
    
    if elite_status == 'silver':
        elite_bonus_rate = earning_rate.elite_bonus_silver or loyalty_program.silver_bonus
    elif elite_status == 'gold':
        elite_bonus_rate = earning_rate.elite_bonus_gold or loyalty_program.gold_bonus
    elif elite_status == 'platinum':
        elite_bonus_rate = earning_rate.elite_bonus_platinum or loyalty_program.platinum_bonus
    
    # FIXED: Elite bonus should be additional miles, not a multiplier
    if elite_bonus_rate > 0:
        elite_bonus_miles = base_miles * elite_bonus_rate
    
    # Calculate total miles
    total_miles = base_miles + elite_bonus_miles
    
    # Calculate elite qualifying miles (EQMs)
    # For distance-based: usually same as base miles
    # For revenue-based: usually actual distance flown
    if loyalty_program.earning_model == 'revenue':
        elite_qualifying_miles = distance  # Actual distance for EQM
    else:
        elite_qualifying_miles = base_miles  # Same as redeemable miles
    
    # Apply minimum EQM rule
    if elite_qualifying_miles < minimum_miles:
        elite_qualifying_miles = minimum_miles
    
    return {
        'base_miles': round(base_miles, 2),
        'elite_bonus_miles': round(elite_bonus_miles, 2),
        'total_miles': round(total_miles, 2),
        'elite_qualifying_miles': round(elite_qualifying_miles, 2),
        'elite_bonus_rate': round(elite_bonus_rate * 100, 1),  # Convert to percentage for display
        'earning_model': loyalty_program.earning_model,
        'minimum_miles_applied': minimum_applied,
        'maximum_miles_applied': maximum_applied,
        'partner_reduction_applied': is_partner,
        'calculation_details': {
            'distance_miles': round(distance, 2),
            'earning_percentage': round(earning_rate.earning_percentage * 100, 1),
            'base_earning_rate': loyalty_program.base_earning_rate,
            'ticket_price': ticket_price,
            'minimum_miles_threshold': minimum_miles,
            'maximum_miles_threshold': earning_rate.maximum_miles,
            'partner_multiplier': 0.75 if is_partner else 1.0,
            'elite_status': elite_status,
            'loyalty_program': loyalty_program.name
        }
    }

# Test function to validate calculations
def test_calculation():
    """Test the calculation with known examples"""
    
    # Create mock objects for testing
    class MockLoyaltyProgram:
        def __init__(self):
            self.earning_model = 'distance'
            self.base_earning_rate = 1.0
            self.silver_bonus = 0.25  # 25% bonus
            self.gold_bonus = 0.50    # 50% bonus
            self.platinum_bonus = 1.00 # 100% bonus
            self.name = "Test Program"
    
    class MockEarningRate:
        def __init__(self):
            self.earning_percentage = 1.0  # 100% of distance
            self.minimum_miles = 500
            self.maximum_miles = None
            self.elite_bonus_silver = None
            self.elite_bonus_gold = None
            self.elite_bonus_platinum = None
            self.loyalty_program = MockLoyaltyProgram()
    
    # Test 1: Short flight with minimum miles
    print("Test 1: Short flight (200 miles) with minimum miles rule")
    result = calculate_miles_earned(200, MockEarningRate(), 'none')
    print(f"Base miles: {result['base_miles']} (should be 500 due to minimum)")
    print(f"Total miles: {result['total_miles']}")
    print(f"Minimum applied: {result['minimum_miles_applied']}")
    print()
    
    # Test 2: Long flight with elite status
    print("Test 2: Long flight (3000 miles) with Gold status")
    result = calculate_miles_earned(3000, MockEarningRate(), 'gold')
    print(f"Base miles: {result['base_miles']} (should be 3000)")
    print(f"Elite bonus miles: {result['elite_bonus_miles']} (should be 1500 - 50% of base)")
    print(f"Total miles: {result['total_miles']} (should be 4500)")
    print(f"Elite bonus rate: {result['elite_bonus_rate']}%")
    print()
    
    # Test 3: Partner airline reduction
    print("Test 3: Partner airline flight (1000 miles)")
    result = calculate_miles_earned(1000, MockEarningRate(), 'none', is_partner=True)
    print(f"Base miles: {result['base_miles']} (should be 750 - 25% reduction)")
    print(f"Partner reduction applied: {result['partner_reduction_applied']}")
    print()

if __name__ == "__main__":
    test_calculation()
