import streamlit as st
import pandas as pd
import os
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


st.header('EDA App:')
run = 'rome_static_medium'
sched = 'sched0'
tr = 'tr22'
exp = 'exp1'
bs = 'bs1'
csv = 'bs1'

file = run + os.path.sep + sched + os.path.sep + tr + os.path.sep + exp + os.path.sep + bs + os.path.sep + csv + '.csv'
st.write(file)
df = pd.read_csv(file)

st.write(df.head())
st.divider()

#pr = ProfileReport(df, title="Profiling Report")
#st_profile_report(pr)

