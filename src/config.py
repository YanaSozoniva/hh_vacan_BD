from configparser import ConfigParser


def config(filename="../hh_vacan_BD/src/database.ini", section="postgresql"):
    """Функция чтения конфигурации базы данных из заданного файла"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db
