import os, subprocess, json, re

cpb_name =  re.sub("/lib/lib.pyc?", "", __file__)
compiler_name = "closure-compiler-v20190415.jar"

def transpilePage( entryFile, dependecies, destFile ):
    print("Using " + compiler_name )
    print("Bundling " + entryFile + " -> " + destFile)

    dependecies.append(entryFile)

    common = os.path.commonprefix(dependecies)
   
    cmdList = [
        "java -jar "+cpb_name+"/compilers/"+compiler_name+" ",
        "-O SIMPLE ",
        "-W DEFAULT ",
        "--dependency_mode STRICT ",
        "--js_module_root "+common+" ",
        "--module_resolution NODE ",
        "--language_in ECMASCRIPT6 ",
        "--language_out ECMASCRIPT5_STRICT ",
        "--js_output_file='" + destFile + "' ",
        "--entry_point='" + entryFile[len(common):] + "' ",
    ]

    for f in dependecies:
        cmdList.append("--js '" + f + "' ")

    result = subprocess.call("".join(cmdList), shell=True)

    print("Success" if result == 0 else "Failure")
    print("")

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