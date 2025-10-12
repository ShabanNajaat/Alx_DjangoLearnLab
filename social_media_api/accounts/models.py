from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.followers.add(user)
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user != self:
            self.followers.remove(user)
    
    def is_following(self, user):
        """Check if following a user"""
        return self.followers.filter(id=user.id).exists()
    
    def get_following_count(self):
        """Get number of users this user is following"""
        return self.followers.count()
    
    def get_followers_count(self):
        """Get number of followers"""
        return self.following.count()
