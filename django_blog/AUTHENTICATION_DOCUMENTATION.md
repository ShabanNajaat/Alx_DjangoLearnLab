# Django Blog Authentication System Documentation

## Overview
This authentication system provides user registration, login, logout, and profile management functionality for the Django blog.

## Features

### 1. User Registration
- **URL**: `/register/`
- **Features**:
  - Custom registration form extending Django's UserCreationForm
  - Email field included
  - Password validation and confirmation
  - Automatic redirect to login after successful registration

### 2. User Login
- **URL**: `/login/`
- **Features**:
  - Uses Django's built-in AuthenticationForm
  - Secure password authentication
  - Session-based authentication
  - Redirects to blog home after successful login

### 3. User Logout
- **URL**: `/logout/`
- **Features**:
  - Secure session termination
  - Success message display
  - Redirect to blog home

### 4. Profile Management
- **URL**: `/profile/`
- **Features**:
  - View and update username and email
  - Login required protection
  - Success message on update

## Security Features

- CSRF protection on all forms
- Password hashing using Django's built-in PBKDF2
- Login required decorator for protected views
- Secure session management

## Testing Instructions

### Manual Testing

1. **Registration**:
   - Visit `/register/`
   - Fill out the form with username, email, and password
   - Submit and verify redirection to login page

2. **Login**:
   - Visit `/login/`
   - Enter credentials from registration
   - Verify successful login and welcome message

3. **Profile Management**:
   - While logged in, visit `/profile/`
   - Update username or email
   - Verify changes are saved

4. **Logout**:
   - Click logout link
   - Verify session is terminated and redirect to home

### Automated Testing
Run the test suite:
```bash
python manage.py test blog
