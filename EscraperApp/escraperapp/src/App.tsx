// src/App.tsx

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HeroPage from './pages/HeroPage';
import { NavBar } from './components/NavBar';
import { ResearchPage } from './pages/ResearchPage';
import {GridExample} from './components/dataTable'
const App = () => {
  return (
    <div className="min-h-screen bg-[#0a0b1a] bg-[radial-gradient(ellipse_70%_50%_at_50%_-10%,rgba(54,40,114,0.15),rgba(10,11,26,0))]">

    <Router>
      <Routes>
        <Route path="/" element={<HeroPage />} />
        <Route path = "/header" element = {<NavBar />}/>
        <Route path = "/research" element = {<ResearchPage/>}/>
        <Route path = "/table" element = {<GridExample/>}/>
        {/* Other routes */}
      </Routes>
    </Router>
    </div>
  );
};

export default App;