import services.arangoManager as arangoManager
import config.init_config as config


def init():
    # Init config file
    config.init_config()

    # Init database
    arangoManager.setup()
