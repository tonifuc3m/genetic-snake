#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 04:17:31 2020

@author: antonio
Play one simulation
"""
import tensorflow as tf
import os
from utils import calculate_dist, decide_movement, update_snake_pos, \
    grow_snake, grow_fruit

class Network(tf.keras.Model):

    def __init__(self): 
        super(Network, self).__init__()
        self.h1 = tf.keras.layers.Dense(units=16, activation = 'relu')
        self.h2 = tf.keras.layers.Dense(units=8, activation = 'relu')
        self.out = tf.keras.layers.Dense(units=4, activation='softmax')
    
    def call(self, inputs):
        x = self.h1(inputs)
        x = self.h2(x)
        return self.out(x)
    
def play_simulation(snake, food, wall_left, wall_right, wall_up, wall_down, \
                    model, points):
    # Perceive
    inputs = calculate_dist(snake, food, wall_left, wall_right, wall_up, wall_down)
    # Move
    movement = decide_movement(model, inputs)
    snake, head_tail_direction = update_snake_pos(snake, movement[0])
    
    # End of movement options
    if ((snake[0][0] <= wall_left) | (snake[0][0] >= wall_right) |
        (snake[0][1] <= wall_down) | (snake[0][1] >= wall_up)):
        # Crashed with wall
        snake_alive = False
        
    elif (any(x == snake[0] for x in snake[1:])):
        # Crashed with snake body
        snake_alive = False
        
    elif (snake[0] == food):
        # Eaten fruit
        snake = grow_snake(snake, head_tail_direction)
        food = grow_fruit(snake)
        points = points + 10
        
    points = points + 1
    
    return points, snake_alive

def simulate_snake(model, wall_left, wall_right, wall_up, wall_down, all_points, 
                   max_movementes, food, snake):    
    # Define initial conditions
    snake_alive = True
    num_movements = 0
    points = 0
    
    # Play
    while (snake_alive) & (num_movements < max_movementes):
        points, snake_alive = \
            play_simulation(snake, food, wall_left, wall_right, wall_up, \
                            wall_down, model, points)
        num_movements = num_movements + 1

    return points

def simulate_generation(wall_left, wall_right, wall_up, wall_down, all_points, 
                        max_movementes, num_simulations, generation, path,
                        food, snake):
    snake_num = 0
    # Simulate snakes
    while snake_num < num_simulations:
        
        # Load model
        if generation == 0:
            # Define network
            model=Network()
            model.build((1,12))
            model.save_weights(os.path.join(path, str(snake_num) + '_snake.h5'))
        else:
            pass # Load weights from 2000 stored snakes
        
        # Simulate snake
        points = simulate_snake(model, wall_left, wall_right, wall_up, wall_down, 
                                all_points, max_movementes, food, snake)
        
        all_points.append(points)
        snake_num = snake_num + 1
        
    return all_points