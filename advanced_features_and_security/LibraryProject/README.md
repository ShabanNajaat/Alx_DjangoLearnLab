# LibraryProject - Advanced Features and Security

## Features Implemented:

### 1. Custom User Model
- Extended Django's AbstractUser with additional fields
- Email-based authentication instead of username
- Additional fields: date_of_birth, profile_photo

### 2. Permission System
- Custom permissions for Book model: can_view, can_create, can_edit, can_delete
- Role-based access control with groups: Viewers, Editors, Admins
- Permission decorators on views for access control

### 3. Security Best Practices
- HTTPS enforcement with secure cookies
- CSRF protection on all forms
- XSS and clickjacking protection headers
- Content Security Policy (CSP)
- Secure proxy headers configuration

### 4. Form Security
- Django forms with validation and sanitization
- CSRF tokens on all forms
- Secure file upload handling

## Setup Instructions:

1. Install dependencies: pip install django pillow
2. Run migrations: python manage.py migrate
3. Create groups: python manage.py setup_groups
4. Create superuser: python manage.py createsuperuser
5. Run server: python manage.py runserver

## Admin Access:
- Access at: /admin/
- Manage users, groups, and permissions
- Configure access controls

## API Endpoints:
- /books/ - Book list (requires can_view)
- /books/create/ - Create book (requires can_create)
- /books/<id>/edit/ - Edit book (requires can_edit)
- /books/<id>/delete/ - Delete book (requires can_delete)
- /form-example/ - Example secure form
