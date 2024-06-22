from graphics import Canvas
import time
import random

# Constants for the canvas size, square size, and movement speed
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SQUARE_SIZE = 20
VELOCITY = 20

# Delay between each frame in seconds
DELAY = 0.1

def main():
    # Create the canvas where the game will be played
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Direction variable to track the player's current direction
    direction = None
    
    # Generate possible positions for the food (red square)
    possible_positions = [i for i in range(0, CANVAS_WIDTH, SQUARE_SIZE)]
    
    # Function to create new food at a random position
    create_food(canvas, random.choice(possible_positions), random.choice(possible_positions))

    # Initial score setup
    score = 0
    score_text = canvas.create_text(10, CANVAS_HEIGHT - 30, font_size=30, text='Score:')
    food_ate_score = canvas.create_text(120, CANVAS_HEIGHT - 30, font_size=30, text=str(score), color='green')

    # Create the player (a blue square) at the starting position
    left_x = 0
    top_y = 0
    player = canvas.create_rectangle(left_x, top_y, left_x + SQUARE_SIZE, top_y + SQUARE_SIZE, 'blue')

    while True:
        # Get the last key pressed
        key = canvas.get_last_key_press()

        # Update the direction based on the key pressed
        if key == 'ArrowLeft':
            direction = 'left'
            canvas.move(player, -VELOCITY, 0)
        elif key == 'ArrowRight':
            direction = 'right'
            canvas.move(player, VELOCITY, 0)
        elif key == 'ArrowUp':
            direction = 'up'
            canvas.move(player, 0, -VELOCITY)
        elif key == 'ArrowDown':
            direction = 'down'
            canvas.move(player, 0, VELOCITY)

        # If no key is pressed, keep moving in the last direction
        if key is None:
            if direction is None or direction == 'right':
                canvas.move(player, VELOCITY, 0)
            elif direction == 'down':
                canvas.move(player, 0, VELOCITY)
            elif direction == 'up':
                canvas.move(player, 0, -VELOCITY)
            elif direction == 'left':
                canvas.move(player, -VELOCITY, 0)

        # Get the player's current position
        player_x = canvas.get_left_x(player)
        player_y = canvas.get_top_y(player)

        # Check for collisions with the food
        overlapping_objects = canvas.find_overlapping(player_x, player_y, player_x + SQUARE_SIZE, player_y + SQUARE_SIZE)

        # If the player overlaps with the food, update the score and create new food
        for obj in overlapping_objects:
            if obj != player and obj != food_ate_score and obj != score_text:
                canvas.delete(obj)
                create_food(canvas, random.choice(possible_positions), random.choice(possible_positions))
                score += 1
                food_ate_score = update_score_text(canvas, food_ate_score, score)

        # End the game if the player goes out of bounds
        if player_x > CANVAS_WIDTH or player_y > CANVAS_HEIGHT or player_x < 0 or player_y < 0:
            return

        # Pause for a short time before the next frame
        time.sleep(DELAY)

def create_food(canvas, food_left_x, food_top_y):
    # Create a red square (food) at the specified position
    canvas.create_rectangle(food_left_x, food_top_y, food_left_x + SQUARE_SIZE, food_top_y + SQUARE_SIZE, 'red')

def update_score_text(canvas, old_text, new_score):
    # Update the score display
    canvas.delete(old_text)
    new_text = canvas.create_text(120, CANVAS_HEIGHT - 30, font_size=30, text=str(new_score), color='green')
    return new_text

if __name__ == "__main__":
    main()
