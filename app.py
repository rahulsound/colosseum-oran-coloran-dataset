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
      

###################
root_dir = os.getcwd()
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

#Write-up:
st.divider()
run_writeup()
st.divider()

#Plots:1.
num_cols = df_combo_ue.columns
col1, col2, col3 = st.columns(3)
num_selection1 = 'ul_mcs'
num_selection2 = 'ul_brate'
cat_selection  = 'ue_id'
with col1:
    num_selection1 = st.selectbox("Select x axis to plot fig1:", num_cols)
with col2:
    num_selection2 = st.selectbox("Select y axis to plot fig1:", num_cols)     
with col3:
    cat_selection = st.selectbox("Select criterion to plot fig1:",num_cols)
fig = px.scatter(data_frame=df_combo_ue, x=num_selection1, y=num_selection2, color=cat_selection)
st.plotly_chart(fig) 

st.divider()

profiler = st.checkbox('Run Profiler')
if profiler:
    st.write('Running Profiler:')
    st.write(df_bs.describe())
    pr = ProfileReport(df_bs, title="Profiling Report")
    st_profile_report(pr)

