import os          
import streamlit as st      
from langchain_mistralai import ChatMistralAI

class MistralLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
        
    def get_llm_model(self):
        try:
            mistral_api_key=self.user_controls_input['MISTRAL_API_KEY']
            selected_mistral_model=self.user_controls_input["selected_mistral_model"]
            if mistral_api_key=='' and os.environ["MISTRAL_API_KEY"]=='':
                st.error("Please provide a valid Mistral API Key")
                
            llm=ChatMistralAI(api_key=mistral_api_key, model_name=selected_mistral_model)
        
        except Exception as e:
            raise ValueError(f"Error Occured With Exception : {e}")
        return llm
