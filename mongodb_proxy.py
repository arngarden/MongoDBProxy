
import time
import pymongo

def get_methods(obj):
    attrs = (attr for attr in dir(obj))
    attrs = (attr for attr in attrs if not attr.startswith('_'))
    return set([attr for attr in attrs if hasattr(getattr(obj, attr), '__call__')])

EXECUTABLE_MONGO_METHODS = get_methods(pymongo.collection.Collection)
EXECUTABLE_MONGO_METHODS.update(get_methods(pymongo.Connection))
EXECUTABLE_MONGO_METHODS.update(get_methods(pymongo))


def safe_mongocall(call):
    """ Decorator for automatic handling of AutoReconnect-exceptions.
    """

    def _safe_mongocall(*args, **kwargs):
        for i in xrange(4):
            try:
                return call(*args, **kwargs)
            except pymongo.errors.AutoReconnect:
                print 'AutoReconnecting, try %d' % i
                time.sleep(pow(2, i))
        # Try one more time, but this time, if it fails, let the
        # exception bubble up to the caller.
        return call(*args, **kwargs)
    return _safe_mongocall


class Executable:
    """ Wrap a MongoDB-method and handle AutoReconnect-exceptions
    using the safe_mongocall decorator.
    """

    def __init__(self, method):
        self.method = method

    @safe_mongocall
    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    def __dir__(self):
        return dir(self.method)

    def __str__(self):
        return self.method.__str__()

    def __repr__(self):
        return self.method.__repr__()

class MongoProxy:
    """ Proxy for MongoDB connection.
    Methods that are executable, i.e find, insert etc, get wrapped in an
    Executable-instance that handles AutoReconnect-exceptions transparently.

    """
    def __init__(self, conn):
        """ conn is an ordinary MongoDB-connection.
        
        """
        self.conn = conn
       
    def __getitem__(self, key):
        """ Create and return proxy around the method in the connection
        named "key".
        
        """
        item = self.conn[key]
        if hasattr(item, '__call__'):
            return MongoProxy(item)
        return item

    def __getattr__(self, key):
        """ If key is the name of an executable method in the MongoDB connection,
        for instance find or insert, wrap this method in Executable-class that
        handles AutoReconnect-Exception.

        """
        
        attr = getattr(self.conn, key)
        if hasattr(attr, '__call__') and key in EXECUTABLE_MONGO_METHODS:
            return Executable(attr)
        return attr

    def __call__(self, *args, **kwargs):
        return self.conn(*args, **kwargs)

    def __dir__(self):
        return dir(self.conn)

    def __str__(self):
        return self.conn.__str__()

    def __repr__(self):
        return self.conn.__repr__()

    def __nonzero__(self):
        return True
