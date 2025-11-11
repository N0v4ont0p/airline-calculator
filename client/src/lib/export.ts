/**
 * Export utilities for CSV and PDF generation
 */

import type { CalculationResult, Airport } from './calculator';
import { formatMiles, formatCurrency, formatPercentage } from './calculator';

/**
 * Export results to CSV format
 */
export function exportToCSV(
  results: CalculationResult[],
  origin: Airport,
  destination: Airport,
  bookingClass: string,
  eliteStatus: string,
  distance: number
): void {
  const headers = [
    'Rank',
    'Program',
    'Airline',
    'Alliance',
    'Miles Earned',
    'Estimated Value (USD)',
    'Earning Rate',
    'Cents Per Mile',
    'Currency'
  ];

  const rows = results.map((result, index) => [
    (index + 1).toString(),
    result.program.name,
    result.program.airline,
    result.program.alliance,
    result.milesEarned.toString(),
    result.estimatedValue.toFixed(2),
    (result.earningRate * 100).toFixed(0) + '%',
    result.program.centsPerMile.toFixed(1),
    result.program.currency
  ]);

  // Add metadata rows at the top
  const metadata = [
    ['Flight Details'],
    ['Origin', `${origin.iata} - ${origin.name}, ${origin.city}`],
    ['Destination', `${destination.iata} - ${destination.name}, ${destination.city}`],
    ['Distance', `${distance} nautical miles`],
    ['Booking Class', bookingClass],
    ['Elite Status', eliteStatus],
    [''],
    ['Results']
  ];

  const csvContent = [
    ...metadata.map(row => row.join(',')),
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `airline-miles-${origin.iata}-${destination.iata}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Export results to PDF format (using browser print)
 */
export function exportToPDF(
  results: CalculationResult[],
  origin: Airport,
  destination: Airport,
  bookingClass: string,
  eliteStatus: string,
  distance: number
): void {
  // Create a printable HTML document
  const printWindow = window.open('', '_blank');
  
  if (!printWindow) {
    alert('Please allow popups to export PDF');
    return;
  }

  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Airline Miles Calculation - ${origin.iata} to ${destination.iata}</title>
      <style>
        body {
          font-family: 'Inter', Arial, sans-serif;
          margin: 40px;
          color: #333;
        }
        h1 {
          font-family: 'Playfair Display', serif;
          color: #282C20;
          border-bottom: 3px solid #D2FF00;
          padding-bottom: 10px;
        }
        h2 {
          font-family: 'Playfair Display', serif;
          color: #282C20;
          margin-top: 30px;
        }
        .metadata {
          background: #f5f5f5;
          padding: 20px;
          border-radius: 8px;
          margin: 20px 0;
        }
        .metadata p {
          margin: 5px 0;
        }
        .best-program {
          background: #D2FF00;
          padding: 20px;
          border-radius: 8px;
          margin: 20px 0;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 20px 0;
        }
        th, td {
          border: 1px solid #ddd;
          padding: 12px;
          text-align: left;
        }
        th {
          background-color: #282C20;
          color: white;
        }
        tr:nth-child(even) {
          background-color: #f9f9f9;
        }
        .footer {
          margin-top: 40px;
          padding-top: 20px;
          border-top: 1px solid #ddd;
          font-size: 12px;
          color: #666;
          text-align: center;
        }
        @media print {
          body { margin: 20px; }
        }
      </style>
    </head>
    <body>
      <h1>✈️ Airline Miles Calculation Report</h1>
      
      <div class="metadata">
        <h2>Flight Details</h2>
        <p><strong>Route:</strong> ${origin.iata} (${origin.name}, ${origin.city}) → ${destination.iata} (${destination.name}, ${destination.city})</p>
        <p><strong>Distance:</strong> ${distance.toLocaleString()} nautical miles</p>
        <p><strong>Booking Class:</strong> ${bookingClass}</p>
        <p><strong>Elite Status:</strong> ${eliteStatus}</p>
        <p><strong>Programs Compared:</strong> ${results.length}</p>
      </div>

      <div class="best-program">
        <h2>🏆 Best Program</h2>
        <p><strong>${results[0].program.name}</strong></p>
        <p><strong>Miles Earned:</strong> ${formatMiles(results[0].milesEarned)}</p>
        <p><strong>Estimated Value:</strong> ${formatCurrency(results[0].estimatedValue)}</p>
        <p><strong>Earning Rate:</strong> ${formatPercentage(results[0].earningRate)}</p>
      </div>

      <h2>Full Comparison</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Program</th>
            <th>Alliance</th>
            <th>Miles Earned</th>
            <th>Est. Value</th>
            <th>Rate</th>
            <th>¢/Mile</th>
          </tr>
        </thead>
        <tbody>
          ${results.map((result, index) => `
            <tr>
              <td>${index + 1}</td>
              <td>${result.program.name}</td>
              <td>${result.program.alliance}</td>
              <td>${formatMiles(result.milesEarned)}</td>
              <td>${formatCurrency(result.estimatedValue)}</td>
              <td>${formatPercentage(result.earningRate)}</td>
              <td>${result.program.centsPerMile.toFixed(1)}¢</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div class="footer">
        <p>Generated by SkyMiles Calculator | ${new Date().toLocaleDateString()}</p>
        <p>Data is for informational purposes only. Always verify with official airline programs.</p>
      </div>
    </body>
    </html>
  `;

  printWindow.document.write(html);
  printWindow.document.close();
  
  // Wait for content to load, then print
  printWindow.onload = () => {
    setTimeout(() => {
      printWindow.print();
    }, 250);
  };
}

/**
 * Generate shareable link with calculation parameters
 */
export function generateShareLink(
  origin: Airport,
  destination: Airport,
  bookingClass: string,
  eliteStatus: string,
  selectedPrograms: string[]
): string {
  const params = new URLSearchParams({
    from: origin.iata,
    to: destination.iata,
    class: bookingClass,
    status: eliteStatus,
    programs: selectedPrograms.join(',')
  });

  return `${window.location.origin}?${params.toString()}`;
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
}

/**
 * Save route to localStorage
 */
export interface SavedRoute {
  id: string;
  name: string;
  origin: Airport;
  destination: Airport;
  bookingClass: string;
  eliteStatus: string;
  savedAt: string;
}

export function saveRoute(
  name: string,
  origin: Airport,
  destination: Airport,
  bookingClass: string,
  eliteStatus: string
): void {
  const routes = getSavedRoutes();
  
  const newRoute: SavedRoute = {
    id: Date.now().toString(),
    name,
    origin,
    destination,
    bookingClass,
    eliteStatus,
    savedAt: new Date().toISOString()
  };

  routes.push(newRoute);
  localStorage.setItem('savedRoutes', JSON.stringify(routes));
}

export function getSavedRoutes(): SavedRoute[] {
  const saved = localStorage.getItem('savedRoutes');
  return saved ? JSON.parse(saved) : [];
}

export function deleteSavedRoute(id: string): void {
  const routes = getSavedRoutes();
  const filtered = routes.filter(r => r.id !== id);
  localStorage.setItem('savedRoutes', JSON.stringify(filtered));
}

/**
 * Save calculation to history
 */
export interface CalculationHistory {
  id: string;
  origin: Airport;
  destination: Airport;
  bookingClass: string;
  eliteStatus: string;
  bestProgram: string;
  milesEarned: number;
  estimatedValue: number;
  calculatedAt: string;
}

export function saveToHistory(
  origin: Airport,
  destination: Airport,
  bookingClass: string,
  eliteStatus: string,
  bestResult: CalculationResult
): void {
  const history = getCalculationHistory();
  
  const entry: CalculationHistory = {
    id: Date.now().toString(),
    origin,
    destination,
    bookingClass,
    eliteStatus,
    bestProgram: bestResult.program.name,
    milesEarned: bestResult.milesEarned,
    estimatedValue: bestResult.estimatedValue,
    calculatedAt: new Date().toISOString()
  };

  // Keep only last 50 calculations
  history.unshift(entry);
  if (history.length > 50) {
    history.pop();
  }

  localStorage.setItem('calculationHistory', JSON.stringify(history));
}

export function getCalculationHistory(): CalculationHistory[] {
  const saved = localStorage.getItem('calculationHistory');
  return saved ? JSON.parse(saved) : [];
}

export function clearHistory(): void {
  localStorage.removeItem('calculationHistory');
}
