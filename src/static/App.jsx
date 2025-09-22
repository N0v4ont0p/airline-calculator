import React, { useState, useEffect, useCallback } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { 
  Plane, 
  Calculator, 
  MapPin, 
  Award, 
  Search, 
  Star, 
  TrendingUp,
  Globe,
  Users,
  Zap,
  ArrowRight,
  Trophy,
  Target,
  Sparkles,
  Building2,
  CreditCard,
  Crown,
  ChevronDown,
  Loader2,
  CheckCircle,
  AlertCircle,
  Info
} from 'lucide-react'
import './App.css'

const API_BASE = '/api'

function App() {
  // State for data
  const [airports, setAirports] = useState([])
  const [airlines, setAirlines] = useState([])
  const [alliances, setAlliances] = useState([])
  const [fareClasses, setFareClasses] = useState([])
  const [bookingClasses, setBookingClasses] = useState([])
  const [eliteStatusTiers, setEliteStatusTiers] = useState({})
  
  // State for selections
  const [selectedOrigin, setSelectedOrigin] = useState(null)
  const [selectedDestination, setSelectedDestination] = useState(null)
  const [selectedAlliance, setSelectedAlliance] = useState('')
  const [selectedAirline, setSelectedAirline] = useState(null)
  const [selectedFareClass, setSelectedFareClass] = useState('Economy')
  const [selectedBookingClass, setSelectedBookingClass] = useState('Y')
  const [selectedEliteStatus, setSelectedEliteStatus] = useState('none')
  
  // State for search and UI
  const [originSearch, setOriginSearch] = useState('')
  const [destinationSearch, setDestinationSearch] = useState('')
  const [airlineSearch, setAirlineSearch] = useState('')
  const [filteredOriginAirports, setFilteredOriginAirports] = useState([])
  const [filteredDestinationAirports, setFilteredDestinationAirports] = useState([])
  const [filteredAirlines, setFilteredAirlines] = useState([])
  
  // State for results and loading
  const [comparisonResults, setComparisonResults] = useState(null)
  const [individualResult, setIndividualResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [stats, setStats] = useState(null)
  
  // State for dropdowns
  const [showOriginDropdown, setShowOriginDropdown] = useState(false)
  const [showDestinationDropdown, setShowDestinationDropdown] = useState(false)
  const [showAirlineDropdown, setShowAirlineDropdown] = useState(false)

  // Fetch initial data
  useEffect(() => {
    fetchAlliances()
    fetchFareClasses()
    fetchStats()
    fetchAirports()
    fetchBookingClasses("Economy")
  }, [])

  // Fetch airports with pagination
  const fetchAirports = async (search = '', limit = 1000) => {
    try {
      const response = await fetch(`${API_BASE}/airports?search=${encodeURIComponent(search)}&limit=${limit}`)
      const data = await response.json()
      setAirports(data.airports || [])
    } catch (error) {
      console.error('Error fetching airports:', error)
    }
  }

  // Fetch alliances
  const fetchAlliances = async () => {
    try {
      const response = await fetch(`${API_BASE}/alliances`)
      const data = await response.json()
      setAlliances(data)
    } catch (error) {
      console.error('Error fetching alliances:', error)
    }
  }

  // Fetch airlines based on alliance
  const fetchAirlines = async (alliance) => {
    try {
      const response = await fetch(`${API_BASE}/airlines?alliance=${encodeURIComponent(alliance)}`)
      const data = await response.json()
      setAirlines(data.airlines || [])
      setFilteredAirlines(data.airlines || [])
    } catch (error) {
      console.error('Error fetching airlines:', error)
    }
  }

  // Fetch fare classes
  const fetchFareClasses = async () => {
    try {
      const response = await fetch(`${API_BASE}/fare-classes`)
      const data = await response.json()
      setFareClasses(data)
    } catch (error) {
      console.error('Error fetching fare classes:', error)
    }
  }

  // Fetch booking classes based on fare class
  const fetchBookingClasses = async (fareClass) => {
    try {
      const response = await fetch(`${API_BASE}/booking-classes?fare_class_name=${encodeURIComponent(fareClass)}`)
      const data = await response.json()
      setBookingClasses(data)
    } catch (error) {
      console.error('Error fetching booking classes:', error)
    }
  }

  // Fetch elite status tiers for selected airline
  const fetchEliteStatusTiers = async (airlineCode) => {
    try {
      const response = await fetch(`${API_BASE}/elite-status-tiers?airline_code=${airlineCode}`)
      const data = await response.json()
      setEliteStatusTiers(data)
    } catch (error) {
      console.error('Error fetching elite status tiers:', error)
    }
  }

  // Fetch stats
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`)
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  // Handle alliance selection
  const handleAllianceChange = (alliance) => {
    setSelectedAlliance(alliance)
    setSelectedAirline(null)
    setAirlineSearch('')
    setEliteStatusTiers({})
    fetchAirlines(alliance)
  }

  // Handle airline selection
  const handleAirlineChange = (airline) => {
    setSelectedAirline(airline)
    setAirlineSearch('')
    setShowAirlineDropdown(false)
    fetchEliteStatusTiers(airline.code)
  }

  // Handle fare class change
  const handleFareClassChange = (fareClass) => {
    setSelectedFareClass(fareClass)
    setSelectedBookingClass('Y') // Reset to default
    fetchBookingClasses(fareClass)
  }

  // Filter airports for origin
  useEffect(() => {
    if (originSearch.length >= 1) {
      const filtered = airports.filter(airport =>
        airport.name.toLowerCase().includes(originSearch.toLowerCase()) ||
        airport.code.toLowerCase().includes(originSearch.toLowerCase()) ||
        airport.city.toLowerCase().includes(originSearch.toLowerCase()) ||
        airport.country.toLowerCase().includes(originSearch.toLowerCase())
      ).slice(0, 50)
      setFilteredOriginAirports(filtered)
    } else {
      // Show top 100 major airports by default for scrolling
      setFilteredOriginAirports(airports.slice(0, 100))
    }
  }, [originSearch, airports])

  // Filter airports for destination
  useEffect(() => {
    if (destinationSearch.length >= 1) {
      const filtered = airports.filter(airport =>
        airport.name.toLowerCase().includes(destinationSearch.toLowerCase()) ||
        airport.code.toLowerCase().includes(destinationSearch.toLowerCase()) ||
        airport.city.toLowerCase().includes(destinationSearch.toLowerCase()) ||
        airport.country.toLowerCase().includes(destinationSearch.toLowerCase())
      ).slice(0, 50)
      setFilteredDestinationAirports(filtered)
    } else {
      // Show top 100 major airports by default for scrolling
      setFilteredDestinationAirports(airports.slice(0, 100))
    }
  }, [destinationSearch, airports])

  // Filter airlines
  useEffect(() => {
    if (airlineSearch.length >= 1) {
      const filtered = airlines.filter(airline =>
        airline.name.toLowerCase().includes(airlineSearch.toLowerCase()) ||
        airline.code.toLowerCase().includes(airlineSearch.toLowerCase()) ||
        airline.loyalty_program.toLowerCase().includes(airlineSearch.toLowerCase())
      )
      setFilteredAirlines(filtered)
    } else {
      setFilteredAirlines(airlines)
    }
  }, [airlineSearch, airlines])

  // Compare miles across alliance
  const handleCompareAlliance = async () => {
    if (!selectedOrigin || !selectedDestination || !selectedAlliance) {
      setError('Please select origin, destination, and alliance')
      return
    }

    setLoading(true)
    setError('')
    
    try {
      const response = await fetch(`${API_BASE}/compare-miles`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          origin: selectedOrigin.code,
          destination: selectedDestination.code,
          alliance: selectedAlliance,
          fare_class: selectedFareClass,
          booking_class: selectedBookingClass,
          elite_status: selectedEliteStatus
        })
      })

      if (!response.ok) {
        throw new Error('Failed to compare miles')
      }

      const data = await response.json()
      setComparisonResults(data)
      setIndividualResult(null)
    } catch (error) {
      setError('Error comparing miles: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  // Calculate individual airline miles
  const handleCalculateIndividual = async () => {
    if (!selectedOrigin || !selectedDestination || !selectedAirline) {
      setError('Please select origin, destination, and airline')
      return
    }

    setLoading(true)
    setError('')
    
    try {
      const response = await fetch(`${API_BASE}/calculate-miles`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          origin: selectedOrigin.code,
          destination: selectedDestination.code,
          airline_code: selectedAirline.code,
          fare_class: selectedFareClass,
          booking_class: selectedBookingClass,
          elite_status: selectedEliteStatus
        })
      })

      if (!response.ok) {
        throw new Error('Failed to calculate miles')
      }

      const data = await response.json()
      setIndividualResult(data)
      setComparisonResults(null)
    } catch (error) {
      setError('Error calculating miles: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-white/20 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl">
                <Plane className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Airline Miles Calculator
                </h1>
                <p className="text-sm text-gray-600">The most comprehensive miles calculator</p>
              </div>
            </div>
            {stats && (
              <div className="hidden md:flex items-center space-x-6 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <Globe className="h-4 w-4" />
                  <span>{stats.airports.toLocaleString()} Airports</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Building2 className="h-4 w-4" />
                  <span>{stats.airlines} Airlines</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Users className="h-4 w-4" />
                  <span>{stats.loyalty_programs} Programs</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Selection Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Route Selection */}
          <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MapPin className="h-5 w-5 text-blue-600" />
                <span>Route Selection</span>
              </CardTitle>
              <CardDescription>Choose your origin and destination airports</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Origin Airport */}
              <div className="space-y-2">
                <Label htmlFor="origin">Origin Airport</Label>
                <div className="relative">
                  <div className="flex items-center space-x-2 p-3 border rounded-lg bg-white/50 cursor-pointer"
                       onClick={() => setShowOriginDropdown(!showOriginDropdown)}>
                    <Search className="h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Search origin airport..."
                      value={selectedOrigin ? `${selectedOrigin.code} - ${selectedOrigin.name}` : originSearch}
                      onChange={(e) => {
                        setOriginSearch(e.target.value)
                        setSelectedOrigin(null)
                        setShowOriginDropdown(true)
                      }}
                      className="border-0 bg-transparent p-0 focus:ring-0"
                    />
                    <ChevronDown className="h-4 w-4 text-gray-400" />
                  </div>
                  
                  {showOriginDropdown && (
                    <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg z-50 max-h-80 overflow-hidden">
                      <div className="p-2 bg-gray-50 border-b text-xs text-gray-600 flex items-center justify-between">
                        <span>
                          {filteredOriginAirports.length} airports 
                          {originSearch ? ` matching "${originSearch}"` : ' available'}
                        </span>
                        <span className="text-gray-400">Scroll to see more</span>
                      </div>
                      <ScrollArea className="h-72">
                        {filteredOriginAirports.map((airport) => (
                          <div
                            key={airport.id}
                            className="p-3 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 transition-colors"
                            onClick={() => {
                              setSelectedOrigin(airport)
                              setOriginSearch('')
                              setShowOriginDropdown(false)
                            }}
                          >
                            <div className="font-medium text-gray-900">{airport.code} - {airport.name}</div>
                            <div className="text-sm text-gray-500">{airport.city}, {airport.country}</div>
                          </div>
                        ))}
                        {filteredOriginAirports.length === 0 && (
                          <div className="p-4 text-center text-gray-500">
                            No airports found matching "{originSearch}"
                          </div>
                        )}
                      </ScrollArea>
                    </div>
                  )}
                </div>
              </div>

              {/* Destination Airport */}
              <div className="space-y-2">
                <Label htmlFor="destination">Destination Airport</Label>
                <div className="relative">
                  <div className="flex items-center space-x-2 p-3 border rounded-lg bg-white/50 cursor-pointer"
                       onClick={() => setShowDestinationDropdown(!showDestinationDropdown)}>
                    <Search className="h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Search destination airport..."
                      value={selectedDestination ? `${selectedDestination.code} - ${selectedDestination.name}` : destinationSearch}
                      onChange={(e) => {
                        setDestinationSearch(e.target.value)
                        setSelectedDestination(null)
                        setShowDestinationDropdown(true)
                      }}
                      className="border-0 bg-transparent p-0 focus:ring-0"
                    />
                    <ChevronDown className="h-4 w-4 text-gray-400" />
                  </div>
                  
                  {showDestinationDropdown && (
                    <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg z-50 max-h-80 overflow-hidden">
                      <div className="p-2 bg-gray-50 border-b text-xs text-gray-600 flex items-center justify-between">
                        <span>
                          {filteredDestinationAirports.length} airports 
                          {destinationSearch ? ` matching "${destinationSearch}"` : ' available'}
                        </span>
                        <span className="text-gray-400">Scroll to see more</span>
                      </div>
                      <ScrollArea className="h-72">
                        {filteredDestinationAirports.map((airport) => (
                          <div
                            key={airport.id}
                            className="p-3 hover:bg-blue-50 cursor-pointer border-b last:border-b-0 transition-colors"
                            onClick={() => {
                              setSelectedDestination(airport)
                              setDestinationSearch('')
                              setShowDestinationDropdown(false)
                            }}
                          >
                            <div className="font-medium text-gray-900">{airport.code} - {airport.name}</div>
                            <div className="text-sm text-gray-500">{airport.city}, {airport.country}</div>
                          </div>
                        ))}
                        {filteredDestinationAirports.length === 0 && (
                          <div className="p-4 text-center text-gray-500">
                            No airports found matching "{destinationSearch}"
                          </div>
                        )}
                      </ScrollArea>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Airline Selection */}
          <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Building2 className="h-5 w-5 text-indigo-600" />
                <span>Airline Selection</span>
              </CardTitle>
              <CardDescription>Choose alliance and specific airline</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Alliance Selection */}
              <div className="space-y-2">
                <Label>Alliance</Label>
                <Select value={selectedAlliance} onValueChange={handleAllianceChange}>
                  <SelectTrigger className="bg-white/50">
                    <SelectValue placeholder="Select alliance" />
                  </SelectTrigger>
                  <SelectContent>
                    {alliances.map((alliance) => (
                      <SelectItem key={alliance} value={alliance}>
                        <div className="flex items-center space-x-2">
                          <Users className="h-4 w-4" />
                          <span>{alliance}</span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Airline Selection */}
              {selectedAlliance && (
                <div className="space-y-2">
                  <Label>Airline</Label>
                  <div className="relative">
                    <div className="flex items-center space-x-2 p-3 border rounded-lg bg-white/50 cursor-pointer"
                         onClick={() => setShowAirlineDropdown(!showAirlineDropdown)}>
                      <Search className="h-4 w-4 text-gray-400" />
                      <Input
                        placeholder="Search airline..."
                        value={selectedAirline ? `${selectedAirline.code} - ${selectedAirline.name}` : airlineSearch}
                        onChange={(e) => {
                          setAirlineSearch(e.target.value)
                          setSelectedAirline(null)
                          setShowAirlineDropdown(true)
                        }}
                        className="border-0 bg-transparent p-0 focus:ring-0"
                      />
                      <ChevronDown className="h-4 w-4 text-gray-400" />
                    </div>
                    
                    {showAirlineDropdown && (
                      <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg z-10 max-h-60 overflow-hidden">
                        <ScrollArea className="h-60">
                          {filteredAirlines.map((airline) => (
                            <div
                              key={airline.id}
                              className="p-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                              onClick={() => handleAirlineChange(airline)}
                            >
                              <div className="font-medium">{airline.code} - {airline.name}</div>
                              <div className="text-sm text-gray-500">{airline.loyalty_program}</div>
                            </div>
                          ))}
                        </ScrollArea>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Flight Details */}
        <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CreditCard className="h-5 w-5 text-green-600" />
              <span>Flight Details</span>
            </CardTitle>
            <CardDescription>Configure your booking class and elite status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Fare Class */}
              <div className="space-y-2">
                <Label>Fare Class</Label>
                <Select value={selectedFareClass} onValueChange={handleFareClassChange}>
                  <SelectTrigger className="bg-white/50">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {fareClasses.map((fareClass) => (
                      <SelectItem key={fareClass.id} value={fareClass.name}>
                        {fareClass.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Booking Class */}
              <div className="space-y-2">
                <Label>Booking Class</Label>
                <Select value={selectedBookingClass} onValueChange={setSelectedBookingClass}>
                  <SelectTrigger className="bg-white/50">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {bookingClasses.map((bookingClass) => (
                      <SelectItem key={bookingClass.id} value={bookingClass.code}>
                        {bookingClass.code} - {bookingClass.description}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Elite Status */}
              <div className="space-y-2">
                <Label>Elite Status</Label>
                <Select value={selectedEliteStatus} onValueChange={setSelectedEliteStatus}>
                  <SelectTrigger className="bg-white/50">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">
                      {eliteStatusTiers.none || 'General Member'}
                    </SelectItem>
                    <SelectItem value="silver">
                      {eliteStatusTiers.silver || 'Silver'}
                    </SelectItem>
                    <SelectItem value="gold">
                      {eliteStatusTiers.gold || 'Gold'}
                    </SelectItem>
                    <SelectItem value="platinum">
                      {eliteStatusTiers.platinum || 'Platinum'}
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Button
            onClick={handleCompareAlliance}
            disabled={loading || !selectedOrigin || !selectedDestination || !selectedAlliance}
            className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg"
            size="lg"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Trophy className="h-4 w-4 mr-2" />
            )}
            Compare Alliance Programs
          </Button>
          
          <Button
            onClick={handleCalculateIndividual}
            disabled={loading || !selectedOrigin || !selectedDestination || !selectedAirline}
            variant="outline"
            className="flex-1 border-2 border-indigo-200 hover:bg-indigo-50"
            size="lg"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Calculator className="h-4 w-4 mr-2" />
            )}
            Calculate Individual Miles
          </Button>
        </div>

        {/* Error Display */}
        {error && (
          <Card className="bg-red-50 border-red-200 mb-8">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-red-700">
                <AlertCircle className="h-4 w-4" />
                <span>{error}</span>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {comparisonResults && (
          <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Trophy className="h-5 w-5 text-yellow-600" />
                <span>Alliance Comparison Results</span>
              </CardTitle>
              <CardDescription>
                {comparisonResults.origin.code} → {comparisonResults.destination.code} 
                ({comparisonResults.distance_miles.toLocaleString()} miles)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {comparisonResults.comparisons.map((comparison, index) => (
                  <div
                    key={comparison.loyalty_program.id}
                    className={`p-4 rounded-lg border-2 ${
                      index === 0 
                        ? 'bg-gradient-to-r from-yellow-50 to-amber-50 border-yellow-300' 
                        : 'bg-white/50 border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        {index === 0 && <Crown className="h-5 w-5 text-yellow-600" />}
                        <div>
                          <div className="font-semibold text-lg">
                            {comparison.airline.name}
                          </div>
                          <div className="text-sm text-gray-600">
                            {comparison.loyalty_program.name}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">
                          {comparison.calculation.total_miles.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-600">total miles</div>
                      </div>
                    </div>
                    
                    <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Base Miles</div>
                        <div className="font-medium">{comparison.calculation.base_miles.toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Elite Bonus</div>
                        <div className="font-medium">
                          {comparison.calculation.elite_bonus_miles.toLocaleString()}
                          {comparison.calculation.elite_bonus_rate > 0 && (
                            <span className="text-green-600 ml-1">
                              (+{comparison.calculation.elite_bonus_rate}%)
                            </span>
                          )}
                        </div>
                      </div>
                      <div>
                        <div className="text-gray-600">Earning Rate</div>
                        <div className="font-medium">{comparison.calculation.calculation_details.earning_percentage}%</div>
                      </div>
                      <div>
                        <div className="text-gray-600">EQMs</div>
                        <div className="font-medium">{comparison.calculation.elite_qualifying_miles.toLocaleString()}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {individualResult && (
          <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-blue-600" />
                <span>Individual Calculation Result</span>
              </CardTitle>
              <CardDescription>
                {individualResult.origin.code} → {individualResult.destination.code} 
                with {individualResult.airline.name}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border-2 border-blue-200">
                <div className="text-center mb-6">
                  <div className="text-4xl font-bold text-blue-600 mb-2">
                    {individualResult.calculation.total_miles.toLocaleString()}
                  </div>
                  <div className="text-lg text-gray-600">Total Miles Earned</div>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-gray-800">
                      {individualResult.calculation.base_miles.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Base Miles</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-green-600">
                      {individualResult.calculation.elite_bonus_miles.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Elite Bonus</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-purple-600">
                      {individualResult.calculation.elite_qualifying_miles.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">EQMs</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-semibold text-orange-600">
                      {individualResult.distance_miles.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">Distance</div>
                  </div>
                </div>

                <Separator className="my-4" />

                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">Loyalty Program</div>
                    <div className="font-medium">{individualResult.loyalty_program.name}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Earning Rate</div>
                    <div className="font-medium">{individualResult.calculation.calculation_details.earning_percentage}%</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Elite Bonus Rate</div>
                    <div className="font-medium">
                      {individualResult.calculation.elite_bonus_rate > 0 
                        ? `+${individualResult.calculation.elite_bonus_rate}%` 
                        : 'None'}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-white/20 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <Sparkles className="h-4 w-4" />
              <span className="font-medium">Airline Miles Calculator</span>
            </div>
            <p className="text-sm">
              The most comprehensive miles calculator with {stats?.airports.toLocaleString()} airports, 
              {stats?.airlines} airlines, and {stats?.loyalty_programs} loyalty programs.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

