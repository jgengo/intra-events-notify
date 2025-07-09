#!/usr/bin/env bash
# Send a fake exam webhook to a local intra-events-notify instance for testing.

WEBHOOK_URL="${WEBHOOK_URL:-http://localhost:8000/webhooks/exams}"
WEBHOOK_EXAM_SECRET="${WEBHOOK_EXAM_SECRET:-FAKE-EXAM-SECRET}"

DELIVERY_ID="$(date +%s)"

read -r -d '' PAYLOAD <<'JSON'
{
  "id": 24484,
  "begin_at": "2025-07-09 18:00:00 UTC",
  "end_at": "2025-07-09 19:00:00 UTC",
  "location": "Jordane's home",
  "ip_range": "10.13.1.1/16",
  "max_people": 1,
  "visible": false,
  "name": "Exam",
  "campus_id": 13,
  "created_at": "2025-07-09 17:24:14 UTC",
  "updated_at": "2025-07-09 17:24:14 UTC",
  "projects": [
    {
      "name": "Exam Rank 02",
      "id": 1320,
      "slug": "exam-rank-02",
      "url": "https://projects.intra.42.fr/exam-rank-02/mine"
    },
    {
      "name": "Exam Rank 03",
      "id": 1321,
      "slug": "exam-rank-03",
      "url": "https://projects.intra.42.fr/exam-rank-03/mine"
    },
    {
      "name": "Exam Rank 04",
      "id": 1322,
      "slug": "exam-rank-04",
      "url": "https://projects.intra.42.fr/exam-rank-04/mine"
    },
    {
      "name": "Exam Rank 05",
      "id": 1323,
      "slug": "exam-rank-05",
      "url": "https://projects.intra.42.fr/exam-rank-05/mine"
    },
    {
      "name": "Exam Rank 06",
      "id": 1324,
      "slug": "exam-rank-06",
      "url": "https://projects.intra.42.fr/exam-rank-06/mine"
    }
  ]
}
JSON

curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Secret: ${WEBHOOK_EXAM_SECRET}" \
  -H "X-Model: exam" \
  -H "X-Event: create" \
  -H "X-Delivery: ${DELIVERY_ID}" \
  -d "$PAYLOAD"

echo
echo "Sent exam webhook to $WEBHOOK_URL"

