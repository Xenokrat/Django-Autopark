import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_homepage():
    client = Client()
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login():
    user = User.objects.create_user(username='testuser', password='password')
    client = Client()
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302  # Assuming redirect after login
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_create_car():
    user = User.objects.create_user(username='testuser', password='password')
    client = Client()
    client.login(username='testuser', password='password')
    # response = client.post(reverse('vehicle_create'), kwargs={'name': 'Test Car', 'model': 'Test Model', 'price': 10000, 'pk': 1})
    # assert response.status_code == 302
    # assert response.url == reverse('vehicles')
