import { useState, useRef, useEffect } from 'react';
import { Search, MapPin } from 'lucide-react';
import { Input } from '@/components/ui/input';
import type { Airport } from '@/lib/calculator';
import { searchAirports } from '@/lib/calculator';

interface AirportSearchProps {
  airports: Airport[];
  value: Airport | null;
  onChange: (airport: Airport | null) => void;
  placeholder?: string;
}

export function AirportSearch({ airports, value, onChange, placeholder }: AirportSearchProps) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [results, setResults] = useState<Airport[]>([]);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (query.length > 0) {
      const searchResults = searchAirports(airports, query);
      setResults(searchResults);
      setIsOpen(searchResults.length > 0);
    } else {
      setResults([]);
      setIsOpen(false);
    }
  }, [query, airports]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (airport: Airport) => {
    onChange(airport);
    setQuery('');
    setIsOpen(false);
  };

  const handleClear = () => {
    onChange(null);
    setQuery('');
    setResults([]);
  };

  return (
    <div ref={wrapperRef} className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder={placeholder || 'Search airport...'}
          value={value ? `${value.iata} - ${value.name}, ${value.city}` : query}
          onChange={(e) => {
            if (value) {
              handleClear();
            }
            setQuery(e.target.value);
          }}
          onFocus={() => {
            if (query && results.length > 0) {
              setIsOpen(true);
            }
          }}
          className="pl-10"
        />
      </div>

      {isOpen && results.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-popover border border-border rounded-lg shadow-lg max-h-64 overflow-y-auto">
          {results.map((airport) => (
            <button
              key={airport.iata}
              onClick={() => handleSelect(airport)}
              className="w-full px-4 py-3 text-left hover:bg-accent hover:text-accent-foreground transition-colors flex items-start gap-3 border-b border-border last:border-b-0"
            >
              <MapPin className="w-4 h-4 mt-1 text-primary flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-sm">
                  {airport.iata} - {airport.name}
                </div>
                <div className="text-xs text-muted-foreground">
                  {airport.city}, {airport.country}
                </div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
