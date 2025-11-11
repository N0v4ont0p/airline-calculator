#!/usr/bin/env python3
"""
Process OpenFlights data into JSON format for the airline miles calculator
"""
import json
import csv

def process_airports():
    """Process airports.dat into structured JSON"""
    airports = []
    
    # OpenFlights airport fields:
    # 0: Airport ID, 1: Name, 2: City, 3: Country, 4: IATA, 5: ICAO, 
    # 6: Latitude, 7: Longitude, 8: Altitude, 9: Timezone, 10: DST, 11: Tz database
    
    with open('airports.dat', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            # Clean quotes from fields
            parts = [p.strip('"') for p in parts]
            
            # Only include airports with valid IATA codes
            if len(parts) >= 12 and parts[4] and parts[4] != '\\N' and len(parts[4]) == 3:
                try:
                    airport = {
                        'iata': parts[4],
                        'icao': parts[5] if parts[5] != '\\N' else '',
                        'name': parts[1],
                        'city': parts[2],
                        'country': parts[3],
                        'lat': float(parts[6]),
                        'lon': float(parts[7]),
                        'timezone': parts[9] if parts[9] != '\\N' else '0',
                        'region': get_region(parts[3])
                    }
                    airports.append(airport)
                except (ValueError, IndexError):
                    continue
    
    # Sort by IATA code for faster searching
    airports.sort(key=lambda x: x['iata'])
    
    print(f"Processed {len(airports)} airports")
    return airports

def get_region(country):
    """Determine region based on country"""
    # Simplified region mapping
    north_america = ['United States', 'Canada', 'Mexico']
    europe = ['United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Netherlands', 
              'Belgium', 'Switzerland', 'Austria', 'Sweden', 'Norway', 'Denmark', 
              'Finland', 'Ireland', 'Portugal', 'Greece', 'Poland', 'Czech Republic']
    asia = ['China', 'Japan', 'South Korea', 'India', 'Thailand', 'Singapore', 
            'Malaysia', 'Indonesia', 'Philippines', 'Vietnam', 'Taiwan', 'Hong Kong']
    middle_east = ['United Arab Emirates', 'Qatar', 'Saudi Arabia', 'Israel', 'Turkey']
    oceania = ['Australia', 'New Zealand']
    south_america = ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru']
    africa = ['South Africa', 'Egypt', 'Kenya', 'Morocco', 'Nigeria']
    
    if country in north_america:
        return 'North America'
    elif country in europe:
        return 'Europe'
    elif country in asia:
        return 'Asia'
    elif country in middle_east:
        return 'Middle East'
    elif country in oceania:
        return 'Oceania'
    elif country in south_america:
        return 'South America'
    elif country in africa:
        return 'Africa'
    else:
        return 'Other'

def process_airlines():
    """Process airlines.dat into structured JSON"""
    airlines = []
    
    # OpenFlights airline fields:
    # 0: Airline ID, 1: Name, 2: Alias, 3: IATA, 4: ICAO, 5: Callsign, 6: Country, 7: Active
    
    with open('airlines.dat', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            # Clean quotes
            parts = [p.strip('"') for p in parts]
            
            # Only include active airlines with IATA codes
            if len(parts) >= 8 and parts[3] and parts[3] != '\\N' and parts[7] == 'Y':
                airline = {
                    'iata': parts[3],
                    'icao': parts[4] if parts[4] != '\\N' else '',
                    'name': parts[1],
                    'country': parts[6],
                    'alliance': get_alliance(parts[1])
                }
                airlines.append(airline)
    
    # Sort by name
    airlines.sort(key=lambda x: x['name'])
    
    print(f"Processed {len(airlines)} airlines")
    return airlines

def get_alliance(airline_name):
    """Determine alliance membership"""
    star_alliance = ['United', 'Lufthansa', 'Air Canada', 'ANA', 'Singapore Airlines', 
                     'Thai Airways', 'Turkish Airlines', 'Swiss', 'Austrian', 'SAS',
                     'LOT Polish', 'TAP Portugal', 'Avianca', 'Copa Airlines', 'Air China',
                     'Shenzhen Airlines', 'Air India', 'Asiana', 'EVA Air']
    
    skyteam = ['Delta', 'Air France', 'KLM', 'Korean Air', 'China Eastern', 'China Southern',
               'Aeromexico', 'Aeroflot', 'Alitalia', 'Czech Airlines', 'Kenya Airways',
               'Middle East Airlines', 'Saudia', 'TAROM', 'Vietnam Airlines', 'Xiamen Airlines']
    
    oneworld = ['American Airlines', 'British Airways', 'Cathay Pacific', 'Qantas', 'Japan Airlines',
                'Iberia', 'Finnair', 'Qatar Airways', 'Royal Jordanian', 'S7 Airlines',
                'SriLankan Airlines', 'Malaysia Airlines', 'Royal Air Maroc']
    
    for alliance_member in star_alliance:
        if alliance_member.lower() in airline_name.lower():
            return 'Star Alliance'
    
    for alliance_member in skyteam:
        if alliance_member.lower() in airline_name.lower():
            return 'SkyTeam'
    
    for alliance_member in oneworld:
        if alliance_member.lower() in airline_name.lower():
            return 'Oneworld'
    
    return 'None'

def main():
    print("Processing OpenFlights data...")
    
    # Process airports
    airports = process_airports()
    with open('airports.json', 'w', encoding='utf-8') as f:
        json.dump(airports, f, indent=2, ensure_ascii=False)
    
    # Process airlines
    airlines = process_airlines()
    with open('airlines.json', 'w', encoding='utf-8') as f:
        json.dump(airlines, f, indent=2, ensure_ascii=False)
    
    print("\nData processing complete!")
    print(f"- airports.json: {len(airports)} airports")
    print(f"- airlines.json: {len(airlines)} airlines")

if __name__ == '__main__':
    main()
