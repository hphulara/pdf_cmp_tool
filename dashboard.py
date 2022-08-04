import streamlit as st
import difflib
from markUp import markUpDifferences
import pandas as pd
import os
from diffReport import diffReport,html_output
import glob
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import numpy as np
import smtplib

sender = "hphulara996@gmail.com>"
receiver = "mcdhp214@gmail.com>"

message = f"""\
Subject: PDF Comparison ran successfully.
To: {receiver}
From: {sender}

Hi User, 

PDF Comparison ran successfully. Please download the detailed CSV report with ratios.

Thanks"""

st.set_page_config(page_title='PDF Compare',page_icon='📄',initial_sidebar_state='collapsed')



def main():
    st.markdown("<h2 style='text-align: center; color: grey;'>PDF Comparison</h2>", unsafe_allow_html=True)
    try:
        input1 = st.file_uploader('Upload files from first folder', type=['pdf'],accept_multiple_files=True,)
        filelist1=[]
        if input1 is not None:
            for i in range(len(input1)):
                head, sep, tail = str(input1[i].name).partition(".")
                filelist1.append(str(head))
        st.write(filelist1)
    except Exception as er:
        st.error("Error while readin the files from first folder {} ".format(er))
    else:
        try:
            input2 = st.file_uploader('Upload files from second folder', type=['pdf'],accept_multiple_files=True,)
            filelist2=[]
            if input2 is not None:
                for i in range(len(input2)):
                    head, sep, tail = str(input2[i].name).partition(".")
                    filelist2.append(str(head))
            st.write(filelist2)
        except Exception as er:
            st.error("Error while readin the files from second folder {} ".format(er))
        else:
            try:
                select_ratio =['Partial Ratio','qRatio','wRatio',"tokenSortRatio",'partialRatio','tokenSetRatio','partialTokenSortRatio']
                choice = st.radio('Please select the Partial Ratio',select_ratio)
                st.write('Select options to exclude from analytics:')

                ncol = st.sidebar.number_input('Number of characters/ Substring to exclude', 0, 20, 1)
                cols = st.columns(ncol)

                #st.button("Submit")
                col1, col2, col3 = st.columns(3)
                st.write("List of characters/ Substring to exclude")
                with col1:
                    text_1 = st.text_input('Option 1', key='1')
                with col2:
                    text_2 = st.text_input('Option 2', key='2')
                with col3:
                    text_3 = st.text_input('Option 3', key='3')
                st.write("For more characters or substrings to exclude from analytics, please provide them in the below text box seperated by a comma , Eg: 'text1,text2' ")
                comma_sep_input = st.text_input('Comma seperated characters to exclude')
                list_to_exclude = comma_sep_input.split(',')
                list_to_exclude += [text_1,text_2,text_3]

                for i in range(len(input1)):
                    for j in range(len(input2)):

                        if input1[i].name.split('_')[0] == input2[j].name.split('_')[0]:
                        
                            df = diffReport(input1[i].name,input2[j].name,html_return=True,partial_ratio=choice,exlude_analytics=list_to_exclude)
                            st.header('Comparison difference between ' + input1[i].name + '  &  ' + input2[j].name)
                            st.write(df)
                            #st.write(html_op)
                            file_name = str(input1[i].name.split('_')[0]) + '_compare.csv'
                            df = df.to_csv().encode('utf-8')
                            st.download_button(
                              label = "Download data as CSV",
                              data = df,
                              file_name = file_name,
                              mime = 'text/csv',
                            )
                with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                    server.login("1809d3581cfba7", "7403033333e364")
                    server.sendmail(sender, receiver, message)
            except Exception as er:
                st.error("Error while showing the ratio result {} ".format(er))
            
                    

                

main()
