import pandas as pd
import numpy as np
import streamlit as st
import datetime
from datetime import date

# calcolo data attuale e titolo
data = date.today().strftime("%d/%m/%Y")
st.header('Pankina ' + data)

#Tips totali
tip_amount = st.text_input("Total tips amount", 0.0)

waiters = st.slider('Number of melzarim', value = 1,
            min_value = 0, max_value = 10, step = 1)
barmen = st.slider('Number of barmanim', value = 1,
            min_value = 0, max_value = 10, step = 1)
ahmash = st.slider('Number of ahmash', value = 0,
            min_value = 0, max_value = 10, step = 1)

if int(waiters) > 0:
    st.subheader('Hours per melzar')

melzarim = np.array([0.0 for x in range(int(waiters))])

for i in range(int(waiters)):
    start_hours_txt = "Start time melzar " + str(i+1)
    start_time = st.time_input(start_hours_txt, datetime.time(10, 0))
    start = datetime.datetime.combine(datetime.date.today(), start_time)
    end_hours_txt = "End time melzar " + str(i+1)
    end_time = st.time_input(end_hours_txt, datetime.time(17, 30))
    end = datetime.datetime.combine(datetime.date.today(), end_time)
    difference = end - start
    if difference.total_seconds() / 3600 < 0:
        st.write(24 + difference.total_seconds() / 3600)
        melzarim[i] =  24 + difference.total_seconds() / 3600
    else:
        st.write(difference.total_seconds() / 3600)
        melzarim[i] = difference.total_seconds() / 3600
    
if int(barmen) > 0:
    st.subheader('Hours per barman')

barmanim = np.array([0.0 for x in range(int(barmen))])

for i in range(int(barmen)):
    start_hours_txt = "Start time barman " + str(i+1)
    start_time = st.time_input(start_hours_txt, datetime.time(12, 0))
    start = datetime.datetime.combine(datetime.date.today(), start_time)
    end_hours_txt = "End time barman " + str(i+1)
    end_time = st.time_input(end_hours_txt, datetime.time(18, 0))
    end = datetime.datetime.combine(datetime.date.today(), end_time)
    difference = end - start
    if difference.total_seconds() / 3600 < 0:
        st.write(24 + difference.total_seconds() / 3600)
        barmanim[i] =  24 + difference.total_seconds() / 3600
    else:
        st.write(difference.total_seconds() / 3600)
        barmanim[i] = difference.total_seconds() / 3600

if int(ahmash) > 0:
    st.subheader('Hours per ahmash')

ahmashim = np.array([0.0 for x in range(int(ahmash))])

for i in range(int(ahmash)):
    start_hours_txt = "Start time ahmash " + str(i+1)
    start_time = st.time_input(start_hours_txt, datetime.time(12, 0))
    start = datetime.datetime.combine(datetime.date.today(), start_time)
    end_hours_txt = "End time ahmash " + str(i+1)
    end_time = st.time_input(end_hours_txt, datetime.time(18, 0))
    end = datetime.datetime.combine(datetime.date.today(), end_time)
    difference = end - start
    if difference.total_seconds() / 3600 < 0:
        st.write(24 + difference.total_seconds() / 3600)
        ahmashim[i] =  24 + difference.total_seconds() / 3600
    else:
        st.write(difference.total_seconds() / 3600)
        ahmashim[i] = difference.total_seconds() / 3600

# First two hours are 35 shekels each
melzarim[0] -= 2
total_tip = float(tip_amount) - 70

total_hours_melzarim = np.sum(melzarim)
total_hours_barmanim = np.sum(barmanim)
total_hours_ahmashim = np.sum(ahmashim)

tip_per_hour = total_tip / total_hours_melzarim

#Percentuale barman
if tip_per_hour >= 100:
    ahuz = 0.9
elif tip_per_hour < 100 and tip_per_hour >= 60:
    ahuz = 0.93
else:
    ahuz = 0.95

barman_tip = (total_tip * (1-ahuz))/total_hours_barmanim

#Parametro Ahmash
if tip_per_hour >= 100:
    parametro_ahmash = 4
elif tip_per_hour < 100 and tip_per_hour >= 50:
    parametro_ahmash = 4.5
else:
    parametro_ahmash = total_hours_ahmashim

melzar_tip = (total_tip * ahuz)/(total_hours_melzarim+total_hours_ahmashim/parametro_ahmash)
ahmash_tip = melzar_tip/parametro_ahmash

results = {}
restaurant_entry = 0
for i,melzar in enumerate(melzarim):
    restaurant_entry += melzar*3
    name = 'Waiter ' + str(i+1)
    if i == 0:
        results[name] = (melzar_tip - 3)*melzar + 70
    else:
        results[name] = (melzar_tip - 3)*melzar
for i,barman in enumerate(barmanim):
    name = 'Barman ' + str(i+1)
    results[name] = barman_tip*barman

for i,ahmash in enumerate(ahmashim):
    name = 'Ahmash ' + str(i+1)
    results[name] = ahmash_tip*ahmash
            
results['Restaurant'] = restaurant_entry

results['Tip per hour'] = melzar_tip

st.subheader('Tips per worker')
df = pd.DataFrame.from_dict(results, orient = 'index')
df = df.rename({0: 'tips'}, axis = 'columns')
df.reset_index(inplace = True)
df = df.rename(columns = {'index': 'worker'})
st.write(df)
