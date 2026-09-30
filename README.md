# AI SRE Agent

A containerized AI agent built with Amazon Bedrock, Amazon Bedrock AgentCore,
Strands Agents, Python, and Docker.

This project was created while exploring AI-powered Site Reliability
Engineering workflows and AWS agent infrastructure.

## Tech Stack

- Python 3.12
- Amazon Bedrock
- Amazon Bedrock AgentCore
- Strands Agents
- Anthropic Claude Haiku 4.5
- Boto3
- Docker
- AWS CLI

## Architecture

```text
Client
  |
  | POST /invocations
  v
Docker Container
  |
  v
Bedrock AgentCore App
  |
  v
Strands Agent
  |
  v
Amazon Bedrock
  |
  v
Claude Haiku 4.5
