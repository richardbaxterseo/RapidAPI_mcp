# YouTube Transcript MCP Server

A Model Context Protocol (MCP) server that provides YouTube video transcript functionality through RapidAPI.

## Features

- Get transcripts for any YouTube video
- Support for multiple languages
- Three different output formats:
  - Full transcript data with metadata
  - Plain text transcript
  - Transcript with timestamps
- Handles various YouTube URL formats and video IDs

## Prerequisites

- Python 3.8+
- RapidAPI account with access to [YouTube Transcript API](https://rapidapi.com/solid-api-solid-api-default/api/youtube-transcript3)
- `uv` (recommended) or `pip` for package management

## Installation

### Option 1: Using uv (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/richardbaxterseo/RapidAPI_mcp.git
cd RapidAPI_mcp
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Option 2: Using pip

1. Clone the repository:
```bash
git clone https://github.com/richardbaxterseo/RapidAPI_mcp.git
cd RapidAPI_mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### For Claude Desktop

1. Open your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the YouTube Transcript MCP server:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "requests",
        "python",
        "/path/to/RapidAPI_mcp/server.py"
      ],
      "env": {
        "RAPIDAPI_KEY": "your-rapidapi-key-here"
      }
    }
  }
}
```

If you're not using `uv`, use this configuration instead:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python",
      "args": ["/path/to/RapidAPI_mcp/server.py"],
      "env": {
        "RAPIDAPI_KEY": "your-rapidapi-key-here"
      }
    }
  }
}
```

3. Replace `/path/to/RapidAPI_mcp` with the actual path to your cloned repository
4. Replace `your-rapidapi-key-here` with your actual RapidAPI key

### For Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python",
      "args": ["/path/to/RapidAPI_mcp/server.py"],
      "env": {
        "RAPIDAPI_KEY": "your-rapidapi-key-here"
      }
    }
  }
}
```

## Usage

Once configured, the MCP server provides three tools:

### 1. get_youtube_transcript
Get full transcript data including metadata:
```
Get the transcript for video dQw4w9WgXcQ
```

### 2. get_youtube_transcript_text
Get plain text transcript without timestamps:
```
Get the plain text transcript for https://youtube.com/watch?v=dQw4w9WgXcQ
```

### 3. get_youtube_transcript_with_timestamps
Get transcript segments with timing information:
```
Get the timestamped transcript for the video at https://youtu.be/dQw4w9WgXcQ
```

## Supported Input Formats

The server accepts various YouTube URL formats:
- Video ID: `dQw4w9WgXcQ`
- Standard URL: `https://youtube.com/watch?v=dQw4w9WgXcQ`
- Short URL: `https://youtu.be/dQw4w9WgXcQ`
- Embed URL: `https://youtube.com/embed/dQw4w9WgXcQ`

## Testing

### Using FastMCP Inspector

```bash
fastmcp dev server.py
```

### Manual Testing

```bash
python server.py
```

## Troubleshooting

1. **"RapidAPI key is required" error**
   - Ensure you've set the `RAPIDAPI_KEY` environment variable in your MCP configuration

2. **"API request failed" errors**
   - Verify your RapidAPI key is valid
   - Check if you have access to the YouTube Transcript API on RapidAPI
   - Ensure you haven't exceeded your API rate limits

3. **MCP server not showing in Claude**
   - Restart Claude Desktop after updating the configuration
   - Check that the path to server.py is correct
   - Verify Python is in your system PATH

## API Limits

Please check your RapidAPI subscription for rate limits and usage quotas.

## License

This project is based on the original RapidAPI_mcp by SecurFi.
