from Home import st
from Home import face_rec
from auth import is_authenticated



#is_authenticated()
## I need to first get the list of all retrieved data


Role_User = st.selectbox(label='Select Role first', options=['Student', 'Teacher'])
#print("Selected Role is {}".format(Role_User))
#print("I am the one to be deleted {}".format(del_user))
retrieved_data = face_rec.retrive_data('acadmey:register')
passed_list = retrieved_data['Name'].to_list()
teacher_list = retrieved_data.query("Role == 'Teacher'")['Name'].to_list()
student_list = retrieved_data.query("Role == 'Student'")['Name'].to_list()
if Role_User == 'Teacher':
    del_user  = st.selectbox(label='Select User to Delete', options=teacher_list)
elif Role_User == 'Student':
    del_user  = st.selectbox(label='Select User to Delete', options=student_list)
st.write("Are you sure you want to delete User {}".format(del_user))
if st.button("Submit"):
    name_db = 'academy:register'
    value = face_rec.delete_user(name_db, del_user, Role_User)
    if value == True:
        st.success("You have successfully Deleted User {}".format(del_user))
    else:
        st.error("Not Deleted Successfully")    
#print(passed_list)



## and then store those as a list
## and pass that list to opiton in streamlit selection
## pass the selected to a function i will define in the face rec
## make the function delete it and if deleted send true or else false
