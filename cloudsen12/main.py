import pathlib
import pickle

import gdown
import pystac


def metadata() -> pystac.collection.Collection:
    """Get the metadata of cloudSEN12 as a STAC collection.

    Returns:
        pystac.collection.Collection: The metadata of cloudSEN12 as a STAC collection.
    """

    # Check if the cloudsen12 stac collection exists
    stac_collection_path = pathlib.Path(get_stac_path())
    stac_file = stac_collection_path / "cloudsen12_stac.pkl"

    if not stac_file.exists():
        # Download the pickle file
        url = "https://drive.google.com/uc?id=1ifoD-eRZ6uj7xvLeGqg1ofgJgwNay6AM"
        gdown.download(url, stac_file.as_posix(), quiet=False)

    # Read the pickle file
    with open(stac_file, "rb") as f:
        stac_collection = pickle.load(f)

    return stac_collection


def get_stac_path():
    """ Get the path to the cloud detection models."""

    # Path to save the models
    cred_path = pathlib.Path(
        "~/.config/cloudsen12/",
    ).expanduser()

    # create the folder if it does not exist
    if not cred_path.is_dir():
        cred_path.mkdir(parents=True, exist_ok=True)

    return cred_path.as_posix()
