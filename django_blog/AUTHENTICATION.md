# Django Blog Authentication System

## Overview
This authentication system provides user registration, login, logout, and profile management functionality.

## Features

### User Registration
- **URL**: `/register/`
- Creates new user accounts with username, email, and password
- Includes email validation
- Uses Django's built-in password validation

### User Login
- **URL**: `/login/`
- Authenticates users with username and password
- Uses Django's built-in AuthenticationForm
- Creates user sessions

### User Logout
- **URL**: `/logout/`
- Terminates user sessions
- Redirects to home page

### Profile Management
- **URL**: `/profile/`
- Allows users to update username and email
- Requires authentication
- Handles POST requests for updates

## Security Features
- CSRF protection on all forms
- Password hashing using Django's PBKDF2
- Session-based authentication
- Login requirement for protected views

## Static Files
- CSS styling for all authentication pages
- JavaScript for form enhancements
- Responsive design

## Testing Instructions

1. **Registration Test**:
   - Visit `/register/`
   - Fill out the form with test data
   - Verify redirection to login page

2. **Login Test**:
   - Visit `/login/`
   - Use credentials from registration
   - Verify successful login and redirect

3. **Profile Test**:
   - While logged in, visit `/profile/`
   - Update profile information
   - Verify changes are saved

4. **Logout Test**:
   - Click logout link
   - Verify session termination
