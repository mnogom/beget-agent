"""Logger agent."""

import sys
import logging


def get_logger(debug_mode):
    """Init logger configuration.

    :param debug_mode: activate debug output
    :return: logger
    """

    root = logging.getLogger()

    if debug_mode:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - "
                                  "[%(levelname)s] -  "
                                  "%(name)s - "
                                  "(%(filename)s)."
                                  "%(funcName)s"
                                  "(%(lineno)d) - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return root
