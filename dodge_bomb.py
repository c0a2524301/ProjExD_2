import os
import sys
import time
import random
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate 
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9) 
    img1 = pg.transform.flip(img0, True, False)  
    
    return {
        (0, 0): img0,  # 停止
        (-5, 0): img0,  # 左
        (+5, 0): img1,  # 右
        (0, -5): pg.transform.rotozoom(img1, 90, 1.0),  # 上
        (0, +5): pg.transform.rotozoom(img1, -90, 1.0), # 下
        (+5, -5): pg.transform.rotozoom(img1, 45, 1.0), # 右上
        (+5, +5): pg.transform.rotozoom(img1, -45, 1.0),# 右下
        (-5, -5): pg.transform.rotozoom(img0, -45, 1.0),# 左上
        (-5, +5): pg.transform.rotozoom(img0, 45, 1.0), # 左下
    }
def gameover(screen: pg.Surface) -> None:
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.set_alpha(128)
    black_sfc.fill((0, 0, 0))
    screen.blit(black_sfc, [0, 0])

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    screen.blit(txt, txt_rct)

    kk_img = pg.image.load("fig/8.png")
    kk_rct_left = kk_img.get_rect()
    kk_rct_left.center = WIDTH // 2 - 200, HEIGHT // 2
    screen.blit(kk_img, kk_rct_left)

    kk_rct_right = kk_img.get_rect()
    kk_rct_right.center = WIDTH // 2 + 200, HEIGHT // 2
    screen.blit(kk_img, kk_rct_right)

    pg.display.update()
    time.sleep(5)
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))


    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width, bb_rct.height = bb_img.get_rect().width, bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko: 
            vx *= -1
        if not tate:  
            vy *= -1
        screen.blit(bb_img, bb_rct)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
