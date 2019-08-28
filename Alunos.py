import re

ORIGINAL_FILE = "C:\\Users\\user\\Documents\\Ciência dos Dados\\Trabalho 01\\0 - Dados originais\\Base de Alunos1.csv"
STANDARDIZED_FILE = "C:\\Users\\user\\Documents\\Ciência dos Dados\\Trabalho 01\\1 - Padronização\\Alunos.csv"

REGEX_SEPARATOR = ";"
REGEX = r'(\d{1,2})-(\d{1,2})-(\d{4})'

indexDate = 5


def get_row_formatted(row, index, regex):
    array = row.split(REGEX_SEPARATOR)
    target = ""
    match = re.match(regex, array[index])

    if match is None:
        return row

    for i in reversed(range(1, len(match.groups()) + 1)):

        if i == 3 and len(match.group(i)) < 4:
            target += match.group(i).rjust(4, "0")
        elif (i == 1 or i == 2) and len(match.group(i)) < 2:
            target += match.group(i).rjust(2, "0")
        else:
            target += match.group(i)

    if len(target) > 0:
        array[index] = target

    return ";".join(array)


with open(STANDARDIZED_FILE, mode='w') as fileNovoAlunos:

    with open(ORIGINAL_FILE, mode='r') as fileAlunos:
        for line in fileAlunos.readlines():
            fileNovoAlunos.write(get_row_formatted(line, indexDate, REGEX))
