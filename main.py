# todo 所有注释非常重点，详情参csdn收藏部分
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
# “sys”为系统模块，“traceback”为Python用来捕获异常的模块，“random”为随机数生成模块，
# “pygame.locals”则包含了Pygame中的一些固定的标志常量，在下面的程序中将会用到。
from pygame.locals import *
from random import *

pygame.init()
# 用于加载和播放声音的pygame模块
pygame.mixer.init()
# ,表示一一对应关系
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

background = pygame.image.load('images/background.png').convert()


# 定义颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 载入音乐
# 由于pygame音频处理能力有限，在读取音频信息时，需要将音频文件转换成wav格式，普通的MP3格式一般情况下是无法正常读取的
pygame.mixer.music.load('sound/hundouluo.wav')
# pygame.mixer.Sound.set_volume        -        设置此声音的播放音量
pygame.mixer.music.set_volume(0.2)
# 加载各种声音，子弹声音，爆炸声音，增幅声音等
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)

supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
# pygame.mixer.Sound.set_volume        -        设置此声音的播放音量
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)

get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.6)

enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)

enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)

me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        # 加两组
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)
        # 参数group1、group2是两个精灵组类型的形参，用以存储多个精灵对象（敌机）。
        # 需要注意的一点是group既然是特定的精灵组结构体，在向其内部添加精灵对象时需要调用其对应的成员函数add（），
        # 不能使用列表添加函数append（）。


def inc_speed(target, inc):
    # 确定加速
    for each in target:
        each.speed += inc


def main():
    # 播放音乐
    # play(loops=0, maxtime=0, fade_ms=0) -> Channel
    # loops参数控制第一次播放后样本重复的次数。
    # 值 5 表示声音将播放一次，然后重复播放五次，因此共播放六次。
    # 默认值（0）表示声音不重复，因此只播放一次。
    # todo 如果循环设置为-1，则Sound将无限循环（但是您仍然可以调用stop（）来停止它）
    pygame.mixer.music.play(-1)

    # 实例我方飞机
    me = myplane.MyPlane(bg_size=bg_size)

    # 实例敌方飞机组
    enemies = pygame.sprite.Group()

    # 实例敌方小型飞机组
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 实例敌方中型飞机组
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 实例敌方大型飞机组
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 实例我方普通子弹组
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 实例我方超级子弹组
    bullet2 = []
    # index 是1指从0开始，
    # 这里通过for循环语句来产生指定数目的子弹对象，并存储于列表结构体中（bullet1），
    # 值得注意的一点是，在前面已经提到，在实例化子弹对象时，需要外部传入子弹的初始位置，
    # 这里的me.rect.midtop代表的是我方飞机的上方正中间的位置，
    bullet2_index = 0
    BULLET2_NUM = 8
    # //为除法取整数
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 33, me.rect.centery)))

    # 中弹图片索引
    # 基本思路是当程序检测到当前飞机对象（无论是我方飞机还是敌机）因碰撞而挂掉（成员变脸active=false）后，
    # 则依次打印其若干张损毁图像。在因此打印的过程中，我们采用索引值的方式来判别接下来应该打印第几张损毁特效图片，
    # 因此需要在main函数的开始部分（while之前）先声明各个索引值：
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    # 字体文件+字号
    score_font = pygame.font.Font("font/rough.ttf", 36)

    ''' # 先设置一个暂停/开始标志位“paused”，为true表示暂停状态，为false表示非暂停状态。
    # 然后加载四张图片，注意这里四张图片都是由特定含义的，
    # “pause_nor_image”代表未选中状态下的暂停按钮， 
    # “pause_pressed_image”代表选中状态下的暂停按钮，
    # “resume_nor_image”代表未选中状态下的开始按钮，
    # “resume_pressed_image”代表选中状态下的开始按钮，鼠标移动到按钮区域按钮就变为选中状态。
    # 然后创建一个“paused_image”变量用以保存当前需要显示的按钮图片，
    # 游戏开始时默认为“pause_nor_image”。注意这里需要事先得到并设置好按钮图片的区域位置
    '''
    # 标志是否暂停游戏，先设初值
    paused = False
    # 加载四种状态的图片
    paused_nor_image = pygame.image.load(
        "images/pause_nor.png").convert_alpha()
    # 对于含有 alpha 通道的图片（支持部分位置透明，像 PNG 图像），需要使用 Surface.convert_alpha() 函数进行转换。
    # 返回的 Surface  对象将包含与源文件相同的颜色格式，colorkey 和 alpha 透明度通道。
    # 通常需要调用 Surface.convert() 函数进行转换，这样可以使得在屏幕上绘制的速度更快。
    paused_pressed_image = pygame.image.load(
        "images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load(
        'images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load(
        'images/resume_pressed.png').convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    # 默认最初是没有按下暂停的图
    paused_image = paused_nor_image

    # 设置难度
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)

    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 超级子弹定时器
    DOUBLE_BULLTET_TIME = USEREVENT + 1

    # 解除我方重生无敌定时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 标志是否使用超级子弹，初始化为没有
    is_double_bullet = False

    # 生命数量
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 用于切换我方飞机图片
    switch_plane = True

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 用于延迟切换
    delay = 100

    # 限制打开一次记录文件
    recorded = False

    clock = pygame.time.Clock()
    running = True  # 下面直接true就行

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 说明暂停的按钮设置，按下
            # 程序的暂停/开始时通过鼠标单击的动作来决定的，因此需要编写鼠标单击事件的响应函数，
            # todo 在函数中修改“paused”标志位的值来控制暂停/开始状态的切换：
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):   # 如果检测到用户在指定按钮区域按下鼠标左键
                    # 刷新状态
                    paused = not paused
                    # 如果检测到当前为左键单击（event.button == 1）
                    # 并且鼠标指针位于按钮区域之内（paused_rect.collidepoint(event.pos)返回true），
                    # 则认为用户发出了有效的暂停指令，此时需要将paused标志位取反。
                    # 紧接着就需要判断当前状态是暂停还是非暂停，
                    # 如果单击鼠标之后变为暂停状态（paused为真），
                    # 则需要关闭补给机制、关闭背景音效、关闭混音器，将按钮图片设置为resume_pressed_image（待开始），让程序静静的等待即可；
                    # 相反若鼠标单击之后为开始状态，则需要重新开启这些机制，同时调整按钮图片为pause_pressed_image（待暂停）。

                    if paused:
                        # 暂时停止播放所有声道
                        # 这将暂时停止活动混音器通道上的所有播放。
                        # 稍后可以 通过 pygame.mixer.unpause() 恢复播放
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            # 选中和未选中状态是由鼠标是否移动到按钮区域来决定的，因此需要定义鼠标移动的事件响应函数

            elif event.type == MOUSEMOTION:
                # 对于鼠标移动事件，每当鼠标指针的位置坐标发生变化时，都会触发一次“MOUSEMOTION”事件，
                # 在系统接收到鼠标移动事件后，首先要判断当前鼠标指针是否位于按钮的矩形区域，
                # 这个功能可以通过rect类的的collidepoint（）成员函数完成，
                # 它能够实现判断一个坐标点（例如当前的event.pos）是否在调用者的（一个矩形对象）的区域范围之内。
                # 如果鼠标处于按钮区域，则将当前显示的图片指定为“选中状态下的开始/暂停”（resume_pressed_image和pause_pressed_image），
                # 否则设定为“非选中状态下的开始/暂停”（resume_nor_image和pause_nor_image），
                # 这些小逻辑还是挺磨人的，需要仔细的推敲一把才能理清。

                if paused_rect.collidepoint(event.pos):     #  如果鼠标悬停在按钮区域
                    if paused:                              #  如果当前的状态是暂停，就是选中的开始按钮
                        paused_image = resume_pressed_image
                    else:                                   # 反之是选中的暂停按钮
                        paused_image = paused_pressed_image
                else:
                    if paused:                              #  如果鼠标没有悬停在按钮区域
                        paused_image = resume_nor_image     #  如果当前的状态是暂停，就是未选中的开始按钮
                    else:                                   #  如果当前的状态是未暂停，就是未选中的暂停按钮
                        paused_image = paused_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLTET_TIME:
                is_double_bullet = False
                # 要禁用事件的计时器，请将milliseconds参数设置为0
                pygame.time.set_time(DOUBLE_BULLTET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        # 根据用户得分增加难度
        if level == 1 and score > 5000:
            level = 2
            upgrade_sound.play()
            # 增加3架小型敌机, 2架中型敌机和1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)

        elif level == 2 and score > 30000:
            level = 3
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)

        elif level == 3 and score > 60000:
            level = 4
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)

        elif level == 4 and score > 100000:
            level = 5
            upgrade_sound.play()
            # 增加5架小型敌机, 3架中型敌机和2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)

            # 提升小型敌机的速度
            inc_speed(target=small_enemies, inc=1)
            inc_speed(target=mid_enemies, inc=1)
            inc_speed(target=big_enemies, inc=1)
        # 画背景
        screen.blit(background, (0, 0))

        if life_num and not paused:
            # 检测键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 绘制全屏炸弹补给
            if bomb_supply.active:          # active的用处在于判断某时刻是否起作用，一般这种都是针对那种刚开始没有的状态然后有了，
                # 注意最后还是要初始化到没有的，最初的初始化在supply的初始化里面就有了
                bomb_supply.move()
                # 画在屏幕具体位置
                screen.blit(bomb_supply.image, bomb_supply.rect)
                # 判断是否吃到补给
                if pygame.sprite.collide_mask(me, bomb_supply):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                        # 修改状态
                    bomb_supply.active = False

            # 绘制超级子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(me, bullet_supply):
                    get_bullet_sound.play()
                    # 发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLTET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 发射子弹
            if not(delay % 10):     #  # 每十帧发射一颗移动的子弹，
                # if not (delay % 10)是设置子弹打印的速度，即每十帧绘制一发子弹
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset(
                        (me.rect.centerx - 33, me.rect.centery))
                    # 在调用子弹对象的reset（）成员函数是，即将该对象的active成员变量设置为true，
                    # 说明该子弹对象已经处于激活状态了。
                    bullets[bullet2_index +
                            1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:             # 只有激活的子弹才可能击中敌机
                    b.move()            # 子弹移动
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(
                        b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False        # 子弹损毁
                        for each in enemy_hit:
                            each.hit = True     # 还原初始化
                            each.energy -= 1    # 具体几格血
                            if each.energy == 0:
                                each.active = False   # 小型敌机损毁

            # 绘制敌方大型机
            for each in big_enemies:    # 绘制大型敌机并自动移动
                if each.active:     # 如果飞机正常存在
                    each.move()     # 飞机移动move（）
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_plane:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    # 接下来是血槽，只要飞机处于激活状态，就需要绘制血槽，
                    # 而无需考虑飞机当前是否中弹。首先通过pygame.draw.line（）函数绘制血槽背景，
                    # 背景颜色为黑色，线的长度与精灵对象的宽度相等，位置处于精灵图片上方五个像素的位置。
                    # lines(Surface, color, closed, pointlist, width=1) -> Rect
                    # 在 Surface  对象上绘制一系列连续的线段。pointlist 参数是一系列短点。
                    # 如果 closed 参数设置为 True，则绘制首尾相连
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)

                    # 当生命大于20%显示绿色, 否则显示红色
                    # 得到剩余血量比重后，则判断当前剩余血量是否大于百分之二十，如果大于0.2，则血槽颜色为绿色，
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                        # 否色为红色。指定好血槽颜色之后即可再次调用pygame.draw.line（）来绘制血槽长度，位置和背景位置相同，
                        # 但血槽长度需要通过“血槽背景长度（总长度）*剩余血量百分比”来获得，
                        # 即代码中的“each.rect.width * energy_remain”，这样当前血槽长度就和当前血量（self.energy）成正比。
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5),
                                     2)

                    # 即将出现在画面, 播放音效
                    if each.rect.bottom == -10:
                        enemy3_fly_sound.play(-1)
                        each.appear = True
                    # 离开画面, 关闭音效
                    if each.rect.bottom < -10 and each.appear:
                        enemy3_fly_sound.stop()
                        each.appear = False
                else:
                    # 毁灭
                    if e3_destroy_index == 0:
                        # “if e3_destroy_index == 0:”是因为整个飞机损毁的过程是由四帧（或六帧）图像的播放来完成的，
                        # 如果不加这个限制，则在飞机损毁过程中每播放一帧就加一次分，这样小型机和中型机损毁一次就要加4次分，
                        # 大型机损毁一次就要加6次分，
                        # 因此需要规定每次飞机损毁时只在播放损毁最后一帧画面之后再进行加分、复位，播放声音等操作。
                        enemy3_down_sound.play()
                    if not(delay % 2):  # 每2帧播放一张损毁图片
                        screen.blit(each.destroy_images[
                                    e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6   # 大型敌机有六张损毁图片
                        if e3_destroy_index == 0:       # 如果损毁图片播放完毕，则重置飞机属性
                            enemy3_fly_sound.stop()
                            score += 1000
                            each.reset()

            # 绘制敌方中型机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5),
                                     2)

                    # 当生命大于20%显示绿色, 否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5),
                                     2)
                else:
                    # 毁灭
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    if not(delay % 2):
                        screen.blit(each.destroy_images[
                                    e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 600
                            each.reset()

            # 绘制敌方小型机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    if not(delay % 2):
                        screen.blit(each.destroy_images[
                                    e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 100
                            each.reset()

            # 检测我方飞机碰撞
            enemies_down = pygame.sprite.spritecollide(
                me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:  # 如果碰撞检测返回的列表非空，则说明已发生碰撞,若此时我方飞机处于无敌状态
                me.active = False
                for each in enemies_down:
                    each.active = False

            # 绘制我方飞机
            if me.active:
                if switch_plane:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if me_destroy_index == 0:
                    me_down_sound.play()
                if not(delay % 2):
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width,
                                    height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,
                                ((width - 10 - (i + 1) * life_rect.width),
                                 height - 10 - life_rect.height))
            # 绘制得分
            score_text = score_font.render('Score : %d' % score, True, WHITE)
            screen.blit(score_text, (10, 5))

        # 接下来当我方小飞机生命用尽时，程序会进入到“ elif life_num == 0:”的循环分支中，
        #  绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            
            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:        # 读取历史最高分
                recorded =True
                # 读取历史最高分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())

                # 判断是否高于历史最高分
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))

            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:   # pygame.mouse.get_pressed()  ——  获取鼠标按键的情况（是否被按下）
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()    # 获取鼠标光标的位置
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()   


        

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 用于切换图片
        if not(delay % 11):
            switch_plane = not switch_plane

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    try:
        main()

    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
# 这是Python的主程序入口，如果我们运行main.py文件，程序则自动开始运行。
# 如果只是将main.py作为一个模块import到其他工程中，则不会触发这个函数的运行。
# 注意在这里我们使用了try语句来捕获程序运行时出现的异常，
# 如果main（）函数在运行过程中抛出任何异常，
# 除了系统正常退出（SystemExit）的异常外，其他异常都通过“traceback.print_exc()”来打印异常信息，
# 同时调用“pygame.quit()”退出程序。
