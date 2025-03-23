from dataclasses import dataclass
from environs import Env
from sqlalchemy.engine.url import URL


@dataclass
class DatabaseConfig:
    url: URL


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    admin_password: str


@dataclass
class RedisConfig:
    """Redis configuration."""
    host: str
    port: int
    user: str
    password: str
    bot_database: int
    middleware_database: int


@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig


def load_config(path: str | None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(bot=TgBot(token=env('BOT_TOKEN'),
                            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
                            admin_password=env('ADMIN_PASSWORD')),
                  db=DatabaseConfig(url=URL.create(
                                        drivername='postgresql+asyncpg',
                                        host=env('DB_HOST'),
                                        port=env('DB_PORT'),
                                        username=env('DB_USER'),
                                        password=env('DB_PASSWORD'),
                                        database=env('DATABASE')
                                    )),
                  redis=RedisConfig(host=env('REDIS_HOST'),
                                    port=env('REDIS_PORT'),
                                    user=env('REDIS_USER'),
                                    password=env('REDIS_PASSWORD'),
                                    bot_database=int(env('REDIS_BOT_DATABASE')),
                                    middleware_database=int(env('REDIS_MIDDLEWARE_DATABASE'))))
