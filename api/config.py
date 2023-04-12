from os import getenv
from dotenv import load_dotenv

load_dotenv()

ENV = getenv("ENV")

PROJECT_NAME = getenv("PROJECT_NAME")
DESCRIPTION = getenv("DESCRIPTION")
APP_PORT = getenv("APP_PORT")

CAPTCHA_LENGTH = int(getenv("CAPTCHA_LENGTH"))
RECAPTCHA_V3_SECRET_KEY = getenv("RECAPTCHA_V3_SECRET_KEY")
RECAPTCHA_V3_MINIMUM_SCORE = int(float(getenv("RECAPTCHA_V3_MINIMUM_SCORE")))

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")