import argparse, os, lib

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='./', action='store', help='Project directory. Default is ./', metavar='')
    parser.add_argument('-a', '--all', action='store_true', help='Force compile all pages')

    args = parser.parse_args()

    project_path = args.path if args.path.endswith("/") else args.path + "/"

    config = lib.loadConfig(project_path) 

    name    = config[   'name'    ]
    modules = config[  'modules'  ]
    pages   = config[   'pages'   ]
    dest    = config['destination']

    #load old edit dates
    if not os.path.exists("builder/date_cache/" + name + ".json"):
        old_edit_dates = lib.findEditDates(modules, pages)
    else:
        old_edit_dates = lib.loadEditDates(name)

    #find new edit dates
    new_edit_dates = lib.findEditDates(modules, pages)

    #find pages to compile
    if args.all:
        pages_to_compile = os.listdir(pages)
    else:
        pages_to_compile = lib.pagesToTranspile(old_edit_dates, new_edit_dates, pages)

    #compile necessary pages
    for i in pages_to_compile:
        lib.transpilePage(modules, pages + i + "/", dest + i + ".js")

    #store new edit dates
    lib.storeEditDates(new_edit_dates, name)


if __name__ == "__main__":
    main()
