import { useState } from 'react';
import { eventAPI } from '../services/api';

const EVENT_TYPES = ['DIVIDEND', 'STOCK_SPLIT', 'MERGER'];

export default function EventForm({ onEventCreated }) {
  const [eventType, setEventType] = useState('DIVIDEND');
  const [formData, setFormData] = useState({
    symbol: '',
    amount: '',
    ex_date: '',
    record_date: '',
    payment_date: '',
    split_ratio_from: '',
    split_ratio_to: '',
    target_symbol: '',
    exchange_ratio: '',
    cash_component: '',
    effective_date: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const payload = {
        event_type: eventType,
        symbol: formData.symbol.toUpperCase(),
      };

      if (eventType === 'DIVIDEND') {
        payload.amount = parseFloat(formData.amount);
        payload.ex_date = formData.ex_date;
        payload.record_date = formData.record_date;
        payload.payment_date = formData.payment_date;
      } else if (eventType === 'STOCK_SPLIT') {
        payload.split_ratio_from = parseInt(formData.split_ratio_from);
        payload.split_ratio_to = parseInt(formData.split_ratio_to);
        payload.effective_date = formData.effective_date;
      } else if (eventType === 'MERGER') {
        payload.target_symbol = formData.target_symbol.toUpperCase();
        payload.exchange_ratio = parseFloat(formData.exchange_ratio);
        payload.cash_component = parseFloat(formData.cash_component || 0);
        payload.effective_date = formData.effective_date;
      }

      await eventAPI.createEvent(payload);
      setSuccess(true);
      setFormData({
        symbol: '',
        amount: '',
        ex_date: '',
        record_date: '',
        payment_date: '',
        split_ratio_from: '',
        split_ratio_to: '',
        target_symbol: '',
        exchange_ratio: '',
        cash_component: '',
        effective_date: '',
      });
      
      if (onEventCreated) {
        onEventCreated();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create event');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="event-form">
      <h2>Create Corporate Action Event</h2>
      
      {success && (
        <div className="alert alert-success">
          Event created successfully!
        </div>
      )}
      
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Event Type</label>
          <select
            value={eventType}
            onChange={(e) => setEventType(e.target.value)}
            className="form-control"
          >
            {EVENT_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Symbol *</label>
          <input
            type="text"
            name="symbol"
            value={formData.symbol}
            onChange={handleChange}
            required
            className="form-control"
            placeholder="AAPL"
          />
        </div>

        {eventType === 'DIVIDEND' && (
          <>
            <div className="form-group">
              <label>Amount *</label>
              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                required
                step="0.01"
                className="form-control"
                placeholder="0.24"
              />
            </div>
            <div className="form-group">
              <label>Ex-Date *</label>
              <input
                type="date"
                name="ex_date"
                value={formData.ex_date}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>
            <div className="form-group">
              <label>Record Date *</label>
              <input
                type="date"
                name="record_date"
                value={formData.record_date}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>
            <div className="form-group">
              <label>Payment Date *</label>
              <input
                type="date"
                name="payment_date"
                value={formData.payment_date}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>
          </>
        )}

        {eventType === 'STOCK_SPLIT' && (
          <>
            <div className="form-group">
              <label>Split Ratio From *</label>
              <input
                type="number"
                name="split_ratio_from"
                value={formData.split_ratio_from}
                onChange={handleChange}
                required
                className="form-control"
                placeholder="1"
              />
            </div>
            <div className="form-group">
              <label>Split Ratio To *</label>
              <input
                type="number"
                name="split_ratio_to"
                value={formData.split_ratio_to}
                onChange={handleChange}
                required
                className="form-control"
                placeholder="3"
              />
            </div>
            <div className="form-group">
              <label>Effective Date *</label>
              <input
                type="date"
                name="effective_date"
                value={formData.effective_date}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>
          </>
        )}

        {eventType === 'MERGER' && (
          <>
            <div className="form-group">
              <label>Target Symbol *</label>
              <input
                type="text"
                name="target_symbol"
                value={formData.target_symbol}
                onChange={handleChange}
                required
                className="form-control"
                placeholder="ATVI"
              />
            </div>
            <div className="form-group">
              <label>Exchange Ratio *</label>
              <input
                type="number"
                name="exchange_ratio"
                value={formData.exchange_ratio}
                onChange={handleChange}
                required
                step="0.01"
                className="form-control"
                placeholder="1.5"
              />
            </div>
            <div className="form-group">
              <label>Cash Component</label>
              <input
                type="number"
                name="cash_component"
                value={formData.cash_component}
                onChange={handleChange}
                step="0.01"
                className="form-control"
                placeholder="95.00"
              />
            </div>
            <div className="form-group">
              <label>Effective Date *</label>
              <input
                type="date"
                name="effective_date"
                value={formData.effective_date}
                onChange={handleChange}
                required
                className="form-control"
              />
            </div>
          </>
        )}

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary"
        >
          {loading ? 'Creating...' : 'Create Event'}
        </button>
      </form>
    </div>
  );
}
