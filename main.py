import pygame
import random
import time
from sprite import *
from settings import *
from pygame.locals import KEYDOWN
import tkinter
from tkinter import messagebox
from puzzle_solver import Solution
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.click_sound = pygame.mixer.Sound('clicksound.ogg')
        # self.high_score = float(self.get_high_scores()[0])

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def convert_puzzle_state(self):
        puzzle = []
        for row in self.tiles:
            for tile in row:
                if tile.text != "empty":
                    puzzle.append(int(tile.text))
                else:
                    puzzle.append(9)
        return puzzle

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(RoundedButton(500, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(RoundedButton(500, 170, 200, 50, "Solve", WHITE, BLACK))
        self.buttons_list.append(RoundedButton(500, 240, 200, 50, "Start", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                root = tkinter.Tk()
                root.withdraw()  # Hide main window
                messagebox.showinfo("Game Completed", "Congratulations! You have completed the game!")
                root.destroy()  # Destroy main window
                self.start_game = False

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        for button in self.buttons_list:
                            if button.click(mouse_x, mouse_y):
                                if button.text == "Shuffle":
                                    self.click_sound.play()
                                    self.shuffle_time = 0
                                    self.start_shuffle = True
                                if button.text == "Start":
                                    self.click_sound.play()
                                    self.start_game = True
                                if button.text == "Solve":
                                    self.click_sound.play()
                                    # Redirect stdout to a file
                                    original_stdout = sys.stdout  # Save a reference
                                    with open('log.txt', 'a') as f:  # Using 'a' to append instead of overwriting
                                        sys.stdout = f  # Change the standard output to the file created

                                        # Convert the current game state to the puzzle state
                                        puzzle_state = self.convert_puzzle_state()

                                        # Create a Solution object and run the solution
                                        solution = Solution(puzzle_state)
                                        solution.solution()

                                        # TODO: Update game's state with the solution...

                                        self.new()
                                    sys.stdout = original_stdout  # Reset the standard output to its original value
            if event.type == KEYDOWN:
                key = event.key
                if key == pygame.K_LEFT or key == pygame.K_a:  # Move left
                    self.move_tiles(1, 0)
                elif key == pygame.K_RIGHT or key == pygame.K_d:  # Move right
                    self.move_tiles(-1, 0)
                elif key == pygame.K_UP or key == pygame.K_w:  # Move up
                    self.move_tiles(0, 1)
                elif key == pygame.K_DOWN or key == pygame.K_s:  # Move down
                    self.move_tiles(0, -1)

    def move_tiles(self, dx, dy):
        moved = False
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                new_row, new_col = row + dy, col + dx
                if 0 <= new_row < len(self.tiles) and 0 <= new_col < len(tiles) and self.tiles_grid[new_row][
                    new_col] == 0:
                    self.tiles_grid[row][col], self.tiles_grid[new_row][new_col] = self.tiles_grid[new_row][new_col], \
                        self.tiles_grid[row][col]
                    moved = True
                    break
            if moved:
                break
        if moved:
            self.draw_tiles()


game = Game()
while True:
    game.new()
    game.run()
