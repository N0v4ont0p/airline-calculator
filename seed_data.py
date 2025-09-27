#!/usr/bin/env python3
"""
Additional data seeder for comprehensive airport coverage
"""

import os
import sys
import csv
from main import app, db, Airport

def seed_comprehensive_airports():
    """Seed comprehensive airport data from the provided list"""
    
    # Airport data from the user's pasted content
    comprehensive_airports = [
        # Major US Airports
        {'name': 'Hartsfield-Jackson Atlanta International Airport', 'code': 'ATL', 'city': 'Atlanta', 'state': 'GA', 'country': 'United States', 'latitude': 33.6407, 'longitude': -84.4277},
        {'name': 'Dallas/Fort Worth International Airport', 'code': 'DFW', 'city': 'Dallas', 'state': 'TX', 'country': 'United States', 'latitude': 32.8998, 'longitude': -97.0403},
        {'name': 'Denver International Airport', 'code': 'DEN', 'city': 'Denver', 'state': 'CO', 'country': 'United States', 'latitude': 39.8561, 'longitude': -104.6737},
        {'name': 'McCarran International Airport', 'code': 'LAS', 'city': 'Las Vegas', 'state': 'NV', 'country': 'United States', 'latitude': 36.0840, 'longitude': -115.1537},
        {'name': 'Phoenix Sky Harbor International Airport', 'code': 'PHX', 'city': 'Phoenix', 'state': 'AZ', 'country': 'United States', 'latitude': 33.4342, 'longitude': -112.0116},
        {'name': 'George Bush Intercontinental Airport', 'code': 'IAH', 'city': 'Houston', 'state': 'TX', 'country': 'United States', 'latitude': 29.9902, 'longitude': -95.3368},
        {'name': 'Orlando International Airport', 'code': 'MCO', 'city': 'Orlando', 'state': 'FL', 'country': 'United States', 'latitude': 28.4312, 'longitude': -81.3081},
        {'name': 'Seattle-Tacoma International Airport', 'code': 'SEA', 'city': 'Seattle', 'state': 'WA', 'country': 'United States', 'latitude': 47.4502, 'longitude': -122.3088},
        {'name': 'Charlotte Douglas International Airport', 'code': 'CLT', 'city': 'Charlotte', 'state': 'NC', 'country': 'United States', 'latitude': 35.2144, 'longitude': -80.9473},
        {'name': 'Newark Liberty International Airport', 'code': 'EWR', 'city': 'Newark', 'state': 'NJ', 'country': 'United States', 'latitude': 40.6895, 'longitude': -74.1745},
        {'name': 'Logan International Airport', 'code': 'BOS', 'city': 'Boston', 'state': 'MA', 'country': 'United States', 'latitude': 42.3656, 'longitude': -71.0096},
        {'name': 'Fort Lauderdale-Hollywood International Airport', 'code': 'FLL', 'city': 'Fort Lauderdale', 'state': 'FL', 'country': 'United States', 'latitude': 26.0742, 'longitude': -80.1506},
        {'name': 'Honolulu International Airport', 'code': 'HNL', 'city': 'Honolulu', 'state': 'HI', 'country': 'United States', 'latitude': 21.3099, 'longitude': -157.8581},
        {'name': 'Washington Dulles International Airport', 'code': 'IAD', 'city': 'Washington', 'state': 'DC', 'country': 'United States', 'latitude': 38.9531, 'longitude': -77.4565},
        {'name': 'Minneapolis-Saint Paul International Airport', 'code': 'MSP', 'city': 'Minneapolis', 'state': 'MN', 'country': 'United States', 'latitude': 44.8848, 'longitude': -93.2223},
        {'name': 'Detroit Metropolitan Wayne County Airport', 'code': 'DTW', 'city': 'Detroit', 'state': 'MI', 'country': 'United States', 'latitude': 42.2162, 'longitude': -83.3554},
        {'name': 'Philadelphia International Airport', 'code': 'PHL', 'city': 'Philadelphia', 'state': 'PA', 'country': 'United States', 'latitude': 42.2162, 'longitude': -83.3554},
        {'name': 'LaGuardia Airport', 'code': 'LGA', 'city': 'New York', 'state': 'NY', 'country': 'United States', 'latitude': 40.7769, 'longitude': -73.8740},
        {'name': 'Baltimore-Washington International Airport', 'code': 'BWI', 'city': 'Baltimore', 'state': 'MD', 'country': 'United States', 'latitude': 39.1774, 'longitude': -76.6684},
        {'name': 'Salt Lake City International Airport', 'code': 'SLC', 'city': 'Salt Lake City', 'state': 'UT', 'country': 'United States', 'latitude': 40.7899, 'longitude': -111.9791},
        
        # Major International Airports
        {'name': 'Narita International Airport', 'code': 'NRT', 'city': 'Tokyo', 'state': None, 'country': 'Japan', 'latitude': 35.7720, 'longitude': 140.3929},
        {'name': 'Kansai International Airport', 'code': 'KIX', 'city': 'Osaka', 'state': None, 'country': 'Japan', 'latitude': 34.4347, 'longitude': 135.2441},
        {'name': 'Gatwick Airport', 'code': 'LGW', 'city': 'London', 'state': None, 'country': 'United Kingdom', 'latitude': 51.1537, 'longitude': -0.1821},
        {'name': 'Manchester Airport', 'code': 'MAN', 'city': 'Manchester', 'state': None, 'country': 'United Kingdom', 'latitude': 53.3537, 'longitude': -2.2750},
        {'name': 'Madrid-Barajas Airport', 'code': 'MAD', 'city': 'Madrid', 'state': None, 'country': 'Spain', 'latitude': 40.4719, 'longitude': -3.5626},
        {'name': 'Barcelona-El Prat Airport', 'code': 'BCN', 'city': 'Barcelona', 'state': None, 'country': 'Spain', 'latitude': 40.2971, 'longitude': 2.0833},
        {'name': 'Rome Fiumicino Airport', 'code': 'FCO', 'city': 'Rome', 'state': None, 'country': 'Italy', 'latitude': 41.8003, 'longitude': 12.2389},
        {'name': 'Milan Malpensa Airport', 'code': 'MXP', 'city': 'Milan', 'state': None, 'country': 'Italy', 'latitude': 45.6306, 'longitude': 8.7231},
        {'name': 'Vienna International Airport', 'code': 'VIE', 'city': 'Vienna', 'state': None, 'country': 'Austria', 'latitude': 48.1103, 'longitude': 16.5697},
        {'name': 'Brussels Airport', 'code': 'BRU', 'city': 'Brussels', 'state': None, 'country': 'Belgium', 'latitude': 50.9010, 'longitude': 4.4844},
        {'name': 'Copenhagen Airport', 'code': 'CPH', 'city': 'Copenhagen', 'state': None, 'country': 'Denmark', 'latitude': 55.6181, 'longitude': 12.6561},
        {'name': 'Stockholm Arlanda Airport', 'code': 'ARN', 'city': 'Stockholm', 'state': None, 'country': 'Sweden', 'latitude': 59.6519, 'longitude': 17.9186},
        {'name': 'Oslo Airport', 'code': 'OSL', 'city': 'Oslo', 'state': None, 'country': 'Norway', 'latitude': 60.1939, 'longitude': 11.1004},
        {'name': 'Helsinki-Vantaa Airport', 'code': 'HEL', 'city': 'Helsinki', 'state': None, 'country': 'Finland', 'latitude': 60.3172, 'longitude': 24.9633},
        {'name': 'Istanbul Airport', 'code': 'IST', 'city': 'Istanbul', 'state': None, 'country': 'Turkey', 'latitude': 41.2619, 'longitude': 28.7414},
        {'name': 'Doha Hamad International Airport', 'code': 'DOH', 'city': 'Doha', 'state': None, 'country': 'Qatar', 'latitude': 25.2731, 'longitude': 51.6080},
        {'name': 'Abu Dhabi International Airport', 'code': 'AUH', 'city': 'Abu Dhabi', 'state': None, 'country': 'UAE', 'latitude': 24.4330, 'longitude': 54.6511},
        {'name': 'Kuwait International Airport', 'code': 'KWI', 'city': 'Kuwait City', 'state': None, 'country': 'Kuwait', 'latitude': 29.2267, 'longitude': 47.9689},
        {'name': 'King Abdulaziz International Airport', 'code': 'JED', 'city': 'Jeddah', 'state': None, 'country': 'Saudi Arabia', 'latitude': 21.6796, 'longitude': 39.1565},
        {'name': 'King Khalid International Airport', 'code': 'RUH', 'city': 'Riyadh', 'state': None, 'country': 'Saudi Arabia', 'latitude': 24.9576, 'longitude': 46.6988},
        
        # Asia-Pacific
        {'name': 'Suvarnabhumi Airport', 'code': 'BKK', 'city': 'Bangkok', 'state': None, 'country': 'Thailand', 'latitude': 13.6900, 'longitude': 100.7501},
        {'name': 'Kuala Lumpur International Airport', 'code': 'KUL', 'city': 'Kuala Lumpur', 'state': None, 'country': 'Malaysia', 'latitude': 2.7456, 'longitude': 101.7072},
        {'name': 'Soekarno-Hatta International Airport', 'code': 'CGK', 'city': 'Jakarta', 'state': None, 'country': 'Indonesia', 'latitude': -6.1256, 'longitude': 106.6559},
        {'name': 'Ninoy Aquino International Airport', 'code': 'MNL', 'city': 'Manila', 'state': None, 'country': 'Philippines', 'latitude': 14.5086, 'longitude': 121.0194},
        {'name': 'Indira Gandhi International Airport', 'code': 'DEL', 'city': 'New Delhi', 'state': None, 'country': 'India', 'latitude': 28.5562, 'longitude': 77.1000},
        {'name': 'Chhatrapati Shivaji International Airport', 'code': 'BOM', 'city': 'Mumbai', 'state': None, 'country': 'India', 'latitude': 19.0896, 'longitude': 72.8656},
        {'name': 'Kempegowda International Airport', 'code': 'BLR', 'city': 'Bangalore', 'state': None, 'country': 'India', 'latitude': 13.1986, 'longitude': 77.7066},
        {'name': 'Chennai International Airport', 'code': 'MAA', 'city': 'Chennai', 'state': None, 'country': 'India', 'latitude': 12.9941, 'longitude': 80.1709},
        {'name': 'Rajiv Gandhi International Airport', 'code': 'HYD', 'city': 'Hyderabad', 'state': None, 'country': 'India', 'latitude': 17.2403, 'longitude': 78.4294},
        {'name': 'Netaji Subhas Chandra Bose International Airport', 'code': 'CCU', 'city': 'Kolkata', 'state': None, 'country': 'India', 'latitude': 22.6546, 'longitude': 88.4467},
        
        # Canada
        {'name': 'Vancouver International Airport', 'code': 'YVR', 'city': 'Vancouver', 'state': 'BC', 'country': 'Canada', 'latitude': 49.1967, 'longitude': -123.1815},
        {'name': 'Calgary International Airport', 'code': 'YYC', 'city': 'Calgary', 'state': 'AB', 'country': 'Canada', 'latitude': 51.1315, 'longitude': -114.0106},
        {'name': 'Edmonton International Airport', 'code': 'YEG', 'city': 'Edmonton', 'state': 'AB', 'country': 'Canada', 'latitude': 53.3097, 'longitude': -113.5801},
        {'name': 'Winnipeg James Armstrong Richardson International Airport', 'code': 'YWG', 'city': 'Winnipeg', 'state': 'MB', 'country': 'Canada', 'latitude': 49.9100, 'longitude': -97.2390},
        {'name': 'Ottawa Macdonald-Cartier International Airport', 'code': 'YOW', 'city': 'Ottawa', 'state': 'ON', 'country': 'Canada', 'latitude': 45.3225, 'longitude': -75.6692},
        {'name': 'Montreal-Pierre Elliott Trudeau International Airport', 'code': 'YUL', 'city': 'Montreal', 'state': 'QC', 'country': 'Canada', 'latitude': 45.4706, 'longitude': -73.7408},
        {'name': 'Halifax Stanfield International Airport', 'code': 'YHZ', 'city': 'Halifax', 'state': 'NS', 'country': 'Canada', 'latitude': 44.8808, 'longitude': -63.5086},
        
        # Australia & New Zealand
        {'name': 'Melbourne Airport', 'code': 'MEL', 'city': 'Melbourne', 'state': 'VIC', 'country': 'Australia', 'latitude': -37.6690, 'longitude': 144.8410},
        {'name': 'Brisbane Airport', 'code': 'BNE', 'city': 'Brisbane', 'state': 'QLD', 'country': 'Australia', 'latitude': -27.3942, 'longitude': 153.1218},
        {'name': 'Perth Airport', 'code': 'PER', 'city': 'Perth', 'state': 'WA', 'country': 'Australia', 'latitude': -31.9403, 'longitude': 115.9669},
        {'name': 'Adelaide Airport', 'code': 'ADL', 'city': 'Adelaide', 'state': 'SA', 'country': 'Australia', 'latitude': -34.9285, 'longitude': 138.5918},
        {'name': 'Auckland Airport', 'code': 'AKL', 'city': 'Auckland', 'state': None, 'country': 'New Zealand', 'latitude': -37.0082, 'longitude': 174.7850},
        {'name': 'Christchurch Airport', 'code': 'CHC', 'city': 'Christchurch', 'state': None, 'country': 'New Zealand', 'latitude': -43.4894, 'longitude': 172.5320},
        
        # South America
        {'name': 'São Paulo-Guarulhos International Airport', 'code': 'GRU', 'city': 'São Paulo', 'state': None, 'country': 'Brazil', 'latitude': -23.4356, 'longitude': -46.4731},
        {'name': 'Rio de Janeiro-Galeão International Airport', 'code': 'GIG', 'city': 'Rio de Janeiro', 'state': None, 'country': 'Brazil', 'latitude': -22.8099, 'longitude': -43.2505},
        {'name': 'Jorge Newbery Airfield', 'code': 'AEP', 'city': 'Buenos Aires', 'state': None, 'country': 'Argentina', 'latitude': -34.5592, 'longitude': -58.4156},
        {'name': 'Ezeiza International Airport', 'code': 'EZE', 'city': 'Buenos Aires', 'state': None, 'country': 'Argentina', 'latitude': -34.8222, 'longitude': -58.5358},
        {'name': 'El Dorado International Airport', 'code': 'BOG', 'city': 'Bogotá', 'state': None, 'country': 'Colombia', 'latitude': 4.7016, 'longitude': -74.1469},
        {'name': 'Jorge Chávez International Airport', 'code': 'LIM', 'city': 'Lima', 'state': None, 'country': 'Peru', 'latitude': -12.0219, 'longitude': -77.1143},
        {'name': 'Arturo Merino Benítez International Airport', 'code': 'SCL', 'city': 'Santiago', 'state': None, 'country': 'Chile', 'latitude': -33.3930, 'longitude': -70.7858},
        
        # Africa
        {'name': 'O.R. Tambo International Airport', 'code': 'JNB', 'city': 'Johannesburg', 'state': None, 'country': 'South Africa', 'latitude': -26.1392, 'longitude': 28.2460},
        {'name': 'Cape Town International Airport', 'code': 'CPT', 'city': 'Cape Town', 'state': None, 'country': 'South Africa', 'latitude': -33.9649, 'longitude': 18.6017},
        {'name': 'Cairo International Airport', 'code': 'CAI', 'city': 'Cairo', 'state': None, 'country': 'Egypt', 'latitude': 30.1219, 'longitude': 31.4056},
        {'name': 'Addis Ababa Bole International Airport', 'code': 'ADD', 'city': 'Addis Ababa', 'state': None, 'country': 'Ethiopia', 'latitude': 8.9806, 'longitude': 38.7992},
        {'name': 'Jomo Kenyatta International Airport', 'code': 'NBO', 'city': 'Nairobi', 'state': None, 'country': 'Kenya', 'latitude': -1.3192, 'longitude': 36.9278},
        {'name': 'Mohammed V International Airport', 'code': 'CMN', 'city': 'Casablanca', 'state': None, 'country': 'Morocco', 'latitude': 33.3675, 'longitude': -7.5898},
    ]
    
    count = 0
    for airport_data in comprehensive_airports:
        # Check if airport already exists
        existing = Airport.query.filter_by(code=airport_data['code']).first()
        if not existing:
            airport = Airport(**airport_data)
            db.session.add(airport)
            count += 1
    
    db.session.commit()
    print(f"Added {count} additional airports to the database")
    return count

if __name__ == "__main__":
    with app.app_context():
        seed_comprehensive_airports()
        print(f"Total airports in database: {Airport.query.count()}")
