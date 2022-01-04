import json
import pathlib
import os
import sys
import yaml
import requests
from slugify import slugify
from dotenv import load_dotenv

load_dotenv()

BASE_CADDY_CONFIG = {
    "apps": {"http": {"servers": {"local": {"listen": [":80"], "routes": []}}}}
}

BASE_COMPOSE_CONFIG = {
    "version": "3",
    "services": {
        "proxy": {
            "image": "nginx:alpine",
            "volumes": ["./nginx:/etc/nginx/templates"],
            "ports": ["9092:80"],
            "depends_on": ["prism"],
            "environment": [
                "PRISM_HOST=prism",
                "PRISM_PORT=4010",
            ],
        },
        "prism": {
            "image": "stoplight/prism:4",
            "volumes": ["./prism/:/tmp/:ro"],
        },
    },
}


def get_container_name(slug):
    return f"prism_{slug}"


def generate_docker_compose_yaml(slug):
    cmd = f"mock -p 4010 -h 0.0.0.0 /tmp/{slug}.yaml"
    base_compose = BASE_COMPOSE_CONFIG.copy()
    base_compose["services"]["prism"]["command"] = cmd
    return base_compose


def get_auth_header():
    token = os.environ.get("DOCS_AUTH_TOKEN", None)
    return {"Authorization": f"Token {token}"}


def get_spec(spec_id):
    base_url = os.environ.get("DOCS_BASE_URL", None)
    headers = get_auth_header()
    response = requests.get(
        f"{base_url}/api/openapis/{spec_id}", params={"format": "json"}, headers=headers
    )
    doc = response.json()
    doc["slug"] = slugify((doc["title"] or spec_id))
    return doc


def save_spec(spec, output_dir='prism'):
    oas_spec = spec["formatted"]
    slug = spec["slug"]
    output_path = pathlib.Path(f"./{output_dir}/{slug}.yaml")
    with open(output_path, "w+") as f:
        yaml.dump(oas_spec, f)
    return f"{slug}.yaml"


def write_compose_yaml(slug):
    config = generate_docker_compose_yaml(slug)
    with open("docker-compose.yaml", "w+") as f:
        yaml.dump(config, f)


if __name__ == "__main__":
    spec_id = sys.argv[1]
    spec = get_spec(spec_id)
    if spec:
        save_spec(spec)
        write_compose_yaml(spec["slug"])
        print("Done!!")
    else:
        print("Error!! No spec found")
