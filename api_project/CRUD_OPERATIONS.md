# CRUD Operations with ViewSets and Routers

## API Endpoints Created:

### 1. List All Books
- *URL*: GET /api/books_all/
- *Description*: Retrieve all books
- *Response*: JSON array of book objects

### 2. Retrieve Single Book
- *URL*: GET /api/books_all/<id>/
- *Description*: Retrieve a specific book by ID
- *Response*: JSON object of the book

### 3. Create New Book
- *URL*: POST /api/books_all/
- *Description*: Create a new book
- *Body*: JSON object with title and author
- *Response*: JSON object of the created book

### 4. Update Book
- *URL*: PUT /api/books_all/<id>/
- *Description*: Fully update a book
- *Body*: JSON object with all fields
- *Response*: JSON object of the updated book

### 5. Partial Update Book
- *URL*: PATCH /api/books_all/<id>/
- *Description*: Partially update a book
- *Body*: JSON object with fields to update
- *Response*: JSON object of the updated book

### 6. Delete Book
- *URL*: DELETE /api/books_all/<id>/
- *Description*: Delete a book
- *Response*: HTTP 204 No Content

## Testing Examples:

### Create a Book (POST):
```bash
curl -X POST http://127.0.0.1:8000/api/books_all/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "New Author"}'
