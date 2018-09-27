import subprocess, os, lib

#TODO: Command line parsing

config = lib.loadConfig("dev/") #TODO: config validation

name = config['name']
modules = "dev/" + config['modules']
pages   = "dev/" + config['pages']
dest    = "dev/" + config['destination']

#load old edit dates
if not os.path.exists("builder/date_cache/" + name + ".json"):
    old_edit_dates = lib.findEditDates(modules, pages)
else:
    old_edit_dates = lib.loadEditDates(name)

#find new edit dates
new_edit_dates = lib.findEditDates(modules, pages)

#find pages to compile
pages_to_compile = lib.pagesToTranspile(old_edit_dates, new_edit_dates, pages)

#compile necessary pages
for i in pages_to_compile:
    lib.transpilePage(modules, pages + i + "/", dest + i + ".js")

#store new edit dates
lib.storeEditDates(new_edit_dates, name)

