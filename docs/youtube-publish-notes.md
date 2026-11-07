# Optional YouTube Publish Hooks

Research notes for integrating with YouTube Data API v3.

## Requirements

- Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 client credentials (not API key alone)
- Scope: `https://www.googleapis.com/auth/youtube.upload` (minimal for upload)
- Resumable upload protocol recommended for reliability
- Quota: 100 uploads/day per project (separate bucket)
- Important: Unverified projects (post-2020) can only upload **private** videos until Google compliance audit

## Minimal Flow

1. User authorizes via OAuth consent (store refresh token)
2. POST to `https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status`
3. Send metadata (title, description, tags, privacyStatus)
4. Upload binary in chunks
5. Store returned video ID + URL in harness metadata JSON

## Harness Integration Points

- After video generation, optional stage: `publish_to_youtube(video_path, metadata)`
- Update metadata record with `youtube_id` and `youtube_url`
- Platform can link out or embed when available
- Always keep local MP4 + transcript as source of truth

## References

- https://developers.google.com/youtube/v3/docs/videos/insert
- https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol

No live upload is performed in this harness by default; credentials stay user-side.
