import getopt
import configparser


global test_config


def cfg():
    return test_config


def load_config(argv):
    opts, args = getopt.getopt(argv, "c:", ["config="])
    global test_config
    test_config = configparser.ConfigParser()
    test_config.sections()
    cfg_loaded = False
    for opt, arg in opts:
        if opt in ("-c", "--config"):
            test_config.read(arg)
            cfg_loaded = True

    if not cfg_loaded:
        test_config.read("jericho.cfg")