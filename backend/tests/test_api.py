"""Tests for API endpoints."""
from datetime import date

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "healthy"


def test_create_dividend_event(client: TestClient) -> None:
    """Test creating a dividend event."""
    event_data = {
        "event_type": "DIVIDEND",
        "symbol": "AAPL",
        "amount": 0.24,
        "ex_date": "2024-11-15",
        "record_date": "2024-11-18",
        "payment_date": "2024-11-25",
        "currency": "USD",
    }
    
    response = client.post("/api/v1/events", json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "DIVIDEND"
    assert data["symbol"] == "AAPL"
    assert data["status"] == "PENDING"
    assert "id" in data


def test_create_stock_split_event(client: TestClient) -> None:
    """Test creating a stock split event."""
    event_data = {
        "event_type": "STOCK_SPLIT",
        "symbol": "TSLA",
        "split_ratio_from": 1,
        "split_ratio_to": 3,
        "effective_date": "2024-12-01",
    }
    
    response = client.post("/api/v1/events", json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "STOCK_SPLIT"
    assert data["symbol"] == "TSLA"


def test_create_merger_event(client: TestClient) -> None:
    """Test creating a merger event."""
    event_data = {
        "event_type": "MERGER",
        "symbol": "MSFT",
        "target_symbol": "ATVI",
        "exchange_ratio": 1.5,
        "cash_component": 95.00,
        "effective_date": "2024-12-15",
    }
    
    response = client.post("/api/v1/events", json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["event_type"] == "MERGER"


def test_list_events(client: TestClient) -> None:
    """Test listing events with pagination."""
    # Create some events
    for i in range(3):
        client.post(
            "/api/v1/events",
            json={
                "event_type": "DIVIDEND",
                "symbol": f"TEST{i}",
                "amount": 0.25,
                "ex_date": "2024-11-15",
                "record_date": "2024-11-18",
                "payment_date": "2024-11-25",
            },
        )
    
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    assert len(data["events"]) >= 3


def test_get_event_by_id(client: TestClient) -> None:
    """Test retrieving a specific event."""
    # Create event
    create_response = client.post(
        "/api/v1/events",
        json={
            "event_type": "DIVIDEND",
            "symbol": "GOOGL",
            "amount": 0.30,
            "ex_date": "2024-11-15",
            "record_date": "2024-11-18",
            "payment_date": "2024-11-25",
        },
    )
    event_id = create_response.json()["id"]
    
    # Get event
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["symbol"] == "GOOGL"


def test_get_nonexistent_event(client: TestClient) -> None:
    """Test retrieving non-existent event returns 404."""
    response = client.get("/api/v1/events/99999")
    assert response.status_code == 404


def test_cancel_event(client: TestClient) -> None:
    """Test cancelling an event."""
    # Create event
    create_response = client.post(
        "/api/v1/events",
        json={
            "event_type": "DIVIDEND",
            "symbol": "META",
            "amount": 0.20,
            "ex_date": "2024-11-15",
            "record_date": "2024-11-18",
            "payment_date": "2024-11-25",
        },
    )
    event_id = create_response.json()["id"]
    
    # Cancel event
    response = client.post(f"/api/v1/events/{event_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CANCELLED"


def test_idempotency(client: TestClient) -> None:
    """Test idempotency key prevents duplicates."""
    event_data = {
        "event_type": "DIVIDEND",
        "symbol": "NFLX",
        "amount": 0.25,
        "ex_date": "2024-11-15",
        "record_date": "2024-11-18",
        "payment_date": "2024-11-25",
        "idempotency_key": "test-key-123",
    }
    
    # First request succeeds
    response1 = client.post("/api/v1/events", json=event_data)
    assert response1.status_code == 201
    
    # Second request with same key fails
    response2 = client.post("/api/v1/events", json=event_data)
    assert response2.status_code == 409


def test_invalid_symbol(client: TestClient) -> None:
    """Test invalid symbol format is rejected."""
    event_data = {
        "event_type": "DIVIDEND",
        "symbol": "invalid symbol with spaces",
        "amount": 0.25,
        "ex_date": "2024-11-15",
        "record_date": "2024-11-18",
        "payment_date": "2024-11-25",
    }
    
    response = client.post("/api/v1/events", json=event_data)
    assert response.status_code == 422  # Validation error


def test_metrics_endpoint(client: TestClient) -> None:
    """Test metrics endpoint."""
    # Create some events
    client.post(
        "/api/v1/events",
        json={
            "event_type": "DIVIDEND",
            "symbol": "TEST",
            "amount": 0.25,
            "ex_date": "2024-11-15",
            "record_date": "2024-11-18",
            "payment_date": "2024-11-25",
        },
    )
    
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data
    assert "events_by_type" in data
    assert "events_by_status" in data
    assert data["total_events"] >= 1
