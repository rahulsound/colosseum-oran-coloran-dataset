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

root_dir = os.getcwd()
st.header('EDA App:')
run = 'rome_static_medium'
os.chdir(run)
sched_list = os.listdir()
os.chdir(sched_list[1])
train_list = natsorted(os.listdir())
os.chdir(train_list[1])
exp_list = os.listdir()
os.chdir(exp_list[1])
bs_list = os.listdir()

sched = st.sidebar.radio("Select scheduler:",sched_list, horizontal=True)
train = st.sidebar.radio("Select Training #:",train_list, horizontal=True)
exp = st.sidebar.radio("Select Experiment # :",exp_list, horizontal=True)
bs = st.sidebar.radio("Select Base station #:",bs_list, horizontal=True)

os.chdir(root_dir)
bsdir = run + os.path.sep + sched + os.path.sep + train + os.path.sep + exp + os.path.sep + bs + os.path.sep 
bsfile = run + os.path.sep + sched + os.path.sep + train + os.path.sep + exp + os.path.sep + bs + os.path.sep + bs + '.csv'
all_files = glob.glob(os.path.join(bsdir, "ue*.csv"))
#df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
df_combo_ue = pd.DataFrame()
#append all files together
for file in all_files:
            df_temp = pd.read_csv(file)
            df_temp['ue_id'] = file.split('.')[0].split('\\')[-1]
            df_combo_ue = pd.concat([df_combo_ue, df_temp])

st.divider()
st.write(bsfile)
df_bs = pd.read_csv(bsfile)
st.subheader('BS File:', bsfile)
st.write(df_bs.head())
st.divider()
st.subheader('UE files:')
st.write(df_combo_ue.head())
st.divider()
num_cols = df_combo_ue.columns

col1, col2, col3 = st.columns(3)
with col1:
    num_selection1 = st.selectbox("Select x axis to plot fig1:", num_cols)
with col2:
    num_selection2 = st.selectbox("Select y axis to plot fig1:", num_cols)     
with col3:
    cat_selection = st.selectbox("Select criterion to plot fig1:",num_cols)
fig = px.scatter(data_frame=df_combo_ue, x=num_selection1, y=num_selection2, color=cat_selection)
st.plotly_chart(fig) 
# with col2:
#        st.write('Col2')
    # charts = ('box', 'violin', 'kdeplot', 'histogram')
    # chart_selection = st.selectbox('Choose the chart type', charts)
    # # cat_selectiona = st.selectbox("Select criterion to plot fig2:",num_cols)
    # num_selectiona1 = st.selectbox("Select feature 1 to plot fig2:", num_cols)
    # num_selectiona2 = st.selectbox("Select feature 2 to plot fig2:", num_cols)
    # fig, ax = plt.subplots()
    # if chart_selection == 'box':
    #     sns.boxplot(x=num_selectiona1, y=num_selectiona2, data=df_combo_ue, ax=ax)
    # elif chart_selection == 'violin':
    #     sns.violinplot(x=num_selectiona1, y=num_selectiona2, data=df_combo_ue, ax=ax)
    # elif chart_selection == 'kdeplot':
    #     sns.kdeplot(x=num_selectiona1, y=num_selectiona2, data=df_combo_ue, ax=ax)
    # else:
    #     sns.histplot(x=num_selectiona1, y=num_selectiona2, data=df_combo_ue, ax=ax)
    # st.pyplot(fig)

profiler = st.checkbox('Run Profiler')
if profiler:
    st.write('Running Profiler:')
    st.write(df_bs.describe())
    pr = ProfileReport(df_bs, title="Profiling Report")
    st_profile_report(pr)

