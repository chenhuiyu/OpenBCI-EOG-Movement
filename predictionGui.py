import random
import time
import winsound

import numpy as np
import pygame


class PredictGUI(object):
    def __init__(self):
        pygame.init()
        # 创建刺激产生的窗口 600 * 600
        self.screen = pygame.display.set_mode((600, 600))
        # 字体
        self.font = pygame.font.SysFont('华文中宋', 80)
        self.state = None

    def stateShow(self, state):
        if state == 0:
            loopRight_img = pygame.image.load("simu_fig\向前平视.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('您在向前平视', True, (0, 0, 0)), (80, 300))
        elif state == 1:
            loopRight_img = pygame.image.load("simu_fig\向右看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('您在向右看', True, (0, 0, 0)), (100, 300))
        elif state == 2:
            loopRight_img = pygame.image.load("simu_fig\向左看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('您在向左看', True, (0, 0, 0)), (100, 300))
        elif state == 3:
            loopRight_img = pygame.image.load("simu_fig\向上看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('您在向上看', True, (0, 0, 0)), (100, 300))
        elif state == 4:
            loopRight_img = pygame.image.load("simu_fig\向下看.png").convert_alpha()
            self.screen.blit(loopRight_img, (250, 150))  # 绘制图片
            self.screen.blit(self.font.render('您在向下看', True, (0, 0, 0)), (100, 300))

    def display(self, state):

        # blit 绘制图像
        self.screen.fill((128, 128, 128))
        self.stateShow(state)
        # update 更新屏幕显示
        winsound.Beep(800, 200)
        pygame.display.update()
        time.sleep(1)
        pygame.quit()


gui = PredictGUI()
gui.display(1)