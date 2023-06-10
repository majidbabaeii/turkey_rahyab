import environ

# https://django-environ.readthedocs.io/en/latest/tips.html
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str, "debug"),
    ALLOWED_HOSTS=(list, []),
)

env.read_env(".env")
