import pathlib
import yaml
BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = 'config' + '/' + 'aio.yaml'

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 160


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)
