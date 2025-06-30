# Python Code Executor Service

A Flask-based service that automatically executes Python scripts in a secure Cloud Run sandbox environment. This service provides instant Python code execution through a simple REST API, making it perfect for automation, CI/CD pipelines, and remote code execution scenarios.

## Key Features

- **Automatic Execution**: Submit Python code and get results instantly
- **Cloud Run Sandbox**: Secure, isolated execution environment
- **Zero Setup**: No need to install Python packages locally
- **CI/CD Ready**: Perfect for automated testing and deployment pipelines
- **Real-time Output**: Captures both return values and stdout output
- **Error Handling**: Comprehensive error reporting and validation
- **JSON API**: RESTful interface for easy integration

## How It Works

The service runs your Python code in Google Cloud Run's secure sandbox environment. Simply send a POST request with your Python script, and the service will:

1. Validate your script format
2. Execute it in an isolated environment
3. Capture all outputs and results
4. Return structured JSON response

## Script Requirements

Your Python script must follow these simple rules:

1. **Define a `main()` function**: This serves as the entry point
2. **Return JSON-serializable data**: The return value will be converted to JSON
3. **Handle imports within the script**: Import any required libraries inside your script

## Usage Examples

### Basic Example

```bash
curl -X POST https://py-executor-service-57650711197.us-central1.run.app/execute \
     -H "Content-Type: application/json" \
     -d '{
  "script": "def main():\n    result = 2 + 2\n    print(\"Calculation completed!\")\n    return {\"calculation\": \"2 + 2\", \"result\": result}"
}' | python -m json.tool
```

**Response:**
```json
{
  "result": {
    "calculation": "2 + 2", 
    "result": 4
  },
  "stdout": "Calculation completed!\n"
}
```

### Data Science Example

```bash
curl -X POST https://py-executor-service-57650711197.us-central1.run.app/execute \
     -H "Content-Type: application/json" \
     -d '{
  "script": "import numpy as np\nimport pandas as pd\ndef main():\n    print(\"Creating a pandas DataFrame...\")\n    s = pd.Series([1, 3, 5, np.nan, 6, 8])\n    print(\"DataFrame created!\")\n    return {\"sum\": s.sum(), \"is_json\": True}"
}' | python -m json.tool
```

**Response:**
```json
{
  "result": {
    "sum": 23.0,
    "is_json": true
  },
  "stdout": "Creating a pandas DataFrame...\nDataFrame created!\n"
}
```


## Automated CI/CD Deployment

This project features **automated CI/CD deployment** that automatically builds and deploys the service to Google Cloud Run whenever changes are pushed to the repository.


## Security & Limitations

- **Sandbox Environment**: Code runs in Cloud Run's isolated containers
- **Resource Limits**: Execution time and memory are limited by Cloud Run
- **No Persistent Storage**: Each execution is stateless
- **Authentication**: Consider adding authentication for production use
- **Rate Limiting**: Implement rate limiting for production deployments

## Error Handling

The service handles various error scenarios:

- **Missing `script` field**: Returns 400 error
- **No `main()` function**: Returns 400 error  
- **Runtime errors**: Returns 400 with error details
- **Non-serializable returns**: Returns 400 error
- **Invalid JSON**: Returns 400 error

Example error response:
```json
{
  "error": "NameError: name 'undefined_variable' is not defined",
  "stdout": "Some output before error\n"
}
```


## API Reference

### Execute Script

**Endpoint:** `POST /execute`

**Request Body:**
```json
{
  "script": "def main():\n    return {'result': 'success'}"
}
```

**Success Response (200):**
```json
{
  "result": {"result": "success"},
  "stdout": ""
}
```

**Error Response (400):**
```json
{
  "error": "Error description",
  "stdout": "Any output before error"
}
```

## License

This project is licensed under the MIT License. 