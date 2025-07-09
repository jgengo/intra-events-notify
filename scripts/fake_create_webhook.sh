#!/usr/bin/env bash
# Send a fake webhook to a local intra-events-notify instance.
# This is useful for testing the webhook endpoint without creating real events.

WEBHOOK_URL="${WEBHOOK_URL:-http://localhost:8000/webhooks/events}"
WEBHOOK_EVENT_SECRET="${WEBHOOK_EVENT_SECRET:-FAKE-EVENT-SECRET}"

DELIVERY_ID="$(date +%s)"

read -r -d '' PAYLOAD <<'JSON'
{
  "id": 33480,
  "begin_at": "2025-07-09 18:00:00 UTC",
  "end_at": "2025-07-09 19:00:00 UTC",
  "name": "🩵 Running just a test",
  "description": "I'm sorry for the ping, just running one last test.",
  "location": "Titus' Boiler Room",
  "kind": "conference",
  "max_people": 1,
  "prohibition_of_cancellation": null,
  "campus_ids": [13],
  "cursus_ids": [1],
  "created_at": "2025-07-09 17:36:23 UTC",
  "updated_at": "2025-07-09 17:36:23 UTC"
}
JSON

echo "Sending webhook to: $WEBHOOK_URL"
echo "Delivery ID: $DELIVERY_ID"

curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Secret: ${WEBHOOK_EVENT_SECRET}" \
  -H "X-Model: event" \
  -H "X-Event: create" \
  -H "X-Delivery: ${DELIVERY_ID}" \
  -d "$PAYLOAD"

printf '\n'