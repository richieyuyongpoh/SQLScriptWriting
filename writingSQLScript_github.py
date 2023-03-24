
import openai 
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["api_secret"] 




st.title("AI based SQL Script Writing")


readme = st.checkbox("readme first")

if readme:

    st.write("""
        This is a text-to-sql demo using [ChatGPT API](https://openai.com/). 
        The web app is hosted on [streamlit cloud](https://streamlit.io/cloud).
        
        """)
    st.write ("For more info, please contact:")
    st.write("<a href='https://www.linkedin.com/in/yong-poh-yu/'>Dr. Yong Poh Yu </a>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("Instruction:")
    st.write("")

    st.write("On the sidebar, choose the type of scripts you want the AI assistant, Jane to write.")
    st.write("Choose <General Script> if you want Jane to write a general script.")
    st.write("Choose <Specific Database> if you want Jane to write a specific script referring to a specific database. In this case, you need to upload the database scheme. You may get an example [here](https://drive.google.com/file/d/1BGE_N1WZZqncsAkYx34j5oz47kFF_nJf/view?usp=sharing). This scheme is written by [Ankit Kumar](https://github.com/jinxankit/Bank-Database-Design)")
    
    

def generate_general_response(prompt):
  
    init_messages = [
        {"role": "system", "content": "You are Jane, Dr. Yong Poh's assistant. You will write a sql query (strictly no explanation) based on the following prompt. If user doesn't ask you to write sql query, you will ask user to do so."},
        {"role": "user", "content": prompt}]
  
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens = 500,
            messages= init_messages)

    return response["choices"][0]["message"].content 

def generate_specific_response(prompt,schema):
  
    init_messages = [
        {"role": "system", "content": f"You are Jane, Dr. Yong Poh's assistant. Based on the database schema ### {schema} ###, you will write a sql query (strictly no explanation) based on the following prompt. If user doesn't ask you to write sql query, you will ask user to do so. If the schema is not appropriate, you will ask user to check the schema."},
        {"role": "user", "content": prompt}]
  
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens = 500,
            messages= init_messages)

    return response["choices"][0]["message"].content 



option = st.sidebar.radio(
    'Type of Scripts',
    ('General Script', 'Specific Database'))



if option =='General Script':
    def get_text():
        input_text = st.text_input("You: ","", key="input")
        return input_text
    
    user_input = get_text()
    
    
    if user_input:

        output = generate_general_response(user_input)
        
        message(output)
        message(user_input, is_user=True)
        
        

            
else:
    def get_text():
        input_text = st.text_input("You: ","", key="input")
        return input_text
    user_input = get_text()
    
    uploaded_file = st.sidebar.file_uploader("Upload a txt file", type=['txt'])
    
    if uploaded_file!=None:
        b = uploaded_file.getvalue()
        schema = bytes.decode(b, 'utf-8')
            

        if user_input:
            output = generate_specific_response(user_input,schema)
            
            message(output)
            message(user_input, is_user=True)
        
        
        
