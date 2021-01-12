from django.http import HttpRequest
import environ
import os
from pathlib import Path


def constant_text(request):

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    env = environ.Env()
    env.read_env(os.path.join(BASE_DIR,'.env'))

    GOOGLE_API_KEY_URL = env('GOOGLE_SECRET_KEY_URL')

    return {
        'GOOGLE_API_KEY_URL': GOOGLE_API_KEY_URL,
    }
