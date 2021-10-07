from pathlib import Path
from typing import Dict

from dotenv import dotenv_values

from clima import utils


def get_env(_schema) -> Dict:
    """Load values found in _schema from .env file"""
    verbose: bool = utils.chain_get(
        (getattr, _schema, 'debug', None),
        (getattr, _schema, 'verbose', None),
    ) is not None

    cwd = utils.chain_get(
        (getattr, _schema, 'cwd', None),
        tuple([Path.cwd]),
    )

    env_file = Path(cwd) / '.env'
    env_dict = dotenv_values(stream=env_file)

    return utils.filter_fields(env_dict, _schema)
