import threading


class SingletonLogger:
    _instance = None
    _lock = threading.Lock() # Lock so that only one thread can access at a time

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None: # check for each thread that no class is initiated
                    # this is the single instance that will be created
                    cls._instance = super(SingletonLogger, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance # return the existing instance if already created

    def _initialize(self):
        self.log_file = "app.log"

    def log(self, message: str, module: str = "General"):
        formatted_message = f"[{module}] {message}"
        with open(self.log_file, "a") as f:
            f.write(formatted_message + "\n")