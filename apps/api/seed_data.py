#!/usr/bin/env python
"""Seed script to create initial data"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from students.models import User
from university.models import University, Faculty, Department, Programme, Session, Semester
from decimal import Decimal

# Create superuser
try:
    user = User.objects.create_superuser('admin', 'admin@university.edu', 'admin123')
    print(f'✓ Admin user created: {user.username}')
except Exception as e:
    print(f'⚠ Admin exists or error: {e}')

# Create a test university (British/Nigerian)
uni, created = University.objects.get_or_create(
    code='UNN',
    defaults={
        'name': 'University of Nigeria',
        'short_name': 'UNN',
        'academic_system': 'british_nigerian',
        'system_type': 'university',
        'email': 'info@unn.edu.ng',
        'phone': '+234-80-xxxxxxx',
        'address': 'Nsukka, Enugu State, Nigeria',
    }
)
print(f'✓ University: {uni.short_name} ({uni.get_academic_system_display()})')

# Create Faculty
faculty, created = Faculty.objects.get_or_create(
    university=uni,
    code='ENG',
    defaults={'name': 'Faculty of Engineering', 'dean': 'Prof. ABC'}
)
print(f'✓ Faculty: {faculty.code}')

# Create Department
dept, created = Department.objects.get_or_create(
    faculty=faculty,
    code='CSE',
    defaults={'name': 'Computer Science', 'hod': 'Dr. XYZ'}
)
print(f'✓ Department: {dept.code}')

# Create Programme
prog, created = Programme.objects.get_or_create(
    department=dept,
    code='CSC',
    defaults={
        'name': 'Computer Science',
        'programme_type': 'BACHELOR',
        'duration_years': 4,
        'CCMAS_code': 'ENG/CSC/001'
    }
)
print(f'✓ Programme: {prog.code}')

# Create Session
session, created = Session.objects.get_or_create(
    university=uni,
    session='2025/2026',
    defaults={
        'start_date': '2025-01-01',
        'end_date': '2025-12-31',
        'is_current': True,
        'tuition_fee': Decimal('150000.00'),
    }
)
print(f'✓ Session: {session.session}')

# Create Semester
sem, created = Semester.objects.get_or_create(
    session=session,
    semester=1,
    defaults={
        'name': 'First Semester',
        'start_date': '2025-01-01',
        'end_date': '2025-06-30',
    }
)
print(f'✓ Semester: {sem.name}')

# Create American University for comparison
uni_us, created = University.objects.get_or_create(
    code='AUS',
    defaults={
        'name': 'American University Nigeria',
        'short_name': 'AUN',
        'academic_system': 'american',
        'system_type': 'university',
        'email': 'info@aun.edu.ng',
        'address': 'Abuja, Nigeria',
    }
)
print(f'✓ American-style University: {uni_us.short_name}')

# Create Polytechnic
poly, created = University.objects.get_or_create(
    code='POLY',
    defaults={
        'name': 'Federal Polytechnic',
        'short_name': 'FEDPO',
        'academic_system': 'polytechnic',
        'system_type': 'polytechnic',
        'email': 'info@fedpo.edu.ng',
        'address': 'Niger State, Nigeria',
        'nbte_accredited': True,
    }
)
print(f'✓ Polytechnic: {poly.short_name}')

print('\n✅ Database seeded successfully!')
print('\nAvailable Endpoints:')
print('  - http://localhost:8001/api/config')
print('  - http://localhost:8001/api/config/presets')
print('  - http://localhost:8001/api/system-info')
print('  - http://localhost:8001/admin/')
print('\nAdmin Login: admin / admin123')