import logging

def setup_logging(log_file_path):
    logger = logging.getLogger('my_logger')

    # Check if the logger already has handlers to avoid duplicates
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Create handlers for file and console logging
        file_handler = logging.FileHandler(log_file_path)
        console_handler = logging.StreamHandler()

        # Set levels for the handlers
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

        # Define log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
