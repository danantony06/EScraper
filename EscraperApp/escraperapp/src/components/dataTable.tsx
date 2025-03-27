import React, { useEffect, useMemo, useState } from 'react';
import { 
  useReactTable, 
  getCoreRowModel, 
  getSortedRowModel, 
  SortingState,
  ColumnDef,
  flexRender 
} from '@tanstack/react-table';

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
  const columns = useMemo<ColumnDef<RowData>[]>(
    () => [
      {
        accessorKey: 'Player',
        header: () => 'Player',
        cell: info => (
          <span className="text-indigo-300 font-semibold">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'Matchup',
        header: () => 'Matchup',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'Stat_Type',
        header: () => 'Stat Type',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'PrizePicks_Line',
        header: () => 'PrizePicks',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'Underdog_Line',
        header: () => 'Underdog',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'ParlayPlay_Line',
        header: () => 'ParlayPlay',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'HotstreakLine',
        header: () => 'HotStreak',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'HotstreakOver',
        header: () => 'Over',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'HotstreakUnder',
        header: () => 'Under',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      {
        accessorKey: 'Date',
        header: () => 'Date',
        cell: info => (
          <span className="text-blue-200">
            {info.getValue<string>()}
          </span>
        )
      },
      
      
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="bg-gray-900 p-4 rounded-xl shadow-2xl">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead className="bg-gray-800">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id} className="border-b border-gray-700">
                {headerGroup.headers.map(header => (
                  <th 
                    key={header.id} 
                    className="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-700"
                    onClick={header.column.getToggleSortingHandler()}
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                    {header.column.getIsSorted() === 'asc'
                      ? ' ▲'
                      : header.column.getIsSorted() === 'desc'
                      ? ' ▼'
                      : null}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="bg-gray-900 divide-y divide-gray-700">
            {table.getRowModel().rows.map((row, index) => (
              <tr 
                key={row.id} 
                className={`${
                  index % 2 === 0 ? 'bg-gray-800/50' : 'bg-gray-900/50'
                } hover:bg-blue-900/20 transition duration-200`}
              >
                {row.getVisibleCells().map(cell => (
                  <td 
                    key={cell.id} 
                    className="px-4 py-3 whitespace-nowrap text-sm text-gray-300"
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

export default GridExample;
