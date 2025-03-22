// src/App.tsx

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HeroPage from './pages/HeroPage';
import { LampDemo } from './components/ui/lamp';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HeroPage />} />
        {/* Other routes */}
      </Routes>
    </Router>
  );
};

export default App;