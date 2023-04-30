import streamlit as st
import google.oauth2.credentials
import google_auth_oauthlib.flow

from pathlib import Path
import pickle
import webbrowser

st.set_page_config(layout="wide")

st.title("Google Photos Uploader")


def loadPickledCredentials() -> google.oauth2.credentials.Credentials:
    """
    Loads credentials from a pickle file
    """
    with open(".secret/credentials.pickle", "rb") as fp:
        credentials = pickle.load(fp)
    st.success("Credentials loaded")
    return credentials


def getCredentialsAndSavePickle() -> google.oauth2.credentials.Credentials:
    """
    Gets credentials from Google and saves them to a pickle file
    """
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        ".secret/client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/photoslibrary",
            "https://www.googleapis.com/auth/photoslibrary.sharing",
            "https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata",
        ],
    )
    flow.redirect_uri = "http://localhost:8501/"
    flow.fetch_token(code=st.experimental_get_query_params()["code"][0])
    credentials = flow.credentials

    if not credentials.refresh_token == None:
        with open(".secret/credentials.pickle", "wb") as pickleFile:
            pickle.dump(credentials, pickleFile)
        st.info("Credentials saved")

    st.experimental_set_query_params()
    return credentials


def redirectGoogleLogin():
    """
    Redirects to Google Login
    """
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        ".secret/client_secret.json",
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
    st.write("Please login, this tab cen be closed")


if __name__ == "__main__":
    credentials: google.oauth2.credentials.Credentials = None

    if Path(".secret/credentials.pickle").is_file():
        credentials = loadPickledCredentials()
    elif "code" in st.experimental_get_query_params():
        credentials = getCredentialsAndSavePickle()
    else:
        if st.button("Login with Google"):
            redirectGoogleLogin()
        st.stop()

    with st.expander("Credentials", expanded=False):
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
