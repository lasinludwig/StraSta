"""activities page"""

import streamlit as st

from modules import constants as con
from modules import page_setup as ps

PAGE = "activities"
ps.page_setup(PAGE)

st.dataframe(con.ALL_ACTIVITIES)
