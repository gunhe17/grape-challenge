from abc import ABC, abstractmethod
import os


#########################
#
#    App Environment
#
#########################

def get_app_env() -> str:
    APP_ENV = os.getenv("APP_ENV", "")

    if APP_ENV == "":
        raise Exception("APP_ENV is not set")

    if APP_ENV not in ["dev", "prod"]:
        raise Exception("APP_ENV is not valid")

    return APP_ENV


###################################
## Database Configuration
###################################

class DatabaseConfig(ABC):
    @property
    @abstractmethod
    def POSTGRES_USER(self) -> str:
        pass

    @property
    @abstractmethod
    def POSTGRES_PASSWORD(self) -> str:
        pass

    @property
    @abstractmethod
    def POSTGRES_HOST(self) -> str:
        pass

    @property
    @abstractmethod
    def POSTGRES_PORT(self) -> str:
        pass

    @property
    @abstractmethod
    def POSTGRES_DB(self) -> str:
        pass

    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class DevDatabaseConfig(DatabaseConfig):
    @property
    def POSTGRES_USER(self) -> str:
        return os.getenv("POSTGRES_USER", "dev_user")

    @property
    def POSTGRES_PASSWORD(self) -> str:
        return os.getenv("POSTGRES_PASSWORD", "dev_password")

    @property
    def POSTGRES_HOST(self) -> str:
        return os.getenv("POSTGRES_HOST", "localhost")

    @property
    def POSTGRES_PORT(self) -> str:
        return os.getenv("POSTGRES_PORT", "5432")

    @property
    def POSTGRES_DB(self) -> str:
        return os.getenv("POSTGRES_DB", "grape_dev")


class ProdDatabaseConfig(DatabaseConfig):
    @property
    def POSTGRES_USER(self) -> str:
        return os.getenv("POSTGRES_USER", "user")

    @property
    def POSTGRES_PASSWORD(self) -> str:
        return os.getenv("POSTGRES_PASSWORD", "password")

    @property
    def POSTGRES_HOST(self) -> str:
        return os.getenv("POSTGRES_HOST", "localhost")

    @property
    def POSTGRES_PORT(self) -> str:
        return os.getenv("POSTGRES_PORT", "5432")

    @property
    def POSTGRES_DB(self) -> str:
        return os.getenv("POSTGRES_DB", "grape_dev")


def get_database_config() -> DatabaseConfig:
    APP_ENV = get_app_env()

    if APP_ENV == "dev":
        return DevDatabaseConfig()
    elif APP_ENV == "prod":
        return ProdDatabaseConfig()
    else:
        raise NotImplementedError(f"Unknown environment: {APP_ENV}")
