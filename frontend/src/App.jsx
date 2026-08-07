import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DashboardSummary from './pages/DashboardSummary';
import SlowAPIs from './pages/SlowAPIs';
import DatabasePerformance from './pages/DatabasePerformance';
import Recommendations from './pages/Recommendations';
import Issues from './pages/Issues';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DashboardSummary />} />
            <Route path="/slow-apis" element={<SlowAPIs />} />
            <Route path="/queries" element={<DatabasePerformance />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/issues" element={<Issues />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
