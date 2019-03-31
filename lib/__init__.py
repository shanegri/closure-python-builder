import os, subprocess, json, re
from .DependencyBuilder import DependencyBuilder

cpb_name =  re.sub("/lib/__init__.pyc?", "", __file__)
compiler_name = "compiler7"

def transpilePage( entryFile, dependecies, destFile ):
    print("Using " + compiler_name + ".jar")
    print("Bundling " + entryFile + " -> " + destFile)

    dependecies.append(entryFile)

    common = os.path.commonprefix(dependecies)

    cmdList = [
        "java -jar "+cpb_name+"/compilers/"+compiler_name+".jar ",
        "-O SIMPLE ",
        "-W DEFAULT ",
        "--dependency_mode STRICT ",
        "--entry_point='" + entryFile + "' ",
        "--js_module_root "+common+" ",
        "--module_resolution NODE ",
        "--language_in ECMASCRIPT6 ",
        "--language_out ECMASCRIPT5_STRICT ",
        "--js_output_file='" + destFile + "' ",
    ]

    for f in dependecies:
        cmdList.append("--js '" + f + "' ")

    result = subprocess.call("".join(cmdList), shell=True)

    print("Success" if result == 0 else "Failure")
    print("")


def loadConfig(root):
    config_path = root + "closure.json"
    if not os.path.exists(config_path):
        raise Exception("No config found")
    
    required_params = ["name", "common", "pages", "destination"]
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

        for page in config['pages']:
            configPages.append(page)

        # config[  'modules'  ] = validateFolder(root + config[  'modules'  ])
        config[   'common'  ] = validateFolder(root + config['common'])
        config[   'pages'   ] = configPages
        config['destination'] = validateFolder(root + config['destination'])

        if 'java-version' not in config:
            config['java-version'] = 8 
        elif config['java-version'] != 7 and config['java-version'] != 8:
            print("Invalid java-version given, setting to 8")
            config['java-version'] = 8 

        global compiler_name
        compiler_name = "compiler" + str(config['java-version'])

        return config

def storeEditDates(pages, name):
    edit_dates = {}
    for page in pages:
        edit_dates[page.src] = page.edit_date

    with open(cpb_name+"/date_cache/" + name + ".json", "w") as f:
        json.dump(edit_dates, f)

def findFolderEditDate(folder):
    contents = os.listdir(folder)
    max_date = 0
    for i in contents:
        path = folder + i
        i_date = 0
        if os.path.isdir(path):
            i_date = findFolderEditDate(path + "/")
        else:
            i_date = os.path.getmtime(folder + i)
        if i_date > max_date: max_date = i_date

    return max_date


def loadEditDates(name):
    with open(cpb_name+"/date_cache/" + name + ".json", "r") as f:
        return json.load(f)

def destinationName(page, destination, common):
    name_rel = page.src_raw.replace(common, "")
    name = name_rel.replace("/", "$")
    return os.path.abspath(destination) + "/" + name