import os
import pandas as pd
import faker
import random
from datetime import datetime
import pytz
import uuid

# Configurable number of records
start_num_record = 1001
num_records = 100
user_id_prefix = "CUST-A"


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

# Timezone for Bangkok
bkk_tz = pytz.timezone('Asia/Bangkok')

customer_profiles = []

def extract_province_zip_code(address):
    address_parts = address.split(' ')
    if len(address_parts) > 1:
        zip_code = address_parts[-1]
        province = address_parts[-2]
        return province, zip_code
    return None, None

def generate_customer(tier, customer_id):
    gender = random.choice(['Male', 'Female', 'Other'])
    if gender == 'Male':
        first_name = fake_en.first_name_male()
    elif gender == 'Female':
        first_name = fake_en.first_name_female()
    else:
        first_name = random.choice([fake_en.first_name_male(), fake_en.first_name_female()])
    
    last_name = fake_en.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{random.choice(['@gmailx.com', '@hotmailx.com'])}"
    dob = fake_en.date_of_birth()
    account_creation_date = fake_en.date_between(start_date='-1y', end_date='today')

    dob_iso = bkk_tz.localize(datetime(dob.year, dob.month, dob.day, 0, 0, 0)).isoformat()
    account_creation_date_iso = bkk_tz.localize(datetime(account_creation_date.year, account_creation_date.month, account_creation_date.day, 0, 0, 0)).isoformat()
    
    signup_source = random.choice(['Web', 'iOS', 'Android'])
    
    anonymous_id = str(uuid.uuid4())

    while True:
        address = fake_th.address()
        province, zip_code = extract_province_zip_code(address)

        
        if len(zip_code) > 1 and zip_code.isdigit() and len(zip_code) == 5:
            # Remove "จ." and "จังหวัด" from the province names
            province = province.replace("จ.", "").replace("จังหวัด", "").strip()
            if province in ["กทม.", "กรุงเทพ", "กรุงเทพมหานคร", "กรุงเทพฯ"]:
                province = "กรุงเทพมหานคร"
            break

    return [
        customer_id, anonymous_id, first_name, last_name, dob_iso, gender, email, f"+661{random.randint(1000000, 9999999)}",
        address, 'Thailand', account_creation_date_iso,
        # random.choice([True, False]), 
        # random.choice([True, False]),
        # random.choice([True, False]), 
        # random.choice([True, False]), 
        # random.choice([True, False]), 
        # signup_source,
        province,
        zip_code,
        tier
    ]

for i in range(start_num_record, start_num_record + num_bronze + 1):
    customer_id = f"{user_id_prefix}{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Bronze', customer_id))

for i in range(start_num_record + num_bronze + 1, start_num_record + num_bronze + num_silver + 1):
    customer_id = f"{user_id_prefix}{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Silver', customer_id))

for i in range(start_num_record + num_bronze + num_silver + 1, start_num_record + num_bronze + num_silver + num_gold + 1):
    customer_id = f"{user_id_prefix}{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Gold', customer_id))

for i in range(start_num_record + num_bronze + num_silver + num_gold + 1, num_records + start_num_record):
    customer_id = f"{user_id_prefix}{str(i).zfill(6)}"
    customer_profiles.append(generate_customer('Elite', customer_id))

columns = [
    'user_id', 'anonymousId', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone_number',
    'address', 'country', 'account_creation_date', 
    # 'marketing_consent_email',
    # 'marketing_consent_sms', 
    # 'marketing_consent_line_oa', 
    # 'marketing_consent_web_mobile_push',
    # 'data_processing_consent', 
    # 'signup_source',
    'province',
    'zip_code',
    'customer_tier'
]

df_customer_profile = pd.DataFrame(customer_profiles, columns=columns)

# Ensure output directory exists
output_dir = '..\\outputs'
os.makedirs(output_dir, exist_ok=True)

# Ensure output directory exists
input_dir = '..\\inputs'
os.makedirs(input_dir, exist_ok=True)

df_user_id = df_customer_profile[['user_id']]

# Save the dataframe to a CSV file
csv_path = os.path.join(output_dir, 'customer_profile_ecomm.csv')
df_customer_profile.to_csv(csv_path, index=False)

# Save the 'user_id' column to a new CSV file
csv_path_user_id = os.path.join(input_dir, 'user_ids.csv')
df_user_id.to_csv(csv_path_user_id, index=False, header=False)

# Save the dataframe to a JSON file
# json_path = os.path.join(output_dir, 'customer_profile_ecomm.json')
# df_customer_profile.to_json(json_path, orient='records', lines=True)

# Save the dataframe to a JSON file (single array)
json_path = os.path.join(output_dir, 'customer_profile_ecomm.json')
df_customer_profile.to_json(json_path, orient='records', lines=False)

# Display the first 10 records
df_first_10_customers = df_customer_profile.head(10)
print(df_first_10_customers)


df_last_10_customers = df_customer_profile.tail(10)
print(df_last_10_customers)