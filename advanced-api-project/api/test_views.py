"""
Test views for Django REST Framework APIs
Testing API endpoints with proper test database configuration
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookViewTests(TestCase):
    """
    Test cases for Book views using separate test database
    Django automatically creates and manages test database
    """
    
    def setUp(self):
        """
        Set up test data - uses separate test database automatically
        Test database is created fresh for each test run
        """
        # Create test client - using force_authenticate instead of login
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="J.R.R. Tolkien")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author2
        )
    
    def test_book_list_view_returns_200(self):
        """
        Test book list view returns HTTP 200 status code
        Uses separate test database automatically
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_book_detail_view_returns_200(self):
        """
        Test book detail view returns HTTP 200 status code
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_book_create_view_authenticated_returns_201(self):
        """
        Test book create view with authentication returns HTTP 201
        Using force_authenticate instead of client.login
        """
        # Use force_authenticate instead of self.client.login
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check status code - HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_book_create_view_unauthenticated_returns_403(self):
        """
        Test book create view without authentication returns HTTP 403
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # Check status code - HTTP 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_update_view_returns_200(self):
        """
        Test book update view returns HTTP 200 status code
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_delete_view_returns_204(self):
        """
        Test book delete view returns HTTP 204 status code
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        # Check status code - HTTP 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    def test_book_filter_view_returns_200(self):
        """
        Test book filter view returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'harry'})
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_search_view_returns_200(self):
        """
        Test book search view returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_ordering_view_returns_200(self):
        """
        Test book ordering view returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorViewTests(TestCase):
    """
    Test cases for Author views using separate test database
    """
    
    def setUp(self):
        """
        Set up test data for author view tests
        Uses separate test database automatically
        """
        self.client = APIClient()
        
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")
    
    def test_author_list_view_returns_200(self):
        """
        Test author list view returns HTTP 200 status code
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_author_detail_view_returns_200(self):
        """
        Test author detail view returns HTTP 200 status code
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        # Check status code - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
