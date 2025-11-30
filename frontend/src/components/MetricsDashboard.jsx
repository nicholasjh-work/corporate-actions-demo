import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import { eventAPI } from '../services/api';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

export default function MetricsDashboard({ refreshTrigger }) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMetrics = async () => {
    try {
      const response = await eventAPI.getMetrics();
      setMetrics(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load metrics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  if (loading) {
    return <div className="loading">Loading metrics...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  if (!metrics) {
    return null;
  }

  const typeChartData = {
    labels: Object.keys(metrics.events_by_type),
    datasets: [
      {
        label: 'Events by Type',
        data: Object.values(metrics.events_by_type),
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#ef4444',
          '#8b5cf6',
          '#ec4899',
        ],
      },
    ],
  };

  const statusChartData = {
    labels: Object.keys(metrics.events_by_status),
    datasets: [
      {
        label: 'Event Count',
        data: Object.values(metrics.events_by_status),
        backgroundColor: [
          '#fbbf24',
          '#60a5fa',
          '#34d399',
          '#f87171',
          '#9ca3af',
        ],
      },
    ],
  };

  return (
    <div className="metrics-dashboard">
      <h2>System Metrics</h2>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{metrics.total_events}</div>
          <div className="metric-label">Total Events</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{metrics.recent_events_1h}</div>
          <div className="metric-label">Last Hour</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{metrics.recent_events_24h}</div>
          <div className="metric-label">Last 24 Hours</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{(metrics.error_rate * 100).toFixed(1)}%</div>
          <div className="metric-label">Error Rate</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-container">
          <h3>Events by Type</h3>
          {Object.keys(metrics.events_by_type).length > 0 ? (
            <Doughnut data={typeChartData} options={{ maintainAspectRatio: true }} />
          ) : (
            <p>No data available</p>
          )}
        </div>
        
        <div className="chart-container">
          <h3>Events by Status</h3>
          {Object.keys(metrics.events_by_status).length > 0 ? (
            <Bar
              data={statusChartData}
              options={{
                maintainAspectRatio: true,
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      stepSize: 1,
                    },
                  },
                },
              }}
            />
          ) : (
            <p>No data available</p>
          )}
        </div>
      </div>
    </div>
  );
}
