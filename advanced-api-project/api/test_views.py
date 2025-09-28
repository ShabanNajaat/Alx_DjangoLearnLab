"""
Unit tests for Django REST Framework APIs
Testing API endpoints, filtering, searching, ordering, and permissions
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    """
    Test case for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and permissions.
    """
    
    def setUp(self):
        """
        Set up test data and client for each test
        Configure separate test database automatically handled by Django
        """
        # Create test client
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
        self.author3 = Author.objects.create(name="George Orwell")
        
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
        self.book3 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author3
        )
    
    def test_list_books_returns_200_status_code(self):
        """
        Test that listing books returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_retrieve_book_returns_200_status_code(self):
        """
        Test that retrieving a single book returns HTTP 200 status code
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_create_book_returns_201_status_code(self):
        """
        Test that creating a book returns HTTP 201 status code
        """
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # MUST CHECK STATUS CODE - HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_create_book_unauthenticated_returns_403_status_code(self):
        """
        Test that unauthenticated book creation returns HTTP 403 status code
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # MUST CHECK STATUS CODE - HTTP 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_returns_200_status_code(self):
        """
        Test that updating a book returns HTTP 200 status code
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_book_returns_204_status_code(self):
        """
        Test that deleting a book returns HTTP 204 status code
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        # MUST CHECK STATUS CODE - HTTP 204 NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_filter_books_returns_200_status_code(self):
        """
        Test that filtering books returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'harry'})
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_books_returns_200_status_code(self):
        """
        Test that searching books returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_books_returns_200_status_code(self):
        """
        Test that ordering books returns HTTP 200 status code
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_data_returns_400_status_code(self):
        """
        Test that invalid data returns HTTP 400 status code
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Invalid future year
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        # MUST CHECK STATUS CODE - HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthorAPITestCase(TestCase):
    """
    Test case for Author API endpoints
    """
    
    def setUp(self):
        """
        Set up test data for author tests
        Uses separate test database automatically
        """
        self.client = APIClient()
        
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")
    
    def test_list_authors_returns_200_status_code(self):
        """
        Test that listing authors returns HTTP 200 status code
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_author_returns_200_status_code(self):
        """
        Test that retrieving an author returns HTTP 200 status code
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        # MUST CHECK STATUS CODE - HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
