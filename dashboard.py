import shutil

import streamlit as st
import difflib
from markUp import markUpDifferences
import pandas as pd
import os
from diffReport import diffReport, html_output
import glob
import matplotlib.pyplot as plt
import matplotlib
import smtplib

matplotlib.use('Agg')
import seaborn as sns

shutil.rmtree('tempDir')
os.mkdir("tempDir")
os.mkdir("tempDir/input1")
os.mkdir("tempDir/input2")

#files = glob.glob('tempDir/input1/*')  # Delete every file present in temp directory
#for f in files:
#    os.remove(f)

#files = glob.glob('tempDir/input2/*')  # Delete every file present in temp directory
#for f in files:
#    os.remove(f)


st.set_page_config(page_title='PDF Compare', page_icon='📄', initial_sidebar_state='collapsed')

sender = "hphulara996@gmail.com>"
receiver = "mcdhp214@gmail.com>"

message = f"""\
Subject: Batch job for PDF Comparison ran successfully.
To: {receiver}
From: {sender}

Hi User, 

Batch job for PDF Comparison ran successfully. Please find detailed report with ratios in output folder.

Thanks"""

def save_uploadedfile(uploadedfile, filenum, path):
    with open(os.path.join("tempDir",path, "file" + str(filenum) + ".pdf"), "wb") as f:
        f.write(uploadedfile.getbuffer())
        f.close()
    return #st.success("Saved File:{} to tempDir".format(uploadedfile.name))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    st.markdown("<h2 style='text-align: center; color: grey;'>PDF Comparison</h2>", unsafe_allow_html=True)
    input1 = st.file_uploader('Please upload your 1st file', type=['pdf'], accept_multiple_files=True)
    i=1
    for input_file in input1:
        if input_file is not None:
            save_uploadedfile(input_file, i, "input1")
            i+=1
    #if input1 is not None:
    #    file_details = {'File Name': input1.name, 'File Size': input1.size}
    #    st.write(file_details)
    #    save_uploadedfile(input1, 1)
    input2 = st.file_uploader('Please upload your 2nd file', type=['pdf'], accept_multiple_files=True)
    i = 1
    for input_file in input2:
        if input_file is not None:
            save_uploadedfile(input_file, i, "input2")
            i+=1

    #if input2 is not None:
    #    file_details = {'File Name': input2.name, 'File Size': input2.size}
    #    st.write(file_details)
    #    save_uploadedfile(input2, 2)

    select_ratio = ['Partial Ratio', 'qRatio', 'wRatio', "tokenSortRatio", 'partialRatio', 'tokenSetRatio',
                    'partialTokenSortRatio']
    choice1 = st.radio('Please select the Partial Ratio', select_ratio)
    st.write('Select options to exclude from analytics:')

    ncol = st.sidebar.number_input('Number of characters/ Substring to exclude', 0, 20, 1)
    cols = st.columns(ncol)

    st.button("Submit")
    col1, col2, col3 = st.columns(3)
    st.write("List of characters/ Substring to exclude")
    with col1:
        text_1 = st.text_input('Option 1', key='1')
    with col2:
        text_2 = st.text_input('Option 2', key='2')
    with col3:
        text_3 = st.text_input('Option 3', key='3')
    st.write(
        "For more characters or substrings to exclude from analytics, please provide them in the below text box seperated by a coma , Ex: 'text1,text2' ")
    comma_sep_input = st.text_input('Comma seperated characters to exclude')
    list_to_exclude = comma_sep_input.split(',')
    list_to_exclude += [text_1, text_2, text_3]

    files_in_input1 = len([name for name in os.listdir('tempDir/input1') if os.path.isfile(os.path.join('tempDir/input1', name))])
    files_in_input2 = len([name for name in os.listdir('tempDir/input2') if os.path.isfile(os.path.join('tempDir/input2', name))])

    if(files_in_input1 != files_in_input2):
        st.write("Number of files in input 1 does not match with number of files in input 2, Please provide the same number of files for one to one comparison")
    else:
        for i in range(1,files_in_input1+1):
            os.mkdir(os.path.join("tempDir", "output" + str(i)))
            df = diffReport("tempDir/input1/file"+str(i)+".pdf","tempDir/input2/file"+str(i)+".pdf",html_return=False, partial_ratio=choice1, exlude_analytics=list_to_exclude, path_file_output="tempDir/output"+str(i)+"/")
            html = html_output(df,path_file_output="tempDir/output"+str(i)+"/")
    #if os.path.isfile("tempDir/file1.pdf") and os.path.isfile("tempDir/file2.pdf"):
    #df = diffReport("tempDir/file1.pdf", "tempDir/file2.pdf", html_return=False, partial_ratio=choice1,
                        #exlude_analytics=list_to_exclude)
            #st.write(df)
            #html_file = html_output(df, 'tempDir/')
            #st.markdown(html_file, unsafe_allow_html=True)
            fig = plt.figure()
            df['Partial Ratio'].value_counts().plot(kind='bar')
            st.pyplot(fig)
            sns.countplot(df['Partial Ratio'])
            sns.barplot()

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("1809d3581cfba7", "7403033333e364")
        server.sendmail(sender, receiver, message)

    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
