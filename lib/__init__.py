import os, subprocess, json

cpb_name =  __file__.replace("/lib/__init__.py", "")

def transpilePage(moduleDir, pageDir, destPath):
    print("Bundling " + pageDir + " -> " + destPath)
    
    cmdList = [
        "java -jar "+cpb_name+"/compilers/compiler.jar ",
        "-O SIMPLE ",
        "-W QUIET ",
        "--dependency_mode STRICT ",
        "--entry_point=" + pageDir + "index.js ",
        "--js_module_root "+os.path.commonprefix([moduleDir, pageDir])+" ",
        "--module_resolution NODE ",
        "--language_in ECMASCRIPT6 ",
        "--language_out ECMASCRIPT5_STRICT ",
        "--js=" + moduleDir + "**.js ",
        "--js=" +  pageDir  + "**.js ",
        "--js_output_file='" + destPath + "'",
    ]

    result = subprocess.call("".join(cmdList).split(" "))

    print("Success" if result == 0 else "Failure")
    print("")


def loadConfig(root):
    config_path = root + "closure.json"
    if not os.path.exists(config_path):
        raise Exception("No config found")
    
    required_params = ["name", "modules", "pages", "destination"]
    with open(config_path, "r") as f:
        config = json.load(f)
        for i in required_params:
            if i not in config: raise Exception("Missing config param: " + i)

        def validateFolder(path):
            if not path.endswith("/"): path = path + "/"

            if not os.path.isdir(path):
                raise Exception("Invalid path: " + path)

            return path

        config[  'modules'  ] = validateFolder(root + config[  'modules'  ])
        config[   'pages'   ] = validateFolder(root + config[   'pages'   ])
        config['destination'] = validateFolder(root + config['destination'])

        return config


'''
Return map in this format:
modules -> most recent edit date
pages ->
        page1 -> most recent edit date
        page2 -> most recent edit date
'''
def findEditDates(modules, pages):
    date_map = {}
    date_map['modules'] = findFolderEditDate(modules)
    pages_map = {}
    pages_path = os.listdir(pages)
    for i in pages_path:
        pages_map[i] = findFolderEditDate(pages + i + "/")

    date_map['pages'] = pages_map

    return date_map

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

def storeEditDates(edit_dates, name):
    with open(cpb_name+"/date_cache/" + name + ".json", "w") as f:
        json.dump(edit_dates, f)


def loadEditDates(name):
    with open(cpb_name+"/date_cache/" + name + ".json", "r") as f:
        return json.load(f)


'''
Return array of pages that need to be transpiled
'''
def pagesToTranspile(old_edit_dates, new_edit_dates, pages):
    pages = os.listdir(pages)
    if new_edit_dates['modules'] > old_edit_dates['modules']:
        return pages
    
    pages_to_compile = []
    for i in pages:
        if i in new_edit_dates['pages'] and i in old_edit_dates['pages'] :
            if new_edit_dates['pages'][i] > old_edit_dates['pages'][i]:
                pages_to_compile.append(i)
        else:
            pages_to_compile.append(i)

    return pages_to_compile