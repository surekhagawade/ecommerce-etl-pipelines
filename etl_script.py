import os
import pandas as pd
from sqlalchemy import create_engine

print("--- ETL Pipeline Started ---")

# १. तुमच्या कम्प्युटरमधील CSV फाईल्सचा अचूक पाथ (Path) इथे टाका
# (उदा. जर फाईल्स 'archive' फोल्डरमध्ये असतील तर)
data_folder = "./archive"  

# २. PostgreSQL डेटाबेस कनेक्शन (तुमचा पासवर्ड 'Dnya@123' वापरला आहे)
db_url = "postgresql://postgres:Dnya@123@localhost:5432/ecommerce_dw"
engine = create_engine(db_url)
print("डेटाबेस कनेक्शन यशस्वी झाले!")

# ३. लोड करायच्या मुख्य CSV फाईल्सची यादी
files_to_load = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products"
}

# ४. लूप चालवून सर्व डेटा डेटाबेसमध्ये भरणे (ETL Process)
for file_name, table_name in files_to_load.items():
    file_path = os.path.join(data_folder, file_name)
    
    if os.path.exists(file_path):
        print(f"लोड होत आहे: {file_name} -> टेबल: {table_name}...")
        
        # डेटा रीड करणे
        df = pd.read_csv(file_path)
        
        # डेटाबेसमध्ये टेबल तयार करून डेटा लोड करणे
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"यशस्वीरित्या लोड झाले! एकूण रोज: {len(df)}")
    else:
        print(f"⚠️ एरर: फाईल सापडली नाही: {file_name}")

print("--- ETL Pipeline Successfully Completed! ---")
