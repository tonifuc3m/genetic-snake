#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 01:35:30 2020

@author: antonio
0: left, 1: right, 2: up, 3: down
"""
import os
from play_simulation import simulate_generation

    
if __name__ == '__main__':
    
    path_main = '/home/antonio/Documents/Personal/Development/genetic-algorithms/snake/'
    
    # Initialize stuff   
    num_simulations = 2000
    max_movementes = 200
    num_generations = 20
    num_survivals = 100
    
    generation = 0
    all_points = []
    wall_left = 0
    wall_right = 20
    wall_up = 20
    wall_down = 0
    food = [2,2]
    snake = [[10,10], [9,10], [8,10]]
    
    while generation < num_generations:
        
        # Create path
        path = os.path.join(path_main, str(generation))
        if os.path.exists(path) == False:
            os.makedirs(path)
        
        # Simulate generation
        all_points = simulate_generation(wall_left, wall_right, wall_up, 
                                         wall_down, all_points, max_movementes,
                                         num_simulations, generation, path, food, snake)
            
        # Get highest scoring snakes
        best_snakes = sorted(range(len(all_points)), 
                             key=lambda i: all_points[i])[-num_survivals:]
        
        # TODO: Pair best snakes (until I generate another 2000) and store their new weights
    
        
        generation = generation + 1
