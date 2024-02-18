import logging

def log_info():
    logging.basicConfig(level=logging.INFO, filename='logging_info.log',
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                        datefmt="%d/%m/%Y %I:%M:%S", encoding = 'utf-8', filemode='a')