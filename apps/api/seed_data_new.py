#!/usr/bin/env python
"""
Seed script - Creates EMPTY database by default
Each university/polytechnic configures their own data via API
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

from students.models import User

try:
    User.objects.create_superuser("admin", "admin@uni.edu", "admin123")
    print("✓ Admin: admin@uni.edu / admin123")
except Exception as e:
    print(f"⚠ {e}")

print("""
================================================
SYSTEM READY FOR MULTI-UNIVERSITY CONFIGURATION
================================================

INITIAL LOGIN:
  Email:    admin@uni.edu
  Password: admin123

TO CONFIGURE YOUR INSTITUTION:

1. Login to get token:
   POST /api/auth/login
   { "email": "admin@uni.edu", "password": "admin123" }

2. Create YOUR university:
   POST /api/university/universities
   Headers: Authorization: Bearer <token>
   {
     "name": "Your University Name",
     "short_name": "SHORTNAME",
     "code": "CODE",
     "academic_system": "british_nigerian",  // or "american", "polytechnic"
     "system_type": "university",  // or "polytechnic"
     "email": "admin@youruni.edu",
     "phone": "+234xxxxxxxxxx",
     "address": "City, State, Nigeria"
   }

3. Add faculties:
   POST /api/university/faculties

4. Add departments:
   POST /api/university/departments

5. Add programmes:
   POST /api/university/programmes

NO DEFAULT DATA - Each institution configures their own!
""")