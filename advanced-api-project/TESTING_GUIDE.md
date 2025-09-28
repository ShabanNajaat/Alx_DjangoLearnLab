# Unit Testing Guide for Django REST Framework APIs

## Overview
This document outlines the testing strategy and approach for the advanced_api_project API endpoints.

## Test Structure

### Test Cases Implemented:

#### 1. Book API Tests (`BookAPITestCase`)
- **Authentication Tests**: Verify permission controls
- **CRUD Operations**: Create, retrieve, update, delete books
- **Filtering Tests**: Filter by title, author, publication year
- **Search Tests**: Search across title and author fields
- **Ordering Tests**: Order by title and publication year
- **Validation Tests**: Publication year validation

#### 2. Author API Tests (`AuthorAPITestCase`)
- **List Authors**: Retrieve all authors
- **Retrieve Author**: Get single author with nested books

## Running Tests

### Run All Tests:
```bash
python manage.py test api
