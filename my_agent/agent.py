from google.adk.agents.llm_agent import Agent

from google.adk.tools.google_search_tool import google_search
from google.adk.tools.agent_tool import AgentTool


from google.adk.tools.mcp_tool import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)

mcp_toolbox = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:8000/mcp",
    )
)

search_agent = Agent(
    name="SearchExpert",
    model="gemini-2.5-flash",
    description="Searches the web for accurate and comprehensive information.",
    instruction="""
        Search the web for relevant information.
        Cross-reference multiple sources for accuracy.
        Return a summary with source URLs.
    """,
    tools=[
        google_search
    ]
)


file_manager_agent = Agent(
    name="FileManager",
    model="gemini-2.5-flash",
    description="Manages files in /data directory via the MCP server.",
    instruction="""
        Use MCP server tools to manage files in /data:
        - read_file: Read file content
        - create_file: Create new files
        - update_file: Update existing files
        - delete_file: Delete files
    """,
    tools=[mcp_toolbox]
)


plagiarism_checker_agent = Agent(
    name="PlagiarismChecker",
    model="gemini-2.5-flash",
    description="Checks content for plagiarism using the MCP server.",
    instruction="""
        Use check_plagiarism tool from MCP server.
        Pass article content and online sources.
        Return the plagiarism report with percentage.
    """,
    tools=[mcp_toolbox]
)


citation_agent = Agent(
    name="CitationManager",
    model="gemini-2.5-flash",
    description="Adds citations to articles using the MCP server.",
    instruction="""
        Use add_citations tool from MCP server.
        Pass article content and sources.
        Return the article with citations added.
    """,
    tools=[mcp_toolbox]
)


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Main orchestrator that coordinates all specialized agents.",
    instruction="""
        You coordinate specialized agents based on user requests:
        
        AGENTS:
        - SearchExpert: Web searches
        - FileManager: File operations in /data
        - PlagiarismChecker: Plagiarism detection
        - CitationManager: Add citations to articles
        
        PLAGIARISM WORKFLOW:
        1. FileManager reads the article
        2. SearchExpert finds similar content online
        3. PlagiarismChecker analyzes for plagiarism
        
        CITATION WORKFLOW:
        1. FileManager reads the article
        2. SearchExpert finds authoritative sources
        3. CitationManager adds citations
        4. FileManager saves the result
        
        Coordinate agents as needed and summarize results clearly.
    """,
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=file_manager_agent),
        AgentTool(agent=plagiarism_checker_agent),
        AgentTool(agent=citation_agent)
    ]
)
