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
    env: Env = Env()
    env.read_env(path)

    return Config(
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
