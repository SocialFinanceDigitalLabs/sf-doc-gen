class NumberContext:
    def __init__(self) -> None:
        self.__levels = []

    def reset(self):
        self.__levels = []

    def get_level(self, level_number: int) -> str:
        while len(self.__levels) < level_number:
            self.__levels.append(0)
        self.__levels = self.__levels[:level_number]
        self.__levels[level_number - 1] += 1
        return ".".join([str(x) for x in self.__levels]) + "."
