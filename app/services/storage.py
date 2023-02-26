import os


def get_cloud_storage_credentials() -> dict:
    try:
        key = os.environ["API_KEY"]
        secret = os.environ["API_SECRET"]
        cloudName = os.environ["CLOUD_NAME"]

    except (ValueError, IndexError) as args:
        raise ValueError(args)

    else:
        return {
            "cloud_name": cloudName,
            "api_key": key,
            "api_secret": secret,
            "secure": True,
        }
