"""
login page
"""

import datetime
import locale
import secrets

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv

from modules import classes as cl
from modules import constants as co
from modules import page_setup as ps
from modules import user_authentication as uauth

locale.setlocale(locale.LC_ALL, "")

# setup
PAGE = st.session_state["page"] = "login"
ps.page_setup(PAGE)


def delete_user_form() -> None:
    """Benutzer löschen"""

    with st.form("Benutzer löschen"):
        st.multiselect(
            label="Benutzer wählen, die gelöscht werden sollen",
            options=[
                f"{user['key']} ({user['name']})"
                for user in uauth.list_all_users()
                if user["key"] not in ("utec", "fl")
            ],
            key="ms_del_user",
        )

        st.markdown("###")
        st.form_submit_button("Knöpfle")


def new_user_form() -> None:
    """neuen Benutzer hinzufügen"""
    with st.form("Neuer Benutzer"):

        st.text_input(
            label="Benutzername",
            key="new_user_user",
            help=("Benutzername, wei er für den login benutzt wird - z.B. fl"),
        )
        st.text_input(
            label="Passwort",
            key="new_user_pw",
            help=("...kann ruhig auch etwas 'merkbares' sein."),
            value=secrets.token_urlsafe(8),
        )
        st.date_input(
            label="Benutzung erlaubt bis:",
            key="new_user_until",
            min_value=datetime.date.today(),
            value=datetime.date.today() + datetime.timedelta(weeks=3),
        )

        st.text_input(
            label="Name oder Firma",
            key="new_user_name",
            help=("z.B. Florian"),
        )
        st.multiselect(
            label="Zugriffsrechte",
            key="new_user_access",
            help=("Auswahl der Module, auf die dieser Benutzer zugreifen darf."),
            options=[key for key in co.PAGES if key not in ("login")],
            default=[key for key in co.PAGES if key not in ("login")],
        )

        st.markdown("###")
        st.form_submit_button("Knöpfle")


def list_all_accounts() -> None:
    """Liste aller Benutzerkonten"""
    users = uauth.list_all_users()
    df_users = pd.DataFrame()
    df_users["Benutzername"] = [user["key"] for user in users]
    df_users["Name"] = [user["name"] for user in users]
    df_users["Verfallsdatum"] = [user["access_until"] for user in users]
    df_users["Zugriffsrechte"] = [str(user["access_lvl"]) for user in users]

    st.dataframe(df_users)
    st.button("ok")


def user_accounts() -> None:
    """Benutzerkontensteuerung"""

    st.markdown("###")
    st.markdown("---")

    lis_butt = [
        "butt_add_new_user",
        "butt_del_user",
    ]

    # Knöpfle für neuen Benutzer, Benutzer löschen...
    if not any(st.session_state.get(butt) for butt in lis_butt):
        st.button("Liste aller Konten", "butt_list_all")
        st.button("neuen Benutzer hinzufügen", "butt_add_new_user")
        st.button("Benutzer löschen", "butt_del_user")
        st.button("Benutzerdaten ändern", "butt_change_user", disabled=True)

        st.markdown("---")

    # Menu für neuen Benutzer
    if st.session_state.get("butt_add_new_user"):
        new_user_form()
        st.button("abbrechen")
    st.session_state["butt_sub_new_user"] = st.session_state.get(
        "FormSubmitter:Neuer Benutzer-Knöpfle"
    )

    # Menu zum Löschen von Benutzern
    if st.session_state.get("butt_del_user"):
        delete_user_form()
        st.button("abbrechen")
    st.session_state["butt_sub_del_user"] = st.session_state.get(
        "FormSubmitter:Benutzer löschen-Knöpfle"
    )

    if st.session_state.get("butt_list_all"):
        list_all_accounts()


col1, col2 = st.columns(2)

with col2:
    cl.LottieAnimation("login", height=450).show_animation()

with col1:

    # user authentication
    load_dotenv(".streamlit/secrets.toml")

    if "li_all_users" not in st.session_state:
        st.session_state["li_all_users"] = uauth.list_all_users()
        # users = st.session_state["li_all_users"]

    if "dic_credentials" not in st.session_state:
        st.session_state["dic_credentials"] = {
            "usernames": {
                user["key"]: {
                    "name": user["name"],
                    "email": user["email"],
                    "password": user["password"],
                }
                for user in st.session_state["li_all_users"]
            }
        }

    if "authenticator" not in st.session_state:
        st.session_state["authenticator"] = stauth.Authenticate(
            credentials=st.session_state["dic_credentials"],
            cookie_name="utec_tools",
            key="uauth",
            cookie_expiry_days=30,
        )

    name, authentication_status, username = st.session_state["authenticator"].login(
        "Login", "main"
    )

    if authentication_status:
        st.session_state["access_lvl_user"] = [
            u["access_lvl"]
            for u in st.session_state["li_all_users"]
            if u["key"] == st.session_state.get("username")
        ][0]
        st.session_state["access_lvl"] = st.session_state["access_lvl_user"]
        if st.session_state["access_lvl_user"] in ("god", "full"):
            st.session_state["access_pages"] = co.PAGES
            st.session_state["access_until"] = datetime.date.max
        else:
            st.session_state["access_pages"] = st.session_state["access_lvl_user"]
            st.session_state["access_until"] = [
                datetime.datetime.strptime(u["access_until"], "%Y-%m-%d").date()
                for u in st.session_state["li_all_users"]
                if u["key"] == st.session_state.get("username")
            ][0]

        if st.session_state.get("username") in ("utec"):

            st.markdown(
                """
                Du bist mit dem allgemeinen UTEC-Account angemeldet.  \n  \n
                Viel Spaß mit den Tools!
                """
            )

        else:
            st.markdown(
                f"""
                Angemeldet als "{st.session_state.get('name')}"
                """
            )

            if st.session_state.get("access_until") < datetime.date.max:
                st.markdown(
                    f"""
                    Mit diesem Account kann auf folgende Module bis zum {st.session_state['access_until']:%d.%m.%Y} zugegriffen werden:
                    """
                )
            else:
                st.markdown(
                    """
                    Mit diesem Account kann auf folgende Module zugegriffen werden:
                    """
                )

            for page in st.session_state["access_pages"]:
                if page != "login":
                    st.markdown(f"- {cl.Page(page).title}")
                    # st.markdown(f"- {dics.PAGES[page]['page_tit']}")

        st.markdown("###")
        st.session_state["authenticator"].logout("Logout", "main")

        if not isinstance(
            st.session_state["access_lvl_user"], list
        ) and st.session_state["access_lvl_user"] in ("god"):
            user_accounts()
            # neuen Benutzer eintragen
            if st.session_state.get("butt_sub_new_user"):
                with st.spinner("Momentle bitte, Benutzer wird hinzugefügt..."):
                    uauth.insert_new_user(
                        st.session_state.get("new_user_user"),
                        st.session_state.get("new_user_name"),
                        st.session_state.get("new_user_email"),
                        st.session_state.get("new_user_pw"),
                        st.session_state.get("new_user_access"),
                        str(st.session_state.get("new_user_until")),
                    )

            # Benutzer löschen
            if st.session_state.get("butt_sub_del_user"):
                uauth.delete_user()

    elif authentication_status is None:
        st.warning("Bitte Benutzernamen und Passwort eingeben")

    elif authentication_status is False:
        st.error("Benutzername oder Passwort falsch")
