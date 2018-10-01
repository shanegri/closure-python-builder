# [closure-python-builder](https://github.com/shanegri/closure-python-builder)

*-work in progress-*


This script is a wrapper for Google's JavaScript [Closure Compiler](https://github.com/google/closure-compiler) that allows for easy set up and configuration. Closure-python-builder saves time by only compiling the files that have changed since the last compilation. This script was tested and developed with Python 2.7.

Version 20180910 of the closure compiler is included in this repository. Newer versions can be downloaded from [here](https://github.com/google/closure-compiler/wiki/Binary-Downloads).


## Usage

Clone the script into your app directory.

```shell
$ git clone git://github.com/shanegri/closure-python-builder
```

The folder structure for this example looks like this:
```
├── app
│   ├── closure-python-builder/
│   ├── resources/
|   |   ├─js/
|   |    ├─js-src/
|   |     ├─modules/
|   |        ├─module1.js
|   |     ├─pages/
|   |       ├─home/
|   |          ├─index.js
|   |       ├─about/
|   |          ├─index.js
```

Each page must contain an index.js file. This is the entry point for each page. All other JS files and modules will be imported into index.js. Modules can consist of a single file or a folder with sub folders.

Inside of your project directory, create a closure.json file. This tells closure-python-builder where the src files are and where to build.

```JSON
{
    "name": "closure-testing",

    "modules" : "resources/js-src/modules/",

    "pages" : "resources/js-src/pages/",

    "destination": "resources/js/"

}
```

You can now run the compiler:

```SHELL
$ python closure-python-builder 
```

After compilation, each page becomes a single compressed file. The resources/js folder now contains home.js and about.js.

If you cloned closure-python-builder outside of the app directory, you can use the --path command to specify the app location.

```SHELL
$ python closure-python-builder -p <path to app>
```

## Reference

Comamnd line arguments

| Command       |   | Info  |
| ------------- |:----------:| -----:|
| -h            | --help     | Display all cli options |
| -p   \<VAL>   | --path     | Sets project directory path. Default is './' (Current directory) |
| -a            | --all      | Ignore file modification date and compile all pages |

- [Closure compiler wiki](https://github.com/google/closure-compiler/wiki)
- [Closure compiler website](https://developers.google.com/closure/compiler/)

## Possible Future Additions

- Integration with closure-stylesheets compiler 
- Watch mode, i.e. automatically recompile on file changes