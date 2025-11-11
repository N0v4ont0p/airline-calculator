import { useState, useEffect } from 'react';
import { Plane, Search, Calculator as CalcIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { Airport, Airline, LoyaltyProgram, FlightInput, CalculationResult } from '@/lib/calculator';
import { searchAirports, calculateDistance, comparePrograms, getBookingClassesForCabin, getProgramsByAlliance, getTopPrograms } from '@/lib/calculator';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { AirportSearch } from '@/components/AirportSearch';

export default function Calculator() {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [airlines, setAirlines] = useState<Airline[]>([]);
  const [programs, setPrograms] = useState<LoyaltyProgram[]>([]);
  
  const [origin, setOrigin] = useState<Airport | null>(null);
  const [destination, setDestination] = useState<Airport | null>(null);
  const [cabin, setCabin] = useState<string>('Economy');
  const [bookingClass, setBookingClass] = useState<string>('Y');
  const [eliteStatus, setEliteStatus] = useState<'none' | 'silver' | 'gold' | 'platinum' | 'top'>('none');
  const [ticketPrice, setTicketPrice] = useState<string>('');
  const [selectedPrograms, setSelectedPrograms] = useState<string[]>([]);
  const [programFilter, setProgramFilter] = useState<string>('Top 10');
  
  const [results, setResults] = useState<CalculationResult[] | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [distance, setDistance] = useState<number>(0);

  // Load data
  useEffect(() => {
    Promise.all([
      fetch('/airports.json').then(r => r.json()),
      fetch('/airlines.json').then(r => r.json()),
      fetch('/programs.json').then(r => r.json())
    ]).then(([airportsData, airlinesData, programsData]) => {
      setAirports(airportsData);
      setAirlines(airlinesData);
      setPrograms(programsData);
      
      // Default to top 10 programs
      const top10 = getTopPrograms(programsData, 10);
      setSelectedPrograms(top10.map(p => p.id));
    });
  }, []);

  // Calculate distance when origin and destination change
  useEffect(() => {
    if (origin && destination) {
      const dist = calculateDistance(origin, destination);
      setDistance(dist);
    } else {
      setDistance(0);
    }
  }, [origin, destination]);

  // Update booking class when cabin changes
  useEffect(() => {
    const classes = getBookingClassesForCabin(cabin);
    if (classes.length > 0) {
      setBookingClass(classes[0]);
    }
  }, [cabin]);

  const handleProgramFilterChange = (filter: string) => {
    setProgramFilter(filter);
    
    if (filter === 'All Star Alliance') {
      const starPrograms = getProgramsByAlliance(programs, 'Star Alliance');
      setSelectedPrograms(starPrograms.map(p => p.id));
    } else if (filter === 'All SkyTeam') {
      const skyteamPrograms = getProgramsByAlliance(programs, 'SkyTeam');
      setSelectedPrograms(skyteamPrograms.map(p => p.id));
    } else if (filter === 'All Oneworld') {
      const oneworldPrograms = getProgramsByAlliance(programs, 'Oneworld');
      setSelectedPrograms(oneworldPrograms.map(p => p.id));
    } else if (filter === 'Top 10') {
      const top10 = getTopPrograms(programs, 10);
      setSelectedPrograms(top10.map(p => p.id));
    } else if (filter === 'Custom') {
      // Keep current selection
    }
  };

  const toggleProgram = (programId: string) => {
    setSelectedPrograms(prev => 
      prev.includes(programId) 
        ? prev.filter(id => id !== programId)
        : [...prev, programId]
    );
    setProgramFilter('Custom');
  };

  const handleCalculate = () => {
    if (!origin || !destination || selectedPrograms.length === 0) {
      return;
    }

    setIsCalculating(true);

    // Simulate calculation delay for animation
    setTimeout(() => {
      const flight: FlightInput = {
        origin,
        destination,
        bookingClass,
        eliteStatus,
        ticketPrice: ticketPrice ? parseFloat(ticketPrice) : undefined
      };

      const selectedProgramsData = programs.filter(p => selectedPrograms.includes(p.id));
      const calculationResults = comparePrograms(flight, selectedProgramsData);
      
      setResults(calculationResults);
      setIsCalculating(false);
    }, 1500);
  };

  const handleReset = () => {
    setOrigin(null);
    setDestination(null);
    setCabin('Economy');
    setBookingClass('Y');
    setEliteStatus('none');
    setTicketPrice('');
    setResults(null);
    setDistance(0);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border sticky top-0 z-50 glass">
        <div className="container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Plane className="w-8 h-8 text-primary" />
              <h1 className="text-2xl font-bold neon-text">SkyMiles Calculator</h1>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <a href="#calculator" className="text-sm hover:text-primary transition-colors">Calculator</a>
              <a href="#programs" className="text-sm hover:text-primary transition-colors">Programs</a>
              <a href="#guide" className="text-sm hover:text-primary transition-colors">Guide</a>
              <a href="#about" className="text-sm hover:text-primary transition-colors">About</a>
            </nav>
            <Button className="neon-glow">Get Started</Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Hero Section */}
          <div className="text-center space-y-4 animate-fade-slide-up">
            <h2 className="text-5xl md:text-6xl font-bold neon-text">
              Calculate Your Miles
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Compare 50+ airline loyalty programs instantly. Find the best value for your flights.
            </p>
          </div>

          {/* Calculator Form */}
          <Card className="glass neon-glow">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CalcIcon className="w-6 h-6 text-primary" />
                Flight Calculator
              </CardTitle>
              <CardDescription>
                Enter your flight details to compare miles earned across programs
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Route Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Route Details</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="origin">Origin Airport</Label>
                    <AirportSearch
                      airports={airports}
                      value={origin}
                      onChange={setOrigin}
                      placeholder="Search airport (e.g., JFK, LAX)"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="destination">Destination Airport</Label>
                    <AirportSearch
                      airports={airports}
                      value={destination}
                      onChange={setDestination}
                      placeholder="Search airport (e.g., LHR, NRT)"
                    />
                  </div>
                </div>
                
                {distance > 0 && (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Plane className="w-4 h-4" />
                    <span>Distance: {distance.toLocaleString()} nautical miles</span>
                  </div>
                )}
              </div>

              {/* Flight Details */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Flight Details</h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="cabin">Cabin Class</Label>
                    <Select value={cabin} onValueChange={setCabin}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="First">First Class</SelectItem>
                        <SelectItem value="Business">Business Class</SelectItem>
                        <SelectItem value="Premium Economy">Premium Economy</SelectItem>
                        <SelectItem value="Economy">Economy</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="bookingClass">Booking Class (Fare Code)</Label>
                    <Select value={bookingClass} onValueChange={setBookingClass}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {getBookingClassesForCabin(cabin).map(bc => (
                          <SelectItem key={bc} value={bc}>{bc}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="ticketPrice">Ticket Price (Optional)</Label>
                    <Input
                      id="ticketPrice"
                      type="number"
                      placeholder="$850.00"
                      value={ticketPrice}
                      onChange={(e) => setTicketPrice(e.target.value)}
                    />
                  </div>
                </div>
              </div>

              {/* Elite Status */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Elite Status & Bonuses</h3>
                <div className="space-y-2">
                  <Label htmlFor="eliteStatus">Elite Status</Label>
                  <Select value={eliteStatus} onValueChange={(v: any) => setEliteStatus(v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None / General Member</SelectItem>
                      <SelectItem value="silver">Silver / Low Tier</SelectItem>
                      <SelectItem value="gold">Gold / Mid Tier</SelectItem>
                      <SelectItem value="platinum">Platinum / High Tier</SelectItem>
                      <SelectItem value="top">Top Tier / Million Miler</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Program Selection */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Loyalty Programs to Compare</h3>
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant={programFilter === 'Top 10' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleProgramFilterChange('Top 10')}
                  >
                    Top 10 Programs
                  </Button>
                  <Button
                    variant={programFilter === 'All Star Alliance' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleProgramFilterChange('All Star Alliance')}
                  >
                    All Star Alliance
                  </Button>
                  <Button
                    variant={programFilter === 'All SkyTeam' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleProgramFilterChange('All SkyTeam')}
                  >
                    All SkyTeam
                  </Button>
                  <Button
                    variant={programFilter === 'All Oneworld' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleProgramFilterChange('All Oneworld')}
                  >
                    All Oneworld
                  </Button>
                  <Button
                    variant={programFilter === 'Custom' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleProgramFilterChange('Custom')}
                  >
                    Custom Selection
                  </Button>
                </div>

                <div className="max-h-64 overflow-y-auto space-y-2 p-4 border border-border rounded-lg">
                  {programs.map(program => (
                    <div key={program.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={program.id}
                        checked={selectedPrograms.includes(program.id)}
                        onCheckedChange={() => toggleProgram(program.id)}
                      />
                      <label
                        htmlFor={program.id}
                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                      >
                        {program.name} ({program.alliance})
                      </label>
                    </div>
                  ))}
                </div>

                <p className="text-sm text-muted-foreground">
                  {selectedPrograms.length} program{selectedPrograms.length !== 1 ? 's' : ''} selected
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                <Button
                  className="flex-1 neon-glow"
                  size="lg"
                  onClick={handleCalculate}
                  disabled={!origin || !destination || selectedPrograms.length === 0 || isCalculating}
                >
                  {isCalculating ? (
                    <>
                      <Plane className="w-5 h-5 mr-2 animate-plane-fly" />
                      Calculating...
                    </>
                  ) : (
                    <>
                      <CalcIcon className="w-5 h-5 mr-2" />
                      Calculate Miles
                    </>
                  )}
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  onClick={handleReset}
                >
                  Reset Form
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results */}
          {results && (
            <ResultsDisplay
              results={results}
              origin={origin!}
              destination={destination!}
              bookingClass={bookingClass}
              eliteStatus={eliteStatus}
              distance={distance}
            />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-20">
        <div className="container py-8">
          <div className="text-center text-sm text-muted-foreground">
            <p>© 2025 SkyMiles Calculator. All rights reserved.</p>
            <p className="mt-2">
              Data is for informational purposes only. Always verify with official airline programs.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
