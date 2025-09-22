# Advanced API Project Setup Guide

## Project Overview
This project demonstrates advanced API development with Django REST Framework, featuring custom serializers with nested relationships and complex data validation.

## Models Implemented

### Author Model
- name: CharField (max_length=100)
- One-to-many relationship with Book model

### Book Model
- title: CharField (max_length=200)
- publication_year: IntegerField
- author: ForeignKey to Author model

## Serializers Implemented

### BookSerializer
- Serializes all Book model fields
- Custom validation: Prevents future publication years
- Used for both serialization and deserialization

### AuthorSerializer
- Serializes Author model with nested Book objects
- Includes related books as nested serialized data
- Read-only nested books field

## Installation:
```bash
pip install -r requirements.txt
