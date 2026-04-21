"""
Library Models
Koha/Alice integration
"""
from django.db import models


class LibraryMember(models.Model):
    """Library member extending student"""
    student = models.OneToOneField(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='library_membership'
    )
    library_id = models.CharField(max_length=50, unique=True)
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('undergraduate', 'Undergraduate'),
            ('postgraduate', 'Postgraduate'),
            ('staff', 'Staff'),
            ('researcher', 'Researcher')
        ]
    )
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    """Library book catalog"""
    isbn = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=50, blank=True)
    copies_total = models.IntegerField(default=1)
    copies_available = models.IntegerField(default=1)


class BookLoan(models.Model):
    """Book loan tracking"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    student = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, related_name='loans')
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
            ('lost', 'Lost')
        ]
    )