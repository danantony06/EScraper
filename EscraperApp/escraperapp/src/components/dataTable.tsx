import { AllCommunityModule, ModuleRegistry, ColDef } from 'ag-grid-community'; 
import { AgGridReact } from 'ag-grid-react';
import { useState,useEffect } from 'react';



// useEffect (()=>{
//     console.log("Hello World")
//     const response = await fetch(

//     )
// })
export function GridExample(){
    const [rowData, setRowData] = useState([
        { make: "Tesla", model: "Model Y", price: 64950, electric: true },
        { make: "Ford", model: "F-Series", price: 33850, electric: false },
        { make: "Toyota", model: "Corolla", price: 29600, electric: false },
    ]);

    // Column Definitions: Defines the columns to be displayed.
    const [colDefs, setColDefs] = useState<ColDef[]>([
        { field: "make" },
        { field: "model" },
        { field: "price" },
        { field: "electric" }
    ]);

    return (
        // Data Grid will fill the size of the parent container
        <div style={{ height: 500, width: '100%' }}>
            <AgGridReact
            rowData={rowData}
            columnDefs={colDefs}
            modules={[AllCommunityModule]}
            />
        </div>
    )
}