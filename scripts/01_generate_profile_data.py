import os
import pandas as pd
import faker
import random
from datetime import datetime, timedelta
import pytz

# Configurable number of records
num_records = 10000

# Distribution of customer tiers
bronze_pct = 0.60
silver_pct = 0.20
gold_pct = 0.15
elite_pct = 0.05

num_bronze = int(num_records * bronze_pct)
num_silver = int(num_records * bronze_pct)
num_gold = int(num_records * gold_pct)
num_elite = int(num_records * elite_pct)

# Adjust for any rounding issues
remaining = num_records - (num_bronze + num_silver + num_gold + num_elite)
num_bronze += remaining

# Use en_TH locale for Faker
fake_en = faker.Faker('en_TH')
fake_th = faker.Faker('th_TH')

# Timezone for Bangkok
bkk_tz = pytz.timezone('Asia/Bangkok')

customer_profiles = []

def generate_customer(tier, customer_id):
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
    account_creation_date = fake_en.date_between(start_date='-1y', end_date='today')
    annual_income = random.randint(500000, 10000000)
    
    if tier == 'Bronze':
        total_aum = random.randint(0, 500000)
    elif tier == 'Silver':
        total_aum = random.randint(500001, 2000000)
    elif tier == 'Gold':
        total_aum = random.randint(2000001, 10000000)
    else:  # Elite
        total_aum = random.randint(10000001, 20000000)
    
    product_holdings = ['deposit', 'payment', 'investment', 'insurance']
    random.shuffle(product_holdings)
    
    asset_allocation = {}
    remaining_aum = total_aum
    
    for product in product_holdings:
        if remaining_aum <= 0:
            asset_allocation[product] = 0
        elif product == product_holdings[-1]:
            asset_allocation[product] = remaining_aum
        else:
            allocation = random.randint(0, remaining_aum)
            asset_allocation[product] = allocation
            remaining_aum -= allocation
    
    product_holding_flags = {product: (asset_allocation[product] > 0) for product in product_holdings}
    
    dob_iso = bkk_tz.localize(datetime(dob.year, dob.month, dob.day, 0, 0, 0)).isoformat()
    account_creation_date_iso = bkk_tz.localize(datetime(account_creation_date.year, account_creation_date.month, account_creation_date.day, 0, 0, 0)).isoformat()
    
    return [
        customer_id, first_name, last_name, dob_iso, gender, email, f"+661{random.randint(1000000, 9999999)}",
        fake_th.address(), 'Thailand', account_creation_date_iso,
        random.choice(['Employed', 'Unemployed', 'Student', 'Retired']),
        annual_income, random.randint(300, 850), random.randint(1, 8),
        random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
        random.randint(0, 5), random.choice([True, False]), random.choice([True, False]),
        random.choice([True, False]), random.choice([True, False]), random.choice([True, False]),
        product_holding_flags['deposit'], product_holding_flags['payment'], product_holding_flags['investment'], product_holding_flags['insurance'],
        asset_allocation['deposit'], asset_allocation['payment'], asset_allocation['investment'], asset_allocation['insurance'],
        total_aum, tier
    ]

for i in range(1, num_bronze + 1):
    customer_id = f"CUST-A{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Bronze', customer_id))

for i in range(num_bronze + 1, num_bronze + num_silver + 1):
    customer_id = f"CUST-A{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Silver', customer_id))

for i in range(num_bronze + num_silver + 1, num_bronze + num_silver + num_gold + 1):
    customer_id = f"CUST-A{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Gold', customer_id))

for i in range(num_bronze + num_silver + num_gold + 1, num_records + 1):
    customer_id = f"CUST-A{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Elite', customer_id))

columns = [
    'customer_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone_number',
    'address', 'country', 'account_creation_date', 'employment_status', 'annual_income', 'credit_score',
    'suitability_test_score', 'marital_status', 'number_of_dependents', 'marketing_consent_email',
    'marketing_consent_sms', 'marketing_consent_line_oa', 'marketing_consent_web_mobile_push',
    'data_processing_consent', 'product_holding_flag_deposit', 'product_holding_flag_payment',
    'product_holding_flag_investment', 'product_holding_flag_insurance', 'asset_under_management_deposit',
    'asset_under_management_payment', 'asset_under_management_investment', 'asset_under_management_insurance',
    'total_asset_under_management', 'customer_tier'
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
