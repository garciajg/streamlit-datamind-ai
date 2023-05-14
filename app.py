import os 
# from apikey import apikey

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

from helpers import process_data, validate_file
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('🦜🔗 DataMind AI')

st.header("Upload Customer Data")
customers_file = st.file_uploader("Upload a csv file with customers data", type=["csv"])

st.header("Upload Product Data")
products_file = st.file_uploader("Upload a csv file with products data", type=["csv"]) 

st.header("Upload Orders Data")
orders_file = st.file_uploader("Upload a csv file with orders data", type=["csv"]) 

is_customers_valid = False
is_products_valid = False
is_orders_valid = False

if customers_file is not None:
  users_dataframe = pd.read_csv(customers_file)
  is_customers_valid = validate_file(users_dataframe, type="customers")
  
  if not is_customers_valid:
    st.stop()
  else:
    with st.expander("Customers Preview"):
      c_preview_number = st.radio("Customers to preview", [10, 20, 50, 100], index=1, horizontal=True)
      st.write(users_dataframe.head(c_preview_number))

if products_file is not None:
  products_dataframe = pd.read_csv(products_file)
  is_products_valid = validate_file(products_dataframe, type="products")
  
  if not is_products_valid:
    st.stop()

  with st.expander("Products Preview"):
    p_preview_number = st.radio("Products to preview", [10, 20, 50, 100], index=1, horizontal=True)
    st.write(products_dataframe.head(p_preview_number))

if orders_file is not None:
  order_dataframe = pd.read_csv(orders_file)
  is_orders_valid = validate_file(order_dataframe, type="orders")
  
  if not is_orders_valid:
    st.stop()

  with st.expander("Orders Preview"):
    o_preview_number = st.radio("Orders to preview", [10, 20, 50, 100], index=1, horizontal=True)
    st.write(order_dataframe.head(o_preview_number))

if is_customers_valid and is_products_valid and is_orders_valid:
  st.subheader("Chat about your data")
  process_data(users_dataframe, products_dataframe, order_dataframe)
