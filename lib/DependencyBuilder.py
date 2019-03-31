import re, os

class DependencyBuilder:

    def __init__(self, src):
        self.edit_date = os.path.getmtime(src)
        self.src = os.path.abspath(src)
        self.src_raw = src
        self.dependencies = []
        self._build(self.src)

    def _build(self, file):
        
        dList = self._dependencyList(file)
        
        for d in dList:
            if d in self.dependencies or d == self.src:
                continue

            edit_date = os.path.getmtime(d)
            if edit_date > self.edit_date:
                self.edit_date = edit_date

            self.dependencies.append(d)
            self._build(d)

        return ""

    def _dependencyList(self, file):
        retVal = []
        dir_path = os.path.dirname(os.path.realpath(file)) + "/"

        # Node style imports
        reImport = re.compile("(import(.*)from(.*)(\"|')(.*)(\"|');?)") 
        
        with open(file) as f:
            for line in iter(f):
                matches = re.match(reImport, line)
                if matches:
                    path = os.path.realpath(dir_path + matches.group(5))
                    retVal.append(path)

        return retVal


    def editDate(self):
        return (self.src, self.edit_date)


    def __str__(self):
            return self.src
