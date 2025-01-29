import yaml

def load_site_config(domain):
    with open("config/sites.yaml") as f:
        config = yaml.safe_load(f)
    return config.get(domain, {})