from getScores import getScores
from makeJson import generateJSON

if __name__ == '__main__':
    for grade in range(1, 5):
        generateJSON(grade, getScores(grade))
