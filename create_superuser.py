import os
import django
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv('.env')

django.setup()

User = get_user_model()
username = os.getenv('USERNAME')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print("Superuser already exists.")