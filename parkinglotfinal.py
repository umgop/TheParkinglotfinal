import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import datetime
import html
import requests 

api_key = "cc065131-fcfa-4953-b182-15958b278b38"
headers = {"Api-Key": api_key, "Content-Type": "application/json"}
store_name = "Parkinglotstore"
store_url = f"https://json.psty.io/api_v1/stores/{store_name}"

def save_information():
    res = requests.get(store_url, headers=headers).json()['data']
    Carstatus = [0,0,0,0,0,0,0,0,0,0]
    for item in res:
        print(item)
        spotnumber = item["Spot"]
        if (item["Reservation Status"] == "reserved"):
            Carstatus[spotnumber-1] = 1
        if (item["Reservation Status"] == "free"):
            Carstatus[spotnumber-1] = 0
    return Carstatus


    

def add_reservation():

  st.write("Reserve Spots")
  st.write("We charge a total of 10 dollars per a spot. Please pay when freeing your spot. Thank you.")
  Carstatus =  save_information()
  
  if Carstatus[spotnumber-1] == 0:
    now = datetime.datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    d = {
            "Name" : name,
            "Time" : nowstr,
            "Spot" : spotnumber,
            "Reservation Status" : "reserved",
            "Car Information" : information,
            "Revenue" : revenue
    }
    data = load_data()
    data.append(d)
    res = requests.put(store_url, headers=headers, data=json.dumps(data))
    Carstatus[spotnumber-1] == 0
    print(Carstatus)
    
    st.success('You have succesfuly reserved your spot')
    
    
  else:
      st.error('This spot is taken.')
def calculate_revenue():
    revenue = 0
    res = requests.get(store_url, headers=headers).json()['data']
    Carstatus = [0,0,0,0,0,0,0,0,0,0]
    for item in res:
        print(item)
        revenue = revenue + item["Revenue"]
    return revenue


def free_reservation():
  global information
  Carstatus =  save_information()
  
  if Carstatus[spotnumber-1] == 1:
    
    now = datetime.datetime.now()
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S")
    revenue = 10
    data = load_data()
    # for d in data:
    #     if d["Spot"] == spotnumber:
    #         d["Time"] = nowstr
    #         d["Reservation Status"] = "free"
    #         d["Revenue = revenue"]
    d = {
            
            "Time" : nowstr,
            "Spot" : spotnumber,
            "Reservation Status" : "free",
            "Revenue" : revenue
    }
    
    data.append(d)
    res = requests.put(store_url, headers=headers, data=json.dumps(data))
    st.success('You have succesfuly freed your spot')
  else:
      st.error('This spot is not taken.')

def spot_statistics(): 
    fig1, axl = plt.subplots(1,1)
    slots = ['1', '2','3','4','5','6','7','8','9','10' ]
    res = requests.get(store_url, headers=headers).json()['data']
    reservations = [0,0,0,0,0,0,0,0,0,0]
    for item in res:
      spotnumber = item["Spot"]
      if (item["Reservation Status"] == "reserved"):
        reservations[int(spotnumber)-1] = reservations[int(spotnumber)-1] + 1
    colors = ['red', 'yellow', 'lightgrey', 'lightcoral','linen','yellowgreen','lightblue','lightgreen','pink','aqua'] 
    axl.pie(reservations, labels = slots, colors=colors,  
        startangle=50, shadow = True,
        radius = 2.0,  autopct = '%1.1f%%' )  
    st.pyplot(fig1)
def spot_Stats():
    fig, ax = plt.subplots(1, 2, figsize = (12,6))
    res = requests.get(store_url, headers=headers).json()['data']
    spots = [0,0,0,0,0,0,0,0,0,0]
    for item in res:
      spotnumber = item["Spot"]
      if (item["Reservation Status"] == "reserved"):
        spots[int(spotnumber-1)] = spots[int(spotnumber -1)] + 1
      if (item["Reservation Status"] == "free"):
        spots[int(spotnumber-1)] = spots[int(spotnumber -1)] - 1
    print(spots)
    ax[0].imshow([spots], extent=[1,10,0,1])
    ax[0].set_title("Vacant Spots - Yellow Spots are Taken, Purple spots are free")
    ax[1].set_axis_off()
    st.pyplot(fig)
      

    


def load_data():

    res = requests.get(store_url, headers=headers)
    data = res.json()["data"]
    return data

    


Carstatus = [0,0,0,0,0,0,0,0,0,0]
CarInformation = ["","","","","","","","","",""]
st.write("# Parking lot Simulator 2.0")
st.write("What do you want to do? - Reserve(2), Free(3), Vacant spots Graph (Tells Which spots are free or taken)- Graph on reservation percentages made per a spot made(4), Calculate Revenue (5)")
main_question = st.selectbox("Choose from the options",[1,2,3,4,5])

revenue = 0
if main_question == 2:
    spotnumber = st.selectbox('Please select a number from 1-10', [1,2,3,4,5,6,7,8,9,10])
    name = st.text_input("Name")
    information = st.text_input("Car Information:Ex(Color, Car, License plate number) - (Red, Toyota Siena, 6Trj56)")
    if st.button("Reserve"):
        add_reservation()
        
        
    df = load_data()
    st.write(df)
    
    

if main_question == 3:
    st.write("Free Spots")
    spotnumber = st.selectbox('Please select a number from 1-10', [1,2,3,4,5,6,7,8,9,10])
    if st.button("Free"):
        free_reservation()
    df = load_data()
    st.write(df)
    print(Carstatus)
if main_question == 4:
    spot_Stats()
    st.write("This is a graph made for how many reservations made for a spot.")
    spot_statistics()
    
if main_question == 5:
    revenue = 0
    revenue = calculate_revenue()
    st.write(revenue)
    # res = requests.get(store_url, headers=headers)
    # print("Res: ", res)
    # file = open('Commands.json', 'r')
    # for line in file :
    #     json_data = json.loads(line)
    #     revenue = revenue + json_data['Revenue']
    
     










