import React, { useState } from 'react';
import DashboardBaseline from './views/DashboardBaseline';
import SimulationEngine from './views/SimulationEngine';
import RoadmapReport from './views/RoadmapReport';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('simulation');

  return (
    <div className="App">
      <header className="App-header" style={{ padding: '1rem', backgroundColor: '#2c3e50', color: 'white' }}>
        <h1>🏊‍♂️ AquaDecide Tool (HEIG-VD)</h1>
        <nav style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
            <button onClick={() => setActiveTab('baseline')} style={{ padding: '8px 15px', cursor: 'pointer' }}>1. Diagnostic (Baseline)</button>
            <button onClick={() => setActiveTab('simulation')} style={{ padding: '8px 15px', cursor: 'pointer' }}>2. Moteur de Variantes</button>
            <button onClick={() => setActiveTab('roadmap')} style={{ padding: '8px 15px', cursor: 'pointer' }}>3. Feuille de Route</button>
        </nav>
      </header>

      <main className="App-content" style={{ padding: '2rem' }}>
        {activeTab === 'baseline' && <DashboardBaseline />}
        {activeTab === 'simulation' && <SimulationEngine />}
        {activeTab === 'roadmap' && <RoadmapReport />}
      </main>
    </div>
  );
}

export default App;