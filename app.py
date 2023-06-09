import os 
# from apikey import apikey

import streamlit as st 
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain, SequentialChain 
# from langchain.memory import ConversationBufferMemory
# from langchain.utilities import WikipediaAPIWrapper
import pandas as pd
# from io import StringIO
from dotenv import load_dotenv

from helpers import process_data, validate_file
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.set_page_config("DataMind AI", layout="wide", page_icon="🧠")
st.title('📈 DataMind AI')

with st.sidebar:
  st.header("Settings")
  api_key = st.text_input("OpenAI API Key", type="password")
  st.caption("You can get your API key from https://beta.openai.com/account/api-keys")
  st.caption("You can also set your API key as an environment variable named OPENAI_API_KEY")
  st.divider()
  selected_model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt4"], disabled=True, index=0)
  with st.expander("Additional Settings"):
    temperate = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.9, step=0.10)
    tokens = st.slider("Tokens", min_value=200, max_value=2000, value=300, step=10)
    
  st.divider()
  
  with st.expander("Upload Data", expanded=True):

    st.header("Upload Customer Data")
    customers_file = st.file_uploader("Upload a csv file with customers data", type=["csv"])

    st.header("Upload Product Data")
    products_file = st.file_uploader("Upload a csv file with products data", type=["csv"])

    st.header("Upload Orders Data")
    orders_file = st.file_uploader("Upload a csv file with orders data", type=["csv"])

    st.header("Upload Orders with Products Data")
    orders_products_file = st.file_uploader("Upload a csv file with orders including product/items data", type=["csv"])

is_customers_valid = False
is_products_valid = False
is_orders_valid = False
is_orders_products_valid = False

if not customers_file and not products_file and not orders_file and not orders_products_file:
  st.header("Upload your documents on the sidebar to get started")
  st.image("https://media.giphy.com/media/TJP7EH5i1fB2rKeWbf/giphy.gif")

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
    
if orders_products_file is not None:
  order_products_dataframe = pd.read_csv(orders_products_file)
  is_orders_products_valid = validate_file(order_products_dataframe, type="orders_products")
  
  if not is_orders_products_valid:
    st.stop()

  with st.expander("Orders Products Preview"):
    op_preview_number = st.radio("Orders Products to preview", [10, 20, 50, 100], index=1, horizontal=True)
    st.write(order_products_dataframe.head(op_preview_number))

if is_customers_valid and is_products_valid and is_orders_valid and is_orders_products_valid:
  st.subheader("Chat about your data")
  process_data(users_dataframe, products_dataframe, order_dataframe, order_products_dataframe, temperate, tokens)
