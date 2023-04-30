import streamlit as st
import google.oauth2.credentials
import google_auth_oauthlib.flow

from pathlib import Path
import pickle
import webbrowser

st.set_page_config(layout="wide")

st.title("Google Photos Uploader")
st.write(st.experimental_get_query_params())

st.write(st.session_state)



if "code" in st.experimental_get_query_params():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        ".streamlit/client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/photoslibrary.sharing",
            "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
        ],
    )
    flow.redirect_uri = "http://localhost:8501/"
    flow.fetch_token(code=st.experimental_get_query_params()["code"][0])
    credentials = flow.credentials
    st.write(
        {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }
    )

    st.experimental_set_query_params()


if st.button("Login"):

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        ".streamlit/client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/photoslibrary.sharing",
            "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
        ],
    )
    flow.redirect_uri = "http://localhost:8501/"
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    webbrowser.open(authorization_url)
