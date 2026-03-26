"""
levels : 
        debug
        info
        warning
        error
        fatal

    whichever is in basic config , it logs only down levels ;
        ex. basicconfig - error , logs only - error,fatal
            basicconfig - warning , logs only - warning, error,fatal

"""

import logging

# logging.basicConfig(level=logging.WARNING, filename="neww.log")

# logging.debug("user logging")
# logging.info("user clicked login button")
# logging.warning("user enterd wrong password")
# logging.error("user credinitial are invalid")
# logging.fatal("system crashed")


logger = logging.getLogger("mytestlogger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(message)s]')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

fh = logging.FileHandler("Pages/custom_log.log")
fh.setFormatter(formatter)

logger.addHandler(fh)

logger.info("user logged in")
logger.warning("user enterd wrong password")
logger.error("user is invalid")
 