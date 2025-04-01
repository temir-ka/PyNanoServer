import importlib.util

class Config:
    def __init__(self):
        self._settings = {
            "HOST": "127.0.0.1",
            "PORT": 8080,
            "TEMPLATE_DIR": "templates",
            "STATIC_DIR": "static", 
            "LOG_LEVEL": "INFO",
            "DEBUG": True
        }

    def __getitem__(self, key):
        return self._settings[key]
    
    def __setitem__(self, key, value):
        self._settings[key] = value
    
    def __delitem__(self, key):
        del self._settings[key]
    
    def load_from_pyfile(self, path):
        spec = importlib.util.spec_from_file_location("config", path)

        if spec is None:
            raise FileNotFoundError(f"Could not find the config file: {path}")
        
        config = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(config)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not load the config file: {path}")
            
        config_dict = {k: v for k, v in vars(config).items() if not k.startswith("__")}
        self._settings.update(config_dict)