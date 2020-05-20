from django.contrib.auth.models import User
from django.db.models import Sum
from accounts.models import Account
from transactions.models import Transaction
from django.utils import timezone
from datetime import timedelta

import os

def generate_report():
    end_time = timezone.now()
    start_time = end_time - timedelta(days=1)

    dirname = os.path.dirname(os.path.abspath(__file__))
    report_file = os.path.join(dirname, f'report-{end_time}.txt')

    with open(report_file, 'w') as f:
        f.write(f"""
Total number of users: {User.objects.all().count()}
Total number of accounts: {Account.objects.all().count()}
Total number of transactions: {Transaction.objects.all().count()}

Total cash on platform: {list(Account.objects.all().aggregate(Sum('balance')).values())[0]}

===
Daily stats (as of {end_time})
===
New accounts: {Account.objects.filter(created_at__range=(start_time, end_time)).count()}
New transactions: {Transaction.objects.filter(created_at__range=(start_time, end_time)).count()}
Amount in new transactions: {list(
    Transaction.objects
        .filter(created_at__range=(start_time, end_time))
        .aggregate(Sum('amount'))
        .values()
    )[0]}
        """)

    # upload to gcloud storage
    
    from google.cloud import storage
    client = storage.Client()
    bucket = client.get_bucket(os.getenv('GCP_REPORT_BUCKET_ID', 'mobile_wallet_test_reports'))

    blob = bucket.blob('report-{end_time}.txt')
    blob.upload_from_filename(filename=report_file)

    latest_blob = bucket.blob('latest_report.txt')
    latest_blob.upload_from_filename(filename=report_file)