import logging


def setup_logging(lvl="INFO"):
    format_str = "%(asctime)s.%(msecs)d [%(levelname)s][%(threadName)s] %(name)s.%(funcName)s :: %(message)s"
    dt_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=format_str, datefmt=dt_format, level=lvl)
