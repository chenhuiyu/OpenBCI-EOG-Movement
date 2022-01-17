import random
import time
import winsound

import numpy as np
import pygame


class EyeMovementSimulation(object):
    def __init__(self, tralsNum=2, duration=2, flags=0):
        # 整个实验重复的次数
        self.tralsNum = tralsNum
        # 每个刺激停留的秒钟（默认两秒）
        self.duration = duration
        pygame.init()
        # 创建刺激产生的窗口 600 * 600
        self.screen = pygame.display.set_mode((600, 600), flags)
        # 字体
        self.font = pygame.font.SysFont('华文中宋', 80)
        self.state = None

    def EOGSimulation(self, state):
        if state == 0:
            loopRight_img = pygame.image.load("simu_fig\向前平视.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('向前平视', True, (0, 0, 0)), (150, 300))
        elif state == 1:
            loopRight_img = pygame.image.load("simu_fig\向右看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('请向右看', True, (0, 0, 0)), (150, 300))
        elif state == 2:
            loopRight_img = pygame.image.load("simu_fig\向左看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('请向左看', True, (0, 0, 0)), (150, 300))
        elif state == 3:
            loopRight_img = pygame.image.load("simu_fig\向上看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('请向上看', True, (0, 0, 0)), (150, 300))
        elif state == 4:
            loopRight_img = pygame.image.load("simu_fig\向下看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('请向下看', True, (0, 0, 0)), (150, 300))

    def start_display(self, state, streaming, terminate):
        for _ in range(self.tralsNum):
            self.state = state
            # 随机生成刺激顺序
            stim_shuffle = np.arange(0, 5).tolist()
            random.shuffle(stim_shuffle)
            for i in range(len(stim_shuffle)):
                # Begin stimuli display when the board is connected and it starts
                # streaming the data.
                print(' & stimuli & Waiting for the board to connect ...')
                streaming.wait()
                print(' & stimuli & Board connected ...')
                state.value = stim_shuffle[i]

                # blit 绘制图像
                self.screen.fill((128, 128, 128))
                print(state)
                self.EOGSimulation(state.value)
                # update 更新屏幕显示
                winsound.Beep(800, 200)
                pygame.display.update()
                time.sleep(self.duration)
        pygame.quit()
        terminate.set()
