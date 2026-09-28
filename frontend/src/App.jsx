import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import RiskPrediction from './pages/RiskPrediction';
import DataAnalysis from './pages/DataAnalysis';
import ModelPerformance from './pages/ModelPerformance';
import Visualizations from './pages/Visualizations';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="predict" element={<RiskPrediction />} />
          <Route path="analysis" element={<DataAnalysis />} />
          <Route path="performance" element={<ModelPerformance />} />
          <Route path="visualizations" element={<Visualizations />} />
          <Route path="about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;