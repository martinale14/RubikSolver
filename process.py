import cv2
import matplotlib.pyplot as plt
from rubik_solver import utils
from ursina import *


def imageProcesing():
    cv2.imshow("instructions", cv2.imread('./instruction.png'))

    defaultColors = [
        [208, 218, 210, 'w'],
        [208, 23, 29, 'r'],
        [225, 204, 15, 'y'],
        [6, 130, 192, 'b'],
        [36, 204, 17, 'g'],
        [255, 104, 29, 'o']
    ]

    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    print(frame.shape)
    posX = int(frame.shape[1] / 2)
    posY = int(frame.shape[0] / 2)
    print(posX, posY)
    centered = frame[posY - 101:posY + 101, posX - 101:posX + 101]
    faces = []
    faceColors = []
    cube = ''
    while len(faces) < 6:
        _, frame = cap.read()
        myColors = []
        rectangles = []
        n = int(centered.shape[1] / 3)
        size = 20

        for i in range(0, 3):
            for j in range(0, 3):
                pix = 0+(j*n) + posX - 101 + size
                pfx = (n+j*n) + posX - 101 - size
                piy = 0+(i*n) + posY - 101 + size
                pfy = (n+i*n) + posY - 101 - size
                rectangles.append(cv2.cvtColor(
                    frame[piy:pfy, pix:pfx], cv2.COLOR_BGR2RGB))
                cv2.rectangle(frame, (pix, piy), (pfx, pfy),
                              (255, 255, 255), 2)

        cv2.imshow("Frame", frame)

        reC = int(rectangles[0].shape[1] / 2)

        for i in range(0, len(rectangles)):
            myColors.append(rectangles[i][reC, reC])

        finalColors = []
        for i in range(0, len(myColors)):
            result = abs(myColors[i][0] - defaultColors[0][0]) + abs(
                myColors[i][1] - defaultColors[0][1]) + abs(myColors[i][2] - defaultColors[0][2])
            finalColor = defaultColors[0]
            for j in range(0, len(defaultColors)):
                temp = abs(myColors[i][0] - defaultColors[j][0]) + abs(
                    myColors[i][1] - defaultColors[j][1]) + abs(myColors[i][2] - defaultColors[j][2])
                if temp < result:
                    result = temp
                    finalColor = defaultColors[j]
            finalColors.append(finalColor)

        preview = centered
        count = 0

        for i in range(0, 3):
            for j in range(0, 3):
                preview[i*n:(i*n)+n, j*n:(j*n)+n] = [finalColors[count]
                                                     [2], finalColors[count][1], finalColors[count][0]]
                count += 1
        cv2.imshow('preview', preview)

        key = cv2.waitKey(1)
        if key == 27:
            break

        if key == 32:
            for i in range(0, len(finalColors)):
                cube += finalColors[i][3]
            faces.append(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
            faceColors.append(finalColors)
            print('agregado')
            # showImage(rectangles)
    solution = []
    solution.append(faceColors)
    solution.append(utils.solve(cube, 'Kociemba'))
    cv2.destroyAllWindows()
    return(solution)


def showImage(imgs):
    plt.figure(figsize=(10, 6))
    for i in range(0, len(imgs)):
        plt.subplot(
            3, 3, i+1), plt.imshow(imgs[i])
        plt.xticks([])
        plt.yticks([])
    plt.show()


def defineColor(fcolor):
    faceColor = ''

    if fcolor == 'w':
        faceColor = './textures/white.png'
    if fcolor == 'o':
        faceColor = './textures/orange.png'
    if fcolor == 'r':
        faceColor = './textures/red.png'
    if fcolor == 'y':
        faceColor = './textures/yellow.png'
    if fcolor == 'b':
        faceColor = './textures/blue.png'
    if fcolor == 'g':
        faceColor = './textures/green.png'

    return faceColor
