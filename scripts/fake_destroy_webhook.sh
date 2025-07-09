#!/usr/bin/env bash
# Send a fake webhook to a local intra-events-notify instance.
# This is useful for testing the webhook endpoint without creating real events.

WEBHOOK_URL="${WEBHOOK_URL:-http://localhost:8000/webhooks/events}"
WEBHOOK_EVENT_SECRET="${WEBHOOK_EVENT_SECRET:-FAKE-EVENT-SECRET}"

DELIVERY_ID="$(date +%s)"

read -r -d '' PAYLOAD <<'JSON'
{
  "id": 123,
  "begin_at": "2024-05-01 12:00:00 UTC",
  "end_at": "2024-05-01 14:00:00 UTC",
  "name": "Local Test Event",
  "description": "This is a fake event used for local webhook testing.",
  "location": "Helsinki",
  "kind": "event",
  "max_people": 42,
  "prohibition_of_cancellation": false,
  "campus_ids": [1],
  "cursus_ids": [1],
  "created_at": "2024-04-30 10:00:00 UTC",
  "updated_at": "2024-04-30 10:00:00 UTC"
}
JSON

curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Secret: ${WEBHOOK_EVENT_SECRET}" \
  -H "X-Model: event" \
  -H "X-Event: destroy" \
  -H "X-Delivery: ${DELIVERY_ID}" \
  -d "$PAYLOAD"

printf '\n'