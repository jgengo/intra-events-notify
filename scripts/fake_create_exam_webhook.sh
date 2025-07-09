#!/usr/bin/env bash
# Send a fake exam webhook to a local intra-events-notify instance for testing.

WEBHOOK_URL="${WEBHOOK_URL:-http://localhost:8000/webhooks/exams}"
WEBHOOK_SECRET="${WEBHOOK_SECRET:-FAKE-WEBHOOK-SECRET}"

DELIVERY_ID="$(date +%s)"

read -r -d '' PAYLOAD <<'JSON'
{
  "id": 4978,
  "begin_at": "2021-07-08 19:00:00 UTC",
  "end_at": "2021-07-08 21:00:00 UTC",
  "location": "c1r16,c1r17",
  "ip_range": "10.11.16.0/16,10.11.17.0/16",
  "max_people": 50,
  "visible": true,
  "name": "Exam Session Afternoon",
  "campus_id": 22,
  "created_at": "2021-07-06 18:00:21 UTC",
  "updated_at": "2021-07-08 15:24:53 UTC",
  "projects": []
}
JSON

curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Secret: ${WEBHOOK_SECRET}" \
  -H "X-Model: exam" \
  -H "X-Event: create" \
  -H "X-Delivery: ${DELIVERY_ID}" \
  -d "$PAYLOAD"

echo
echo "Sent exam webhook to $WEBHOOK_URL"

