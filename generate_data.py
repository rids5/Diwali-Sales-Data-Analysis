import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 11251

states = {
    'Uttar Pradesh': 'Central', 'Maharashtra': 'Western', 'Karnataka': 'Southern',
    'Delhi': 'Northern', 'Madhya Pradesh': 'Central', 'Andhra Pradesh': 'Southern',
    'Himachal Pradesh': 'Northern', 'Gujarat': 'Western', 'Telangana': 'Southern',
    'Tamil Nadu': 'Southern', 'Rajasthan': 'Northern', 'Punjab': 'Northern'
}
state_names = list(states.keys())
state_weights = [0.18, 0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.03]

occupations = ['IT Sector', 'Healthcare', 'Aviation', 'Banking', 'Govt', 'Lawyer',
               'Media', 'Agriculture', 'Food Processing', 'Textile', 'Automobile', 'Construction']

product_categories = ['Clothing & Apparel', 'Food', 'Electronics & Gadgets', 'Footwear & Shoes',
                      'Games & Toys', 'Home & Furniture', 'Sports Products', 'Auto', 'Beauty', 'Office', 'Books']

age_groups = ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+']
age_group_weights = [0.02, 0.18, 0.35, 0.25, 0.10, 0.07, 0.03]

category_price = {
    'Electronics & Gadgets': (5000, 80000),
    'Home & Furniture':      (3000, 50000),
    'Auto':                  (10000, 100000),
    'Clothing & Apparel':    (500,  8000),
    'Footwear & Shoes':      (800,  12000),
    'Food':                  (200,  3000),
    'Games & Toys':          (500,  15000),
    'Sports Products':       (1000, 20000),
    'Beauty':                (300,  5000),
    'Office':                (1000, 25000),
    'Books':                 (200,  2000),
}

rows = []
for i in range(n):
    state = random.choices(state_names, weights=state_weights)[0]
    zone  = states[state]
    age_group = random.choices(age_groups, weights=age_group_weights)[0]
    if age_group == '0-17':    age = random.randint(10, 17)
    elif age_group == '18-25': age = random.randint(18, 25)
    elif age_group == '26-35': age = random.randint(26, 35)
    elif age_group == '36-45': age = random.randint(36, 45)
    elif age_group == '46-50': age = random.randint(46, 50)
    elif age_group == '51-55': age = random.randint(51, 55)
    else:                      age = random.randint(56, 70)

    gender = random.choices(['F', 'M'], weights=[0.55, 0.45])[0]
    marital = random.choices([0, 1], weights=[0.4, 0.6])[0]
    occ = random.choice(occupations)
    cat = random.choices(product_categories,
                         weights=[0.20, 0.15, 0.13, 0.10, 0.08, 0.08, 0.07, 0.05, 0.05, 0.05, 0.04])[0]
    orders = random.randint(1, 4)
    lo, hi = category_price[cat]
    amount = round(random.uniform(lo, hi) * orders, 2)

    rows.append({
        'User_ID':          f'U{1000000 + i}',
        'Cust_name':        f'Customer_{i+1}',
        'Product_ID':       f'P{random.randint(10000, 19000)}',
        'Gender':           gender,
        'Age Group':        age_group,
        'Age':              age,
        'Marital_Status':   marital,
        'State':            state,
        'Zone':             zone,
        'Occupation':       occ,
        'Product_Category': cat,
        'Orders':           orders,
        'Amount':           amount,
        'Status':           None,
        'unnamed1':         None,
    })

df = pd.DataFrame(rows)
df.to_csv('Diwali Sales Data.csv', index=False, encoding='utf-8')
print(f"Dataset created: {df.shape}")
print(df.head(3))
