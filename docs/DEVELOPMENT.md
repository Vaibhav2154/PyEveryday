# 🛠️ Development Guide

This guide will help you set up a development environment for PyEveryday and understand the development workflow.

## 🎯 Prerequisites

### Required Software

- **Python 3.8+** - Backend development
- **Node.js 16+** - Frontend development  
- **Git** - Version control
- **Docker** (optional) - Containerized development

### Recommended Tools

- **VS Code** - Code editor with excellent Python/TypeScript support
- **Postman** or **Insomnia** - API testing
- **Chrome DevTools** - Frontend debugging
- **Python extension** for VS Code
- **Pylint** and **Black** for Python code formatting

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Vaibhav2154/PyEveryday.git
cd PyEveryday
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd ui

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

### 4. Database Setup (if needed)

```bash
# SQLite (default)
cd backend
python -c "from app.database import create_tables; create_tables()"

# PostgreSQL (production)
# Update DATABASE_URL in .env file
# Run migrations: alembic upgrade head
```

## 🏃‍♂️ Running the Application

### Development Servers

Start both servers in separate terminals:

```bash
# Terminal 1: Backend
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend  
cd ui
npm run dev
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Using Docker (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📁 Project Structure

```
PyEveryday/
├── backend/                    # FastAPI backend
│   ├── app/                   # Main application
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app instance
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database connection
│   │   ├── dependencies.py   # Common dependencies
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── utilities.py
│   │   │   ├── productivity.py
│   │   │   └── automation.py
│   │   ├── services/         # Business logic
│   │   └── utils/            # Helper functions
│   ├── scripts/              # Core Python scripts
│   │   ├── automation/
│   │   ├── productivity/
│   │   ├── utilities/
│   │   ├── web_scraping/
│   │   ├── data_tools/
│   │   ├── security/
│   │   └── image_audio_video/
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-dev.txt  # Development dependencies
│   └── .env.example         # Environment variables template
│
├── ui/                       # Next.js frontend
│   ├── app/                  # App router (Next.js 13+)
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page
│   │   ├── globals.css      # Global styles
│   │   ├── utilities/       # Utility tool pages
│   │   ├── productivity/    # Productivity tool pages
│   │   └── automation/      # Automation tool pages
│   ├── components/          # Reusable components
│   │   ├── ui/              # Basic UI components
│   │   ├── forms/           # Form components
│   │   ├── layout/          # Layout components
│   │   └── tools/           # Tool-specific components
│   ├── lib/                 # Utility functions
│   │   ├── api.ts           # API client
│   │   ├── utils.ts         # Helper functions
│   │   └── validations.ts   # Form validations
│   ├── public/              # Static assets
│   ├── styles/              # Additional styles
│   ├── package.json         # Node.js dependencies
│   └── .env.local.example   # Environment variables template
│
├── docs/                    # Documentation
├── tests/                   # Integration tests
├── .github/                 # GitHub workflows
├── docker-compose.yml       # Docker configuration
└── README.md               # Project overview
```

## 🔧 Development Workflow

### 1. Creating a New Feature

```bash
# Create feature branch
git checkout -b feature/currency-converter-api

# Make your changes
# ... develop the feature ...

# Run tests
npm test                    # Frontend tests
pytest                     # Backend tests

# Commit changes
git add .
git commit -m "feat: add currency converter API endpoint"

# Push and create PR
git push origin feature/currency-converter-api
```

### 2. Adding a New Script

When adding a new automation script:

1. **Create the core script** in `backend/scripts/{category}/`
2. **Add API endpoint** in `backend/app/routers/{category}.py`
3. **Create frontend component** in `ui/components/tools/`
4. **Add page route** in `ui/app/{category}/`
5. **Write tests** for both frontend and backend
6. **Update documentation**

### 3. Code Quality Checks

```bash
# Backend linting and formatting
cd backend
black .                     # Format code
flake8 .                   # Lint code
mypy .                     # Type checking
pytest                     # Run tests

# Frontend linting and formatting
cd ui
npm run lint               # ESLint
npm run type-check         # TypeScript check
npm run format             # Prettier
npm test                   # Run tests
```

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_utilities.py

# Run specific test
pytest tests/test_utilities.py::test_currency_converter
```

### Frontend Testing

```bash
cd ui

# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test CurrencyConverter.test.tsx
```

### Integration Testing

```bash
# Run end-to-end tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui
```

## 🎨 Styling and UI

### Design System

We use a consistent design system:

- **Colors**: Defined in `ui/app/globals.css`
- **Typography**: System fonts with fallbacks
- **Spacing**: Tailwind CSS spacing scale
- **Components**: shadcn/ui component library

### Adding New Components

```typescript
// ui/components/ui/Button.tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({ 
  className, 
  variant = 'primary', 
  size = 'md',
  ...props 
}: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-600 text-white hover:bg-gray-700': variant === 'secondary',
          'border border-gray-300 hover:bg-gray-50': variant === 'outline',
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        className
      )}
      {...props}
    />
  );
}
```

## 📊 API Development

### Creating New Endpoints

```python
# backend/app/routers/utilities.py
from fastapi import APIRouter, HTTPException
from app.schemas.utilities import CurrencyConvertRequest, CurrencyConvertResponse
from app.services.currency_service import CurrencyService

router = APIRouter()

@router.post("/currency-convert", response_model=CurrencyConvertResponse)
async def convert_currency(request: CurrencyConvertRequest):
    """Convert currency using real-time exchange rates."""
    try:
        service = CurrencyService()
        result = await service.convert(
            request.amount,
            request.from_currency, 
            request.to_currency
        )
        return CurrencyConvertResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Schema Definition

```python
# backend/app/schemas/utilities.py
from pydantic import BaseModel, Field
from typing import Optional

class CurrencyConvertRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to convert")
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)

class CurrencyConvertResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
```

## 🐛 Debugging

### Backend Debugging

```python
# Add breakpoints in VS Code or use pdb
import pdb; pdb.set_trace()

# Enable debug mode
# In .env file:
DEBUG=true

# View logs
uvicorn app:app --reload --log-level debug
```

### Frontend Debugging

```javascript
// Use console.log for simple debugging
console.log('API response:', response);

// Use browser DevTools
debugger;

// React DevTools for component debugging
// Install React DevTools browser extension
```

## 🔒 Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=sqlite:///./pyeveryday.db

# External APIs
EXCHANGE_RATE_API_KEY=your_api_key_here
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret

# Development
DEBUG=true
LOG_LEVEL=debug
```

### Frontend (.env.local)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ENVIRONMENT=development

# Analytics (optional)
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
```

## 📱 Mobile Development

### Responsive Design

- Use Tailwind CSS responsive utilities
- Test on multiple screen sizes
- Ensure touch-friendly interactions

### PWA Support

```javascript
// ui/next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
});

module.exports = withPWA({
  // Next.js config
});
```

## 🚀 Deployment

### Development Deployment

```bash
# Build frontend
cd ui
npm run build

# Start production servers
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000

cd ui  
npm start
```

### Docker Deployment

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 💡 Tips and Best Practices

### Code Quality

- **Write descriptive commit messages**
- **Keep functions small and focused**
- **Use type hints in Python**
- **Write comprehensive tests**
- **Document complex logic**

### Performance

- **Use async/await for I/O operations**
- **Implement caching for expensive operations**
- **Optimize database queries**
- **Minimize frontend bundle size**

### Security

- **Validate all inputs**
- **Use environment variables for secrets**
- **Implement rate limiting**
- **Keep dependencies updated**

## 🆘 Common Issues

### Backend Issues

```bash
# Port already in use
lsof -ti:8000 | xargs kill -9

# Python module not found
pip install -e .

# Database connection error
# Check DATABASE_URL in .env
```

### Frontend Issues

```bash
# Node modules issues
rm -rf node_modules package-lock.json
npm install

# Build errors
npm run build -- --verbose

# Type errors
npm run type-check
```

## 📞 Getting Help

- **Discord**: [PyEveryday Discord](https://discord.gg/pyeveryday)
- **GitHub Issues**: [Report bugs](https://github.com/Vaibhav2154/PyEveryday/issues)
- **Discussions**: [Ask questions](https://github.com/Vaibhav2154/PyEveryday/discussions)

---

Happy coding! 🚀
