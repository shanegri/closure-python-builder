import os, subprocess, json, re
from .DependencyBuilder import DependencyBuilder
from .lib import *


def loadConfig(root):
    config_path = root + "closure.json"
    if not os.path.exists(config_path):
        raise Exception("No config found")
    
    required_params = ["name", "common", "sources", "compiled"]
    with open(config_path, "r") as f:
        config = json.load(f)
        for i in required_params:
            if i not in config: raise Exception("Missing config param: " + i)

        def validateFolder(path):
            if not path.endswith("/"): path = path + "/"

            if not os.path.isdir(path):
                raise Exception("Invalid path: " + path)

            return path

        
        configPages = []

        for page in config['sources']:
            configPages.append(page)

        # config[  'modules'  ] = validateFolder(root + config[  'modules'  ])
        config['common']   = validateFolder(root + config['common'])
        config['sources']  = configPages
        config['compiled'] = validateFolder(root + config['compiled'])

        if 'compiler' not in config:
            config['compiler'] = "compiler8"

        global compiler_name
        compiler_name = config['compiler']

        return config

