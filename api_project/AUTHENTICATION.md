# Authentication and Permissions Setup

## Authentication Methods:
1. *Token Authentication*: Primary method for API access
2. *Session Authentication*: For browsable API interface

## API Endpoints:

### 1. Get Authentication Token
- *URL*: POST /api/auth-token/
- *Body*: {"username": "your_username", "password": "your_password"}
- *Response*: {"token": "your_auth_token"}

### 2. User Registration
- *URL*: POST /api/register/
- *Body*: {"username": "new_user", "password": "password123", "email": "user@example.com"}
- *Response*: {"message": "User created successfully", "username": "new_user"}

### 3. Protected Endpoints
All book endpoints now require authentication:

- GET /api/books/ - Read-only access (public)
- GET /api/books_all/ - List books (authenticated)
- POST /api/books_all/ - Create book (authenticated)
- GET /api/books_all/<id>/ - Get book (authenticated)
- PUT /api/books_all/<id>/ - Update book (authenticated)
- DELETE /api/books_all/<id>/ - Delete book (authenticated)

## Testing Authentication:

### Get Token:
```bash
curl -X POST http://127.0.0.1:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
