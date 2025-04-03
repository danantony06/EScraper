import React, { useEffect, useMemo, useState } from 'react';
import { 
  useReactTable, 
  getCoreRowModel, 
  getSortedRowModel,
  getFilteredRowModel,
  SortingState,
  ColumnDef,
  flexRender 
} from '@tanstack/react-table';
import PrizeLogo from "../assets/PrizePicks.avif";
import UDLogo from "../assets/Underdog.webp"
import PplayLogo from "../assets/ParlayPlay.png"
import HotLogo from "../assets/HotStreak.png"

interface RowData {
  Player: string;
  Matchup: string;
  Stat_Type: string;
  PrizePicks: string;
  Underdog: string;
  ParlayPlay: string;
  HotStreak: string;
  Over: string;
  Under: string;
  Date: string;
  L5: string;
  L10: string;
  L15: string;
  AllTime: string;
  EMA: string;
  LowestLine: string;
}

interface GridExampleProps {
  selectedStat: string;
  searchTerm?: string;
  selectedSportsbook?: string;
}

export function GridExample({ selectedStat, searchTerm, selectedSportsbook }: GridExampleProps) {
  const [data, setData] = useState<RowData[]>([]);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [filteredData, setFilteredData] = useState<RowData[]>([]);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:3000/finalData");
        const finalData = await response.json();
        setData(finalData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    
    fetchData();
  }, []);
  
  useEffect(() => {
    let filtered = [...data];
        if (selectedStat) {
      filtered = filtered.filter(item => item.Stat_Type === selectedStat);
    }
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(item => 
        item.Player.toLowerCase().includes(term)
      );
    }
    
    if (selectedSportsbook) {
      filtered = filtered.filter(item => {
        const sportsbookValue = item[selectedSportsbook as keyof RowData];
        return sportsbookValue && sportsbookValue !== '-';
      });
    }
    
    setFilteredData(filtered);
  }, [data, selectedStat, searchTerm, selectedSportsbook]);
  
  const renderPercentageCell = (value: string) => {
    const numValue = parseInt(value);
    let colorClass = "text-gray-400";
    
    if (!isNaN(numValue)) {
      if (numValue >= 70) colorClass = "text-green-400 font-bold";
      else if (numValue >= 60) colorClass = "text-green-300";
      else if (numValue >= 50) colorClass = "text-yellow-300";
      else if (numValue >= 40) colorClass = "text-orange-400";
      else colorClass = "text-red-400";
    }
    
    return <span className={`${colorClass} text-xs`}>{value}%</span>;
  };
  
  const columns = useMemo<ColumnDef<RowData>[]>(() => [
    {
      accessorKey: 'Player',
      header: () => <span className="text-gray-300">Player</span>,
      cell: info => <span className="text-cyan-300 font-medium tracking-wide text-sm">{info.getValue<string>()}</span>,
      size: 120
    },
    {
      accessorKey: 'Matchup',
      header: () => <span className="text-gray-300">Matchup</span>,
      cell: info => <span className="text-teal-200 text-xs">{info.getValue<string>()}</span>,
      size: 100
    },
    {
      accessorKey: 'Stat_Type',
      header: () => <span className="text-gray-300">Stat</span>,
      cell: info => <span className="text-emerald-200 text-xs font-medium">{info.getValue<string>()}</span>,
      size: 80
    },
    {
      accessorKey: 'PrizePicks',
      header: () => (
        <div className="flex items-center justify-center">
          <img src={PrizeLogo} alt="PrizePicks" className="h-5 mr-1" />
        </div>
      ),
      cell: info => <div className="text-center text-amber-200 font-mono text-sm font-bold">{info.getValue<string>()}</div>,
      size: 60
    },
    {
      accessorKey: 'Underdog',
      header: () => (
        <div className="flex items-center justify-center">
          <img src={UDLogo} alt="Underdog" className="h-5" />
        </div>
      ),
      cell: info => <div className="text-center text-amber-200 font-mono text-sm font-bold">{info.getValue<string>()}</div>,
      size: 60
    },
    {
      accessorKey: 'ParlayPlay',
      header: () => (
        <div className="flex items-center justify-center">
          <img src={PplayLogo} alt="ParlayPlay" className="h-5" />
        </div>
      ),
      cell: info => <div className="text-center text-amber-200 font-mono text-sm font-bold">{info.getValue<string>()}</div>,
      size: 60
    },
    {
      accessorKey: 'HotStreak',
      header: () => (
        <div className="flex items-center justify-center">
          <img src={HotLogo} alt="HotStreak" className="h-5" />
        </div>
      ),
      cell: info => <div className="text-center text-amber-200 font-mono text-sm font-bold">{info.getValue<string>()}</div>,
      size: 60
    },
    {
      accessorKey: 'Over',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">O</div>,
      cell: info => <div className="text-center text-green-300 text-xs font-bold">{info.getValue<string>()}</div>,
      size: 40
    },
    {
      accessorKey: 'Under',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">U</div>,
      cell: info => <div className="text-center text-red-300 text-xs font-bold">{info.getValue<string>()}</div>,
      size: 40
    },
    {
      accessorKey: 'Date',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">Date</div>,
      cell: info => <div className="text-center text-gray-400 text-xs">{info.getValue<string>()}</div>,
      size: 80
    },
    {
      accessorKey: 'L5',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">L5</div>,
      cell: info => <div className="text-center">{renderPercentageCell(info.getValue<string>())}</div>,
      size: 50
    },
    {
      accessorKey: 'L10',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">L10</div>,
      cell: info => <div className="text-center">{renderPercentageCell(info.getValue<string>())}</div>,
      size: 50
    },
    {
      accessorKey: 'L15',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">L15</div>,
      cell: info => <div className="text-center">{renderPercentageCell(info.getValue<string>())}</div>,
      size: 50
    },
    {
      accessorKey: 'AllTime',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">All</div>,
      cell: info => <div className="text-center">{renderPercentageCell(info.getValue<string>())}</div>,
      size: 50
    },
    {
      accessorKey: 'EMA',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">Avg</div>,
      cell: info => <div className="text-center font-bold text-fuchsia-300 text-xs">{info.getValue<string>()}</div>,
      size: 50
    },
    {
      accessorKey: 'LowestLine',
      header: () => <div className="text-center text-gray-300 text-xs font-medium">Line</div>,
      cell: info => <div className="text-center font-bold text-amber-300 text-xs">{info.getValue<string>()}</div>,
      size: 50
    }
  ], []);
  
  const table = useReactTable({
    data: filteredData,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel()
  });
  
  return (
    <div className="w-full bg-gray-900 p-4 rounded-xl shadow-2xl border border-gray-700">
      <div className="h-[680px] overflow-y-auto custom-scrollbar">
        <table className="w-full">
          <thead className="bg-gray-800 sticky top-0 z-20">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th 
                    key={header.id}
                    className={`px-2 py-3 text-center text-xs font-semibold text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700 transition-colors duration-200 border-b border-gray-700`}
                    style={{ width: `${header.getSize()}px` }}
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    <div className="flex items-center justify-center">
                      {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                      <span className="ml-1">
                        {header.column.getIsSorted() === 'asc' ? ' ▲' : header.column.getIsSorted() === 'desc' ? ' ▼' : ''}
                      </span>
                    </div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-gray-700">
            {table.getRowModel().rows.map((row, index) => (
              <tr 
                key={row.id} 
                className={`${index % 2 === 0 ? 'bg-gray-800/50' : 'bg-gray-900/50'} hover:bg-blue-900/20 transition-colors duration-150`}
              >
                {row.getVisibleCells().map(cell => (
                  <td 
                    key={cell.id} 
                    className="px-2 py-3 text-center"
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(31, 41, 55, 0.5);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(75, 85, 99, 0.8);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(107, 114, 128, 0.8);
        }
      `}</style>
    </div>
  );
};

export default GridExample;