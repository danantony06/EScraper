import React, { useEffect, useMemo, useState } from 'react';
import { 
  useReactTable, 
  getCoreRowModel, 
  getSortedRowModel, 
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
  PrizePicks_Line: string;
  Underdog_Line: string;
  ParlayPlay_Line: string;
  HotstreakLine: string;
  HotstreakOver: string;
  HotstreakUnder: string;
  Date: string;
}

export const GridExample: React.FC = () => {
    const [data, setData] = useState<RowData[]>([]);
    const [sorting, setSorting] = useState<SortingState>([]);
  
    useEffect(() => {
      const fetchFinal = async () => {
        try {
          const response = await fetch("http://localhost:3000/finalData");
          const finalData = await response.json();
          setData(finalData);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
  
      fetchFinal();
    }, []);
  
    const columns = useMemo<ColumnDef<RowData>[]>(() => [
      {
        accessorKey: 'Player',
        header: () => 'Player',
        cell: info => <span className="text-indigo-300 font-semibold">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'Matchup',
        header: () => 'Matchup',
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'Stat_Type',
        header: () => 'Stat Type',
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'PrizePicks_Line',
        header: () => (
          <div className="flex align-right items-center">
            PrizePicks <img src={PrizeLogo} alt="PrizePicks Logo" className="h-5 ml-1" />
          </div>
        ),
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'Underdog_Line',
        header: () =>  <div className="flex align-right items-center">
        Underdog <img src={UDLogo} alt="Underdog Logo" className="h-6 ml-1" />
      </div>,
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'ParlayPlay_Line',
        header: () =>  <div className="flex align-right items-center">
        ParlayPlay <img src={PplayLogo} alt="ParlayPlay Logo" className="h-5 ml-1" />
      </div>,
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'HotstreakLine',
        header: () =>   <div className="flex align-right items-center">
        HotStreak <img src={HotLogo} alt="Hotstreak Logo" className="h-5 ml-1" />
      </div>,
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'HotstreakOver',
        header: () => 'Over',
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'HotstreakUnder',
        header: () => 'Under',
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      },
      {
        accessorKey: 'Date',
        header: () => 'Date',
        cell: info => <span className="text-blue-200">{info.getValue<string>()}</span>
      }
    ], []);
  
    const table = useReactTable({
      data,
      columns,
      state: { sorting },
      onSortingChange: setSorting,
      getCoreRowModel: getCoreRowModel(),
      getSortedRowModel: getSortedRowModel()
    });
  
    return (
      <div className="w-full bg-gray-900 p-3 rounded-xl shadow-2xl">
        <div className="h-[680px] overflow-y-auto">
          <table className="w-full border-collapse table-fixed">
            <thead className="bg-gray-800 sticky top-0 z-20">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id} className="border-b border-gray-700">
                  {headerGroup.headers.map(header => (
                    <th 
                      key={header.id} 
                      className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700"
                      onClick={header.column.getToggleSortingHandler()}
                    >
                      {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getIsSorted() === 'asc' ? ' ▲' : header.column.getIsSorted() === 'desc' ? ' ▼' : null}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="bg-gray-900 divide-y divide-gray-700">
              {table.getRowModel().rows.map((row, index) => (
                <tr 
                  key={row.id} 
                  className={`${index % 2 === 0 ? 'bg-gray-800/50' : 'bg-gray-900/50'} hover:bg-blue-900/20 transition duration-200`}
                >
                  {row.getVisibleCells().map(cell => (
                    <td 
                      key={cell.id} 
                      className="px-4 py-3 text-sm text-gray-300 whitespace-normal break-words max-w-[150px]"
                    >
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
export default GridExample