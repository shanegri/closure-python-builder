import argparse, os, lib


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='./', action='store', help='Project directory. Default is ./', metavar='')
    parser.add_argument('-a', '--all', action='store_true', help='Force compile all pages')

    args = parser.parse_args()

    project_path = args.path if args.path.endswith("/") else args.path + "/"

    config = lib.loadConfig(project_path) 

    name     = config[   'name'    ]
    pagesSrc = config[   'pages'   ]
    dest     = config['destination']

    pages = []

    # generate page date 
    for page in pagesSrc:
        pages.append( lib.DependencyBuilder(config['common'] + page) )

    #load old edit dates
    if os.path.exists( lib.cpb_name + "/date_cache/" + name + ".json" ):
        old_edit_dates = lib.loadEditDates(name)
    else:
        args.all = True

    #find pages to compile
    if args.all:
        pages_to_compile = pages
    else:
        pages_to_compile = list( filter(lambda p : p.edit_date > old_edit_dates[p.src], pages) )

    # compile necessary pages
    for page in pages_to_compile:
        destination = lib.destinationName(page, dest, config['common']) 
        lib.transpilePage( page.src, page.dependencies, destination )

    # store new edit dates
    lib.storeEditDates(pages, name)


if __name__ == "__main__":
    main()
