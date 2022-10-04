"""General page setup (Title, Logo, etc.)"""


import sys

import streamlit as st

from modules import classes as cl
from modules import css_hacks as css
from modules import functions as fuc
from modules import user_authentication as uauth


# browser tab
def page_setup(page: str) -> None:
    """Seitenaufbau"""

    st.set_page_config(page_title="Strava Stats", layout="wide")

    css.widget_headers()

    st.session_state["title_container"] = st.container()

    with st.session_state["title_container"]:

        # Logo und Titel
        col1, col2, col3 = st.columns([33, 33, 33])
        with col1:
            st.title(cl.Page(page).title)

        # animation
        with col2:
            if cl.Page(page).title_animation:
                cl.LottieAnimation("running").show_animation()

        # Version info
        with col3:
            if "com_date" not in st.session_state:
                fuc.get_com_date()
            st.write(
                f"""
                    <i><span style="line-height: 110%; font-size: 12px; float:right; text-align:right">
                        letzte Änderungen: <br>
                        {st.session_state["com_date"]:%d.%m.%Y}  {st.session_state["com_date"]:%H:%M}<br><br>
                        "{st.session_state["com_msg"]}"
                    </span></i>
                """,
                unsafe_allow_html=True,
            )

            users = uauth.list_all_users()
            god_users = [user["key"] for user in users if user["access_lvl"] == "god"]
            if st.session_state.get("username") in god_users:
                st.write(
                    f"""
                        <i><span style="line-height: 110%; font-size: 12px; float:right; text-align:right">
                            (Python version {sys.version.split()[0]})
                        </span></i>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
