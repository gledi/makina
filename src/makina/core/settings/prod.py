from .base import *
from .base import ALLOWED_HOSTS, env

RENDER_EXTERNAL_HOSTNAME = env.str("RENDER_EXTERNAL_HOSTNAME", default="")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
