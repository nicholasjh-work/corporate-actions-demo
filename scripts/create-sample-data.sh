#!/bin/bash

echo "🎬 Creating sample corporate action events..."
echo ""

API_URL="http://localhost:8000/api/v1"

# Create dividend event
echo "📊 Creating DIVIDEND event for AAPL..."
curl -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "DIVIDEND",
    "symbol": "AAPL",
    "amount": 0.24,
    "ex_date": "2024-11-15",
    "record_date": "2024-11-18",
    "payment_date": "2024-11-25"
  }' | jq .

sleep 1

# Create stock split event
echo ""
echo "📊 Creating STOCK_SPLIT event for TSLA..."
curl -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "STOCK_SPLIT",
    "symbol": "TSLA",
    "split_ratio_from": 1,
    "split_ratio_to": 3,
    "effective_date": "2024-12-01"
  }' | jq .

sleep 1

# Create merger event
echo ""
echo "📊 Creating MERGER event for MSFT acquiring ATVI..."
curl -X POST "$API_URL/events" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "MERGER",
    "symbol": "MSFT",
    "target_symbol": "ATVI",
    "exchange_ratio": 1.5,
    "cash_component": 95.00,
    "effective_date": "2024-12-15"
  }' | jq .

sleep 1

# Create more events for metrics
echo ""
echo "📊 Creating additional events for metrics..."

for symbol in GOOGL AMZN META NFLX; do
  curl -s -X POST "$API_URL/events" \
    -H "Content-Type: application/json" \
    -d "{
      \"event_type\": \"DIVIDEND\",
      \"symbol\": \"$symbol\",
      \"amount\": 0.25,
      \"ex_date\": \"2024-11-20\",
      \"record_date\": \"2024-11-23\",
      \"payment_date\": \"2024-11-30\"
    }" > /dev/null
  echo "   ✅ Created DIVIDEND for $symbol"
  sleep 0.5
done

echo ""
echo "✨ Sample events created!"
echo ""
echo "📊 View events at: http://localhost:3000"
echo "📈 View metrics at: http://localhost:8000/api/v1/metrics"
echo ""
