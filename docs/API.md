# 📚 API Reference

Welcome to the PyEveryday API documentation. This RESTful API provides programmatic access to all automation tools and utilities available in PyEveryday.

## 🔗 Base URL

```
Production: https://api.pyeveryday.app/api/v1
Development: http://localhost:8000/api/v1
```

## 🔐 Authentication

Currently, the API is open and doesn't require authentication. Future versions will include:

- API key authentication
- OAuth 2.0 integration
- Rate limiting per user

## 📋 API Endpoints

### 🔧 Utilities

#### Currency Converter

Convert between different currencies using real-time exchange rates.

**Endpoint:** `POST /utilities/currency-convert`

**Request Body:**
```json
{
  "amount": 100.0,
  "from_currency": "USD",
  "to_currency": "EUR"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original_amount": 100.0,
    "converted_amount": 85.42,
    "from_currency": "USD",
    "to_currency": "EUR",
    "exchange_rate": 0.8542,
    "timestamp": "2024-08-22T10:30:00Z"
  }
}
```

**Example Usage:**
```bash
curl -X POST "https://api.pyeveryday.app/api/v1/utilities/currency-convert" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100,
    "from_currency": "USD", 
    "to_currency": "EUR"
  }'
```

#### Password Generator

Generate secure passwords with customizable criteria.

**Endpoint:** `POST /utilities/password-generate`

**Request Body:**
```json
{
  "length": 16,
  "include_uppercase": true,
  "include_lowercase": true,
  "include_numbers": true,
  "include_symbols": true,
  "exclude_ambiguous": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "password": "Kx7#mP9$nQ2&vR8!",
    "strength": "Very Strong",
    "entropy": 104.2,
    "estimated_crack_time": "centuries"
  }
}
```

#### Unit Converter

Convert between different units of measurement.

**Endpoint:** `POST /utilities/unit-convert`

**Request Body:**
```json
{
  "value": 100,
  "from_unit": "celsius",
  "to_unit": "fahrenheit",
  "category": "temperature"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original_value": 100,
    "converted_value": 212,
    "from_unit": "celsius",
    "to_unit": "fahrenheit",
    "category": "temperature"
  }
}
```

#### Age Calculator

Calculate precise age with detailed breakdown.

**Endpoint:** `POST /utilities/age-calculate`

**Request Body:**
```json
{
  "birth_date": "1990-05-15",
  "target_date": "2024-08-22"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "age_years": 34,
    "age_months": 3,
    "age_days": 7,
    "total_days": 12517,
    "total_hours": 300408,
    "total_minutes": 18024480,
    "next_birthday": "2025-05-15",
    "days_until_birthday": 266
  }
}
```

### 📈 Productivity

#### Todo Manager

Manage your tasks and todos.

**Create Todo:** `POST /productivity/todos`

**Request Body:**
```json
{
  "title": "Complete API documentation",
  "description": "Finish writing comprehensive API docs",
  "priority": "high",
  "due_date": "2024-08-25T18:00:00Z",
  "category": "work"
}
```

**List Todos:** `GET /productivity/todos?status=pending&limit=10`

**Update Todo:** `PUT /productivity/todos/{todo_id}`

**Delete Todo:** `DELETE /productivity/todos/{todo_id}`

#### Pomodoro Timer

Start and manage focus sessions.

**Start Session:** `POST /productivity/pomodoro/start`

**Request Body:**
```json
{
  "work_duration": 25,
  "break_duration": 5,
  "task_name": "Code review"
}
```

**Get Session Status:** `GET /productivity/pomodoro/status/{session_id}`

### 🌐 Web Tools

#### Weather Checker

Get current weather information.

**Endpoint:** `GET /web-tools/weather?location={city}&country={country}`

**Example:** `GET /web-tools/weather?location=London&country=UK`

**Response:**
```json
{
  "success": true,
  "data": {
    "location": "London, UK",
    "temperature": 18.5,
    "feels_like": 17.2,
    "humidity": 65,
    "pressure": 1015,
    "description": "Partly cloudy",
    "wind_speed": 12.5,
    "visibility": 10,
    "uv_index": 3,
    "forecast": [
      {
        "date": "2024-08-23",
        "high": 22,
        "low": 14,
        "description": "Sunny"
      }
    ]
  }
}
```

#### News Fetcher

Get latest news headlines.

**Endpoint:** `GET /web-tools/news?category={category}&limit={limit}`

**Response:**
```json
{
  "success": true,
  "data": {
    "articles": [
      {
        "title": "Breaking News Title",
        "description": "Article description...",
        "url": "https://example.com/article",
        "source": "News Source",
        "published_at": "2024-08-22T10:00:00Z",
        "image_url": "https://example.com/image.jpg"
      }
    ],
    "total_results": 50,
    "page": 1
  }
}
```

### 🤖 Automation

#### File Organizer

Organize files in a directory.

**Endpoint:** `POST /automation/organize-files`

**Request Body:**
```json
{
  "directory_path": "/path/to/directory",
  "organization_type": "by_extension",
  "create_subdirectories": true,
  "dry_run": false
}
```

### 🔒 Security

#### Password Strength Checker

Check password strength and get improvement suggestions.

**Endpoint:** `POST /security/password-check`

**Request Body:**
```json
{
  "password": "mypassword123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "strength": "Weak",
    "score": 2,
    "entropy": 42.5,
    "estimated_crack_time": "3 hours",
    "feedback": [
      "Add uppercase letters",
      "Include special characters",
      "Make it longer (12+ characters)"
    ],
    "has_uppercase": false,
    "has_lowercase": true,
    "has_numbers": true,
    "has_symbols": false,
    "length": 13
  }
}
```

## 📊 Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "timestamp": "2024-08-22T10:30:00Z",
  "version": "1.0.0"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "amount",
      "issue": "Must be a positive number"
    }
  },
  "timestamp": "2024-08-22T10:30:00Z",
  "version": "1.0.0"
}
```

## 🚨 HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Endpoint doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## 📝 Error Codes

| Error Code | Description |
|------------|-------------|
| `VALIDATION_ERROR` | Input validation failed |
| `INVALID_CURRENCY` | Unsupported currency code |
| `EXTERNAL_API_ERROR` | Third-party service unavailable |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `INTERNAL_ERROR` | Server error |

## 🔢 Rate Limiting

- **Free Tier**: 1000 requests per hour
- **Premium**: 10,000 requests per hour
- **Enterprise**: Unlimited

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1692705600
```

## 📘 SDKs and Libraries

### Python SDK
```bash
pip install pyeveryday-sdk
```

```python
from pyeveryday import PyEverydayClient

client = PyEverydayClient(api_key="your-api-key")
result = client.utilities.convert_currency(
    amount=100, 
    from_currency="USD", 
    to_currency="EUR"
)
```

### JavaScript SDK
```bash
npm install pyeveryday-js
```

```javascript
import { PyEverydayClient } from 'pyeveryday-js';

const client = new PyEverydayClient({ apiKey: 'your-api-key' });
const result = await client.utilities.convertCurrency({
  amount: 100,
  fromCurrency: 'USD',
  toCurrency: 'EUR'
});
```

## 🔗 Interactive Documentation

Visit our interactive API documentation:

- **Swagger UI**: [https://api.pyeveryday.app/docs](https://api.pyeveryday.app/docs)
- **ReDoc**: [https://api.pyeveryday.app/redoc](https://api.pyeveryday.app/redoc)

## 💬 Support

Need help with the API?

- **Discord**: [pyeveryday Discord server](https://discord.gg/pyeveryday)
- **Email**: [api-support@pyeveryday.app](mailto:api-support@pyeveryday.app)
- **GitHub Issues**: [Report API issues](https://github.com/Vaibhav2154/PyEveryday/issues)

---

*Last updated: August 22, 2024*
