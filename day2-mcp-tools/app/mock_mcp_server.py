# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from mcp.server.fastmcp import FastMCP

# Initialize the mock Developer Knowledge MCP server
mcp = FastMCP("Google Developer Knowledge Mock Server")

# Resolve docs directory relative to the location of this script
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))


@mcp.tool()
def search_documents(query: str) -> str:
    """Queries the documentation corpus to find relevant pages and snippets.

    Args:
        query: The search term or phrase to query in the developer docs.

    Returns:
        A list of matching document IDs and relevant snippets.
    """
    if not os.path.exists(DOCS_DIR):
        return f"Error: docs directory not found at {DOCS_DIR}"

    results = []
    query_lower = query.lower()

    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(DOCS_DIR, filename)
            try:
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue

            if query_lower in content.lower() or query_lower in filename.lower():
                lines = content.split("\n")
                snippets = []
                for line in lines:
                    if query_lower in line.lower() and len(line.strip()) > 3:
                        snippets.append(line.strip())
                snippet_text = "\n  > ".join(snippets[:2]) if snippets else lines[0]
                results.append(
                    f"- **{filename[:-3]}** (ID: {filename})\n  Snippet: {snippet_text}"
                )

    if not results:
        return f"No documentation found matching: '{query}'"
    return "Search Results:\n" + "\n".join(results)


@mcp.tool()
def get_document(doc_name: str) -> str:
    """Retrieves the full content of a specific document by its name/ID.

    Args:
        doc_name: The name or ID of the document to retrieve (e.g. adk_guidance.md).

    Returns:
        The complete markdown content of the document.
    """
    if not doc_name.endswith(".md"):
        doc_name += ".md"

    filepath = os.path.join(DOCS_DIR, doc_name)
    if not os.path.exists(filepath):
        # Fallback to check basename
        base_name = os.path.basename(doc_name)
        filepath = os.path.join(DOCS_DIR, base_name)
        if not os.path.exists(filepath):
            return f"Error: Document '{doc_name}' not found."

    try:
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading document: {e}"


@mcp.tool()
def get_documents(doc_names: list[str]) -> str:
    """Retrieves the full content of multiple specified documents.

    Args:
        doc_names: A list of document names or IDs to retrieve.

    Returns:
        The combined contents of the documents.
    """
    results = []
    for name in doc_names:
        results.append(f"=== Document: {name} ===\n" + get_document(name))
    return "\n\n".join(results)


if __name__ == "__main__":
    mcp.run()
