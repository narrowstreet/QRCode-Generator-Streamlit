import numpy as np
import streamlit as st
import pandas as pd
import os
import time

import pickle
import os
# from google_auth_oauthlib.flow import Flow, InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from google.auth.transport.requests import Request


timestr = time.strftime("%Y%m%d-%H%M%S")
# For QR Code
import qrcode
qr = qrcode.QRCode(version=1, 
                   error_correction=qrcode.constants.ERROR_CORRECT_L, 
                   box_size=10,
                   border=14)

from PIL import Image
# Function to Load Image
def load_image(img):
    im = Image.open(img)
    return im
# Application
def main():
    st.set_page_config(page_title="NWST Check In QRCode", page_icon="📈")
    database = pd.read_excel("ALL-Narrowstreet_2023-09-20.xlsx")
    menu = ["Generate QRCode", "Newcomers Form"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Generate QRCode":
        st.subheader("Generate QRCode")
        # Text Input
        with st.form("mobile_number_form"):
            phone_number = st.number_input(label='Put your mobile number here (e.g. 012xxxxxxx)', value=1, format="%i", help="e.g. 012xxxxxxx")
            submit_button = st.form_submit_button("Generate")
        if submit_button:
            mobile_number = "0"+str(phone_number)
            
            # Add Data
            qr.add_data(mobile_number)
            
            # Generate
            qr.make(fit=True)
            img = qr.make_image(fill_color='black',back_color='white')
            
            # Filename
            img_filename = 'generate_image_{}.png'.format(timestr)
            img.save(img_filename)

            st.write('Your mobile number is ', mobile_number)
            database['Mobile Number']=database['Mobile Number'].fillna("0")
            database['Mobile Number']=database['Mobile Number'].replace('-', '', regex=True)
            database['Mobile Number']=database['Mobile Number'].replace(' ', '', regex=True)
            
        # Layout
            if mobile_number in database['Mobile Number'].unique():
                name = database.loc[database['Mobile Number'] == mobile_number].iloc[0, 1]
                st.write("Hello ", name, "!")
                st.image(image=img_filename, width=200)
            else: 
                st.write("Your number is not in the system.")

    elif choice == "Newcomers Form":
        st.subheader("Newcomers Form")
if __name__ == '__main__':
    main()
    