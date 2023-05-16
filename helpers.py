from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
import streamlit as st
import pandas as pd

CUSTOMERS_COLUMNS = [
  "customer_id",
  "customer_unique_id",
  "customer_zip_code_prefix",
  "customer_city",
  "customer_state",
]

PRODUCT_COLUMNS = [
  "product_id",
  "product_category_name",
  "product_name_lenght",
  "product_description_lenght",
  "product_photos_qty",
  "product_weight_g",
  "product_length_cm",
  "product_height_cm",
  "product_width_cm",
]

ORDER_COLUMNS = [
  "order_id",
  "customer_id",
  "order_status",
  "order_purchase_timestamp",
  "order_approved_at",
  "order_delivered_carrier_date",
  "order_delivered_customer_date",
  "order_estimated_delivery_date",
]

ORDER__PRODUCT_COLUMNS = [
  "order_id",
  "order_item_id",
  "product_id",
  "seller_id",
  "shipping_limit_date",
  "price",
  "freight_value"
]

def validate_file(dataframe, type="customers"):
  if dataframe is None:
    st.error(f"Please upload a {type} file", icon="🚨")
    return False
  
  if type == "customers":
    columns = CUSTOMERS_COLUMNS
  elif type == "products":
    columns = PRODUCT_COLUMNS
  elif type == "orders":
    columns = ORDER_COLUMNS
  elif type == "orders_products":
    columns = ORDER__PRODUCT_COLUMNS
  else:
    st.error(f"Please upload a valid {type} file", icon="🚨")
    return False

  missing_columns = [column for column in columns if column not in dataframe.columns]

  if not all([column in dataframe.columns for column in columns]):
    st.error(f"Your file is for {type} missing the following columns: {missing_columns}", icon="🚨")
    return False
  
  return True
  
  
def process_data(customers_dataframe, products_dataframe, orders_dataframe, orders_products_dataframe):
  # Total number of customers
  total_customers = customers_dataframe.shape[0]
  # st.write(f"Total number of customers: {total_customers}")
  #total number of unique customers
  total_unique_customers = customers_dataframe["customer_unique_id"].nunique()
  
  # Total number of products
  total_products = products_dataframe.shape[0]
  # st.write(f"Total number of products: {total_products}")
  # Total number of unique products
  total_unique_products = products_dataframe["product_id"].nunique()
  
  # Total number of orders
  total_orders = orders_dataframe.shape[0]
  # st.write(f"Total number of orders: {total_orders}")
  #total number of unique orders
  total_unique_orders = orders_dataframe["order_id"].nunique()
  
  question = st.text_area("Enter questions about your data here, ex: How many customers are there?")
  
  if question:
    llm = OpenAI(temperature=0.9)
    customers_orders_df = pd.merge(customers_dataframe, orders_dataframe, on="customer_id")
    customers_orders_products_items_df = pd.merge(customers_orders_df, orders_products_dataframe, on="order_id")
    customers_orders_products_df = pd.merge(customers_orders_products_items_df, products_dataframe, on="product_id")

    agent = create_pandas_dataframe_agent(llm, customers_orders_products_df, verbose=True)
    with st.spinner("Getting answer..."):
      answer = agent.run(question)
    st.success("Answer retrieved!", icon="✅")
    st.balloons()
    st.markdown(answer, unsafe_allow_html=False)