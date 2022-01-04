import os
from dotenv import load_dotenv

load_dotenv()

import docker
import settings
from api import get_spec, save_spec

client = docker.from_env()

#PRISM_IMAGE_NAME = 'myop/mockdock'
PRISM_IMAGE_NAME = 'stoplight/prism:4'

def get_container():
    try:
        return client.containers.get("prism")
    except docker.errors.NotFound:
        return None

def kill_container():
    container = get_container()
    if container:
        container.remove(v=True, force=True)

def run_prism():
    if is_mock_running():
        kill_container()

    spec = get_spec(settings.DOCS_ID)
    output_filepath = save_spec(spec)
    cmd = f"mock -p 4010 -h 0.0.0.0 /tmp/{output_filepath}"
    prism_vol_path = os.path.join(os.getcwd(), "prism")
#    environment=[f"DOCS_BASE_URL={settings.DOCS_BASE_URL}", f"DOCS_ID={settings.DOCS_ID}", f"DOCS_AUTH_TOKEN={settings.DOCS_AUTH_TOKEN}"]
    prism = client.containers.run(
             PRISM_IMAGE_NAME,
             command=cmd,
             name="prism",
             ports={4010:9092},
             detach=True,
             volumes={
                 prism_vol_path : {'bind': '/tmp', 'mode': 'ro'}
             }
    )
    return prism

def is_mock_running():
    return get_container() is not None

if __name__ == "__main__":
    container = run_prism()
    print(container)
