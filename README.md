# MotorAPI MCP Server

MCP (Model Context Protocol) integration for [MotorAPI.dk](https://motorapi.dk) - Danish vehicle registration lookup service.

## Features

This MCP server provides tools to lookup Danish vehicle information by registration number or VIN:

- **get_vehicle**: Get detailed vehicle information (make, model, year, specifications, etc.)
- **get_vehicle_environment**: Get environmental data (emissions, fuel consumption, environmental class)
- **get_vehicle_equipment**: Get equipment and features list
- **get_api_usage**: Check API usage statistics and quota

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ShredderAlex/motorapi-mcp.git
cd motorapi-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set your API key as an environment variable:
```bash
export MOTORAPI_KEY="your-api-key-here"
```

Note: A default API key is included for testing, but you should obtain your own from [MotorAPI.dk](https://motorapi.dk)

## Usage

### Running the Server

Run the MCP server:
```bash
python server.py
```

### Using with Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "motorapi": {
      "command": "python",
      "args": ["/path/to/motorapi-mcp/server.py"],
      "env": {
        "MOTORAPI_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

### Example Queries

Once connected, you can ask Claude:

- "Look up vehicle information for registration AB12345"
- "Get environmental data for VIN WBA12345678901234"
- "Show me the equipment list for registration XY98765"
- "Check my MotorAPI usage statistics"

## API Endpoints

The server integrates these MotorAPI.dk endpoints:

- `GET /vehicles/{reg-no-or-vin}` - Vehicle details
- `GET /vehicles/{reg-no-or-vin}/environment` - Environmental data
- `GET /vehicles/{reg-no-or-vin}/equipment` - Equipment list
- `GET /usage` - API usage statistics

## Cloud Deployment

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ShredderAlex/motorapi-mcp)

#### Manual Render Deployment

1. Fork this repository to your GitHub account
2. Sign up/login to [Render](https://render.com)
3. Create a new **Web Service**
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: motorapi-mcp (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
6. Add environment variable:
   - **Key**: `MOTORAPI_KEY`
   - **Value**: Your MotorAPI.dk API key
7. Click **Create Web Service**

#### Using render.yaml (Infrastructure as Code)

The repository includes a `render.yaml` file for automated deployment:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Set the `MOTORAPI_KEY` environment variable
6. Click **Apply**

**Note**: The server uses only pure Python dependencies (no Rust compilation required), ensuring fast and reliable builds on Render's free tier.

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/ShredderAlex/motorapi-mcp)

1. Click the button above or create a new project on Railway
2. Connect your GitHub repository
3. Set the `MOTORAPI_KEY` environment variable
4. Deploy!

## Development

### Project Structure

```
motorapi-mcp/
├── server.py           # Main MCP server implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── pyproject.toml     # Python project configuration
├── railway.json       # Railway deployment configuration
├── render.yaml        # Render deployment configuration
└── .gitignore         # Git ignore rules
```

### Testing

Test the server using the MCP inspector:

```bash
pip install mcp-inspector
mcp-inspector python server.py
```

## Error Handling

The server includes proper error handling for:

- 404 Not Found (vehicle doesn't exist)
- Network errors
- API authentication errors
- Timeout errors

Errors are returned as JSON objects with an `error` field.

## Dependencies

This project uses only pure Python packages with no Rust compilation required:

- **mcp** (>=1.0.0) - Model Context Protocol SDK
- **httpx** (>=0.27.0) - Modern async HTTP client

This ensures fast builds and compatibility with all cloud platforms.

## License

MIT License - feel free to use and modify as needed.

## Resources

- [MotorAPI.dk Documentation](https://motorapi.dk)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/ShredderAlex/motorapi-mcp/issues)
- Check MotorAPI.dk documentation for API-related questions
