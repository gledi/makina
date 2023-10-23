from .base import *
from .base import INSTALLED_APPS, MIDDLEWARE, env

INSTALLED_APPS.extend(["debug_toolbar", "django_extensions"])
MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]
if env.bool("RUNNING_IN_DOCKER", default=False):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip for ip in ips if ":" not in ip]
    del ips
    del hostname
