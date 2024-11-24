import configparser

# data types
_str = lambda x: x
_int = lambda x: int(x)
_bool = lambda x: x == "YES"
_dir = lambda x: x.removesuffix("/")


def read():
    path = __file__.removesuffix("config.py") + "xread.conf"
    cf = configparser.ConfigParser()
    cf.read(path)

    config = {
        "server/host": _str(cf.get("server", "host")),
        "server/port": _int(cf.get("server", "port")),
        "server/debug": _bool(cf.get("server", "debug")),

        "data/dir": _dir(cf.get("data", "data_dir")),
        
    }

    return config
