import os
from cachetools import TTLCache

if os.environ.get("DISABLE_CACHE"):
    print("DISABLE_CACHE=1. disabling cache")

    from functools import wraps

    def cached(cache):
        def true_decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped
        return true_decorator
else:
    print("Using cache")

    from cachetools import cached
    
