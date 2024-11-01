import streamlit as st
import httpx


def register_user(username, password):
    url = "http://localhost:5000/api/register"
    #print("I have the name {} and password {}".format(username, password))
    response = httpx.post(url, json={'username': username, 'password':password})
    if response.status_code == 302:
        return True

