from Home import st
from Home import face_rec
import pandas as pd
#from auth import is_authenticated
st.set_page_config(page_title='Reporting', layout='wide')
#is_authenticated()

st.subheader("Reporting")


name = 'attendance:logs'

def retrieve_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name=name, start=0, end=end)
    return logs_list


## create tabs
tab1, tab2, tab3 = st.tabs(['Registerd Data', 'Logs', 'Attendance Report'])

with tab1:
    if st.button("Refresh Data"):
        with st.spinner('Retriving Data from Redis DB...'):
            redis_face_db = face_rec.retrive_data(name='academy:register')
            st.dataframe(redis_face_db[['Name', 'Role']])

with tab2:
    if st.button("Refresh Logs"):
        st.write(retrieve_logs(name=name))

with tab3:
    ## I retrieved the logs using the function logs
    logs = retrieve_logs(name)
    decoded_list = []
    #I am decoding to a list
    for byte_data in logs:
        decoded_string = byte_data.decode('utf-8')
        decoded_list.append(decoded_string)
    #st.write(decoded_list)

    nested_list = []
    for element in decoded_list:
        sublist = []
        name = element.split('@')[0]
        role = element.split('@')[1]
        timestamp = element.split('@')[2]
        sublist.append(name)
        sublist.append(role)
        sublist.append(timestamp)
        nested_list.append(sublist)
    #st.write(nested_list)
    ## we need to convert this to dataframe now
    dataframe = pd.DataFrame(nested_list, columns=['Name', 'Role', 'Timestamp'])
    #st.write(dataframe)

    ## Now I have to do analysis based on the Timestamp
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
    dataframe['Date'] = dataframe['Timestamp'].dt.date
    dataframe['Day Name'] = dataframe['Timestamp'].dt.day_name()
    dataframe.groupby(by=['Name', 'Timestamp'])
    list_of_all_logs = []
    dict_of_logs = {}
    for index, row in dataframe.iterrows():
        dt_name = str(row['Date']) + '@' + row['Name'] + '@' + row['Role']
        #row[]
        if dt_name in dict_of_logs:
            dict_of_logs[dt_name].append(row['Timestamp'])
        else:
            dict_of_logs[dt_name] = []
            dttime = row['Timestamp']
            dict_of_logs[dt_name].append(row['Timestamp'])
    #st.write(dict_of_logs)
    for key, value in dict_of_logs.items():
        row_list = []
        date_row = key.split('@')[0]
        name_row = key.split('@')[1]
        role_row = key.split('@')[2]
        min_time = value[0]
        ## the one below can be imporved using sorting algorithms
        for element in value:
            if min_time > element:
                min_time = element
        max_time = value[0]
        for element in value:
            if max_time < element:
                max_time = element
        row_list.append(date_row)
        row_list.append(name_row)
        row_list.append(role_row)
        row_list.append(min_time)
        row_list.append(max_time)
        list_of_all_logs.append(row_list)

    df_attendance_time = pd.DataFrame(list_of_all_logs, columns=['Date', 'Name', 'Role', 'In-Time', 'Out-Time'])
    df_attendance_time['Duration'] = df_attendance_time['In-Time'] - df_attendance_time['Out-Time']
    #st.write(df_attendance_time)
    #st.write("The one below I am list of all logs")
    #st.write(list_of_all_logs)

    all_dates_present = sorted(dataframe['Timestamp'].dt.date.to_list())
    all_date_logs = []
    for date_present in all_dates_present:
        if date_present not in all_date_logs:
            all_date_logs.append(date_present)
    
    #print(all_dates_present)
    #st.write("The one below I am all dates present")
    #st.write(all_date_logs)
    absentee_records = []
    for time_stamp_daily in all_date_logs:
        
        for each_element in list_of_all_logs:
            if str(time_stamp_daily) not in each_element[0]:
                #print("I am in because {} is not in {}".format(time_stamp_daily, each_element))
                list_absentee = []
                name = each_element[1]
                role = each_element[2]
                min_time = None
                max_time = None
                date_of_absence = str(time_stamp_daily)
                list_absentee.append(date_of_absence)
                list_absentee.append(name)
                list_absentee.append(role)
                list_absentee.append(min_time)
                list_absentee.append(max_time)
                absentee_records.append(list_absentee)
    ##Let me try the final log of attendance
    final_attendance_list = []
    count = 0
    list_of_index = []
    for val_ in absentee_records:
        
        for val_2 in list_of_all_logs:
            if val_[0] in val_2[0] and val_[1] == val_2[1]:
                #print("I am inside {} in {} and my count is {}".format(val_, val_2, count))
                list_of_index.append(count)
        count = count + 1
    df_attendance_time = pd.DataFrame(list_of_all_logs, columns=['Date', 'Name', 'Role', 'In-Time', 'Out-Time'])
    df_attendance_time['Duration'] = df_attendance_time['In-Time'] - df_attendance_time['Out-Time']
    new_dataframe = pd.DataFrame(list_of_all_logs, columns=['Date', 'Name', 'Role', 'In-Time', 'Out-Time'])
    st.write(df_attendance_time)
    main_absentee_records = []
    tracker = 0
    for student in absentee_records:
        if tracker not in list_of_index:
            lists_std = []
            date = student[0]
            name = student[1]
            role = student[2]
            In_Time = "Absent"
            Out_time = "Absent"
            lists_std.append(date)
            lists_std.append(name)
            lists_std.append(role)
            lists_std.append(In_Time)
            lists_std.append(Out_time)
            main_absentee_records.append(lists_std)
        tracker = tracker + 1
    absentee_dataframe = pd.DataFrame(main_absentee_records, columns=['Date', 'Name', 'Role', 'In-Time', 'Out-Time'])
    st.write(absentee_dataframe)
    
