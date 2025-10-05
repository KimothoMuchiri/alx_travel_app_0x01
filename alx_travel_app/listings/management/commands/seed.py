from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Bookings, Review
from faker import Faker
from datetime import timedelta
import random
from ...models import Listing, Bookings, Review

class Command(BaseCommand):
    
    help = 'Seeds the database with sample Listings, Bokings and Reviews'

    # main execution logic
    def handle(self, *args, **options):
        # initialize Faker
        fake = Faker()

        # Cleanup code
        self.stdout.write("Cleaning old data .....")
        Review.objects.all().delete()
        Bookings.objects.all().delete()
        Listing.objects.all().delete()

        self.stdout.write("Creating Users for foreign Keys.....")
        if not User.objects.exists():
            User.objects.create_user(username = 'tester1', email = 't1@example.com', password = 'password1')
            User.objects.create_user(username = 'tester2', email = 't2@example.com', password = 'password2')
            User.objects.create_user(username = 'tester3', email = 't3@example.com', password = 'password3')
        users = list(User.objects.all())

        self.stdout.write("Creating 50 listings....")
        listings = []

        for _ in range(50):
            listing = Listing.objects.create(
                title = fake.catch_phrase(),
                description = fake.text(max_nb_chars = 500),
                price_per_night = random.randint(50, 500)*10,
                location = fake.city() + ", " + fake.country_code(),
            )

            listings.append(listing)

        self.stdout.write("Creating 50 bookings....")
        bookings = []
        for _ in range(50):
            random_user = random.choice(users)
            random_listing = random.choice(listings)

            check_in = fake.future_date(end_date='+180d') # Example date in the next month
            stay_duration = random.randint(1, 14)
            # Use timedelta to calculate the check_out date
            check_out = check_in + timedelta(days=stay_duration)
            #check_out = fake.date_between(start_date=check_in, end_date='+7d')
            price = random.randint(100, 500) 
            
            booking = Bookings.objects.create(
                guest = random_user,
                Listing = random_listing,
                check_in_date = check_in,
                check_out_date = check_out,
                total_price = price,
            )
            bookings.append(booking)

        self.stdout.write("Creating 50 reviews....")
        reviews = []
        for _ in range(50):
            random_user = random.choice(users)
            random_listing = random.choice(listings)
            rating_score = random.randint(1, 5)

            review = Review.objects.create(
                author = random_user,
                Listing = random_listing,
                rating = rating_score,
                comment = fake.text(max_nb_chars = 500),
                # since we set created_at with auto_now_add=True in the model, 
                # you can actually remove that line entirely and let Django handle it for simplicity
            )
            reviews.append(review)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded the database with {len(listings)} Listings, {len(bookings)} Bookings, and {len(reviews)} Reviews!'))