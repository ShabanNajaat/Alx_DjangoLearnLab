# Custom Views and Generic Views Documentation

## Overview
This project implements custom views using Django REST Framework's generic views to handle CRUD operations for Book and Author models.

## View Configurations

### Book Views

#### 1. BookListView (`/api/books/`)
- **Purpose**: Retrieve all books
- **HTTP Method**: GET
- **Permissions**: AllowAny (public access)
- **Generic View**: `ListAPIView`
- **Features**: Returns serialized list of all books

#### 2. BookDetailView (`/api/books/<int:pk>/`)
- **Purpose**: Retrieve single book by ID
- **HTTP Method**: GET
- **Permissions**: AllowAny (public access)
- **Generic View**: `RetrieveAPIView`
- **Features**: Returns serialized book details

#### 3. BookCreateView (`/api/books/create/`)
- **Purpose**: Create new book
- **HTTP Method**: POST
- **Permissions**: IsAuthenticated (requires authentication)
- **Generic View**: `CreateAPIView`
- **Features**: Handles book creation with validation

#### 4. BookUpdateView (`/api/books/<int:pk>/update/`)
- **Purpose**: Update existing book
- **HTTP Method**: PUT, PATCH
- **Permissions**: IsAuthenticated (requires authentication)
- **Generic View**: `UpdateAPIView`
- **Features**: Handles partial/full book updates

#### 5. BookDeleteView (`/api/books/<int:pk>/delete/`)
- **Purpose**: Delete book
- **HTTP Method**: DELETE
- **Permissions**: IsAuthenticated (requires authentication)
- **Generic View**: `DestroyAPIView`
- **Features**: Handles book deletion

### Author Views

#### 1. AuthorListView (`/api/authors/`)
- **Purpose**: Retrieve all authors with their books
- **HTTP Method**: GET
- **Permissions**: AllowAny (public access)
- **Generic View**: `ListAPIView`
- **Features**: Returns authors with nested book data

#### 2. AuthorDetailView (`/api/authors/<int:pk>/`)
- **Purpose**: Retrieve single author with their books
- **HTTP Method**: GET
- **Permissions**: AllowAny (public access)
- **Generic View**: `RetrieveAPIView`
- **Features**: Returns author details with nested book data

## Permission Strategy

- **Read Operations** (GET): Available to all users (AllowAny)
- **Write Operations** (POST, PUT, PATCH, DELETE): Restricted to authenticated users (IsAuthenticated)

## Testing Guidelines

### Testing Read Operations (No Authentication Required):
```bash
# List all books
curl http://127.0.0.1:8000/api/books/

# Get specific book
curl http://127.0.0.1:8000/api/books/1/

# List all authors
curl http://127.0.0.1:8000/api/authors/
