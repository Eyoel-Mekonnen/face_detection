import streamlit as st
import httpx

def authenticate_user(username, password):
    
    url = "http://localhost:5000/api/login"
    response = httpx.post(url, json={'username': username, 'password':password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        return None

def is_authenticated():
    if 'auth_token' in st.session_state:
        return True
    else:
        st.error("You are Not authorized")
        st.stop()
