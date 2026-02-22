from utils.logger import logger

def lof_function(func):
    def wrapper(*args,**kwargs):
        logger.info(f"Executing {func.__name__}")
        return func(*args,**kwargs)
    return wrapper
