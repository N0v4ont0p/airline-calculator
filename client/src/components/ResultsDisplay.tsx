import { Trophy, TrendingUp, Info, Download, Share2, Save } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import type { Airport, CalculationResult } from '@/lib/calculator';
import { formatMiles, formatCurrency, formatPercentage } from '@/lib/calculator';
import { exportToCSV, exportToPDF, generateShareLink, copyToClipboard, saveRoute, saveToHistory } from '@/lib/export';
import { toast } from 'sonner';
import { useState } from 'react';

interface ResultsDisplayProps {
  results: CalculationResult[];
  origin: Airport;
  destination: Airport;
  bookingClass: string;
  eliteStatus: string;
  distance: number;
}

export function ResultsDisplay({
  results,
  origin,
  destination,
  bookingClass,
  eliteStatus,
  distance
}: ResultsDisplayProps) {
  const [isSaving, setIsSaving] = useState(false);

  if (results.length === 0) return null;

  const bestResult = results[0];
  const maxValue = Math.max(...results.map(r => r.estimatedValue));

  const getEliteStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      none: 'No Elite Status',
      silver: 'Silver Status',
      gold: 'Gold Status',
      platinum: 'Platinum Status',
      top: 'Top Tier Status'
    };
    return labels[status] || status;
  };

  const getMedalIcon = (index: number) => {
    if (index === 0) return '🥇';
    if (index === 1) return '🥈';
    if (index === 2) return '🥉';
    return '';
  };

  return (
    <div className="space-y-6 animate-fade-slide-up">
      {/* Results Header */}
      <Card className="glass neon-glow">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-primary" />
            Results for: {origin.iata} → {destination.iata}
          </CardTitle>
          <CardDescription>
            {distance.toLocaleString()} nautical miles | {bookingClass} Class | {getEliteStatusLabel(eliteStatus)}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Best Program */}
      <Card className="glass neon-glow border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-6 h-6 text-primary" />
            Best Program
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <h3 className="text-2xl font-bold neon-text">{bestResult.program.name}</h3>
            <div className="grid md:grid-cols-3 gap-4 mt-4">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Miles Earned</p>
                <p className="text-3xl font-bold text-primary">{formatMiles(bestResult.milesEarned)}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Estimated Value</p>
                <p className="text-3xl font-bold text-primary">{formatCurrency(bestResult.estimatedValue)}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Earning Rate</p>
                <p className="text-3xl font-bold text-primary">{formatPercentage(bestResult.earningRate)}</p>
              </div>
            </div>
            <div className="mt-4 p-4 bg-accent/10 rounded-lg">
              <p className="text-sm flex items-start gap-2">
                <Info className="w-4 h-4 mt-0.5 text-primary flex-shrink-0" />
                <span>
                  <strong>Tip:</strong> {bestResult.program.currency === 'Avios' 
                    ? 'Great for short-haul flights and partner redemptions'
                    : bestResult.program.isRevenueBased 
                      ? 'Revenue-based program - higher ticket prices earn more miles'
                      : 'Distance-based program - premium cabins earn more miles per mile flown'}
                </span>
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Full Comparison Table */}
      <Card className="glass">
        <CardHeader>
          <CardTitle>Full Comparison</CardTitle>
          <CardDescription>
            All {results.length} programs sorted by estimated value
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12"></TableHead>
                  <TableHead>Program</TableHead>
                  <TableHead>Alliance</TableHead>
                  <TableHead className="text-right">Miles Earned</TableHead>
                  <TableHead className="text-right">Est. Value</TableHead>
                  <TableHead className="text-right">Rate</TableHead>
                  <TableHead className="text-right">¢/Mile</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((result, index) => (
                  <TableRow key={result.program.id} className="hover:bg-accent/50">
                    <TableCell className="font-medium text-lg">
                      {getMedalIcon(index)}
                    </TableCell>
                    <TableCell className="font-medium">
                      {result.program.name}
                      {index === 0 && (
                        <Badge className="ml-2 bg-primary text-primary-foreground">Best</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{result.program.alliance}</Badge>
                    </TableCell>
                    <TableCell className="text-right font-mono">
                      {formatMiles(result.milesEarned)}
                    </TableCell>
                    <TableCell className="text-right font-mono font-semibold">
                      {formatCurrency(result.estimatedValue)}
                    </TableCell>
                    <TableCell className="text-right">
                      {formatPercentage(result.earningRate)}
                    </TableCell>
                    <TableCell className="text-right text-muted-foreground">
                      {result.program.centsPerMile.toFixed(1)}¢
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Visual Comparison Chart */}
      <Card className="glass">
        <CardHeader>
          <CardTitle>Visual Comparison</CardTitle>
          <CardDescription>Miles earned by program (top 10)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {results.slice(0, 10).map((result, index) => {
              const percentage = (result.milesEarned / results[0].milesEarned) * 100;
              return (
                <div key={result.program.id} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{result.program.name}</span>
                    <span className="font-mono">{formatMiles(result.milesEarned)}</span>
                  </div>
                  <div className="h-8 bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-primary flex items-center justify-end px-3 text-sm font-semibold transition-all duration-1000"
                      style={{ width: `${percentage}%` }}
                    >
                      {percentage < 30 ? '' : `${percentage.toFixed(0)}%`}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card className="glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="w-6 h-6 text-primary" />
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start gap-2">
              <span className="text-primary mt-1">•</span>
              <span><strong>Best for this route:</strong> {bestResult.program.name} with {formatMiles(bestResult.milesEarned)} miles</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-1">•</span>
              <span><strong>Best overall value:</strong> {bestResult.program.name} at {formatCurrency(bestResult.estimatedValue)} ({bestResult.program.centsPerMile}¢ per mile)</span>
            </li>
            {results.length > 1 && (
              <li className="flex items-start gap-2">
                <span className="text-primary mt-1">•</span>
                <span><strong>Alternative option:</strong> {results[1].program.name} with {formatMiles(results[1].milesEarned)} miles</span>
              </li>
            )}
            <li className="flex items-start gap-2">
              <span className="text-primary mt-1">•</span>
              <span><strong>Tip:</strong> Consider your home airport and preferred redemption destinations when choosing a program</span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <Card className="glass">
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-3">
            <Button 
              variant="outline" 
              className="flex-1 min-w-[200px]"
              onClick={() => {
                exportToPDF(results, origin, destination, bookingClass, eliteStatus, distance);
                toast.success('Opening PDF preview...');
              }}
            >
              <Download className="w-4 h-4 mr-2" />
              Export to PDF
            </Button>
            <Button 
              variant="outline" 
              className="flex-1 min-w-[200px]"
              onClick={() => {
                exportToCSV(results, origin, destination, bookingClass, eliteStatus, distance);
                toast.success('CSV file downloaded!');
              }}
            >
              <Download className="w-4 h-4 mr-2" />
              Export to CSV
            </Button>
            <Button 
              variant="outline" 
              className="flex-1 min-w-[200px]"
              onClick={async () => {
                const link = generateShareLink(origin, destination, bookingClass, eliteStatus, results.map(r => r.program.id));
                const success = await copyToClipboard(link);
                if (success) {
                  toast.success('Link copied to clipboard!');
                } else {
                  toast.error('Failed to copy link');
                }
              }}
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share Link
            </Button>
            <Button 
              variant="outline" 
              className="flex-1 min-w-[200px]"
              disabled={isSaving}
              onClick={() => {
                setIsSaving(true);
                const routeName = `${origin.iata} → ${destination.iata}`;
                saveRoute(routeName, origin, destination, bookingClass, eliteStatus);
                saveToHistory(origin, destination, bookingClass, eliteStatus, results[0]);
                toast.success('Route saved!');
                setTimeout(() => setIsSaving(false), 1000);
              }}
            >
              <Save className="w-4 h-4 mr-2" />
              {isSaving ? 'Saving...' : 'Save Route'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
