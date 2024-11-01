from Home import st
from auth import authenticate_user

st.title("User Login")
username = st.text_input("Enter Your Name")
if username is None or "":
    st.error("Provide a Name Please")

password = st.text_input("Enter your Password")
if password is None or "":
    st.error("Provide a password Please")

if st.button("Submit"):
    token = authenticate_user(username, password)
    if token:
        st.session_state['auth_token'] = token
        st.success("Logged in successfully")
    else:
        st.error("Invalide Username or password")
if st.button("Logout"):
    if 'auth_token' in st.session_state:
        del st.session_state['auth_token']
        st.success("Logged Out Successfully")
