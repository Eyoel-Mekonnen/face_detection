from Home import st, face_rec
#from auth import is_authenticated
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
st.set_page_config(page_title='Registration Form', layout='centered')

#is_authenticated()


st.subheader("Registration Form")


person_name = st.text_input(label='Name', placeholder='First and Last Name')
role = st.selectbox(label='Select Your Role', options=('Student', 'Teacher'))

registrationform = face_rec.RegistrationForm()
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24')
    regis_image, embeddings = registrationform.extract_embeddings(img)
    if embeddings is not None:
        try:
            with open('face_embedding.txt', mode='ab') as f:
                np.savetxt(f, embeddings)
        except FileNotFoundError:
            print("You have not uploaded video stream")
    return av.VideoFrame.from_ndarray(regis_image, format="bgr24")
webrtc_streamer(key='Registration', video_frame_callback=video_callback_func)
uploaded_files = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
if st.button("Upload Photo"):
    if uploaded_files is not None and len(uploaded_files) > 0:
        for uploaded_file in uploaded_files:
            uploaded_bytes = uploaded_file.read()
            uploaded_image = np.frombuffer(uploaded_bytes, np.uint8)
            uploaded_image = cv2.imdecode(uploaded_image, cv2.IMREAD_COLOR)
            regis_image, embeddings = registrationform.extract_embeddings(uploaded_image)
            if embeddings is not None:
                with open('face_embedding.txt', mode = 'ab') as f:
                    np.savetxt(f, embeddings)
            st.success(f"Processed {len(uploaded_files)} images and saved embeddings.")
    else:
        st.error("Please enter atleast one photo")

if st.button('Submit'):
    value = registrationform.save_embedding_to_db(person_name, role)
    if value == True:
        st.success("{} registered successfully".format(person_name))
    elif value == 'Name is false':
        st.error("Please Enter the name: Name can not be empty or spaces")
    elif value == "File Does not Exist":
        st.error("face_embedding.txt is not Found so Upload short Video please")
        st.error("Click on the start to register yourself via Video")
    st.write("{}".format(person_name))
    st.write("{}".format(role))
