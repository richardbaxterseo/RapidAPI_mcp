# RapidAPI MCP
[![smithery badge](https://smithery.ai/badge/@SecurFi/rapidapi_mcp)](https://smithery.ai/server/@SecurFi/rapidapi_mcp)

``` bash
uv add -r requirements.txt

# install the server in Claude (and restart Claude manually)
fastmcp install server.py

# debug in the inspector
fastmcp dev server.py
```
## claude config
```
    "RapidAPI": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
	      "--with",
	      "requests",
        "fastmcp",
        "run",
        "/Users/{YOUR_USERNAME}/Documents/rapidapi_mcp/server.py"
      ]
    }
```
