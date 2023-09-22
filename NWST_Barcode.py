import numpy as np
import streamlit as st
import pandas as pd
import time


timestr = time.strftime("%Y%m%d-%H%M%S")
# For QR Code
import qrcode
qr = qrcode.QRCode(version=1, 
                   error_correction=qrcode.constants.ERROR_CORRECT_L, 
                   box_size=5,
                   border=1)

from PIL import Image
# Function to Load Image
def load_image(img):
    im = Image.open(img)
    return im
# Application
def main():
    st.set_page_config(page_title="NWST Check In QRCode", page_icon="🕶️")
    database = pd.read_excel("ALL-Narrowstreet_2023-09-20.xlsx")

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

            st.write('*Mobile number given:*', f'*{mobile_number}*')
            database['Mobile Number']=database['Mobile Number'].fillna("0")
            database['Mobile Number']=database['Mobile Number'].replace('-', '', regex=True)
            database['Mobile Number']=database['Mobile Number'].replace(' ', '', regex=True)

    # Layout
    if submit_button:
        if mobile_number in database['Mobile Number'].unique():
            name = database.loc[database['Mobile Number'] == mobile_number].iloc[0, 1]
            st.header(f"**Hello {name} !**")
            st.image(image=img_filename, width=100)
        else: 
            st.header("**Your number is NOT in the system.**")
            st.link_button("Please fill NEWCOMER'S FORM here", "https://sibkl.elvanto.com.au/form/ae45fdca-47a2-4d2f-9cf9-87d338a03625")

if __name__ == '__main__':
    main()
    
