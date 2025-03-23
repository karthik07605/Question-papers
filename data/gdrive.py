import os
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2 import service_account
from io import BytesIO

# Path to service account JSON
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "data.json")

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    """Authenticate and return the Google Drive service instance."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
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
