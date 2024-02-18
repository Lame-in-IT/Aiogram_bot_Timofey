from  environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    dbuser: str
    dbpassword: str
    dbdatabase: str
    dbhost: str
    dbport: int

@dataclass
class Settings:
    bots: Bots

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN_BOT"),
            admin_id=env.int("ADMIN_ID"),
            dbuser=env.str("DBUSER"),
            dbpassword=env.str("DBPASSWORD"),
            dbdatabase=env.str("DBDATABASE"),
            dbhost=env.str("DBHOST"),
            dbport=env.int("DBPORT")
        )
    )

settings = get_settings(".env")