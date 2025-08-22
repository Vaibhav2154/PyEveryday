# 🏗️ Architecture Guide

This document provides a comprehensive overview of PyEveryday's system architecture, design patterns, and technical decisions.

## 🎯 Architecture Overview

PyEveryday follows a modern **microservices-inspired** architecture with a clear separation between frontend, backend, and script layers.

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Next.js UI]
        PWA[Progressive Web App]
        Mobile[Mobile Interface]
    end
    
    subgraph "API Layer" 
        API[FastAPI Backend]
        Auth[Authentication]
        Rate[Rate Limiting]
        Valid[Validation]
    end
    
    subgraph "Business Logic"
        Scripts[Python Scripts]
        Services[Business Services]
        Utils[Utility Functions]
    end
    
    subgraph "Data Layer"
        DB[(Database)]
        Cache[(Redis Cache)]
        Files[(File Storage)]
    end
    
    subgraph "External Services"
        Exchange[Exchange Rate API]
        Weather[Weather API]
        News[News API]
    end
    
    UI --> API
    PWA --> API
    Mobile --> API
    
    API --> Auth
    API --> Rate
    API --> Valid
    
    API --> Scripts
    API --> Services
    Scripts --> Utils
    
    Services --> DB
    Services --> Cache
    Services --> Files
    
    Services --> Exchange
    Services --> Weather
    Services --> News
```

## 🔧 Technology Stack

### Frontend Technologies

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Next.js 14** | React Framework | Server-side rendering, file-based routing, optimizations |
| **TypeScript** | Type Safety | Better developer experience, fewer runtime errors |
| **Tailwind CSS** | Styling | Utility-first, responsive design, fast development |
| **React Hook Form** | Form Management | Performance, validation, developer experience |
| **Zustand** | State Management | Lightweight, TypeScript-friendly, simple API |
| **React Query** | Data Fetching | Caching, background updates, optimistic updates |

### Backend Technologies

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **FastAPI** | Web Framework | Automatic documentation, type hints, performance |
| **Pydantic** | Data Validation | Type-safe validation, automatic JSON schema |
| **SQLAlchemy** | ORM | Database abstraction, migrations, relationships |
| **Alembic** | Database Migrations | Version control for database schema |
| **Redis** | Caching | In-memory storage, session management |
| **Celery** | Background Tasks | Async task processing, scheduling |

### Infrastructure & DevOps

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Docker** | Containerization | Environment consistency, easy deployment |
| **PostgreSQL** | Primary Database | ACID compliance, performance, features |
| **Nginx** | Reverse Proxy | Load balancing, SSL termination, static files |
| **GitHub Actions** | CI/CD | Automated testing, deployment, integration |
| **Vercel** | Frontend Hosting | Edge network, automatic deployments |
| **Railway/Heroku** | Backend Hosting | Easy deployment, managed infrastructure |

## 🏛️ System Design Patterns

### 1. Repository Pattern

Abstracts data access logic from business logic.

```python
# backend/app/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def create(self, user_data: dict) -> User:
        pass

class SQLUserRepository(UserRepository):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        # SQLAlchemy implementation
        pass
```

### 2. Service Layer Pattern

Encapsulates business logic and coordinates between repositories.

```python
# backend/app/services/currency_service.py
class CurrencyService:
    def __init__(self, repository: CurrencyRepository, cache: CacheService):
        self.repository = repository
        self.cache = cache
    
    async def convert(self, amount: float, from_currency: str, to_currency: str):
        # Business logic for currency conversion
        rate = await self._get_exchange_rate(from_currency, to_currency)
        return amount * rate
```

### 3. Factory Pattern

Creates objects without specifying exact classes.

```python
# backend/app/factories/script_factory.py
class ScriptFactory:
    @staticmethod
    def create_script(script_type: str, config: dict):
        if script_type == "currency_converter":
            return CurrencyConverterScript(config)
        elif script_type == "password_generator":
            return PasswordGeneratorScript(config)
        # ... more script types
```

### 4. Observer Pattern

For real-time updates and notifications.

```typescript
// ui/lib/hooks/useRealTimeUpdates.ts
export function useRealTimeUpdates() {
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Update UI based on real-time data
    };
    
    return () => ws.close();
  }, []);
}
```

## 🔄 Data Flow Architecture

### Request Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant NextJS
    participant FastAPI
    participant Service
    participant Database
    participant External
    
    Client->>NextJS: User Action
    NextJS->>FastAPI: API Request
    FastAPI->>FastAPI: Authentication
    FastAPI->>FastAPI: Validation
    FastAPI->>Service: Business Logic
    Service->>Database: Data Query
    Service->>External: External API Call
    Service->>FastAPI: Result
    FastAPI->>NextJS: JSON Response
    NextJS->>Client: UI Update
```

### State Management Flow

```mermaid
graph LR
    A[User Action] --> B[React Component]
    B --> C[Zustand Store]
    C --> D[API Call]
    D --> E[FastAPI Endpoint]
    E --> F[Service Layer]
    F --> G[Database/External API]
    G --> F
    F --> E
    E --> D
    D --> C
    C --> B
    B --> H[UI Update]
```

## 🗄️ Database Design

### Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ TODO : creates
    USER ||--o{ POMODORO_SESSION : starts
    USER ||--o{ API_KEY : owns
    
    USER {
        int id PK
        string email UK
        string username UK
        string hashed_password
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    TODO {
        int id PK
        int user_id FK
        string title
        text description
        string priority
        datetime due_date
        boolean completed
        datetime created_at
    }
    
    POMODORO_SESSION {
        int id PK
        int user_id FK
        string task_name
        int work_duration
        int break_duration
        datetime started_at
        datetime completed_at
        string status
    }
    
    API_KEY {
        int id PK
        int user_id FK
        string key_hash
        string name
        datetime expires_at
        boolean is_active
        int usage_count
    }
```

### Database Schema Principles

1. **Normalization**: Tables are normalized to 3NF to reduce redundancy
2. **Indexing**: Strategic indexing on frequently queried columns
3. **Constraints**: Foreign keys and check constraints ensure data integrity
4. **Audit Fields**: Created/updated timestamps on all entities
5. **Soft Deletes**: Important data is soft-deleted rather than physically removed

## 🔐 Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant Frontend
    participant Backend
    participant Database
    
    Client->>Frontend: Login Credentials
    Frontend->>Backend: POST /auth/login
    Backend->>Database: Verify User
    Database->>Backend: User Data
    Backend->>Backend: Generate JWT
    Backend->>Frontend: JWT Token
    Frontend->>Frontend: Store Token
    Frontend->>Client: Redirect to Dashboard
    
    Note over Client,Database: Subsequent Requests
    Client->>Frontend: API Request
    Frontend->>Backend: Request + JWT Header
    Backend->>Backend: Validate JWT
    Backend->>Frontend: Protected Resource
    Frontend->>Client: Display Data
```

### Security Measures

1. **JWT Authentication**: Stateless token-based authentication
2. **Password Hashing**: bcrypt with salt for password storage
3. **CORS Configuration**: Restricted origins for API access
4. **Rate Limiting**: Prevent abuse and DoS attacks
5. **Input Validation**: Pydantic schemas validate all inputs
6. **SQL Injection Prevention**: ORM with parameterized queries
7. **XSS Protection**: Content Security Policy headers
8. **HTTPS Only**: All communication encrypted in production

## 📊 Performance Architecture

### Caching Strategy

```mermaid
graph TD
    A[Client Request] --> B{Cache Hit?}
    B -->|Yes| C[Return Cached Data]
    B -->|No| D[Query Database/API]
    D --> E[Store in Cache]
    E --> F[Return Data]
    
    subgraph "Cache Layers"
        G[Browser Cache]
        H[CDN Cache]
        I[Redis Cache]
        J[Database Query Cache]
    end
```

### Performance Optimizations

1. **Frontend Optimizations**:
   - Code splitting and lazy loading
   - Image optimization with Next.js
   - Static site generation where possible
   - Service worker for offline support

2. **Backend Optimizations**:
   - Async/await for non-blocking operations
   - Connection pooling for database
   - Redis caching for frequent queries
   - Background tasks for heavy operations

3. **Database Optimizations**:
   - Strategic indexing
   - Query optimization
   - Connection pooling
   - Read replicas for scaling

## 🔌 API Design Philosophy

### RESTful Principles

1. **Resource-based URLs**: `/api/v1/utilities/currency-convert`
2. **HTTP Methods**: GET, POST, PUT, DELETE for CRUD operations
3. **Status Codes**: Meaningful HTTP status codes
4. **Stateless**: Each request contains all necessary information
5. **Cacheable**: Responses indicate if they can be cached

### API Versioning Strategy

```
/api/v1/utilities/currency-convert  # Current version
/api/v2/utilities/currency-convert  # Future version
```

- **Backward Compatibility**: v1 maintained while v2 is introduced
- **Deprecation Timeline**: 6-month notice before version removal
- **Documentation**: Clear migration guides between versions

## 🧪 Testing Architecture

### Testing Pyramid

```mermaid
graph TD
    A[Unit Tests - 70%] --> B[Integration Tests - 20%]
    B --> C[E2E Tests - 10%]
    
    subgraph "Unit Tests"
        D[Python Functions]
        E[React Components]
        F[Utility Functions]
    end
    
    subgraph "Integration Tests"
        G[API Endpoints]
        H[Database Operations]
        I[External Service Mocks]
    end
    
    subgraph "E2E Tests"
        J[User Workflows]
        K[Cross-browser Testing]
        L[Mobile Responsiveness]
    end
```

### Testing Strategy

1. **Unit Tests**: Fast, isolated tests for individual functions
2. **Integration Tests**: Test interaction between components
3. **E2E Tests**: Test complete user workflows
4. **Performance Tests**: Load testing and benchmarking
5. **Security Tests**: Vulnerability scanning and penetration testing

## 🚀 Deployment Architecture

### Production Environment

```mermaid
graph TB
    subgraph "CDN Layer"
        CDN[Cloudflare CDN]
    end
    
    subgraph "Load Balancer"
        LB[Nginx Load Balancer]
    end
    
    subgraph "Application Layer"
        App1[App Instance 1]
        App2[App Instance 2]
        App3[App Instance 3]
    end
    
    subgraph "Database Layer"
        Primary[(Primary DB)]
        Replica[(Read Replica)]
    end
    
    subgraph "Cache Layer"
        Redis[(Redis Cluster)]
    end
    
    CDN --> LB
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> Primary
    App2 --> Primary
    App3 --> Primary
    
    App1 --> Replica
    App2 --> Replica
    App3 --> Replica
    
    App1 --> Redis
    App2 --> Redis
    App3 --> Redis
```

### Deployment Pipeline

```mermaid
graph LR
    A[Code Push] --> B[GitHub Actions]
    B --> C[Build & Test]
    C --> D[Docker Build]
    D --> E[Security Scan]
    E --> F[Deploy to Staging]
    F --> G[Integration Tests]
    G --> H[Deploy to Production]
    H --> I[Health Checks]
    I --> J[Rollback if Failed]
```

## 📈 Scalability Considerations

### Horizontal Scaling

1. **Stateless Design**: No server-side sessions, use JWT tokens
2. **Database Scaling**: Read replicas, sharding strategies
3. **Caching**: Redis cluster for distributed caching
4. **Load Balancing**: Multiple application instances
5. **CDN**: Global content distribution

### Vertical Scaling

1. **Resource Optimization**: CPU and memory profiling
2. **Database Tuning**: Query optimization, indexing
3. **Application Optimization**: Async processing, connection pooling

## 🔮 Future Architecture Plans

### Microservices Migration

```mermaid
graph TB
    subgraph "Current Monolith"
        API[FastAPI App]
    end
    
    subgraph "Future Microservices"
        Auth[Auth Service]
        Utils[Utilities Service]
        Prod[Productivity Service]
        Auto[Automation Service]
        Notify[Notification Service]
    end
    
    subgraph "Service Mesh"
        Gateway[API Gateway]
        Discovery[Service Discovery]
        Monitor[Monitoring]
    end
    
    API -.-> Auth
    API -.-> Utils
    API -.-> Prod
    API -.-> Auto
    
    Gateway --> Auth
    Gateway --> Utils
    Gateway --> Prod
    Gateway --> Auto
    Gateway --> Notify
```

### Technology Roadmap

- **Q4 2024**: Redis caching implementation
- **Q1 2025**: Microservices architecture
- **Q2 2025**: Kubernetes deployment
- **Q3 2025**: GraphQL API option
- **Q4 2025**: Real-time collaboration features

---

This architecture guide serves as a living document that evolves with the system. For questions or suggestions, please reach out to the development team.
