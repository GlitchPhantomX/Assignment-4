import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
COLORS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 165, 0),  
    (0, 255, 255),  
    (128, 0, 128)   
]

SHAPES = [
    [[1, 1, 1, 1]],                          
    [[1, 1], [1, 1]],                        
    [[0, 1, 0], [1, 1, 1]],                  
    [[1, 0], [1, 0], [1, 1]],                
    [[0, 1], [0, 1], [1, 1]],                
    [[0, 1, 1], [1, 1, 0]],                  
    [[1, 1, 0], [0, 1, 1]]                   
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 40)
        
        self.reset_game()
        
    def reset_game(self):
        self.board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 0.5 
        self.last_fall_time = time.time()
        
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_idx]
        return {
            'shape': shape,
            'color': COLORS[shape_idx],
            'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2,
            'y': 0
        }
        
    def draw_block(self, x, y, color, alpha=255):
        s = pygame.Surface((BLOCK_SIZE-1, BLOCK_SIZE-1))
        s.set_alpha(alpha)
        s.fill(color)
        self.screen.blit(s, (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1))
        
    def draw_board(self):
        self.screen.fill(BLACK)
        
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x]:
                    self.draw_block(x, y, self.board[y][x])
        
        self.draw_piece(self.current_piece)
        
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_text, (SCREEN_WIDTH + 10, 10))
        
        next_x = SCREEN_WIDTH // BLOCK_SIZE + 1
        next_y = 2
        for y, row in enumerate(self.next_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    self.draw_block(next_x + x, next_y + y, self.next_piece['color'], 150)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (SCREEN_WIDTH + 10, 100))
        self.screen.blit(level_text, (SCREEN_WIDTH + 10, 130))
        self.screen.blit(lines_text, (SCREEN_WIDTH + 10, 160))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                           SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                                          SCREEN_HEIGHT//2 + 50))
    
    def draw_piece(self, piece, alpha=255):
        for y, row in enumerate(piece['shape']):
            for x, block in enumerate(row):
                if block:
                    self.draw_block(piece['x'] + x, piece['y'] + y, piece['color'], alpha)
    
    def rotate_piece(self):
        rotated = [list(row) for row in zip(*self.current_piece['shape'][::-1])]
        
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        
        if self.check_collision():
            self.current_piece['shape'] = old_shape
    
    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    if (self.current_piece['x'] + x < 0 or
                        self.current_piece['x'] + x >= len(self.board[0]) or
                        self.current_piece['y'] + y >= len(self.board) or
                        (self.current_piece['y'] + y >= 0 and 
                         self.board[self.current_piece['y'] + y][self.current_piece['x'] + x])):
                        return True
        return False
    
    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block and self.current_piece['y'] + y >= 0:
                    self.board[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if self.check_collision():
            self.game_over = True
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(len(self.board)):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
        
        if len(lines_to_clear) == 1:
            self.score += 100 * self.level
        elif len(lines_to_clear) == 2:
            self.score += 300 * self.level
        elif len(lines_to_clear) == 3:
            self.score += 500 * self.level
        elif len(lines_to_clear) == 4:
            self.score += 800 * self.level
        
        self.lines_cleared += len(lines_to_clear)
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)
    
    def hard_drop(self):
        while not self.check_collision():
            self.current_piece['y'] += 1
        self.current_piece['y'] -= 1
        self.lock_piece()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision():
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision():
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision():
                            self.current_piece['y'] -= 1
                            self.lock_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        current_time = time.time()
        if current_time - self.last_fall_time > self.fall_speed:
            self.current_piece['y'] += 1
            if self.check_collision():
                self.current_piece['y'] -= 1
                self.lock_piece()
            self.last_fall_time = current_time
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()