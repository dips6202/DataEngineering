import json
import pandas as pd
import re
import hashlib
import matplotlib.pyplot as plt




with open('C:/Users/lenovo/Documents/Python/lab_5/DataEngineeringQ2.json', 'r') as file:
    data = json.load(file)


if isinstance(data, dict):
    print(data['key'])

if isinstance(data, list):
    print(data[0]) 

appointment_id = data['appointmentId']
phone_number = data['phoneNumber']
first_name = data['patientDetails']['firstName']
last_name = data['patientDetails']['lastName']
gender = data['patientDetails']['gender']
birth_date = data['patientDetails']['birthDate']
medicines = data['consultationData']['medicines']
#this is the code

print("Appointment ID:", appointment_id)
print("Phone Number:", phone_number)
print("First Name:", first_name)
print("Last Name:", last_name)
print("Gender:", gender)
print("Birth Date:", birth_date)
print("Medicines:", medicines)

df = pd.read_json('your_file.json')

df['gender'] = df['gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

df.rename(columns={'birthDate': 'DOB'}, inplace=True)

print(df)


df['fullName'] = df['firstName'] + ' ' + df['lastName']


print(df)

import pandas as pd
from datetime import datetime

df['Age'] = pd.to_datetime(df['DOB']).apply(lambda x: (datetime.now().year - x.year) if pd.notnull(x) else None)

print(df)


import pandas as pd

noOfMedicines = df.groupby('appointmentId').size().reset_index(name='noOfMedicines')

noOfActiveMedicines = df[df['IsActive'] == True].groupby('appointmentId').size().reset_index(name='noOfActiveMedicines')

noOfInActiveMedicines = df[df['IsActive'] == False].groupby('appointmentId').size().reset_index(name='noOfInActiveMedicines')

df = pd.merge(df, noOfMedicines, on='appointmentId', how='left')
df = pd.merge(df, noOfActiveMedicines, on='appointmentId', how='left')
df = pd.merge(df, noOfInActiveMedicines, on='appointmentId', how='left')

print(df)

df['isValidMobile'] = df['phoneNumber'].apply(lambda x: re.match(r'^(?:\+91|91)?[6-9]\d{9}$', str(x)) is not None)

print(df)


def hash_phone_number(number):
    if re.match(r'^(?:\+91|91)?[6-9]\d{9}$', str(number)):
        return hashlib.sha256(str(number).encode()).hexdigest()
    else:
        return None

df['phoneNumberHash'] = df['phoneNumber'].apply(hash_phone_number)

print(df)

active_medicines = df[df['IsActive'] == True]

medicineNames = active_medicines.groupby('appointmentId')['MedicineName'].apply(lambda x: ', '.join(x)).reset_index(name='medicineNames')

df = pd.merge(df, medicineNames, on='appointmentId', how='left')

print(df)

final_df = df[['appointmentId', 'fullName', 'phoneNumber', 'isValidMobile', 'phoneNumberHash', 'gender', 'DOB', 'Age', 'noOfMedicines', 'noOfActiveMedicines', 'noOfInActiveMedicines', 'MedicineNames']]

final_df.to_csv('final_dataframe.csv', sep='~', index=False)



aggregated_data = {
    'Age': df['Age'].mean(),
    'gender': df['gender'].value_counts().to_dict(),
    'validPhoneNumbers': df['isValidMobile'].sum(),
    'appointments': len(df['appointmentId'].unique()),
    'medicines': df['noOfMedicines'].sum(),
    'activeMedicines': df['noOfActiveMedicines'].sum()
}

with open('aggregated_data.json', 'w') as json_file:
    json.dump(aggregated_data, json_file)

gender_counts = df['gender'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
plt.title('Number of Appointments by Gender')
plt.axis('equal')
plt.show()
