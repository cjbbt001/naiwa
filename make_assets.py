from PIL import Image
import os

os.makedirs("assets", exist_ok=True)

Y = (255, 214, 64, 255)
YD = (214, 156, 28, 255)
YL = (255, 238, 170, 255)
G = (46, 168, 74, 255)
K = (42, 32, 24, 255)
FT = (96, 72, 42, 255)
W = (255, 255, 255, 255)
RED = (220, 48, 40, 255)
ORG = (255, 140, 40, 255)
MILK = (248, 248, 252, 255)


def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def rect(im, x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= xx < im.width and 0 <= yy < im.height:
                im.putpixel((xx, yy), c)


def frog(frame=0, hurt=False):
    im = new(48, 40)
    body = set()
    for y in range(8, 34):
        for x in range(8, 38):
            nx = (x - 22) / 14.2
            ny = (y - 21) / 11.6
            if nx * nx + ny * ny <= 1:
                body.add((x, y))
    for x, y in body:
        nx = (x - 22) / 14.2
        ny = (y - 21) / 11.6
        if ny > 0.12 and abs(nx) < 0.5:
            c = YL
        elif nx < -0.22:
            c = YD
        else:
            c = Y
        if hurt and (x + y) % 3 == 0:
            c = (255, 150, 150, 255)
        im.putpixel((x, y), c)
    for x, y in list(body):
        if any((x + dx, y + dy) not in body for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            im.putpixel((x, y), K)

    bob = 0 if frame % 2 == 0 else 1
    for x in range(11, 19):
        im.putpixel((x, 33), K)
        im.putpixel((x, 34), FT)
        im.putpixel((x, 35), FT)
    for x in range(27, 37):
        im.putpixel((x, 33 + bob), K)
        im.putpixel((x, 34 + bob), FT)
        im.putpixel((x, 35 + bob), FT)
    for x in (27, 31, 35):
        im.putpixel((x, 36 + bob), K)

    arm_y = 20 if frame == 2 else 22 + bob
    for x in range(34, 41):
        im.putpixel((x, arm_y), YD)
        im.putpixel((x, arm_y + 1), Y)
        im.putpixel((x, arm_y + 2), K)
    im.putpixel((41, arm_y), K)
    im.putpixel((42, arm_y), FT)
    im.putpixel((42, arm_y + 1), FT)

    ex, ey = 28, 13
    rect(im, ex, ey, 7, 6, W)
    rect(im, ex + 2, ey + 1, 4, 4, G)
    rect(im, ex + 4, ey + 2, 2, 2, K)
    im.putpixel((ex + 2, ey + 1), W)
    for x in range(ex, ex + 7):
        im.putpixel((x, ey), K)
        im.putpixel((x, ey + 5), K)
    for y in range(ey, ey + 6):
        im.putpixel((ex, y), K)
        im.putpixel((ex + 6, y), K)

    for x in range(27, 34):
        im.putpixel((x, 22), K)
    im.putpixel((26, 21), K)
    im.putpixel((34, 21), K)
    im.putpixel((25, 19), (255, 150, 130, 255))
    im.putpixel((26, 19), (255, 150, 130, 255))

    for y in range(18, 24):
        im.putpixel((8, y), YD)
        im.putpixel((7, y), K)
    return im


frog(0).save("assets/frog_idle.png")
frog(1).save("assets/frog_walk.png")
frog(2).save("assets/frog_shoot.png")
frog(0, hurt=True).save("assets/frog_hurt.png")

bullet = new(10, 8)
rect(bullet, 2, 1, 6, 6, MILK)
rect(bullet, 1, 2, 8, 4, MILK)
bullet.putpixel((8, 3), YL)
bullet.putpixel((8, 4), YL)
for x in range(1, 9):
    if bullet.getpixel((x, 2))[3]:
        bullet.putpixel((x, 2), K)
    if bullet.getpixel((x, 5))[3]:
        bullet.putpixel((x, 5), K)
bullet.save("assets/bullet.png")


def slime():
    im = new(28, 22)
    cells = set()
    for y in range(4, 20):
        for x in range(3, 25):
            nx = (x - 14) / 10.2
            ny = (y - 13) / 8.0
            if nx * nx + ny * ny <= 1:
                cells.add((x, y))
    col = (78, 196, 86, 255)
    dark = (36, 120, 48, 255)
    for x, y in cells:
        im.putpixel((x, y), col if x > 12 else dark)
    for x, y in cells:
        if any((x + dx, y + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            im.putpixel((x, y), K)
    rect(im, 15, 9, 3, 3, W)
    rect(im, 20, 9, 3, 3, W)
    im.putpixel((16, 10), K)
    im.putpixel((21, 10), K)
    return im


def bat(frame):
    im = new(32, 20)
    col = (168, 96, 210, 255)
    wing = (110, 48, 150, 255)
    rect(im, 12, 7, 8, 8, col)
    for x in range(12, 20):
        im.putpixel((x, 7), K)
        im.putpixel((x, 14), K)
    lift = -2 if frame else 1
    for i, x in enumerate(range(2, 12)):
        yy = 9 + abs(i - 4) // 2 + lift
        im.putpixel((x, yy), col)
        im.putpixel((x, yy + 1), wing)
        im.putpixel((31 - x, yy), col)
        im.putpixel((31 - x, yy + 1), wing)
    im.putpixel((14, 9), W)
    im.putpixel((17, 9), W)
    im.putpixel((14, 10), RED)
    im.putpixel((17, 10), RED)
    return im


slime().save("assets/slime.png")
bat(0).save("assets/bat0.png")
bat(1).save("assets/bat1.png")

boss = new(96, 72)
cells = set()
for y in range(12, 62):
    for x in range(8, 88):
        nx = (x - 48) / 38
        ny = (y - 38) / 24
        if nx * nx + ny * ny <= 1:
            cells.add((x, y))
body_c = (206, 164, 42, 255)
belly = (242, 224, 150, 255)
sh = (148, 102, 32, 255)
for x, y in cells:
    nx = (x - 48) / 38
    ny = (y - 38) / 24
    if ny > 0.08 and abs(nx) < 0.42:
        c = belly
    elif nx < -0.15:
        c = sh
    else:
        c = body_c
    boss.putpixel((x, y), c)
for x, y in cells:
    if any((x + dx, y + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        boss.putpixel((x, y), K)
for i, sx in enumerate(range(30, 68, 8)):
    hgt = 9 if i % 2 == 0 else 5
    for k in range(hgt):
        boss.putpixel((sx, 14 - k), RED)
        boss.putpixel((sx + 1, 14 - k), (150, 28, 28, 255))
    boss.putpixel((sx, 14 - hgt), K)
for ex in (30, 54):
    rect(boss, ex, 28, 12, 10, W)
    rect(boss, ex + 3, 31, 7, 6, RED)
    rect(boss, ex + 6, 33, 3, 3, K)
    for i in range(12):
        brow = i // 5 if ex < 50 else (11 - i) // 5
        boss.putpixel((ex + i, 26 + brow), K)
        boss.putpixel((ex + i, 27 + brow), K)
for x in range(36, 64):
    boss.putpixel((x, 48), K)
    boss.putpixel((x, 49), (90, 24, 24, 255))
    if 42 < x < 58 and x % 4 < 2:
        boss.putpixel((x, 51), W)
for base in (20, 60):
    for x in range(base, base + 18):
        boss.putpixel((x, 60), K)
        boss.putpixel((x, 61), FT)
        boss.putpixel((x, 62), FT)
        boss.putpixel((x, 63), FT)
boss.save("assets/boss.png")

bb = new(12, 12)
for y in range(12):
    for x in range(12):
        d = (x - 5.5) ** 2 + (y - 5.5) ** 2
        if d <= 25:
            bb.putpixel((x, y), RED if (x + y) % 2 == 0 else ORG)
        if d <= 5:
            bb.putpixel((x, y), YL)
bb.save("assets/boss_bullet.png")


def ground():
    im = new(32, 32)
    rect(im, 0, 0, 32, 32, (96, 66, 40, 255))
    rect(im, 0, 0, 32, 7, (118, 168, 58, 255))
    rect(im, 0, 7, 32, 2, (64, 104, 38, 255))
    for x, y in ((4, 14), (11, 20), (18, 16), (25, 24), (8, 27), (21, 29), (29, 18)):
        im.putpixel((x, y), (70, 46, 28, 255))
        im.putpixel((x + 1, y), (140, 96, 58, 255))
    for x in (2, 9, 16, 23, 30):
        im.putpixel((x, 0), (186, 214, 78, 255))
        im.putpixel((x, 1), (78, 136, 40, 255))
    return im


def brick():
    im = new(32, 32)
    rect(im, 0, 0, 32, 32, (154, 88, 58, 255))
    mortar = (92, 52, 38, 255)
    for y in (0, 10, 11, 21, 22, 31):
        for x in range(32):
            im.putpixel((x, y), mortar)
    for x in (0, 16, 31):
        for y in list(range(0, 11)) + list(range(22, 32)):
            im.putpixel((x, y), mortar)
    for x in (8, 24):
        for y in range(11, 22):
            im.putpixel((x, y), mortar)
    im.putpixel((2, 2), (196, 126, 86, 255))
    im.putpixel((3, 2), (196, 126, 86, 255))
    return im


def plat():
    im = new(32, 16)
    rect(im, 0, 4, 32, 8, (124, 80, 48, 255))
    rect(im, 0, 0, 32, 4, (92, 172, 68, 255))
    rect(im, 0, 12, 32, 4, (72, 46, 30, 255))
    for x in range(1, 32, 8):
        im.putpixel((x, 1), (200, 230, 110, 255))
    return im


ground().save("assets/ground.png")
brick().save("assets/brick.png")
plat().save("assets/plat.png")

ht = new(13, 12)
rows = [
    " ##   ## ",
    "#### ####",
    "#########",
    "#########",
    "#########",
    " ####### ",
    "  #####  ",
    "   ###   ",
    "    #    ",
]
for y, row in enumerate(rows):
    for x, ch in enumerate(row):
        if ch == "#":
            ht.putpixel((x + 1, y + 1), (255, 96, 110, 255) if x + y < 8 else (214, 36, 52, 255))
ht.save("assets/heart.png")

cl = new(48, 20)
for y in range(20):
    for x in range(48):
        ok = False
        for cx, cy, r in ((14, 12, 9), (26, 9, 11), (36, 13, 8)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                ok = True
        if ok:
            cl.putpixel((x, y), (255, 255, 255, 235) if y < 11 else (214, 226, 242, 235))
cl.save("assets/cloud.png")

mb = new(16, 22)
rect(mb, 6, 0, 4, 2, (255, 150, 176, 255))
rect(mb, 5, 2, 6, 3, (190, 214, 236, 255))
rect(mb, 3, 5, 10, 15, MILK)
rect(mb, 3, 5, 10, 2, (176, 198, 226, 255))
for y in range(6, 19):
    mb.putpixel((3, y), (170, 184, 206, 255))
    mb.putpixel((12, y), (150, 164, 186, 255))
mb.putpixel((6, 11), W)
mb.putpixel((7, 11), W)
mb.save("assets/milk.png")

print("ok", sorted(os.listdir("assets")))
