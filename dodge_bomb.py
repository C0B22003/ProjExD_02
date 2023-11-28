import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1300, 650
delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:#練習4
    """
    オブジェクトが画面内or画面外を判定し、真理値をタプルに返す関数
    引数　rct：コウカトンor爆弾SurfaceのRect
    戻り値：横方向、縦方向判断結果（画面内：True/画面外False）
    """
    yoko ,tate = True, True

    if rct.left < 0 or WIDTH < rct.right:#横方向はみだし判定
        yoko = False

    if rct.top < 0 or HEIGHT < rct.bottom:#縦方向はみだし判定
        tate = False

    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    aa_img = pg.image.load("ex02/fig/3.png")
    cc_img = pg.image.load("ex02/fig/11.jpg")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    aa_img = pg.transform.rotozoom(aa_img, 0, 1.0)
    cc_img = pg.transform.rotozoom(cc_img, 0, 2.0)
    #cc_img = pg.transform.resize(cc_img,(800,800),mode='constant',anti_aliasing=True)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400#
    bb_img = pg.Surface((20,20))  #練習1　透明なsurfaceを作る
    bb_img.set_colorkey((0,0,0)) #練習1　黒をなくす
    pg.draw.circle(bb_img,(255,0,0), (10,10), 10)
    bb_rct = bb_img.get_rect() #練習1-3
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy =+5,+5

    """"
    演習課題1の辞書を作成する
    """

    kk_zis = { 
        (5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (5,-5):pg.transform.rotozoom(kk_img, 316, 1.0),
        (0,-5):pg.transform.rotozoom(kk_img, 270, 1.0),
        (-5,-5):pg.transform.rotozoom(kk_img, 315, 1.0),
        (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5,5):pg.transform.rotozoom(kk_img, 45, 1.0),
        (0,5):pg.transform.rotozoom(kk_img, 90, 1.0),
        (5,5):pg.transform.rotozoom(kk_img, 45, 1.0)
    }

    aa_zis = { #　息子の辞書
        (5,0):pg.transform.rotozoom(aa_img, 0, 1.0),
        (5,-5):pg.transform.rotozoom(aa_img, 316, 1.0),
        (0,-5):pg.transform.rotozoom(aa_img, 270, 1.0),
        (-5,-5):pg.transform.rotozoom(aa_img, 315, 1.0),
        (-5,0):pg.transform.rotozoom(aa_img, 0, 1.0),
        (-5,5):pg.transform.rotozoom(aa_img, 45, 1.0),
        (0,5):pg.transform.rotozoom(aa_img, 90, 1.0),
        (5,5):pg.transform.rotozoom(aa_img, 45, 1.0)
    }

    #===================
    """
    演習2
    """
    #加速度のリスト1を生成
    accs = [a for a in range(1, 11)]
    #====================

    #オリジナル==========
    fonto =  pg.font.Font(None, 80)
    moji = fonto.render("HOLY SHIT", True, (255,255,255))
    #===================

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            #オリジナル============
            screen.blit(bg_img,[0,0])
            screen.blit(cc_img, [0,0])
            screen.blit(moji, [20,350]) #文字の表示の追加機能
            pg.display.update()
            print("勉強不足だね")
            time.sleep(5)
            #====================
            return
        
        key_lst = pg.key.get_pressed() #練習3
        sum_mv = [0,0]
        for k, tpl in delta.items():
            if key_lst[k]:  #キーが押されたら反応
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True): # 練習4 はみ出てない判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        """
        演習課題１
        """
        if(sum_mv[0] >= 5): #演習課題1
            kk_img = pg.transform.flip(kk_img, False, True)
        if sum_mv != [0, 0]:
            kk_img = kk_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                kk_img = pg.transform.flip(kk_img, True, False)
        
        if(sum_mv[0] >= 5): #演習課題1（息子）
            aa_img = pg.transform.flip(aa_img, False, True)
        if sum_mv != [0, 0]:
            aa_img = aa_zis[tuple(sum_mv)]
            if sum_mv[0] >= 5:
                aa_img = pg.transform.flip(aa_img, True, False)

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct) #練習1 画像のblit
        screen.blit(aa_img,kk_rct)
    #======================
        """
        演習2
        """
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        #bb_rct.move_ip(vx,vy) #練習2　爆弾の移動
    #======================
        yoko, tate = check_bound(bb_rct)
        if not yoko:#横方向にはみ出たら
            vx *= -1
        if not tate:#縦方向にはみ出たら
            vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()