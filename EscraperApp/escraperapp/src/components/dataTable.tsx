import { ColDef, ClientSideRowModelModule } from 'ag-grid-community'; 
import { AgGridReact } from 'ag-grid-react';
import { useState, useEffect } from 'react';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

export function GridExample() {
    const [prizeData, setPrizeData] = useState([]);
    const [underdogData, setUnderdogData] = useState([])
    const [hotStreakData, setHotStreakData] = useState([])
    const [parlayPlayData, setParlayPlayData] = useState([])
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [colDefs] = useState<ColDef[]>([
        {
            field: "Player", 
            headerName: "Player", 
            sortable: true, 
            filter: true,
            cellStyle: { fontWeight: 'bold', color: '#333' }
        },
        {
            field: "Matchup", 
            headerName: "Matchup", 
            sortable: true, 
            filter: true,
            cellStyle: { color: '#666' }
        },
        {
            field: "stat_type", 
            headerName: "Stat Type", 
            sortable: true, 
            filter: true,
            cellStyle: { fontStyle: 'italic' }
        },
        {
            field: "stat_line", 
            headerName: "Stat Line", 
            sortable: true, 
            filter: true,
            cellStyle: { fontWeight: '500' }
        },
        {
            field: "Over", 
            headerName: "Over", 
            sortable: true, 
            filter: true,
            cellStyle: (params) => ({
                color: parseFloat(params.value) > 0 ? 'green' : 'red'
            })
        },
        {
            field: "Under", 
            headerName: "Under", 
            sortable: true, 
            filter: true,
            cellStyle: (params) => ({
                color: parseFloat(params.value) > 0 ? 'green' : 'red'
            })
        },
        {
            field: "Date", 
            headerName: "Date", 
            sortable: true, 
            filter: true,
            cellStyle: { color: '#888' }
        },
        {
            field: "Source", 
            headerName: "Source", 
            sortable: true, 
            filter: true,
            cellStyle: { fontWeight: '600', color: '#444' }
        }
    ]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);
                const endpoints = [
                    { url: 'http://localhost:3000/PrizePicks', setter: setPrizeData },
                    { url: 'http://localhost:3000/underdog', setter: setUnderdogData },
                    { url: 'http://localhost:3000/HotStreak', setter: setHotStreakData },
                    { url: 'http://localhost:3000/parlayPlay', setter: setParlayPlayData }
                ];

                const fetchPromises = endpoints.map(async (endpoint) => {
                    const response = await fetch(endpoint.url);
                    if (!response.ok) {
                        throw new Error(`HTTP error: ${response.status} for ${endpoint.url}`);
                    }
                    const data = await response.json();
                    endpoint.setter(data);
                });

                await Promise.all(fetchPromises);
                setIsLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError(error instanceof Error ? error.message : 'An unknown error occurred');
                setIsLoading(false);
            }
        };

        fetchData();
    }, []); 

    const combinedData = [...prizeData, ...underdogData, ...hotStreakData, ...parlayPlayData];

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-blue-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                <strong className="font-bold">Error: </strong>
                <span className="block sm:inline">{error}</span>
            </div>
        );
    }

    return (
        <div 
            className="ag-theme-alpine shadow-lg rounded-lg overflow-hidden" 
            style={{ height: 500, width: '100%' }}
        >
            <AgGridReact
                rowData={combinedData} 
                columnDefs={colDefs}
                modules={[ClientSideRowModelModule]}
                pagination={true}
                paginationPageSize={10}
                defaultColDef={{
                    resizable: true,
                    sortable: true,
                    filter: true
                }}
                // Enhanced grid styling
                rowHeight={45}
                headerHeight={50}
                className="font-sans"
                // Optional: add some hover and selection styles
                rowSelection="multiple"
                getRowStyle={(params) => ({
                    backgroundColor: params.node && params.node.rowIndex !== null && params.node.rowIndex % 2 === 0 ? '#f9fafb' : 'white',
                    transition: 'background-color 0.3s ease'
                })}
            />
        </div>
    );
}