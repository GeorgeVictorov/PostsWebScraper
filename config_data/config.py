import logging
from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class ApiToken:
    token: str


@dataclass
class Config:
    api: ApiToken
    db: DatabaseConfig


def load_config(path: str = 'env/.env') -> Config:
    logging.basicConfig(filename='config.log', level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        env: Env = Env()
        env.read_env(path)

        config = Config(
            api=ApiToken(
                token=env('API_TOKEN')
            ),
            db=DatabaseConfig(
                database=env('DB_NAME'),
                db_host=env('DB_HOST'),
                db_user=env('DB_USER'),
                db_password=env('DB_PASSWORD')
            )
        )

        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise
