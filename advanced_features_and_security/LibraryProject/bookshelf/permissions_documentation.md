# Permissions and Groups Setup

## Custom Permissions Defined:
- can_view - View books
- can_create - Create new books  
- can_edit - Edit existing books
- can_delete - Delete books

## Groups Created:
1. *Viewers*: can_view permission only
2. *Editors*: can_view, can_create, can_edit permissions
3. *Admins*: All permissions (can_view, can_create, can_edit, can_delete)

## How to Setup:
1. Run: python manage.py setup_groups to create groups and assign permissions
2. Assign users to appropriate groups in Django Admin
3. Views are protected with @permission_required decorators

## Usage:
- Users in Viewers group can only view books
- Users in Editors group can view, create, and edit books  
- Users in Admins group have full access to all book operations
