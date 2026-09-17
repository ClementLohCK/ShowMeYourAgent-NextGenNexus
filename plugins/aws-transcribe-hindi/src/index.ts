import { AwsTranscribeHindi, type TranscriptionConfig } from "./transcribe.js";

export type OpenClawPluginApi = {
  registerMediaUnderstandingProvider?: (provider: {
    id: string;
    transcribe: AwsTranscribeHindi["transcribe"];
  }) => void;
};

export const createAwsTranscribeHindi = (config: TranscriptionConfig): AwsTranscribeHindi =>
  new AwsTranscribeHindi(config);

export default {
  id: "aws-transcribe-hindi",
  name: "AWS Transcribe Hindi",
  description: "Transcribe inbound OpenClaw audio with AWS Transcribe.",
  register(api: OpenClawPluginApi) {
    const region = process.env.AWS_REGION;
    const outputBucket = process.env.AWS_TRANSCRIBE_OUTPUT_BUCKET;

    if (!region || !outputBucket) {
      throw new Error(
        "AWS_REGION and AWS_TRANSCRIBE_OUTPUT_BUCKET are required for aws-transcribe-hindi",
      );
    }

    const provider = createAwsTranscribeHindi({ region, outputBucket });
    api.registerMediaUnderstandingProvider?.({
      id: "aws-transcribe-hindi",
      transcribe: provider.transcribe.bind(provider),
    });
  },
};
