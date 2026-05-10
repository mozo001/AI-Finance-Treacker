from django.db import models

# Create your models here.


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    
    # Categories for AI to target later
    CATEGORIES = (
        ('food', 'Food & Dining'),
        ('tech', 'Tech & Subscription'),
        ('travel', 'Travel/Commute'),
        ('education', 'Education/Books'),
        ('other', 'Misc'),
    )

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"