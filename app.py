import streamlit as st
import google.oauth2.credentials
import google_auth_oauthlib.flow
import webbrowser

st.title("Google Photos Uploader")
st.write(st.experimental_get_query_params())

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
        access_type='offline',
        include_granted_scopes='true')

    webbrowser.open(authorization_url)
