import yaml
from yaml.loader import SafeLoader


def get_app_version():
    # Read the version from the API YAML file
    try:
        with open("api.yaml") as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data["info"]["version"]
    except Exception as e:
        print(e)
        return "?.?.?"


# Clean text
def clean_text(text):
    # Remove "/" and "\" from the text
    text = text.replace("/", "")
    text = text.replace("/", "")

    # Remove spaces
    text = text.replace(" ", "_")

    return text
