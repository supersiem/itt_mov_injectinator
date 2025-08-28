import os


class Document:
    def __init__(self, file=None):
        if file:
            self.document = file
            self.set_doc(file)
        else:
            self.document = ""

    def getlength(self):
        file = self.document
        file_path = file

        with open(file_path, "r") as f:
            num_lines = 0
            for line in f:
                num_lines += 1

        return num_lines

    def read_full(self):
        file = self.document
        openfile = open(file)
        re = openfile.read()
        openfile.close()
        return re

    def read_line(self, num):
        file = self.document
        with open(file, "r") as openfile:
            lines = openfile.readlines()
            if 1 <= num <= len(lines):
                return lines[num - 1]
            else:
                return None

    def write_to_line(self, line, input):
        # krijg de lengte van het bestand
        file = self.document
        file_lengt = self.getlength()
        file_line = line - 1

        # maak lijst klaar
        list = []
        # maak back up
        loop = 1
        # backup = ""
        while loop <= file_lengt:
            # voeg line toe aan lijst
            list.append(self.read_line(loop))
            # backup = backup + get(loop, file)
            # volgende line
            loop += 1
        # over wite de line van de list
        if len(list) == 0:
            list.append("")
        if 1 == 1:
            list[file_line] = input + "\n"
        else:
            list[file_line] = input
        ##print(list)
        list2 = []
        loop = 0
        while loop != len(list):
            if loop == file_line:
                list2.append(input + "\n")
            else:
                list2.append(list[loop])
            loop += 1
        loop = 0
        out = ""
        while loop != len(list2):
            out += list2[loop]
            loop += 1
        f = open(file, "w")
        f.write(out)
        f.close()

    def overwrite(self, data):
        f = open(self.document, "w")
        f.write(data)
        f.close()
        return data

    def append(self, data):
        f = open(self.document, "a")
        f.write(data)
        f.close()
        return data

    def set_doc(self, file):
        self.document = file
        if os.path.exists(self.document):
            return
        else:
            self.document = ""
            return 404

    def make(self, name):
        if not os.path.exists(name):
            open(name, "x")
        self.set_doc(name)

    def delete(self):
        if os.path.exists(self.document):
            return os.remove(self.document)
        else:
            raise FileNotFoundError(f"The file {self.document} does not exist.")
