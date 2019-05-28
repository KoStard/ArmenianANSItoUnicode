from threading import Thread
from functools import wraps


def as_daemon(f):
    """
    Decorator to call the function as a daemon thread
    """
    @wraps(f)
    def inner(*args, **kwargs):
        t = Thread(target=f, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    return inner
