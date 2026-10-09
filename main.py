from database import (
    add_user, get_user, add_favorite, get_favorites,
    add_viewed, get_viewed)
from vkapi import get_photos, search_users

age = int(input("Введите возраст:\n"))
gender = int(input("Ваш пол: 1-женский; 2-мужской\n"))
city = int(input("Введите id вашего города:\n"))