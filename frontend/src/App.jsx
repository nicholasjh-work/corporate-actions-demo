import { useState } from 'react';
import EventForm from './components/EventForm';
import EventList from './components/EventList';
import MetricsDashboard from './components/MetricsDashboard';
import './App.css';

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleEventCreated = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Corporate Action Processing System</h1>
        <p>Real-time event-driven architecture demo</p>
      </header>

      <div className="app-container">
        <div className="left-panel">
          <EventForm onEventCreated={handleEventCreated} />
        </div>

        <div className="right-panel">
          <MetricsDashboard refreshTrigger={refreshKey} />
          <EventList refreshTrigger={refreshKey} />
        </div>
      </div>

      <footer className="app-footer">
        <p>Demo by Nick | Built with FastAPI, React, MySQL, Docker</p>
      </footer>
    </div>
  );
}
