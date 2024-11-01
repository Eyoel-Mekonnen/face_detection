from Home import st
from auth import is_authenticated
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time
st.set_page_config(page_title='Prediction', layout='centered')
#is_authenticated()

st.subheader("Real-Time Attendance System")

## Retreive the data from Redis Database
### academy:register
with st.spinner('Retriving Data from Redis DB...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)
st.success("Data sucessfully Retrived from Redis")
settime = time.time()
waittime = 5
realtimepred = face_rec.RealTimePred()
## Real time prediction
def video_frame_callback(frame):
    global settime
    """converting it numpyarray so that i can pass it to face_prediction method"""
    img = frame.to_ndarray(format="bgr24")
    # face_prediction(image_test,dataframe, face_features, name_role=['Name', 'Role'], threshold=0.5 )
    pred_image = realtimepred.face_prediction(img,redis_face_db, 'facial_features', ['Name', 'Role'], threshold=0.5 )
    timenow = time.time()
    difftime = timenow - settime
    if difftime >= waittime:
        realtimepred.saveLogs()
        settime = time.time()
        print("Save data to redis database")

    return av.VideoFrame.from_ndarray(pred_image, format="bgr24")

webrtc_streamer(key="realtimeprediction", video_frame_callback=video_frame_callback)
