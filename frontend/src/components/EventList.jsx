import { useState, useEffect } from 'react';
import { eventAPI } from '../services/api';

const STATUS_COLORS = {
  PENDING: '#fbbf24',
  PROCESSING: '#60a5fa',
  COMPLETED: '#34d399',
  FAILED: '#f87171',
  CANCELLED: '#9ca3af',
};

export default function EventList({ refreshTrigger }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [statusFilter, setStatusFilter] = useState('');

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const params = statusFilter ? { status: statusFilter } : {};
      const response = await eventAPI.listEvents(params);
      setEvents(response.data.events);
      setError(null);
    } catch (err) {
      setError('Failed to load events');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, [statusFilter, refreshTrigger]);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading && events.length === 0) {
    return <div className="loading">Loading events...</div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <div className="event-list">
      <div className="event-list-header">
        <h2>Events ({events.length})</h2>
        <div className="filter-group">
          <label>Status:</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="form-control"
          >
            <option value="">All</option>
            <option value="PENDING">Pending</option>
            <option value="PROCESSING">Processing</option>
            <option value="COMPLETED">Completed</option>
            <option value="FAILED">Failed</option>
            <option value="CANCELLED">Cancelled</option>
          </select>
        </div>
      </div>

      <div className="events-container">
        {events.length === 0 ? (
          <p>No events found</p>
        ) : (
          events.map((event) => (
            <div key={event.id} className="event-card">
              <div className="event-card-header">
                <div className="event-type">{event.event_type}</div>
                <div
                  className="event-status"
                  style={{ backgroundColor: STATUS_COLORS[event.status] }}
                >
                  {event.status}
                </div>
              </div>
              <div className="event-card-body">
                <div className="event-symbol">{event.symbol}</div>
                <div className="event-details">
                  {event.event_type === 'DIVIDEND' && event.payload && (
                    <div>
                      Amount: ${event.payload.amount} | Payment: {event.payload.payment_date}
                    </div>
                  )}
                  {event.event_type === 'STOCK_SPLIT' && event.payload && (
                    <div>
                      Ratio: {event.payload.split_ratio_from}:{event.payload.split_ratio_to} | 
                      Effective: {event.payload.effective_date}
                    </div>
                  )}
                  {event.event_type === 'MERGER' && event.payload && (
                    <div>
                      Target: {event.payload.target_symbol} | 
                      Ratio: {event.payload.exchange_ratio}
                    </div>
                  )}
                </div>
                <div className="event-meta">
                  ID: {event.id} | Created: {formatDate(event.created_at)}
                </div>
                {event.error_message && (
                  <div className="event-error">
                    Error: {event.error_message} (Retry: {event.retry_count})
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
