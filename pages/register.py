from Home import st
from user_register import register_user

st.title("Regiseter")
username = st.text_input("Enter your Name")
password = st.text_input("Enter your Password")

if not (username and password):
    st.error("Username and Password Can not be Empty")
if st.button("Submit"):
    response = register_user(username, password)
    print(response)
    if response is True:
        st.success("Successfully Registered")
    else:
        st.error("Registeration Not Successful")


