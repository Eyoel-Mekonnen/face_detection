import numpy as np
import pandas as pd
import cv2
import redis
from insightface.app import FaceAnalysis
import os

from sklearn.metrics import pairwise
import time
from datetime import datetime
##connect to redis database

#Include hostname, port and password from redis cloud
r = redis.StrictRedis(host=hostname,
                      port=portnumber,
                      password=password)

# Retrieve Data from Database
def retrive_data(name):
    ### academy:register
    name = 'academy:register'
    retrive_dict =r.hgetall(name)
    #Converts the dictionary into pandas series, in the serious the dictionary key becomes Series Index, dictionary values becomes Series Values
    retrive_series = pd.Series(retrive_dict)
    #retrive_series = retrive_series.apply(lambda x: np.frombuffer(x, dtype=np.float32))
   
    buffer_list = []
    for values in retrive_series:
        np_datatype = np.frombuffer(values, dtype=np.float32)
        buffer_list.append(np_datatype)
    retrive_series = pd.Series(buffer_list, index=retrive_series.index)
    
    #index = retrive_series.index
    byte_list = []
    for byte_index in retrive_series.index:
        decoded_index = byte_index.decode()
        byte_list.append(decoded_index)
    retrive_series.index = byte_list
    
    #index = list(map(lambda x: x.decode(), index))
    #retrive_series.index = index
    retrive_df =retrive_series.to_frame().reset_index()
    retrive_df.columns=['name_role', 'facial_features']
    
    names = []
    roles = []

    for name_role in retrive_df['name_role']:
        name = name_role.split('@')[0]
        role = name_role.split('@')[1]
        names.append(name)
        roles.append(role)
    retrive_df['Name'] = names
    retrive_df['Role'] = roles
    

    #retrive_df[['Name', 'Role']] = retrive_df['name_role'].apply(lambda x: x.split('@')).apply(pd.Series)
    return retrive_df

#configure face analysis
faceapp = FaceAnalysis(name='buffalo_sc', root = 'insightface_model', providers = ['CPUExecutionProvider'])
faceapp.prepare(ctx_id=0, det_size=(640, 640), det_thresh = 0.5)

#ML search Algorithm

def cosine_similarity_algorithm(dataframe, face_features, image_vector, name_role=['Name', 'Role'], threshold=0.5):
    ##taking and creating a copy of the datafram
    dataframe_copy = dataframe.copy()
    x_list = dataframe_copy[face_features].tolist()
    ## Here X represents the list of embedding which is 50 rows each row containing 512 col..converted to a numpyarray
    X = np.asarray(x_list)
    ## - we need to reshape vector because it contains [] ..should be changed to [[...]]..one row but 512 col
    Y = image_vector.reshape(1, -1)
    ## Now we can calucalte the consine similarity
    cosine_raw = pairwise.cosine_similarity(X, Y)
    ## We need to flatten this to make sure it works with any numpy array
    cosine_similarity = np.array(cosine_raw).flatten()
    ## now i have created a data frame that has a dataframe with name, role, embedding and consine similarity of each image with respect to the image vector
    dataframe_copy['cosine'] = cosine_similarity
    ## I have filtered dataframe with respect to cosine value greater than threshold and stored the object on data_filter_cosine object
    ## It contains the same strucutre as dataframe_copy
    data_filter_cosine = dataframe_copy.query(f'cosine > {threshold}')
    ## Now i will rearragne so that it can have proper indexing number starting from 0
    data_filter_cosine.reset_index(drop=True, inplace=True)

    # i then create a condition to check that we have retrieved a value
    if len(data_filter_cosine) > 0:
        argmax = data_filter_cosine['cosine'].argmax()
        Name_cosine, Role_cosine = data_filter_cosine.loc[argmax][name_role]

    else:
        Name_cosine = 'Unkown'
        Role_cosine = 'Unkown'
    return Name_cosine, Role_cosine

## creating a class in order to sotre the data and the data doesnott disappear

class RealTimePred:
    
     # create a list of dictionary to store the logs
    def __init__(self):
        """initalize a new dictoray that has a key and associated list values"""
        self.logs = {'name': [], 'role': [], 'current_time': []}

    def resetlogs(self):
        """sets the log back to empyt ready to recieve another data"""
        self.logs = {'name': [], 'role': [], 'current_time': []}

    def saveLogs(self):
        """I am going to save the recieved data but remove the duplicates..since pd dataframe is easy i will create a dataframe"""
        dataframe = pd.DataFrame(self.logs)
        #print(self.logs)
        """I then used pd created dataframe to safely remove the duplicate data"""
        dataframe.drop_duplicates('name', inplace=True)
        """After that i have to push the created ..so to do that i will covert what i have in dataframe to list"""
        name_list = dataframe['name'].to_list()
        role_list = dataframe['role'].to_list()
        ctime_list = dataframe['current_time'].to_list()
        #Now that I have them in a list
        encoded_data = []
        for name, role, ctime in zip(name_list, role_list, ctime_list):
            if name != 'Unkown':
                #ctime = str(ctime)
                log = name + '@' + role + '@' + ctime
                encoded_data.append(log)
        if len(encoded_data) > 0:
            r.lpush('attendance:logs', *encoded_data)
        self.resetlogs()

    def face_prediction(self, image_test,dataframe, face_features, name_role=['Name', 'Role'], threshold=0.5 ):
        
        current_time = str(datetime.now())
        
        results = faceapp.get(image_test)
        #print("Structure of results is {}".format(results))
        image_test_copy = image_test.copy()
        for result in results:
            x1 = result['bbox'][0].astype(int)
            y1 = result['bbox'][1].astype(int)
            x2 = result['bbox'][2].astype(int)
            y2 = result['bbox'][3].astype(int)
            embeddings = result['embedding']
            ##text_gen = person_name
            ##
            person_name, person_role = cosine_similarity_algorithm(dataframe, face_features, image_vector=embeddings, name_role=name_role, threshold=threshold)
            if person_name == 'Unkown':
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            cv2.rectangle(image_test_copy, (x1, y1), (x2, y2), color)
            text_gen = person_name
            cv2.putText(image_test_copy, text_gen, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 0, 1)
            cv2.putText(image_test_copy, current_time, (x1, y2 + 15),cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 0, 1)
            self.logs['name'].append(person_name)
            self.logs['role'].append(person_role)
            self.logs['current_time'].append(current_time)
        return image_test_copy
    

## i am going to create a class that is going actaully save facial embeddings
class RegistrationForm():
    """Allow the counting of embeddings"""
    def __init__(self):
        self.samples = 0

    def reset_sample(self):
        self.samples = 0


    def extract_embeddings(self, img):

        """this is going to recieve each frame from the streamweb"""
        results = faceapp.get(img, max_num=1)
        embeddings = []
        for result in results:
            self.samples = self.samples + 1
            x1 = result['bbox'][0].astype(int)
            y1 = result['bbox'][1].astype(int)
            x2 = result['bbox'][2].astype(int)
            y2 = result['bbox'][3].astype(int)
            embeddings = result['embedding']
            """Drawing on the detected face using opencv"""
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            text = "Detected samples = {}".format(self.samples)
            cv2.putText(img, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,255,0), 2)
        return img, embeddings
    
    def save_embedding_to_db(self, name, role):
        """this will load the txt fiel that is stored"""

        if name is not None:
            if name.strip() != '':
                key = key = name + '@' + role
            else:
                return 'Name is false'
        else:
            return 'Name is false'
        
        if 'face_embedding.txt' not in os.listdir():
            return "File Does not Exist"
        #step1 - load "face_embedding.txt"
        embedding_array = np.loadtxt('face_embedding.txt', dtype=np.float32)
        #step2 - convert into array int proper dimenstions
        #basically what it is doing dividing the total number elements by 512 -> this gives how many embeddings are present
        embedding_samples = int(embedding_array.size / 512)
        #now by assuming each row should contain 512 rows it reshapes into a two dimensional array of strucutre [[...], [...],[...]]
        embedding_array = embedding_array.reshape(embedding_samples, 512)
        #converts it to numpyarray
        embedding_array = np.asarray(embedding_array)
        #step3 - cal mean of embeddings
        #This computes the mean of the embeddings across the first axis (vertically down the rows), resulting in a single embedding vector that represents the average of all input embeddings
        embedding_mean = embedding_array.mean(axis=0)
        #saves it byte datatype
        embedding_mean_bytes = embedding_mean.tobytes()
        #step4  - save to redis
        
        r.hset(name='academy:register', key=key, value=embedding_mean_bytes)
        os.remove('face_embedding.txt')
        self.reset_sample()
        return True   
    

def delete_user(db_key, name_user, role):
    """This take the database and the user to delete"""
    #print("Database key passed to function {}".format(db_key))
    #print("Name Passed to function {}".format(name_user))
    if role == 'Student':
        name_user = name_user + '@' + 'Student'
        print(name_user)
    elif role == 'Teacher':
        name_user = name_user + '@' + 'Teacher'
    value = r.hdel(db_key, name_user)
    if value == 1:
        return True
    else:
        return False
