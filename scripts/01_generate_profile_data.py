import os
import pandas as pd
import faker
import random
from datetime import datetime, timedelta

# Configurable number of records
num_records = 100

# Distribution of customer tiers
bronze_pct = 0.60
silver_pct = 0.20
gold_pct = 0.15
elite_pct = 0.05

num_bronze = int(num_records * bronze_pct)
num_silver = int(num_records * silver_pct)
num_gold = int(num_records * gold_pct)
num_elite = int(num_records * elite_pct)

# Adjust for any rounding issues
remaining = num_records - (num_bronze + num_silver + num_gold + num_elite)
num_bronze += remaining

# Use en_TH locale for Faker
fake_en = faker.Faker('en_TH')
fake_th = faker.Faker('th_TH')

customer_profiles = []

def generate_customer(tier):
    gender = random.choice(['Male', 'Female', 'Other'])
    if gender == 'Male':
        first_name = fake_en.first_name_male()
    elif gender == 'Female':
        first_name = fake_en.first_name_female()
    else:
        first_name = random.choice([fake_en.first_name_male(), fake_en.first_name_female()])
    
    last_name = fake_en.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    dob = fake_en.date_of_birth()
    account_creation_date = fake_en.date_between(start_date='-10y', end_date='today')
    annual_income = random.randint(100000, 1000000)
    
    product_holding_deposit = random.choice([True, False])
    product_holding_payment = random.choice([True, False])
    product_holding_investment = random.choice([True, False])
    product_holding_insurance = random.choice([True, False])
    
    asset_deposit = random.randint(0, 500000) if product_holding_deposit else 0
    asset_payment = random.randint(0, 500000) if product_holding_payment else 0
    asset_investment = random.randint(0, 500000) if product_holding_investment else 0
    asset_insurance = random.randint(0, 500000) if product_holding_insurance else 0
    
    if tier == 'Bronze':
        total_aum = random.randint(0, 500000)
    elif tier == 'Silver':
        total_aum = random.randint(500001, 2000000)
    elif tier == 'Gold':
        total_aum = random.randint(2000001, 10000000)
    else: # Elite
        total_aum = random.randint(10000001, 20000000)
    
    return [
        first_name, last_name, dob, gender, email, f"+661{random.randint(1000000, 9999999)}",
        fake_th.street_address(), fake_th.province(), fake_th.amphoe(), fake_th.tambon(),
        fake_th.postcode(), 'Thailand', account_creation_date,
        random.choice(['Employed', 'Unemployed', 'Student', 'Retired']),
        annual_income, random.randint(300, 850), random.randint(1, 8),
        random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
        random.randint(0, 5), random.choice([True, False]), random.choice([True, False]),
        random.choice([True, False]), random.choice([True, False]), random.choice([True, False]),
        product_holding_deposit, product_holding_payment, product_holding_investment, product_holding_insurance,
        asset_deposit, asset_payment, asset_investment, asset_insurance, total_aum, tier
    ]

for i in range(1, num_bronze + 1):
    customer_profiles.append([i] + generate_customer('Bronze'))

for i in range(num_bronze + 1, num_bronze + num_silver + 1):
    customer_profiles.append([i] + generate_customer('Silver'))

for i in range(num_bronze + num_silver + 1, num_bronze + num_silver + num_gold + 1):
    customer_profiles.append([i] + generate_customer('Gold'))

for i in range(num_bronze + num_silver + num_gold + 1, num_records + 1):
    customer_profiles.append([i] + generate_customer('Elite'))

columns = [
    'customer_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone_number',
    'address', 'province', 'amphoe', 'tambon', 'zip_code', 'country', 'account_creation_date',
    'employment_status', 'annual_income', 'credit_score', 'suitability_test_score', 'marital_status',
    'number_of_dependents', 'marketing_consent_email', 'marketing_consent_sms', 'marketing_consent_line_oa',
    'marketing_consent_web_mobile_push', 'data_processing_consent', 'product_holding_flag_deposit',
    'product_holding_flag_payment', 'product_holding_flag_investment', 'product_holding_flag_insurance',
    'asset_under_management_deposit', 'asset_under_management_payment', 'asset_under_management_investment',
    'asset_under_management_insurance', 'total_asset_under_management', 'customer_tier'
]

df_customer_profile = pd.DataFrame(customer_profiles, columns=columns)

# Ensure output directory exists
output_dir = '..\\outputs'
os.makedirs(output_dir, exist_ok=True)

# Save the dataframe to a CSV file
csv_path = os.path.join(output_dir, 'customer_profile.csv')
df_customer_profile.to_csv(csv_path, index=False)

# Display the first 10 records
df_first_10_customers = df_customer_profile.head(10)
print(df_first_10_customers)
