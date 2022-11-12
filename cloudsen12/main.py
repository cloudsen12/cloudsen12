import pathlib
import dill
import gdown


def load(version="1.10"):
    """Get the metadata of cloudSEN12 as a STAC collection.

    Returns:
        pystac.collection.Collection: The metadata of cloudSEN12 as a STAC collection.
    """
    stac_collection_path = pathlib.Path(get_stac_path())

    # Check if the cloudsen12 stac collection exists
    if version == "1.00":
        stac_file = stac_collection_path / "cloudsen12_stac.pkl"

        if not stac_file.exists():
            # Download the pickle file
            url = "https://drive.google.com/uc?id=1D7o727NW445dXGfUuiuxCkK17mTXaDkC"
            gdown.download(url, stac_file.as_posix(), quiet=False)

        # Read the pickle file
        with open(stac_file, "rb") as f:
            stac_collection = dill.load(f)
    elif version == "1.10":
        stac_file = stac_collection_path / "cloudsen12_stac_beta1.pkl"
        if not stac_file.exists():
            # Download the pickle file
            url = "https://drive.google.com/uc?id=1iLBsWfLSYdpxrPUuVZYWkeqDxXOq3-Yi"
            
            gdown.download(url, stac_file.as_posix(), quiet=False)
    else:
        raise ValueError(f"Version {version} not available.")
    return stac_collection


def clean():
    """Clean the STAC collection saved in the local machine."""

    # Check if the cloudsen12 stac collection exists
    stac_collection_path = pathlib.Path(get_stac_path())
    stac_file1 = stac_collection_path / "cloudsen12_stac.pkl"
    stac_file2 = stac_collection_path / "cloudsen12_stac_beta1.pkl"

    if stac_file1.exists():
        stac_file1.unlink()
        print("CloudSEN12 STAC collection v1.0 deleted.")

    if stac_file2.exists():
        stac_file2.unlink()
        print("CloudSEN12 STAC collection v1.1 deleted.")

    return True


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
