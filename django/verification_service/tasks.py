from celery import shared_task
import time
import random


@shared_task
def verify_user(user_id):
    # Simulate the external API call
    time.sleep(random.randint(1, 100))
    # Return the verification result (0 for simplicity)
    return 0


@shared_task
def send_verification_result(user_id, result):
    # Implement the logic to notify the user about the verification result
    # This could be sending an email, updating a status in the database, etc.
    print(f"Verification result for user {user_id}: {result}")
