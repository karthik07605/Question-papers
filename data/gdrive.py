import os
import json
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2 import service_account
from io import BytesIO

# Load service account JSON from environment variable
SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
credentials_info = json.loads(SERVICE_ACCOUNT_JSON)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    """Authenticate and return the Google Drive service instance."""
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )
    return googleapiclient.discovery.build("drive", "v3", credentials=credentials)

def upload_to_drive(file, file_name, folder_id=None):
    """Uploads an In-Memory file to Google Drive and returns a shareable link."""
    service = get_drive_service()

    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    file_stream = BytesIO(file.read())  # Read file into memory
    media = googleapiclient.http.MediaIoBaseUpload(file_stream, mimetype=file.content_type)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # Make the file publicly accessible
    permission = {"role": "reader", "type": "anyone"}
    service.permissions().create(fileId=uploaded_file["id"], body=permission).execute()

    # Return the shareable link
    return f"https://drive.google.com/uc?id={uploaded_file['id']}&export=download"
