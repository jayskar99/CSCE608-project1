import csv
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# Configuration
NUM_BOOKS = 2000
NUM_PERSONS = 300
NUM_HISTORY = 1000
NUM_RESERVATIONS = 500
NUM_PUBLISHERS = 50

def generate_csv(filename, fieldnames, data):
    with open('Data/' + filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(data)

# 1. Generate Publishers
publishers = []
for i in range(1, NUM_PUBLISHERS + 1):
    publishers.append({
        'id': i,
        'name': fake.company(),
        'phone_number': fake.phone_number(),
        'address': fake.address().replace('\n', ', ')
    })

# 2. Generate Books
books = []
genres = ['Sci-Fi', 'Mystery', 'History', 'Fantasy', 'Biography', 'Technical']
for _ in range(NUM_BOOKS):
    books.append({
        'isbn': fake.isbn13(),
        'title': fake.catch_phrase(),
        'author': fake.name(),
        'genre': random.choice(genres),
        'publication_year': random.randint(1950, 2025),
        'page_count': random.randint(100, 1000),
        'rating': round(random.uniform(1.0, 5.0), 2),
        'publisher_id': random.randint(1, NUM_PUBLISHERS)
    })

# 3. Generate Persons
persons = []
for i in range(1000, 1000 + NUM_PERSONS):
    persons.append({
        'card_number': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone_number': fake.phone_number(),
        'address': fake.address().replace('\n', ', ')
    })

# 4. Generate History (and associated Late entries)
history = []
late_entries = []
for i in range(1, NUM_HISTORY + 1):
    checkout = fake.date_time_between(start_date='-1y', end_date='now')
    due = checkout + timedelta(days=14)
    # 80% chance it was returned
    return_date = None
    if random.random() > 0.2:
        return_date = checkout + timedelta(days=random.randint(1, 25))
        
        # Check if it was late
        if return_date.date() > due.date():
            days_late = (return_date.date() - due.date()).days
            late_entries.append({
                'id': len(late_entries) + 1,
                'history_id': i,
                'amount_late': days_late
            })

    history.append({
        'id': i,
        'checkout_dt': checkout.strftime('%Y-%m-%d %H:%M:%S'),
        'due_date': due.strftime('%Y-%m-%d'),
        'return_date': return_date.strftime('%Y-%m-%d') if return_date else '',
        'isbn': random.choice(books)['isbn'],
        'card_number': random.choice(persons)['card_number']
    })

# 5. Generate Price (Rate Card)
prices = []
for days in range(1, 31): # 1 to 30 days late
    prices.append({
        'id': days,
        'late_id': days,
        'dollar_amount': round(days * 0.50, 2) # $0.50 per day
    })

# 6. Generate Reservations
reservations = []
for i in range(1, NUM_RESERVATIONS + 1):
    reservations.append({
        'id': i,
        'end_date': fake.date_between(start_date='now', end_date='+1m'),
        'status': random.choice(['Active', 'Pending', 'Expired']),
        'isbn': random.choice(books)['isbn'],
        'card_number': random.choice(persons)['card_number']
    })

# 7. Generate Fees (for those who are late)
fees = []
for i, late in enumerate(late_entries):
    fees.append({
        'id': i + 1,
        'price_id': late['amount_late'] if late['amount_late'] <= 30 else 30,
        'status': random.choice(['Paid', 'Unpaid']),
        'card_number': next(h['card_number'] for h in history if h['id'] == late['history_id'])
    })

# Export all to CSV
generate_csv('PUBLISHER.csv', publishers[0].keys(), publishers)
generate_csv('BOOK.csv', books[0].keys(), books)
generate_csv('PERSON.csv', persons[0].keys(), persons)
generate_csv('HISTORY.csv', history[0].keys(), history)
generate_csv('LATE.csv', late_entries[0].keys(), late_entries)
generate_csv('PRICE.csv', prices[0].keys(), prices)
generate_csv('FEE.csv', fees[0].keys(), fees)
generate_csv('RESERVATION.csv', reservations[0].keys(), reservations)

print("CSV files generated successfully!")