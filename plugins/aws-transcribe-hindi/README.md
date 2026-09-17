# AWS Transcribe Hindi provider

This plugin is the first implementation slice for routing inbound OpenClaw audio to AWS Transcribe.

## Current scope

- AWS Transcribe adapter with Hindi (`hi-IN`) as the default language.
- Polling, timeout, failed-job, empty-transcript, and transcript-download handling.
- Provider package metadata reserved for OpenClaw media-understanding registration.

## Required runtime configuration

- AWS credentials supplied through the normal AWS SDK credential chain.
- `AWS_REGION`.
- An S3 output bucket that the OpenClaw runtime can write to and read from.
- A Telegram media download/upload adapter supplied by the host runtime.

## Next integration step

Wire `AwsTranscribeHindi` into the OpenClaw media-understanding provider registration for inbound Telegram voice/audio events. The handler should pass a stable, deduplicated job ID and an S3 media URI, then inject the returned transcript into the existing agent session. It must not create a second Telegram receiver.
