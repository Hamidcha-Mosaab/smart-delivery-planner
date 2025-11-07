from loguru import logger
def setup_logger(debug=False):
    logger.remove()
    if debug:
        logger.add(lambda msg: print(msg, end=""))
    else:
        logger.add("logs/app.log", rotation="1 day", level="INFO")
