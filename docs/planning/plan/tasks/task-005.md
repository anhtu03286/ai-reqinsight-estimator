# Task 005 — Object Storage & Message Queue Setup

## Metadata
- **Epic:** EPIC-00 Foundation
- **Story:** S-00d
- **Owner:** Backend Dev / DevOps
- **Status:** Done ✓

## Goal

Configure Object Storage (file upload) and Message Queue (async jobs) for both dev and production environments.

## Files

- `src/storage/storage_service.py`
- `src/queue/queue_service.py`
- `src/queue/events.py`
- `docker-compose.dev.yml`

## Dependencies

- Task 001 (tech stack)

## Acceptance Criteria

- [x] `StorageService.upload(file, key)` saves the file and returns a storage key
- [x] `StorageService.download(key)` returns a file stream
- [x] Files are server-side encrypted (AES-256 SSE) at rest
- [x] `QueueService.publish(event, payload)` pushes a message onto the queue
- [x] `QueueService.subscribe(event, handler)` receives and processes messages
- [x] Dead letter queue exists for failed jobs
- [x] `docker-compose.dev.yml` runs successfully with `docker compose up`
- [x] Env vars: `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `REDIS_URL` (no hardcoding)

## Tests Required

- Unit: upload → storage key returned in correct format
- Unit: publish event → subscriber receives correct payload
- Integration (local): upload a real file → download it back → content matches
- Integration (local): publish → consumer handler is called

## Notes

- Dev: MinIO (S3-compatible local) + Redis
- Prod: AWS S3 + SQS or Upstash Redis (depending on infra)
- Interface-based design so swapping implementations does not affect business logic
