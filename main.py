"""
FastMCP server with file management and AI-powered plagiarism/citation tools.
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path
from google import genai
import os

import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Create an MCP server
mcp = FastMCP(
    "ContentAnalyzer",
    instructions="MCP server for file management, plagiarism detection, and citation generation. Provides CRUD operations for files in /data directory and AI-powered content analysis tools.",
    json_response=True
)

# Base path for data directory
DATA_DIR = Path(__file__).parent / "data"


# List all files in /data directory
@mcp.tool()
def list_files() -> str:
    """List all files in the /data directory"""
    try:
        if not DATA_DIR.exists():
            return "Error: /data directory does not exist"
        files = [f.name for f in DATA_DIR.iterdir() if f.is_file()]
        if not files:
            return "No files found in /data directory"
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


# Read file from /data directory
@mcp.tool()
def read_file(filename: str) -> str:
    """Read content from a file in the /data directory"""
    data_path = DATA_DIR / filename
    if not data_path.exists():
        return f"Error: File '{filename}' not found in /data directory"
    if not data_path.is_file():
        return f"Error: '{filename}' is not a file"
    try:
        return data_path.read_text()
    except Exception as e:
        return f"Error reading file: {str(e)}"


# Create file in /data directory
@mcp.tool()
def create_file(filename: str, content: str) -> str:
    """Create a new file in the /data directory with the specified content"""
    data_path = DATA_DIR / filename
    if data_path.exists():
        return f"Error: File '{filename}' already exists in /data directory"
    try:
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.write_text(content)
        return f"Successfully created file '{filename}'"
    except Exception as e:
        return f"Error creating file: {str(e)}"


# Update file in /data directory
@mcp.tool()
def update_file(filename: str, content: str) -> str:
    """Update an existing file in the /data directory with new content"""
    data_path = DATA_DIR / filename
    if not data_path.exists():
        return f"Error: File '{filename}' not found in /data directory"
    if not data_path.is_file():
        return f"Error: '{filename}' is not a file"
    try:
        data_path.write_text(content)
        return f"Successfully updated file '{filename}'"
    except Exception as e:
        return f"Error updating file: {str(e)}"


# Delete file from /data directory
@mcp.tool()
def delete_file(filename: str) -> str:
    """Delete a file from the /data directory"""
    data_path = DATA_DIR / filename
    if not data_path.exists():
        return f"Error: File '{filename}' not found in /data directory"
    if not data_path.is_file():
        return f"Error: '{filename}' is not a file"
    try:
        data_path.unlink()
        return f"Successfully deleted file '{filename}'"
    except Exception as e:
        return f"Error deleting file: {str(e)}"


# Check plagiarism using Gemini
@mcp.tool()
def check_plagiarism(article_content: str, online_sources: str) -> str:
    """
    Analyze article content for plagiarism by comparing with online sources.
    Returns plagiarism percentage and matched sections.
    """
    try:
        prompt = f"""
        Compare the following article with the online sources provided.
        Find matching or similar text between them.
        Calculate a plagiarism percentage.
        List the matched sections with their source URLs.
        
        ARTICLE:
        {article_content}
        
        ONLINE SOURCES:
        {online_sources}
        
        Provide a clear report with:
        1. Overall plagiarism percentage
        2. List of matched sections
        3. Source URLs for each match
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text or "No response generated"
    except Exception as e:
        return f"Error checking plagiarism: {str(e)}"


# Add citations using Gemini
@mcp.tool()
def add_citations(article_content: str, sources: str) -> str:
    """
    Add citation markers and create a references section for the article.
    Returns the article with citations added.
    """
    try:
        prompt = f"""
        Add citation markers [1], [2], etc. to statements in the article.
        Match each citation to the provided sources.
        Create a References section at the end with source URLs.
        Return the complete article with citations added.
        
        ARTICLE:
        {article_content}
        
        SOURCES:
        {sources}
        
        Return the full article with inline citations and a References section at the end.
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text or "No response generated"
    except Exception as e:
        return f"Error adding citations: {str(e)}"


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
