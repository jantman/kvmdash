"""
Methods to load the storage api classes.

Storage API classes must live in a module
named the lower-case class name.

See filestorage.py for methods.
"""

def get_storage_api(classname):
    """
    Returns a reference to the storage API
    class specified by classname.
    """
    modname = "kvmdash.%s" % classname.lower()
    try:
        import importlib
        i = importlib.import_module(modname)
    except:
        i = __import__(modname, fromlist=[''])

    cls = getattr(i, classname)
    return cls
