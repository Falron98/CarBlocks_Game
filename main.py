from random import randrange

import pygame as pg
import os

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FPS = 60

CAR_SIZE = (25, 50)
BLOCK_SIZE = (10, 10)

CAR_IMAGE = pg.image.load(os.path.join('car.png'))
CAR_IMAGE = pg.transform.scale(CAR_IMAGE, CAR_SIZE)


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        pg.display.set_caption("Race")
        self.current_time = pg.time.get_ticks()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.last_block_time = 0
        self.block_creation_interval = 100
        self.car = Car()
        self.game_over = False

        self.block_list = []

        self.running = True

    def reset(self):
        self.last_block_time = 0
        self.block_creation_interval = 100
        self.car = Car()
        self.game_over = False

        self.block_list = []

    def draw_window(self):
        self.screen.fill(BLACK)
        self.screen.blit(CAR_IMAGE, self.car.car_pos)
        for block in self.block_list:
            self.screen.blit(block.block, block.block_pos)
        pg.display.update()

    def create_blocks(self):
        if not self.game_over:
            if self.current_time - self.last_block_time > self.block_creation_interval:
                new_block = Blocks(self.car.speed)
                self.block_list.append(new_block)
                self.last_block_time = self.current_time
            for block in self.block_list:
                block.move()
                if block.block_pos.y >= HEIGHT:
                    self.block_list.remove(block)

    def controls(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    self.reset()
            if event.type == pg.QUIT:
                self.running = False
            if not self.game_over:
                self.car.controls(event)

        if not self.game_over:
            for block in self.block_list:
                block.block_speed(self.car.speed)
                block.move()

    def is_collision(self):
        for block in self.block_list:
            if self.car.car_pos.colliderect(block.block_pos):
                self.game_over = True

    def update(self):
        self.current_time = pg.time.get_ticks()
        self.clock.tick(FPS)
        self.draw_window()
        self.create_blocks()
        self.controls()
        self.is_collision()


class Car:
    def __init__(self):
        self.car_pos = pg.Rect(WIDTH // 2 - CAR_SIZE[0], HEIGHT - CAR_SIZE[1], CAR_SIZE[0], CAR_SIZE[1])
        self.speed = 1

    def controls(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.speed += 5
            elif event.key == pg.K_s:
                if self.speed > 5:
                    self.speed -= 5
                else:
                    self.speed = 1
            if event.key == pg.K_a:
                self._move(-CAR_SIZE[0])
            elif event.key == pg.K_d:
                self._move(CAR_SIZE[0])

    def _move(self, x=0, y=0):
        self.car_pos.centerx += x
        self.car_pos.centery += y


def get_random_position():
    return randrange(0, WIDTH)


class Blocks:
    def __init__(self, speed):
        self.block = pg.Surface(BLOCK_SIZE)
        self.block_pos = pg.Rect(get_random_position(), 0, BLOCK_SIZE[0], BLOCK_SIZE[1])
        self.block.fill(GREEN)
        self.speed = speed

    def move(self):
        self.block_pos.y += self.speed

    def block_speed(self, speed=1):
        self.speed = speed


if __name__ == "__main__":
    game = Game()

    while game.running:
        game.update()
