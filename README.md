# SeoImproverAgents

A multi-agent system for content analysis with plagiarism detection and citation management, powered by Google Gemini and MCP.

## Overview

This project consists of:
- **MCP Server** (`main.py`) - File management and AI-powered content analysis tools
- **Agent System** (`my_agent/agent.py`) - Coordinated agents for automated workflows

## MCP Server Tools

| Tool | Description |
|------|-------------|
| `list_files` | List all files in /data directory |
| `read_file` | Read file content |
| `create_file` | Create new files |
| `update_file` | Update existing files |
| `delete_file` | Delete files |
| `check_plagiarism` | Analyze content for plagiarism |
| `add_citations` | Add citations to articles |

## Agents

- **SearchExpert** - Web searches for information
- **FileManager** - File operations via MCP
- **PlagiarismChecker** - Plagiarism detection
- **CitationManager** - Add citations to articles
- **root_agent** - Orchestrates all agents

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create `.env` file with your API key:
```
GOOGLE_API_KEY=your_api_key_here
```

3. Run the MCP server:
```bash
uv run main.py
```

4. Run the agent:
```bash
adk run my_agent
```

## Usage

The root agent can:
- Check articles for plagiarism
- Add citations to content
- Manage files in /data directory
- Search the web for information