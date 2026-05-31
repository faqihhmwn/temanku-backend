from google.cloud import storage
import uuid
import os

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def upload_image(file):

    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    filename = f"{uuid.uuid4()}_{file.filename}"

    blob = bucket.blob(filename)

    blob.upload_from_file(
        file.file,
        content_type=file.content_type
    )

    return (
        f"https://storage.googleapis.com/"
        f"{BUCKET_NAME}/{filename}"
    )


def delete_image(image_url):

    if not image_url:
        return

    try:
        filename = image_url.split("/")[-1]

        client = storage.Client()

        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob(filename)

        if blob.exists():
            blob.delete()

    except Exception as e:
        print(f"Failed to delete image: {e}")