import dotenv from 'dotenv';
dotenv.config(); // Ensure this is called BEFORE any imports that might use .env variables

import express, { Request, Response, Express } from 'express';
import cors from 'cors';
import { createClient } from '@supabase/supabase-js';

// Potential Issues and Solutions:

// 1. TypeScript Compilation
// Make sure you have ts-node or have compiled the TypeScript to JavaScript
// You might need to run with: 
// npx ts-node your-file.ts
// OR
// tsc && node dist/your-file.js

// 2. Environment Variable Loading
console.log('Loaded .env variables:', process.env);  // Log the entire env to check

// 3. Explicit Error Handling for .env
if (!process.env.SUPABASE_URL) {
  console.error("SUPABASE_URL is not set!");
  process.exit(1);
}

if (!process.env.SUPABASE_KEY) {
  console.error("SUPABASE_KEY is not set!");
  process.exit(1);
}

// 4. Detailed Environment Logging
console.log("SUPABASE_URL:", process.env.SUPABASE_URL);
console.log("SUPABASE_SERVICE_ROLE_KEY:", process.env.SUPABASE_KEY);
console.log("PORT:", process.env.PORT);

// 5. Create Supabase Client with Error Handling
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY,
  {
    // Optional: Add additional configuration
    db: {
      schema: 'public', // Explicitly set schema if needed
    }
  }
);

const app: Express = express();

app.use(cors());
app.use(express.json());

app.get("/PrizePicks", async (req: Request, res: Response): Promise<void> => {
  try {
    const { data: PrizePicks, error } = await supabase
      .from('PrizePicks')
      .select('*');
    
    if (error) {
      console.error("Supabase Query Error:", error);
      res.status(500).json({ error: error.message });
      return; // Important: return after sending error response
    }

    // Check if data is null or undefined
    if (!PrizePicks) {
      res.status(404).json({ message: 'No data found' });
      return;
    }

    res.json(PrizePicks);
  } catch (error) {
    console.error("Unexpected Error fetching PrizePicks:", error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});


app.get("/underdog",async (req:Request,res:Response): Promise<void>=>{
  try {
  const { data: Underdog, error } = await supabase
  .from('Underdog')
  .select('*')      
  if (error){
    console.log(error)
  }
  res.json(Underdog)
  } catch (error) {
    res.status(500).json({error:"Cant Fetch Underdog Data"});
  }
});

app.get("/parlayPlay", async(req:Request,res:Response) => {
  try {
    const { data: ParlayPlay, error } = await supabase
    .from('ParlayPlay')
    .select('*')
    if (error){
      console.log(error)
    }
    res.json(ParlayPlay)
  } catch (error) {
    res.status(500).json({error:"Cant Fetch Parlay Play Data"});
  }     
});


app.get("/HotStreak", async (req:Request, res:Response)=>{
  try {
  const { data: HotStreak, error } = await supabase
  .from('HotStreak')
  .select('*')
  if(error){
    console.log(error)
  }
  res.json(HotStreak)
  } catch (error) {
    res.status(500).json({error: "Can't get the Hotstreak Data"});
  }
        
});


app.get("/HitRates",async(req:Request,res:Response)=>{ 
  try {
    const { data: HitRates, error } = await supabase
    .from('HitRates')
    .select('*')
    if (error){
      console.log(error)
    }
    res.json(HitRates)
  
  } catch (error) {
    res.status(500).json({error:"Can't get the HitRate Data"});

  }
          
});

app.get("/gameOdds",async(req:Request,res:Response)=>{
  try {
    
  const { data: GameOdds, error } = await supabase
  .from('Game Odds')
  .select('*')
  if(error){
    console.log(error)
  }
  res.json(GameOdds)
  } catch (error) {
    res.status(500).json({error:"Game Odds Couldnt load"});
  }
});






const PORT = process.env.PORT || 3000;

// Improved Error Handling for Server Start
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}).on('error', (error) => {
  console.error(`Error starting server: ${error.message}`);
});

export default app;