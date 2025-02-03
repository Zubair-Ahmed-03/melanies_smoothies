# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order=st.text_input('Name on Smoothie -')
st.write('The name on your smoothie will be',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for i in ingredients_list:
        ingredients_string+=i+' '
        st.subheader(i+" Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+i)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #time_to_insert = st.button('Submit order')
    '''
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")'''
