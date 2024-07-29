import random
from faker import Faker

fake = Faker()

brands = ['Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour']
categories = ['men', 'women', 'kids']
types = ['tops', 'pants', 'shoes', 'accessories']
status_options = [True, False]

def generate_product_data(num_products=10):
    products = []
    for _ in range(num_products):
        product = {
            "PRODUCT_ID": fake.unique.random_int(min=1000000000, max=9999999999),
            "BRAND": random.choice(brands),
            "CATEGORY": random.choice(categories),
            "IMAGE_URL": fake.image_url(),
            "IS_NEW_PRODUCT": random.choice(status_options),
            "IS_SALE_PRODUCT": random.choice(status_options),
            "NAME": fake.catch_phrase(),
            "PRICE": round(random.uniform(10.0, 500.0), 2),
            "SKU": fake.unique.ean13(),
            "TYPE": random.choice(types)
        }
        products.append(product)
    return products

product_data = generate_product_data(20)
import pandas as pd

product_df = pd.DataFrame(product_data)
import ace_tools as tools; tools.display_dataframe_to_user(name="Generated Product Data", dataframe=product_df)