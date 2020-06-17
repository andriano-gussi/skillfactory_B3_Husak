from os import getcwd
class Tag:
    def __init__(self, tag, text="", is_single=False, is_line=False, klass=None, **kwargs):
        self.tag = tag
        self.text = text
        self.is_single = is_single # указать True, если не нужен закрывающий тэг
        self.is_line = is_line # указать True, если тэг вместе с его содержимым нужно вывести в одну строку
        self.attributes = {} # словарь атрибутов тэга
        self.structure = [] # список, в котором хранится построчно собственная структура тэга
        self.opening ="" # для хранения открывающего тэга
        self.internal = [] # для хранения содержимого тэга
        self.ending = "" # для хранения закрывающего тэга
        self.tab = "" # для табуляции строк

        # заполняем self.attributes всеми входящими атрибутами тэга:
        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

        self.make_structure()

    def string_of_attrs(self):
        """распаковывает все атрибуты, склеивает их пробелами и возвращает в виде одной строки"""
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        return attrs

    def make_structure(self):
        """формирует полную структуру тэга и записывает результат в поле self.structure"""
        if self.string_of_attrs():
            self.opening = "{tab}<{tag} {attrs}>".format(tab=self.tab, tag=self.tag, attrs=self.string_of_attrs())
        else:
            self.opening = "{tab}<{tag}>".format(tab=self.tab, tag=self.tag)
        
        if self.text != "":
            self.internal.append(self.text)
        self.ending = "{tab}</{tag}>".format(tab=self.tab, tag=self.tag)

        if self.is_line:
            self.structure.append(self.opening + self.text + self.ending)
        else:
            self.structure.append(self.opening)
            if self.internal:
                for line in self.internal:
                    self.structure.append(line)
            if not self.is_single:
                self.structure.append(self.ending)

    def __iadd__(self, other):
        """при добавлении другого объекта, меняет собственную структуру так, чтобы внутри оказался тот самый другой объект"""
        self.structure.clear()
        self.tab = "    "

        for line in other.structure:
            self.internal.append(self.tab * 2 + line)
        self.make_structure()
        return self

    def __str__(self):
        return "Ошибка! Распечатать можно только объект класса 'HTML')"

class HTML:
    """Главный класс, который создает html-документ из всех объектов класса Tag и выводит либо на экран, либо записывает в файл"""
    def __init__(self, output=None):
        self.output = output # чтобы вывести созданный документ в файл, необходимо указать output="имя.html"
        self.structure = []
        self.opening ="<html>"
        self.internal = []
        self.ending = "</html>"

    def make_structure(self):
        """упрощенная функция создания структуры документа"""
        self.structure.append(self.opening)
        if self.internal:
            for line in self.internal:
                self.structure.append(line)
        self.structure.append(self.ending)

    def __iadd__(self, other):
        """аналогична функции класса Tag"""
        self.structure.clear()

        for line in other.structure:
            self.internal.append(line)
        self.make_structure()
        return self

    def __str__(self):
        """при обращении к объекту, как к строке, выводит созданный документ либо в файл, либо на экран"""
        if self.output is not None:
            output = self.output.lower()
            with open(output, "w") as f:
                for line in self.structure:
                    f.write(line +"\n")
            return "Документ записан в {}\\{}".format(getcwd(), output)
        else:
            output = ""
            for line in self.structure:
                output += (line +"\n")
            return output                

if __name__ == "__main__":
    doc = HTML()

    head = Tag("head")
    title = Tag("title", "hello", is_line=True)
    head += title

    doc += head

    body = Tag("body")

    h1 = Tag("h1", "Test", is_line=True, klass=("main-text",))
    body += h1

    div = Tag("div", klass=("container", "container-fluid"), id="lead")
    paragraph = Tag("p", "another test", is_line=True)
    img = Tag("img", is_single=True, src="/icon.png", data_image="responsive")
    div += paragraph
    div += img
    body += div
  
    doc += body
    # вывод созданного документа:
    print(doc)
