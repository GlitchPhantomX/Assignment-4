import socket
import threading
import pygame
import json
import time
from dataclasses import dataclass

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 20)
CHAT_FONT = pygame.font.SysFont('Arial', 16)

@dataclass
class Player:
    id: str
    x: int
    y: int
    color: tuple
    username: str = "Player"

class GameClient:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Online Multiplayer Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.players = {}
        self.local_player = None
        self.chat_messages = []
        self.input_text = ""
        self.chat_active = False
        self.username = f"Player_{random.randint(1000, 9999)}"
        
        # Networking
        self.client_socket = None
        self.connect_to_server()
        
        # Game state
        self.keys_pressed = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False
        }
    
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 5555))  # Change to your server IP
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_data, daemon=True)
            receive_thread.start()
            
            # Send initial connection message
            self.send_data({
                "type": "connect",
                "username": self.username
            })
            
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.running = False
    
    def send_data(self, data):
        try:
            self.client_socket.send(json.dumps(data).encode('utf-8'))
        except Exception as e:
            print(f"Error sending data: {e}")
            self.running = False
    
    def receive_data(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                # Handle multiple JSON messages in one packet
                messages = data.split('\n')
                for msg in messages:
                    if msg.strip():
                        self.handle_server_message(json.loads(msg))
                        
            except json.JSONDecodeError:
                print("Invalid JSON received")
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False
                break
    
    def handle_server_message(self, data):
        message_type = data.get("type")
        
        if message_type == "game_state":
            # Update all players
            players_data = data.get("players", {})
            self.players = {
                pid: Player(
                    id=pid,
                    x=player_data["x"],
                    y=player_data["y"],
                    color=tuple(player_data["color"]),
                    username=player_data.get("username", "Player")
                )
                for pid, player_data in players_data.items()
            }
            
            # Set local player if not set
            if self.local_player is None and data.get("your_id"):
                self.local_player = data["your_id"]
                
        elif message_type == "chat":
            self.chat_messages.append(data["message"])
            if len(self.chat_messages) > 10:
                self.chat_messages.pop(0)
                
        elif message_type == "player_joined":
            print(f"{data['username']} joined the game!")
            
        elif message_type == "player_left":
            print(f"{data['username']} left the game")
            if data["player_id"] in self.players:
                del self.players[data["player_id"]]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.chat_active:
                        if self.input_text:
                            self.send_data({
                                "type": "chat",
                                "message": f"{self.username}: {self.input_text}"
                            })
                            self.input_text = ""
                        self.chat_active = False
                    else:
                        self.chat_active = True
                        
                elif event.key == pygame.K_BACKSPACE and self.chat_active:
                    self.input_text = self.input_text[:-1]
                    
                elif event.key in self.keys_pressed:
                    self.keys_pressed[event.key] = True
                    
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed[event.key] = False
                    
            elif event.type == pygame.TEXTINPUT and self.chat_active:
                self.input_text += event.text
    
    def update(self):
        # Update player position based on input
        if self.local_player and self.local_player in self.players:
            player = self.players[self.local_player]
            dx, dy = 0, 0
            
            if self.keys_pressed[pygame.K_w]:
                dy -= PLAYER_SPEED
            if self.keys_pressed[pygame.K_s]:
                dy += PLAYER_SPEED
            if self.keys_pressed[pygame.K_a]:
                dx -= PLAYER_SPEED
            if self.keys_pressed[pygame.K_d]:
                dx += PLAYER_SPEED
                
            if dx != 0 or dy != 0:
                player.x += dx
                player.y += dy
                
                # Send position update to server
                self.send_data({
                    "type": "move",
                    "x": player.x,
                    "y": player.y
                })
    
    def render(self):
        self.win.fill(BLACK)
        
        # Draw players
        for player in self.players.values():
            pygame.draw.rect(self.win, player.color, (player.x, player.y, 50, 50))
            name_text = FONT.render(player.username, True, WHITE)
            self.win.blit(name_text, (player.x, player.y - 20))
        
        # Draw chat
        if self.chat_messages:
            for i, msg in enumerate(self.chat_messages[-10:]):
                chat_text = CHAT_FONT.render(msg, True, WHITE)
                self.win.blit(chat_text, (10, HEIGHT - 150 + i * 20))
        
        # Draw chat input
        if self.chat_active:
            pygame.draw.rect(self.win, (50, 50, 50), (10, HEIGHT - 30, 400, 25))
            input_text = CHAT_FONT.render(f"> {self.input_text}", True, WHITE)
            self.win.blit(input_text, (15, HEIGHT - 27))
        else:
            help_text = CHAT_FONT.render("Press Enter to chat", True, (100, 100, 100))
            self.win.blit(help_text, (10, HEIGHT - 27))
        
        # Draw player list
        player_list_text = FONT.render("Players online:", True, WHITE)
        self.win.blit(player_list_text, (WIDTH - 150, 10))
        
        for i, player in enumerate(self.players.values()):
            player_text = CHAT_FONT.render(player.username, True, player.color)
            self.win.blit(player_text, (WIDTH - 150, 40 + i * 20))
        
        pygame.display.update()
    
    def run(self):
        last_update_time = time.time()
        
        while self.running:
            self.handle_events()
            
            # Update at fixed intervals
            current_time = time.time()
            if current_time - last_update_time > 1/30:  # 30 updates per second
                self.update()
                last_update_time = current_time
            
            self.render()
            self.clock.tick(FPS)
        
        # Clean up
        if self.client_socket:
            self.send_data({"type": "disconnect"})
            self.client_socket.close()
        pygame.quit()

if __name__ == "__main__":
    import random
    game = GameClient()
    game.run()