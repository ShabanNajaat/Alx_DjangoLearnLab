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
        """
        # Create test client
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com'
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
        self.book4 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author1
        )
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can list books
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_retrieve_book_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve a single book
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create books
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
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 5)  # Should have 5 books now
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update books
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
        
        # Verify the book was actually updated in the database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)  # Should have 3 books now
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by title
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books
        self.assertIn('Harry', response.data[0]['title'])
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author name
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author__name': 'rowling'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by Rowling
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 book from 1997
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_search_books(self):
        """
        Test searching books across title and author fields
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 Harry Potter books
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'tolkien'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 book by Tolkien
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title ascending
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be in alphabetical order
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title descending
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))  # Should be in reverse alphabetical order
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year descending (newest first)
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))  # Should be newest first
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering
        """
        url = reverse('book-list')
        response = self.client.get(url, {
            'author__name': 'rowling',
            'ordering': '-publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by Rowling
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)
    
    def test_invalid_publication_year_validation(self):
        """
        Test that publication year validation works (cannot be in future)
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class AuthorAPITestCase(TestCase):
    """
    Test case for Author API endpoints
    """
    
    def setUp(self):
        """
        Set up test data for author tests
        """
        self.client = APIClient()
        
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")
        
        # Create books for authors
        self.book1 = Book.objects.create(
            title="Book 1",
            publication_year=2000,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Book 2", 
            publication_year=2001,
            author=self.author1
        )
    
    def test_list_authors(self):
        """
        Test listing all authors
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_author_with_books(self):
        """
        Test retrieving a single author with nested books
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
        self.assertEqual(len(response.data['books']), 2)  # Should have 2 books
        self.assertEqual(response.data['books'][0]['title'], self.book1.title)
