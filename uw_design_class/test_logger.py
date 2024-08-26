from uw_design_class.database_connection import logger as logger_db
from uw_design_class.main import logger as logger_main
from uw_design_class.singleton_logger import SingletonLogger

logger_test = SingletonLogger()

if __name__ == "__main__":
    bool_result = logger_main == logger_db == logger_test
    logger_test.log(f"All loggers are same instance: {bool_result}")

