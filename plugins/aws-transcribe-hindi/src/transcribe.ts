import {
  GetTranscriptionJobCommand,
  StartTranscriptionJobCommand,
  TranscribeClient,
} from "@aws-sdk/client-transcribe";

export type TranscriptionConfig = {
  region: string;
  outputBucket: string;
  languageCode?: string;
  pollIntervalMs?: number;
  timeoutMs?: number;
};

export type AudioInput = {
  jobId: string;
  mediaUri: string;
  mediaFormat: "ogg" | "mp3" | "mp4" | "wav" | "flac" | "amr" | "webm";
};

export class AwsTranscribeHindi {
  private readonly client: TranscribeClient;
  private readonly config: Required<TranscriptionConfig>;

  constructor(config: TranscriptionConfig) {
    this.client = new TranscribeClient({ region: config.region });
    this.config = {
      languageCode: "hi-IN",
      pollIntervalMs: 2000,
      timeoutMs: 120000,
      ...config,
    };
  }

  async transcribe(input: AudioInput): Promise<string> {
    await this.client.send(
      new StartTranscriptionJobCommand({
        TranscriptionJobName: input.jobId,
        LanguageCode: this.config.languageCode,
        MediaFormat: input.mediaFormat,
        Media: { MediaFileUri: input.mediaUri },
        OutputBucketName: this.config.outputBucket,
      }),
    );

    const deadline = Date.now() + this.config.timeoutMs;
    while (Date.now() < deadline) {
      const result = await this.client.send(
        new GetTranscriptionJobCommand({ TranscriptionJobName: input.jobId }),
      );
      const job = result.TranscriptionJob;

      if (job?.TranscriptionJobStatus === "COMPLETED") {
        const transcriptUri = job.Transcript?.TranscriptFileUri;
        if (!transcriptUri) throw new Error("AWS Transcribe returned no transcript URI");
        return fetch(transcriptUri).then(async (response) => {
          if (!response.ok) throw new Error(`Transcript download failed: ${response.status}`);
          const body = (await response.json()) as { results?: { transcripts?: { transcript?: string }[] } };
          const transcript = body.results?.transcripts?.[0]?.transcript?.trim();
          if (!transcript) throw new Error("AWS Transcribe returned an empty transcript");
          return transcript;
        });
      }

      if (job?.TranscriptionJobStatus === "FAILED") {
        throw new Error(job.FailureReason || "AWS Transcribe job failed");
      }

      await new Promise((resolve) => setTimeout(resolve, this.config.pollIntervalMs));
    }

    throw new Error("AWS Transcribe job timed out");
  }
}
