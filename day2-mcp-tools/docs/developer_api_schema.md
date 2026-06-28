# Google Developer API Request Schema

This document details the strict schema and structure for making a Google Developer API request.

## Authentication Headers

All requests to Google Developer APIs (including the Developer Knowledge API) must include the following headers for authentication and content negotiation:

```http
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
X-Goog-Api-Key: <API_KEY> (used for direct Developer Knowledge API validation)
```

## Request URI Template

Requests follow the standard Google API path pattern:

```http
POST https://developerknowledge.googleapis.com/mcp
```

## Strict JSON Payload Schema

Google Developer APIs follow the JSON-RPC 2.0 protocol when used with Model Context Protocol (MCP). The payload for calling tools, such as searching or retrieving documents, must strictly adhere to the following schema:

### 1. Tool Call Request (Client to Server)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_documents",
    "arguments": {
      "query": "strict schema"
    }
  },
  "id": 1
}
```

### 2. Tool Call Response (Server to Client)

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Detailed schema guidelines and snippets..."
      }
    ]
  },
  "id": 1
}
```

This strict message structure ensures seamless tool execution and validation between client and server.
