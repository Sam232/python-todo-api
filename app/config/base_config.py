class BaseConfig:
    HOST = "127.0.0.1"
    PORT = 5000

    MONGODB_DB = "my_todo"
    MONGODB_HOST = "127.0.0.1"
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ""
    MONGODB_PASSWORD = ""

    LOGGING_FORMAT = "%(asctime) %(api_name) %(user) %(message)"
    DEBUG = False
