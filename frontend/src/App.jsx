import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Forecast from "./pages/Forecast";
import Recommendations from "./pages/Recommendations";
import Settings from "./pages/Settings";
import Simulation from "./pages/Simulation";
import CostHealth from "./pages/CostHealth";
export default function App() {
  return (
    <MainLayout>

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/analytics" element={<Analytics />} />

        <Route path="/forecast" element={<Forecast />} />

        <Route
          path="/recommendations"
          element={<Recommendations />}
        />

        <Route path="/settings" element={<Settings />} />

        <Route path="/simulation" element={<Simulation />} />
        <Route path="/health" element={<CostHealth />} />
      </Routes>

    </MainLayout>
  );
}