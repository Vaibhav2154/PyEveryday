# 🤝 Contributing to PyEveryday

Thank you for your interest in contributing to PyEveryday! We're excited to have you join our community of developers working to make automation accessible to everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Types](#contribution-types)
- [Contribution Workflow](#contribution-workflow)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We're committed to fostering a welcoming and inclusive environment for all contributors.

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **Node.js 16+** for frontend development
- **Git** for version control
- A **GitHub account** for submitting contributions

### First Contribution?

If this is your first time contributing to an open-source project, welcome! Here are some great resources:

- [First Contributions](https://github.com/firstcontributions/first-contributions)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/PyEveryday.git
cd PyEveryday

# Add upstream remote
git remote add upstream https://github.com/Vaibhav2154/PyEveryday.git
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Start the backend server
uvicorn app:app --reload
```

### 3. Frontend Setup

```bash
cd ui

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Verify Setup

- Backend: Visit `http://localhost:8000/docs`
- Frontend: Visit `http://localhost:3000`

## 🎯 Contribution Types

We welcome various types of contributions:

### 🐛 Bug Reports

Found a bug? Please check existing issues first, then create a new issue with:

- **Clear title** describing the bug
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, browser)
- **Screenshots** if applicable

### 💡 Feature Requests

Have an idea for a new feature? Create an issue with:

- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Proposed implementation** (if you have ideas)
- **Mockups or examples** (if applicable)

### 📝 Documentation

Help improve our documentation:

- **Fix typos** and grammatical errors
- **Add examples** and clarifications
- **Create tutorials** for complex features
- **Translate** documentation (coming soon)

### 🔧 Code Contributions

Contribute new features or bug fixes:

- **New automation scripts** in any category
- **API endpoints** for script integration
- **Frontend components** for better UX
- **Performance improvements**
- **Security enhancements**

## 🔄 Contribution Workflow

### 1. Create an Issue (Optional but Recommended)

For significant changes, create an issue first to discuss your approach.

### 2. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Changes

Follow our [style guidelines](#style-guidelines) and ensure your changes:

- **Solve the problem** effectively
- **Follow existing patterns** in the codebase
- **Include tests** for new functionality
- **Update documentation** as needed

### 4. Test Your Changes

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd ui
npm test

# End-to-end tests
npm run test:e2e
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add currency converter API endpoint

- Add /api/v1/utilities/currency-convert endpoint
- Implement real-time exchange rate fetching
- Add input validation for currency codes
- Include comprehensive error handling"
```

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **References** to related issues (e.g., "Closes #123")
- **Screenshots** for UI changes
- **Testing instructions** for reviewers

## 📋 Style Guidelines

### Python Code

- **Follow PEP 8** style guide
- **Use type hints** for all function parameters and returns
- **Write docstrings** for all public functions and classes
- **Use meaningful variable names**
- **Keep functions small** and focused

```python
from typing import Dict, Any
import asyncio

async def convert_currency(
    amount: float, 
    from_currency: str, 
    to_currency: str
) -> Dict[str, Any]:
    """
    Convert currency using real-time exchange rates.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
        
    Returns:
        Dictionary containing conversion result and metadata
        
    Raises:
        ValueError: If currency codes are invalid
        APIError: If exchange rate service is unavailable
    """
    # Implementation here
```

### JavaScript/TypeScript

- **Use TypeScript** for all new code
- **Follow React best practices**
- **Use meaningful component names**
- **Write JSDoc comments** for complex functions

```typescript
interface CurrencyConvertRequest {
  amount: number;
  fromCurrency: string;
  toCurrency: string;
}

/**
 * Currency converter component with real-time rates
 */
export function CurrencyConverter(): JSX.Element {
  // Implementation here
}
```

### API Design

- **Use RESTful conventions**
- **Include proper HTTP status codes**
- **Provide comprehensive error messages**
- **Use consistent naming patterns**

```python
@router.post("/currency-convert", response_model=CurrencyConvertResponse)
async def convert_currency(request: CurrencyConvertRequest):
    """Convert currency with real-time exchange rates."""
    try:
        result = await currency_service.convert(
            request.amount, 
            request.from_currency, 
            request.to_currency
        )
        return CurrencyConvertResponse(success=True, data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 🧪 Testing

### Backend Testing

- **Unit tests** for all functions using pytest
- **Integration tests** for API endpoints
- **Test both success and error cases**

```python
import pytest
from fastapi.testclient import TestClient

def test_currency_convert_success():
    response = client.post("/api/v1/utilities/currency-convert", json={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 200
    assert "converted_amount" in response.json()
```

### Frontend Testing

- **Component tests** using Jest and React Testing Library
- **User interaction tests**
- **Accessibility tests**

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { CurrencyConverter } from './CurrencyConverter';

test('converts currency when form is submitted', async () => {
  render(<CurrencyConverter />);
  
  fireEvent.change(screen.getByLabelText('Amount'), {
    target: { value: '100' }
  });
  
  fireEvent.click(screen.getByText('Convert'));
  
  expect(await screen.findByText(/converted/i)).toBeInTheDocument();
});
```

## 📚 Documentation

### Adding New Scripts

When adding a new script, include:

1. **Docstring** explaining purpose and usage
2. **Type hints** for all parameters
3. **Example usage** in the docstring
4. **API documentation** if exposing via web interface
5. **Frontend component** if adding UI

### Documentation Structure

```
docs/
├── api/                 # API documentation
├── guides/             # User guides and tutorials
├── development/        # Development documentation
├── deployment/         # Deployment guides
└── examples/           # Code examples
```

## 🌟 Script Categories

When adding new scripts, place them in the appropriate category:

- **`automation/`** - File management, email, scheduling
- **`productivity/`** - Todo lists, timers, reminders
- **`utilities/`** - Calculators, converters, generators
- **`web_scraping/`** - Data extraction, monitoring
- **`data_tools/`** - Processing, analysis, visualization
- **`security/`** - Password tools, encryption
- **`image_audio_video/`** - Media processing

## 🏆 Recognition

Contributors will be recognized in several ways:

- **Contributors section** in README
- **Changelog credits** for significant contributions
- **Special badges** for major contributors
- **Annual contributor highlights**

## 💬 Community

Join our community channels:

- **[Discord](https://discord.gg/pyeveryday)** - Real-time discussions
- **[GitHub Discussions](https://github.com/Vaibhav2154/PyEveryday/discussions)** - Longer-form conversations
- **[Issues](https://github.com/Vaibhav2154/PyEveryday/issues)** - Bug reports and feature requests

## ❓ Questions?

If you have questions about contributing:

1. **Check existing documentation** and issues
2. **Ask in Discord** for quick help
3. **Create a discussion** for broader questions
4. **Email us** at [contributors@pyeveryday.app](mailto:contributors@pyeveryday.app)

## 🎉 Thank You!

Every contribution, no matter how small, makes PyEveryday better for everyone. We appreciate your time and effort in helping make automation accessible to all!

---

*Happy coding! 🚀*
