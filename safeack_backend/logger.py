import logging


def create_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)

    # Set the logging level (you can set it to DEBUG, INFO, WARNING, ERROR, or CRITICAL)
    logger.setLevel(level)

    # Create a console handler and set the level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
