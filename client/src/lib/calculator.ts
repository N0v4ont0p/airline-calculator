/**
 * Airline Miles Calculator - Core Calculation Engine
 * Implements Haversine formula and miles earning calculations
 */

export interface Airport {
  iata: string;
  icao: string;
  name: string;
  city: string;
  country: string;
  lat: number;
  lon: number;
  timezone: string;
  region: string;
}

export interface Airline {
  iata: string;
  icao: string;
  name: string;
  country: string;
  alliance: string;
}

export interface LoyaltyProgram {
  id: string;
  name: string;
  airline: string;
  alliance: string;
  currency: string;
  website: string;
  centsPerMile: number;
  minimumMiles: number;
  isRevenueBased: boolean;
  revenueMultiplier?: {
    none: number;
    silver: number;
    gold: number;
    platinum: number;
    top: number;
  };
  bookingClasses: Record<string, number>;
  eliteBonuses: {
    none: number;
    silver: number;
    gold: number;
    platinum: number;
    top: number;
  };
}

export interface FlightInput {
  origin: Airport;
  destination: Airport;
  bookingClass: string;
  eliteStatus: 'none' | 'silver' | 'gold' | 'platinum' | 'top';
  ticketPrice?: number;
}

export interface CalculationResult {
  program: LoyaltyProgram;
  milesEarned: number;
  eliteQualifyingMiles: number;
  estimatedValue: number;
  earningRate: number;
  breakdown: {
    baseDistance: number;
    fareClassMultiplier: number;
    distanceWithClass: number;
    eliteBonus: number;
    totalMiles: number;
  };
}

/**
 * Calculate great-circle distance between two airports using Haversine formula
 * Returns distance in nautical miles
 */
export function calculateDistance(origin: Airport, destination: Airport): number {
  const R = 3440.065; // Earth's radius in nautical miles
  
  const lat1 = toRadians(origin.lat);
  const lat2 = toRadians(destination.lat);
  const deltaLat = toRadians(destination.lat - origin.lat);
  const deltaLon = toRadians(destination.lon - origin.lon);
  
  const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
            Math.cos(lat1) * Math.cos(lat2) *
            Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  
  const distance = R * c;
  
  return Math.round(distance);
}

/**
 * Convert degrees to radians
 */
function toRadians(degrees: number): number {
  return degrees * (Math.PI / 180);
}

/**
 * Calculate miles earned for a specific loyalty program
 */
export function calculateMiles(
  flight: FlightInput,
  program: LoyaltyProgram
): CalculationResult {
  const baseDistance = calculateDistance(flight.origin, flight.destination);
  
  // For revenue-based programs
  if (program.isRevenueBased && flight.ticketPrice && program.revenueMultiplier) {
    const multiplier = program.revenueMultiplier[flight.eliteStatus];
    let milesEarned = flight.ticketPrice * multiplier;
    
    // Apply minimum miles guarantee
    if (milesEarned < program.minimumMiles) {
      milesEarned = program.minimumMiles;
    }
    
    milesEarned = Math.round(milesEarned);
    
    return {
      program,
      milesEarned,
      eliteQualifyingMiles: milesEarned,
      estimatedValue: milesEarned * (program.centsPerMile / 100),
      earningRate: multiplier,
      breakdown: {
        baseDistance,
        fareClassMultiplier: multiplier,
        distanceWithClass: flight.ticketPrice,
        eliteBonus: 0,
        totalMiles: milesEarned
      }
    };
  }
  
  // For distance-based programs
  let distance = baseDistance;
  
  // Apply minimum miles guarantee
  if (distance < program.minimumMiles) {
    distance = program.minimumMiles;
  }
  
  // Get fare class multiplier
  const fareClassMultiplier = program.bookingClasses[flight.bookingClass] || 1.0;
  const distanceWithClass = distance * fareClassMultiplier;
  
  // Apply elite status bonus
  const eliteBonusPercentage = program.eliteBonuses[flight.eliteStatus];
  const eliteBonus = distanceWithClass * eliteBonusPercentage;
  
  const totalMiles = Math.round(distanceWithClass + eliteBonus);
  
  // Elite qualifying miles (usually same as total for distance-based)
  const eliteQualifyingMiles = totalMiles;
  
  const estimatedValue = totalMiles * (program.centsPerMile / 100);
  
  return {
    program,
    milesEarned: totalMiles,
    eliteQualifyingMiles,
    estimatedValue,
    earningRate: fareClassMultiplier,
    breakdown: {
      baseDistance,
      fareClassMultiplier,
      distanceWithClass,
      eliteBonus,
      totalMiles
    }
  };
}

/**
 * Calculate miles for multiple programs and sort by estimated value
 */
export function comparePrograms(
  flight: FlightInput,
  programs: LoyaltyProgram[]
): CalculationResult[] {
  const results = programs.map(program => calculateMiles(flight, program));
  
  // Sort by estimated value (descending), then by miles earned
  results.sort((a, b) => {
    if (b.estimatedValue !== a.estimatedValue) {
      return b.estimatedValue - a.estimatedValue;
    }
    return b.milesEarned - a.milesEarned;
  });
  
  return results;
}

/**
 * Get booking class cabin type
 */
export function getBookingClassCabin(bookingClass: string): string {
  const firstClass = ['F', 'A', 'P'];
  const business = ['J', 'C', 'D', 'I', 'Z', 'R'];
  const premiumEconomy = ['W', 'E'];
  
  if (firstClass.includes(bookingClass)) return 'First Class';
  if (business.includes(bookingClass)) return 'Business Class';
  if (premiumEconomy.includes(bookingClass)) return 'Premium Economy';
  return 'Economy';
}

/**
 * Get all booking classes for a cabin type
 */
export function getBookingClassesForCabin(cabin: string): string[] {
  const bookingClasses: Record<string, string[]> = {
    'First': ['F', 'A', 'P'],
    'Business': ['J', 'C', 'D', 'I', 'Z', 'R'],
    'Premium Economy': ['W', 'E'],
    'Economy': ['Y', 'B', 'M', 'H', 'Q', 'V', 'K', 'L', 'S', 'T', 'N', 'O', 'G', 'U', 'X']
  };
  
  return bookingClasses[cabin] || [];
}

/**
 * Format miles with thousands separator
 */
export function formatMiles(miles: number): string {
  return miles.toLocaleString('en-US');
}

/**
 * Format currency value
 */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
}

/**
 * Format percentage
 */
export function formatPercentage(value: number): string {
  return `${Math.round(value * 100)}%`;
}

/**
 * Search airports by IATA code, name, or city
 */
export function searchAirports(airports: Airport[], query: string): Airport[] {
  const searchTerm = query.toLowerCase().trim();
  
  if (!searchTerm) return [];
  
  return airports
    .filter(airport => 
      airport.iata.toLowerCase().includes(searchTerm) ||
      airport.name.toLowerCase().includes(searchTerm) ||
      airport.city.toLowerCase().includes(searchTerm) ||
      airport.country.toLowerCase().includes(searchTerm)
    )
    .slice(0, 10); // Limit to 10 results
}

/**
 * Search airlines by IATA code or name
 */
export function searchAirlines(airlines: Airline[], query: string): Airline[] {
  const searchTerm = query.toLowerCase().trim();
  
  if (!searchTerm) return [];
  
  return airlines
    .filter(airline => 
      airline.iata.toLowerCase().includes(searchTerm) ||
      airline.name.toLowerCase().includes(searchTerm)
    )
    .slice(0, 10);
}

/**
 * Get programs by alliance
 */
export function getProgramsByAlliance(
  programs: LoyaltyProgram[],
  alliance: string
): LoyaltyProgram[] {
  if (alliance === 'All') return programs;
  return programs.filter(p => p.alliance === alliance);
}

/**
 * Get top programs (by cents per mile value)
 */
export function getTopPrograms(programs: LoyaltyProgram[], count: number = 10): LoyaltyProgram[] {
  return [...programs]
    .sort((a, b) => b.centsPerMile - a.centsPerMile)
    .slice(0, count);
}
