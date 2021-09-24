from ursina import *
from process import defineColor
from process import imageProcesing

app = Ursina()
window.title = '3D Rubik Solver'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
solution = imageProcesing()
colorsTemp = solution[0]
toSolve = solution[1]
toSolveFinal = []
planes = [[], [], [], [], [], []]
sky = Entity(model='sphere', color=color.white,
             scale=(100, 100, 100), double_sided=True)
controls = []
miTiempo = [0]
root = Entity(model='cube', color=color.clear, scale=(5, 5, 5))

for i in range(0, len(toSolve)):
    toSolveFinal.append(str(toSolve[i]))
    if '2' in str(toSolve[i]):
        toSolveFinal.append(str(toSolve[i]))
print(toSolveFinal)

for i in range(len(colorsTemp)):

    pos = 0
    siguienteLinea = 0
    controls.append(Entity(model='cube', color=color.clear, scale=(2, 2, 2)))

    for j in range(0, len(colorsTemp[i])):
        faceColor = defineColor(colorsTemp[i][j][3])
        planes[i].append(
            Entity(model='plane', texture=faceColor, scale=(1, 0.2, 1)))
        planes[i][j].x = pos - 1
        planes[i][j].z = siguienteLinea + 1
        pos += 1
        if((j+1) % 3 == 0):
            siguienteLinea -= 1
            pos = 0

    for j in range(0, len(colorsTemp[i])):
        planes[i][j].parent = controls[i]

controls[0].y += 3
controls[1].x -= 3
controls[1].world_rotation_x -= 90
controls[1].world_rotation_y += 90
controls[2].z -= 3
controls[2].world_rotation_x -= 90
controls[3].x += 3
controls[3].world_rotation_x -= 90
controls[3].world_rotation_y -= 90
controls[4].z += 3
controls[4].world_rotation_x -= 90
controls[4].world_rotation_y -= 180
controls[5].y -= 3
controls[5].world_rotation_x += 180


def clearParent():
    for i in range(0, len(planes)):
        for j in range(0, len(planes[i])):
            planes[i][j].reparent_to(scene)


def parenting(rule):

    clearParent()

    direction = 1

    if "'" in rule:
        direction = -1

    if 'U' in rule:
        controls[0].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].y >= 1.5:
                    planes[i][j].reparent_to(controls[0])
        controls[0].animate_rotation_y(
            controls[0].rotation_y+90*direction, duration=1)

    if 'L' in rule:
        controls[1].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].x <= -1.5:
                    planes[i][j].reparent_to(controls[1])
        controls[1].animate_rotation_x(
            controls[1].rotation_x-90*direction, duration=1)

    if 'F' in rule:
        controls[2].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].z <= -1:
                    planes[i][j].reparent_to(controls[2])
        controls[2].animate_rotation_z(
            controls[2].rotation_z+90*direction, duration=1)

    if 'R' in rule:
        controls[3].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].x >= 1:
                    planes[i][j].reparent_to(controls[3])
        controls[3].animate_rotation_x(
            controls[3].rotation_x+90*direction, duration=1)

    if 'B' in rule:
        controls[4].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].z >= 1:
                    planes[i][j].reparent_to(controls[4])
        controls[4].animate_rotation_z(
            controls[4].rotation_z-90*direction, duration=1)

    if 'D' in rule:
        controls[5].rotation = Vec3(0, 0, 0)
        for i in range(0, len(planes)):
            for j in range(0, len(planes[i])):
                if planes[i][j].y <= -1.5:
                    planes[i][j].reparent_to(controls[5])
        controls[5].animate_rotation_y(
            controls[5].rotation_y-90*direction, duration=1)


camera.reparent_to(root)
camera.z -= 3
root.rotation = Vec3(28.7985, -36.9554, 0)

mouseX = [0, 0]
mouseY = [0, 0]

b = Button(text=f'Moves {len(toSolveFinal)}',
           color=color.azure, scale=(.25, .07))


def move():
    if(miTiempo[0] < len(toSolveFinal)):
        parenting(toSolveFinal[miTiempo[0]])
        miTiempo[0] += 1
        b.text = f'Moves left {len(toSolveFinal) - miTiempo[0]}'
    else:
        b.text = 'No more Moves'


b.position = window.bottom_right
b.x -= .15
b.y += .1
b.on_click = move


def update():
    cameraControls()


def cameraControls():
    mouseX[0] = mouseX[1]
    mouseY[0] = mouseY[1]
    mouseX[1] = mouse.x
    mouseY[1] = mouse.y
    deltaX = mouseX[1] - mouseX[0]
    deltaY = mouseY[0] - mouseY[1]
    if mouse.left:
        root.world_rotation_x = root.world_rotation_x + deltaY * 1000
        root.rotation_y = root.rotation_y + deltaX * 1000


# start running the game
app.run()
