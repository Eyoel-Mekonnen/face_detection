import streamlit as st
import httpx
from auth import is_authenticated
st.set_page_config(page_title='Attendance System', layout='wide')


#is_authenticated()


st.title('Attendance System using Face Recognition')
st.header('Welcome to the Attendance System using Face Recognition')

# Display a brief introduction and description of the system
st.markdown("""
Welcome to our cutting-edge Attendance System, leveraging facial recognition technology to provide a seamless and efficient way to manage attendance. This system is designed to enhance security and streamline your daily attendance processes.
""")
#st.title('Attendance System using Face Recognition')
st.write('A streamlined solution for efficient and secure attendance management.')

# Navigation and Call-to-Action Button
#col1, col2 = st.columns([1, 1])


#with col2:
if st.button('View on GitHub'):
    st.write('This button will link to your GitHub repository.')    

with st.spinner("Loading Models and connection to Redis db ..."):
    import face_rec
st.success('Model loaded sucessfully')
st.success('Redis db successfully connected')

st.subheader('How to Use the System')
st.write("""
Navigate through our application using the sidebar to access different functionalities:
- **Real-Time Prediction:** Verify attendance by capturing your face in real time.
- **Register:** Add a new individual to the system by entering their name and role, and taking a facial snapshot.
- **Reports:** View detailed logs and attendance reports.
- **Current Attendance:** Check real-time attendance data, including time-in, time-out, and duration.
- **Absentee List:** Review a list of absentees with dates.
""")

st.header('Explore Other Features')
st.markdown("""
- **Register New Entries:** Easily add new users to the system on the 'Register' page. You can also upload photos(minmum one photo is required).
- **View Reports:** Access comprehensive attendance logs and data analytics in the 'Reports' section.
- **Track Attendance:** Monitor and manage daily attendance efficiently through the Report seciont on the attendance Report section.
""")

st.header('Key Features')

# Feature 1: Real-Time Prediction
st.subheader('Real-Time Prediction')
st.write("""User who enter will be detetected by the Realtime prediction
- Users that are detected will have their Name and time be displaced on box drawn on their face        
- Users that are not detected will have Uknown text along with a box around their face will be displayed
""")
st.image('Realtime prediction image.png')
st.write('After Successfully predicted their Name and Role will be automatically added')
st.image('Realtime prediction image_2.png')
st.write('Utilize state-of-the-art facial recognition to verify identities instantly and securely.')

# Feature 2: User Registration
st.subheader('User Registration')
st.write("""
User will Enter the following
- Enter their Name
- Enter their Role
- Select which way to input their facial data, via Photo(atleast one) or realtime sample collection for a few Seconds
""")
st.image('Registration_form_Detecting Face.png')
st.write('Register users easily with photo capture, enhancing system security and convenience.')
st.write('You can also Upload Photo')
st.write('- Minimum One Photo is Required')
st.image('Registration Section.png')
# Feature 3: Attendance Reporting
st.subheader('Attendance Reporting')
st.write("""The attendace Report will show the following to Users
- Date
- Name
- Role
- Intime
- Outime
- Duration
""")
st.image('Attendance Report.png')
st.write('Access detailed attendance reports through a user-friendly interface, facilitating better management.')

st.subheader('View Absent Records')
st.write('- Absent Log will contain Name, role and Date of absence compared to all the Logs')
st.image('Absent records.png')
#st.write('View Absent records along with the Date.')
# Real Time Prediction
# We are going to use streamlit-webrtc



# About Section Header
st.header('About the Project')

# Inspiration and Story
st.markdown("""
### Inspiration Behind the Attendance System

The concept for this facial recognition attendance system was born out of a need for smoother, more secure access control at the ALX Hub. As someone who regularly experienced the hassle of traditional check-ins during peak hours, I envisioned a system that could expedite this process while enhancing security. This project not only simplifies access but also integrates cutting-edge technology to modernize daily operations. It is also a capstone Portfolio Project for my time at Holberton School, showcasing the practical application of skills acquired during the course.

[Learn more about Holberton School.](https://www.holbertonschool.com)
""")

# Team Member Links
st.subheader('Meet the Developer')
st.markdown("""
#### [Eyoel Mekonnen](#)
Connect with me on professional platforms:
- [LinkedIn](https://www.linkedin.com/in/your-profile)
- [GitHub](https://github.com/your-username)
- [Twitter](https://twitter.com/your-twitter)

Feel free to explore and contribute to the project repository:
- [GitHub Repository](https://github.com/your-username/your-repository)
""")

# Optionally, you can add images or additional design elements to make this section visually appealing
