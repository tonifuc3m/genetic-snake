#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 04:14:45 2020

@author: antonio
UTILS
"""
import numpy as np
from random import randrange

   
def dist_left(snake_head, thing, dist_wall_left, wall_right):
    return (snake_head[0]-thing[0]) if (snake_head[0]-thing[0]) > 0 \
        else (dist_wall_left+wall_right-thing[0])
        
def dist_right(snake_head, thing, dist_wall_right, wall_left):
    return (thing[0]-snake_head[0]) if (thing[0]-snake_head[0]) > 0 \
        else (dist_wall_right+wall_left+thing[0])
        
def dist_up(snake_head, thing, dist_wall_up, wall_down):
    return (thing[1]-snake_head[1]) if (thing[1]-snake_head[1]) > 0 \
        else (dist_wall_up+wall_down+thing[1])
        
def dist_down(snake_head, thing, dist_wall_down, wall_up):
    return (snake_head[1]-thing[1]) if (snake_head[1]-thing[1]) > 0 \
        else (dist_wall_down+wall_up-thing[1])
            
def calculate_dist(snake_pos, food, wall_left, wall_right, wall_up, wall_down):
    dist_wall_left = abs(snake_pos[0][0] - wall_left)
    dist_wall_right = abs(snake_pos[0][0] - wall_right)
    dist_wall_up = abs(snake_pos[0][1] - wall_up)
    dist_wall_down = abs(snake_pos[0][1] - wall_down)
            
    dist_food_left = dist_left(snake_pos[0], food, dist_wall_left, wall_right)
    dist_food_right = dist_right(snake_pos[0], food, dist_wall_right, wall_left)
    dist_food_up = dist_up(snake_pos[0], food, dist_wall_up, wall_down)
    dist_food_down = dist_down(snake_pos[0], food, dist_wall_down, wall_up)
    
    dist_body_left = min(dist_left(snake_pos[0], x, dist_wall_left, wall_right)
                         for x in snake_pos[1:])
    dist_body_right = min(dist_right(snake_pos[0], x, dist_wall_right, wall_left)
                         for x in snake_pos[1:])
    dist_body_up = min(dist_up(snake_pos[0], x, dist_wall_up, wall_down)
                       for x in snake_pos[1:])
    dist_body_down = min(dist_down(snake_pos[0], x, dist_wall_down, wall_up)
                         for x in snake_pos[1:])
    
    inputs = [dist_wall_left, dist_wall_right, dist_wall_up, dist_wall_down, 
              dist_food_left, dist_food_right, dist_food_up, dist_food_down, 
              dist_body_left, dist_body_right, dist_body_up, dist_body_down]
    
    return inputs


def update_snake_pos(snake, _dir):
    head_tail = [snake[0][0] - snake[1][0], snake[0][1] - snake[1][1]]
    if  head_tail == [1,0]:
        head_tail_direction = 0 
    elif head_tail == [-1,0]:
        head_tail_direction = 1
    elif head_tail == [0,-1]:
        head_tail_direction = 2
    elif head_tail == [0, 1]:
        head_tail_direction = 3

    if head_tail_direction == _dir:
        # Cambiar la dirección
        snake = list(reversed(snake))
        
    if _dir == 0: #left
        snake_head = [snake[0][0] - 1, snake[0][1]]
        snake_updated = [snake_head] + snake[0:-1]
    elif _dir == 1: # right
        snake_head = [snake[0][0] + 1, snake[0][1]]
        snake_updated = [snake_head] + snake[0:-1]
    elif _dir == 2: #up
        snake_head = [snake[0][0], snake[0][1] + 1]
        snake_updated = [snake_head] + snake[0:-1]
    elif _dir == 3: # down
        snake_head = [snake[0][0], snake[0][1] - 1]
        snake_updated = [snake_head] + snake[0:-1]     
        
    return snake_updated, head_tail_direction

def grow_snake(snake, head_tail_direction):
    snake.append(snake[-1])
    
    if head_tail_direction == 0:
        snake[-1][0] = snake[-1][0] - 1
    elif head_tail_direction == 1:
        snake[-1][0] = snake[-1][0] + 1
    elif head_tail_direction == 2:
        snake[-1][1] = snake[-1][1] + 1
    elif head_tail_direction == 3:
        snake[-1][1] = snake[-1][1] - 1
        
    return snake

def grow_fruit(snake):
    valid = False
    while valid==False:
        food = [randrange(20), randrange(20)]
        if food not in snake:
            valid = True
    return food

def decide_movement(model, inputs):
    data = np.array(inputs)
    data = np.reshape(data, (1,12))
    return model.predict(data).argmax(-1)

