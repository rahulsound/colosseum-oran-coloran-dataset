import streamlit as st
import pandas as pd
import os
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from natsort import natsorted
import glob
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import random
###################
#Helper functions:

def run_writeup():
      st.markdown('''
##### Colosseum O-RAN ColORAN Dataset
This repository contains the dataset for the paper M. Polese, L. Bonati, S. D'Oro, S. Basagni, T. Melodia, "ColO-RAN: Developing Machine Learning-based xApps for Open RAN Closed-loop Control on Programmable Experimental Platforms," IEEE Transactions on Mobile Computing, pp. 1-14, July 2022. Please cite the paper if you plan to use it in your publication.
This work was partially supported by the U.S. National Science Foundation under Grants CNS-1923789 and NSF CNS-1925601, and the U.S. Office of Naval Research under Grant N00014-20-1-2132. 
##### Experiment setup
- Number of Base Stations (BSs): 7
	- Nodes: 1, 8, 15, 22, 29, 36, 43
- Channel bandwidth: 10 MHz (50 Physical Resource Blocks (PRBs))
- Number of slices for each BS: 3
- Scheduling policies available to each slice:
	- Policy 0: Round-robin (RR)
  - Policy 1: Waterfilling (WF)
  - Policy 2: Proportionally fair (PF)
- Number of User Equipments (UEs): 42
- Radio Frequency (RF) scenario setup (Colosseum Rome scenario):
  	- Medium: UEs uniformly distributed within 50 m of each BS
- UE Mobility: static
- Traffic classes:
  	- eMBB: Constant bitrate traffic (4 Mbps per UE)
  	- MTC: Poisson traffic (30 pkt/s of 125 bytes per UE)
  	- URLLC: Poisson traffic (10 pkt/s of 125 bytes per UE)
- UEs belong to different traffic classes:
	- eMBB UEs (slice 0): 3, 6, 10, 13, 17, 20, 24, 27, 31, 34, 38, 41, 45, 48
	- MTC UEs (slice 1): 4, 7, 11, 14, 18, 21, 25, 28, 32, 35, 39, 42, 46, 49
 	- URLLC UEs (slice 2): 2, 5, 9, 12, 16, 19, 23, 26, 30, 33, 37, 40, 44, 47
- UEs are divided per slice based on traffic types:
  	- Slice 0: eMBB UEs
  	- Slice 1: MTC UEs
  	- Slice 2: URLLC UEs

#### Training configurations
-   Details [here](https://github.com/rahulsound/colosseum-oran-coloran-dataset/edit/master/README.md)
        ''')
      
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

###################


select_option = st.sidebar.selectbox('Select option to analyze:',['About','Individual Runs', 'Summaries'])
if select_option == 'About':
    st.divider()
    run_writeup()
    st.divider()      
elif select_option == 'Individual Runs':
    root_dir = os.getcwd()
    # st.write(root_dir)
    st.header('EDA App for exploring ColORAN Dataset:')
    run = 'rome_static_medium'
    os.chdir(run)
    sched_list = natsorted(os.listdir())
    os.chdir(sched_list[1])
    train_list = natsorted(os.listdir())
    os.chdir(train_list[1])
    exp_list = natsorted(os.listdir())
    os.chdir(exp_list[1])
    bs_list = natsorted(os.listdir())

    sched = st.sidebar.radio("Select scheduler:",sched_list, horizontal=True)
    train = st.sidebar.radio("Select Training #:",train_list, horizontal=True)
    exp = st.sidebar.radio("Select Experiment # :",exp_list, horizontal=True)
    bs = st.sidebar.radio("Select Base station #:",bs_list, horizontal=True)

    os.chdir(root_dir)
    bsdir = run + os.path.sep + sched + os.path.sep + train + os.path.sep + exp + os.path.sep + bs + os.path.sep 
    bsfile = run + os.path.sep + sched + os.path.sep + train + os.path.sep + exp + os.path.sep + bs + os.path.sep + bs + '.csv'

    #Grab the files:
    #BS

    #st.header('Reading files first time')
    df_bs = pd.read_csv(bsfile)
    #All UEs
    all_files = glob.glob(os.path.join(bsdir, "ue*.csv"))
    #df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    df_combo_ue = pd.DataFrame()
    #append all files together
    for file in all_files:
                df_temp = pd.read_csv(file)
                sep = os.path.sep
                df_temp['ue_id'] = file.split('.')[0].split(sep)[-1]
                df_combo_ue = pd.concat([df_combo_ue, df_temp])

    #Plots:1.
    num_cols = df_combo_ue.columns
    col1, col2, col3 = st.columns(3)
    num_selection1 = 'ul_mcs'
    num_selection2 = 'ul_brate'
    cat_selection  = 'ue_id'
    with col1:
        num_selection1 = st.selectbox("Select x axis to plot fig1:", num_cols, index=13)
    with col2:
        num_selection2 = st.selectbox("Select y axis to plot fig1:", num_cols, index=15)     
    with col3:
        cat_selection = st.selectbox("Select criterion to plot fig1:",num_cols, index=21)
    fig = px.scatter(data_frame=df_combo_ue, x=num_selection1, y=num_selection2, color=cat_selection)
    st.plotly_chart(fig) 

    st.divider()

    profiler = st.checkbox('Run Profiler')
    if profiler:
        st.write('Running Profiler:')
        st.write(df_bs.describe())
        pr = ProfileReport(df_bs, title="Profiling Report")
        st_profile_report(pr)

elif select_option == 'Summaries':
    root_dir = os.getcwd()
    # st.write(root_dir)
    st.header('EDA App for exploring ColORAN Dataset:')
    run = 'rome_static_medium'
    os.chdir(run)
    sched_list = natsorted(os.listdir())
    os.chdir(sched_list[1])
    train_list = natsorted(os.listdir())
    os.chdir(train_list[1])
    exp_list = natsorted(os.listdir())
    os.chdir(exp_list[1])
    bs_list = natsorted(os.listdir())
    os.chdir(root_dir)

    if os.path.isfile('bs_combo_df.csv'):
        if 'bs_summary' not in st.session_state:
            st.session_state['bs_summary'] = True
            st.session_state['bs_combo_df']  = pd.read_csv('bs_combo_df.csv')
            st.session_state['bs_summary_redo'] = False
    else: # Complete Init
        st.session_state['bs_summary'] = False
        st.session_state['bs_combo_df']  = None
        st.session_state['bs_summary_redo'] = False        
    
    sample_pct = 0.1 #Default
    sample_pct = st.sidebar.select_slider('Select % to sample', [0.05, 0.1, 1, 25, 50, 100])
    bs_summary = st.checkbox('Prepare summaries of all base stations?')
    # st.write('1. Summary: {}, Redo: {}'.format(st.session_state['bs_summary'], st.session_state['bs_summary_redo']))
    if st.sidebar.button('Rerun Sampling'):
        st.session_state['bs_summary_redo'] = True
    if bs_summary:
        if st.session_state['bs_summary'] and not st.session_state['bs_summary_redo']:
            bs_combo_df = st.session_state['bs_combo_df']
        else:
            st.write('File size too large for summarizing')
            st.write('... sampling {} % of data for quick preview:'.format(sample_pct))
            with st.spinner(text="In progress..."):
                p = float(sample_pct)  # % of the lines
                sep = os.path.sep
                bs_combo_df = pd.DataFrame()
                sched_list = natsorted(glob.glob(os.path.join((run),'sched*')))
                for s in sched_list:
                    st.write('Parsing: [{}] data ... '.format(s.split(sep)[-1] ))
                    tr_list = natsorted(glob.glob(os.path.join((s), 'tr*')))
                    for t in tr_list:
                        exp_list = natsorted(glob.glob(os.path.join((t), 'exp*')))
                        for e in exp_list:
                            bs_list = natsorted(glob.glob(os.path.join((e), 'bs*')))
                            for b in bs_list:
                                file_name = b.split(sep)[-1]
                                #df_temp = pd.read_csv(b+ os.path.sep + file_name + '.csv').sample(n=100) 
                                df_temp = pd.read_csv(b+ os.path.sep + file_name + '.csv', 
                                                      skiprows=lambda i: i>0 and random.random() > p
                                                      )
                                sep = os.path.sep
                                df_temp['base_station'] = b.split(sep)[-1]
                                df_temp['exp'] = e.split(sep)[-1]
                                df_temp['training'] = t.split(sep)[-1]
                                df_temp['sched'] = s.split(sep)[-1]
                                bs_combo_df = pd.concat([bs_combo_df, df_temp])
                st.session_state['bs_summary']  = True
                st.session_state['bs_combo_df'] = bs_combo_df
                st.session_state['bs_summary_redo'] = False
                bs_combo_df.to_csv('bs_combo_df.csv')

            csv = convert_df(bs_combo_df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="base_station_all.csv",
                mime="text/csv",
            )
        #Plots:1.
        
        st.write('[Rows: {}, Columns: {} with {} % of samples]'.format(bs_combo_df.shape[0], bs_combo_df.shape[1], sample_pct))
        # st.write('2. Summary: {}, Redo: {}'.format(st.session_state['bs_summary'], st.session_state['bs_summary_redo']))
        num_cols = bs_combo_df.columns
        col1, col2, col3 = st.columns(3)

        with col1:
            num_selection1 = st.selectbox("Select x axis to plot fig1:", num_cols, index=2)
        with col2:
            num_selection2 = st.selectbox("Select y axis to plot fig1:", num_cols, index=3)     
        with col3:
            cat_selection = st.selectbox("Select criterion to plot fig1:",num_cols, index=7)
        fig = px.scatter(data_frame=bs_combo_df, x=num_selection1, y=num_selection2, color=cat_selection)
        st.plotly_chart(fig) 
        # st.write('2. Summary: {}, Redo: {}'.format(st.session_state['bs_summary'], st.session_state['bs_summary_redo']))


