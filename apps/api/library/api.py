"""
Library API
Koha/Alice integration
"""
from typing import Optional
from django.db.models import Q
from django.utils import timezone
from ninja import Router, Query
from .models import LibraryMember, Book, BookLoan

router = Router()


@router.get("/catalog", response=list)
def search_catalog(request, q: str = '', category: str = ''):
    books = Book.objects.all()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    if category:
        books = books.filter(category=category)
    return [{'title': b.title, 'author': b.author, 'available': b.copies_available} for b in books[:20]]


@router.get("/loans")
def get_loans(request, student_id: str = ''):
    loans = BookLoan.objects.filter(status='borrowed')
    if student_id:
        loans = loans.filter(student_id=student_id)
    return [{'book': l.book.title, 'due': l.due_date} for l in loans]


@router.post("/loan")
def create_loan(request, data: dict):
    loan = BookLoan.objects.create(
        book_id=data['book_id'],
        student_id=data['student_id'],
        issue_date=timezone.now().date(),
        due_date=data['due_date'],
        status='borrowed'
    )
    return {'id': str(loan.id)}


@router.post("/return")
def return_book(request, data: dict):
    loan = BookLoan.objects.get(id=data['loan_id'])
    loan.status = 'returned'
    loan.return_date = timezone.now().date()
    loan.save()
    return {'message': 'Book returned'}