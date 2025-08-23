from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Airline(db.Model):
    __tablename__ = 'airlines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)  # IATA code
    alliance = db.Column(db.String(20), nullable=False)  # SkyTeam, Oneworld, Star Alliance
    loyalty_program = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'alliance': self.alliance,
            'loyalty_program': self.loyalty_program
        }

class Airport(db.Model):
    __tablename__ = 'airports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(3), nullable=False, unique=True)  # IATA code
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

class LoyaltyProgram(db.Model):
    __tablename__ = 'loyalty_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    alliance = db.Column(db.String(20), nullable=False)
    base_earning_rate = db.Column(db.Float, nullable=False)  # Base miles per dollar/euro
    
    # Relationship
    airline = db.relationship('Airline', backref=db.backref('programs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'airline_id': self.airline_id,
            'alliance': self.alliance,
            'base_earning_rate': self.base_earning_rate,
            'airline': self.airline.to_dict() if self.airline else None
        }

class EarningRate(db.Model):
    __tablename__ = 'earning_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    loyalty_program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    fare_class = db.Column(db.String(10), nullable=False)  # Economy, Business, First
    booking_class = db.Column(db.String(5), nullable=False)  # Y, B, M, etc.
    earning_percentage = db.Column(db.Float, nullable=False)  # Percentage of distance or base rate
    elite_bonus = db.Column(db.Float, default=0.0)  # Additional bonus for elite members
    
    # Relationship
    loyalty_program = db.relationship('LoyaltyProgram', backref=db.backref('earning_rates', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'loyalty_program_id': self.loyalty_program_id,
            'fare_class': self.fare_class,
            'booking_class': self.booking_class,
            'earning_percentage': self.earning_percentage,
            'elite_bonus': self.elite_bonus
        }

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    origin_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    destination_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    distance_miles = db.Column(db.Float, nullable=False)
    
    # Relationships
    origin_airport = db.relationship('Airport', foreign_keys=[origin_airport_id], backref=db.backref('origin_routes', lazy=True))
    destination_airport = db.relationship('Airport', foreign_keys=[destination_airport_id], backref=db.backref('destination_routes', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'origin_airport_id': self.origin_airport_id,
            'destination_airport_id': self.destination_airport_id,
            'distance_miles': self.distance_miles,
            'origin_airport': self.origin_airport.to_dict() if self.origin_airport else None,
            'destination_airport': self.destination_airport.to_dict() if self.destination_airport else None
        }

