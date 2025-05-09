import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Navbar from './components/Navbar/Navbar.jsx'
import Games from './components/Games/Games.jsx'
import TicTacToe from './pages/TicTacToe/TicTacToe.jsx';
import Top10 from './pages/Top10/Top10.jsx';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Games />} />
        <Route path="/nba-tic-tac-toe" element={<TicTacToe />} />
        <Route path="/nba-top-10" element={<Top10 />} />
      </Routes>
      <div className="footer">
        <p>© 2025 Huy Le. All rights reserved.</p>
      </div>
    </Router>
  );
};

export default App;