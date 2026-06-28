# Google Cloud Agent Engines Deployment

Google Cloud Agent Engines provides a serverless platform to deploy and scale AI agents built with ADK.

## Deployment Steps

1. Configure Google Cloud project:
```bash
gcloud config set project <project-id>
```

2. Deploy the agent using the Agents CLI:
```bash
agents-cli deploy
```

This command packages your agent container, registers the endpoints, and makes it available to Gemini Enterprise.

## Local Playground Testing

Before deploying, you can run the local interactive playground to test the agent logic and tools:
```bash
agents-cli playground
```
This launches a local web UI where you can send queries to your agent.
