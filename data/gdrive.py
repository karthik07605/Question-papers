import json
from io import BytesIO
import os
from decouple import config
from google.oauth2 import service_account
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    """
    Authenticate with Google Drive using a service account stored in an environment variable.
    Handles private key formatting automatically.
    """
    # Load the service account JSON from environment variable
    service_account_info_str = config("GOOGLE_SERVICE_ACCOUNT_JSON", default=None)
    if not service_account_info_str:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable not set!")

    try:
        service_account_info = json.loads(service_account_info_str)
    except json.JSONDecodeError:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON!")

    # Fix private key newlines if they are escaped (\n)
    if "private_key" in service_account_info:
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
        if not service_account_info["private_key"].startswith("-----BEGIN PRIVATE KEY-----"):
            raise ValueError("Private key format is invalid!")

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
    return googleapiclient.discovery.build("drive", "v3", credentials=credentials)


def upload_to_drive(file, file_name, folder_id=None):
    """
    Upload an in-memory file (e.g., Django UploadedFile) to Google Drive
    and return a publicly shareable link.
    """
    service = get_drive_service()

    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    # Read file into memory
    file_stream = BytesIO(file.read())
    media = googleapiclient.http.MediaIoBaseUpload(file_stream, mimetype=file.content_type)

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # Make file publicly accessible
    permission = {"role": "reader", "type": "anyone"}
    service.permissions().create(fileId=uploaded_file["id"], body=permission).execute()

    # Return shareable link
    return f"https://drive.google.com/uc?id={uploaded_file['id']}&export=download"


# Example usage with Django file:
# from somewhere import uploaded_file
# link = upload_to_drive(uploaded_file, "example.pdf")
# print(link)
