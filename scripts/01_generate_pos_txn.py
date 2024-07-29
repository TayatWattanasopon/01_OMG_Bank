import os
import pandas as pd
import random
from faker import Faker
import uuid

# Initialize Faker
fake = Faker()

# Read USER_IDs from CSV
user_ids_df = pd.read_csv('..\\inputs\\user_ids.csv')
user_ids = user_ids_df.iloc[:, 0].tolist()

# Load master product data with Product IDs
product_df = pd.read_csv('..\\inputs\\products.csv')
products = product_df.to_dict(orient='records')

# Calculate number of orders
num_users = len(user_ids)
num_orders = num_users * 5

# Generate POS_ORDERS data
def generate_pos_orders_data(user_ids, num_orders):
    orders = []
    for _ in range(num_orders):
        order = {
            "ORDER_ID": uuid.uuid4().hex,
            "USER_ID": random.choice(user_ids),
            "ORDER_DATE": fake.date_between(start_date='-1y', end_date='today'),
            "ORDER_AMOUNT": round(random.uniform(20, 500), 2),
            "PROMO_CODE": fake.word() if random.random() > 0.5 else None,
            "PROMO_DISCOUNT": round(random.uniform(0, 50), 2) if random.random() > 0.5 else 0,
            "PURCHASE_LOCATION": fake.city(),
            "TOTAL": 0  # To be calculated based on order details
        }
        orders.append(order)
    return orders

# Generate POS_ORDERS_DETAILS data
def generate_pos_orders_details_data(orders, products):
    order_details = []
    for order in orders:
        num_items = random.randint(1, 5)
        total = 0
        for _ in range(num_items):
            product = random.choice(products)
            detail = {
                "ORDER_DETAIL_ID": uuid.uuid4().hex,
                "PRODUCT_ID": product['Product Id'],
                "ORDER_ID": order['ORDER_ID'],
                "BRAND": product['Brand'],
                "CATEGORY": product['Category'],
                "NAME": product['Model'],
                "PRICE": product['Price'],
                "TYPE": product['Category']
            }
            total += detail["PRICE"]
            order_details.append(detail)
        order["TOTAL"] = total - order["PROMO_DISCOUNT"]
    return order_details

# Generate LOYALTY_TXN data
def generate_loyalty_txn_data(orders):
    loyalty_txns = []
    for order in orders:
        points_earned = round(order["TOTAL"] * 0.25)
        txn = {
            "LOY_TXN_ID": uuid.uuid4().hex,
            "POS_ORDER_ID": order['ORDER_ID'],
            "TRANSACTION_TYPE": 'Earn',
            "POINTS": points_earned,
            "COUPON_ID": None
        }
        loyalty_txns.append(txn)

        # Generate Redeem transaction if there is a discount
        if order["PROMO_DISCOUNT"] > 0:
            redeem_txn = {
                "LOY_TXN_ID": uuid.uuid4().hex,
                "POS_ORDER_ID": order['ORDER_ID'],
                "TRANSACTION_TYPE": 'Redeem',
                "POINTS": -points_earned,
                "COUPON_ID": None
            }
            loyalty_txns.append(redeem_txn)
    return loyalty_txns

# Generate COUPONS data
def generate_coupons_data(loyalty_txns):
    coupons = []
    for txn in loyalty_txns:
        if txn['TRANSACTION_TYPE'] == 'Redeem':
            coupon = {
                "COUPON_ID": uuid.uuid4().hex,
                "COUPON_CODE": fake.bothify(text='????-#####'),
                "STATUS": random.choice(['Redeemed', 'Used', 'Cancelled']),
                "ORDER_ID": txn['POS_ORDER_ID'] if random.random() > 0.5 else None,
                "COUPON_TYPE": random.choice(['Free Coupon', 'Cash Coupon', 'Discount Coupon', 'Cashback Coupon'])
            }
            txn["COUPON_ID"] = coupon["COUPON_ID"]
            coupons.append(coupon)
    return coupons

# Generate data
orders = generate_pos_orders_data(user_ids,num_orders)
order_details = generate_pos_orders_details_data(orders, products)
loyalty_txns = generate_loyalty_txn_data(orders)
coupons = generate_coupons_data(loyalty_txns)

# Save to CSV files
orders_df = pd.DataFrame(orders)
order_details_df = pd.DataFrame(order_details)
loyalty_txns_df = pd.DataFrame(loyalty_txns)
coupons_df = pd.DataFrame(coupons)


# Ensure output directory exists
output_dir = '..\\outputs'
os.makedirs(output_dir, exist_ok=True)

# Save the dataframe to a CSV file
csv_path = os.path.join(output_dir, 'pos_orders.csv')
orders_df.to_csv(csv_path, index=False)

csv_path = os.path.join(output_dir, 'pos_orders_details.csv')
order_details_df.to_csv(csv_path, index=False)

csv_path = os.path.join(output_dir, 'loyalty_txn.csv')
loyalty_txns_df.to_csv(csv_path, index=False)

csv_path = os.path.join(output_dir, 'coupons.csv')
coupons_df.to_csv(csv_path, index=False)

# orders_df.to_csv('/mnt/data/pos_orders.csv', index=False)
# order_details_df.to_csv('/mnt/data/pos_orders_details.csv', index=False)
# loyalty_txns_df.to_csv('/mnt/data/loyalty_txn.csv', index=False)
# coupons_df.to_csv('/mnt/data/coupons.csv', index=False)
