import re
import datetime

NEIGHBORHOOD_FILE = "C:\\Users\\user\\Documents\\Ciência dos Dados\\Trabalho 01\\0 - Dados originais\\Bairros.csv"
ORIGINAL_FILE = "C:\\Users\\user\\Documents\\Ciência dos Dados\\Trabalho 01\\0 - Dados originais\\Base de Alunos1.csv"
STANDARDIZED_FILE = "C:\\Users\\user\\Documents\\Ciência dos Dados\\Trabalho 01\\1 - Padronização e Higienização\\Alunos.csv"

REGEX_SEPARATOR = ";"
REGEX_DATE = r'(\d{1,2})-(\d{1,2})-(\d{4})'

indexDate = 5
indexNeighborhoods = 6

countLinesNeighborhoods = 0
countLinesOriginal = 0


def calculate_age(birth_date):
    today = datetime.date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def distanceJaroWinkler(first, second):
    """
    Função Jaro-Winkler que calcula a distância de semelhança entre duas strings, quanto maior a distância maior a
    similaridade

    :param first: primeira string a ser comparada
    :param second: segunda string a ser comparada
    :return: medida de similaridade
    """

    first_len = len(first)
    second_len = len(second)

    if first_len == 0 and second_len == 0:
        return 1

    match_distance = (max(first_len, second_len) // 2) - 1

    first_matches = [False] * first_len
    second_matches = [False] * second_len

    matches = 0
    transpositions = 0

    for i in range(first_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, second_len)

        for j in range(start, end):
            if second_matches[j]:
                continue
            if first[i] != second[j]:
                continue
            first_matches[i] = True
            second_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0

    k = 0

    for i in range(first_len):
        if not first_matches[i]:
            continue
        while not second_matches[k]:
            k += 1
        if first[i] != second[k]:
            transpositions += 1
        k += 1

    return ((matches / first_len) + (matches / second_len) + ((matches - transpositions / 2) / matches)) / 3


def get_row_formatted_by_date(row, index, regex):
    """
    Função para formatar a data de uma linha a partir de um certo regex

    :param row: linha em formato de array a ser formatada
    :param index: index posicao do array que sera formatado
    :param regex: regex que dirá como sera a formatacao
    :return: linha formatada com a data correta
    """

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
        header = fileAlunos.readline().rstrip('\n')
        fileNovoAlunos.write(header + REGEX_SEPARATOR + "Score Bairro" + REGEX_SEPARATOR + "Idade" + '\n')

        for aluno in fileAlunos.read().splitlines():
            arr = aluno.split(REGEX_SEPARATOR)
            newLine = aluno
            score = -1
            matchingNeighborhood = ""

            with open(NEIGHBORHOOD_FILE, mode='r') as fileBairros:
                fileBairros.readline()

                for bairro in fileBairros.read().splitlines():
                    distance = distanceJaroWinkler(bairro, arr[indexNeighborhoods])

                    if distance > score:
                        score = distance
                        matchingNeighborhood = bairro

            # HIGIENIZANDO BAIRROS
            # Mostra as colunas: Bairro | Score Bairro
            arr[indexNeighborhoods] = matchingNeighborhood
            newLine = ";".join(arr)
            newLine = newLine + REGEX_SEPARATOR + str(score)

            # PADRONIZANDO DATA
            newLine = get_row_formatted_by_date(newLine, indexDate, REGEX_DATE)

            # HIGIENIZANDO AS DATAS DE NASCIMENTO
            try:
                age = calculate_age(datetime.datetime.strptime(newLine.split(REGEX_SEPARATOR)[indexDate], '%Y%m%d'))
            except ValueError:
                age = 0

            # Removendo todas as idades (e datas) negativas e maiores que 150
            # TODO: verificar com professor como escolher a maior idade possível para a tabela de alunos
            if 0 < age < 150:
                newLine += REGEX_SEPARATOR + str(age)
            else:
                newArr = newLine.split(REGEX_SEPARATOR)
                newArr[indexDate] = ""
                newLine = ";".join(newArr)

            fileNovoAlunos.write(newLine + '\n')