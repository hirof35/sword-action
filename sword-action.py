import sys
import pygame
import random as ran
from pygame.locals import *

# --- 定数設定 ---
WIDTH, HEIGHT = 600, 600
FPS = 30
# シーン定義
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_CLEAR = 3

# --- クラス群（これまでの設計を統合） ---
class Player:
    def __init__(self, img):
        self.reset(img)

    def reset(self, img):
        self.rect = Rect(WIDTH//2, HEIGHT//2, 20, 20)
        self.hp = 10
        self.direction = (0, -1)
        self.weapon_active = False
        self.weapon_timer = 0
        self.weapon_img = img
        self.current_img = img

    def update(self, keys):
        dx, dy = 0, 0
        if keys[K_UP]: dy = -1
        elif keys[K_DOWN]: dy = 1
        elif keys[K_LEFT]: dx = -1
        elif keys[K_RIGHT]: dx = 1
        if dx != 0 or dy != 0:
            self.direction = (dx, dy)
            self.rect.x = max(0, min(self.rect.x + dx * 6, WIDTH-20))
            self.rect.y = max(0, min(self.rect.y + dy * 6, HEIGHT-20))
        if self.weapon_active:
            self.weapon_timer -= 1
            if self.weapon_timer <= 0: self.weapon_active = False

    def attack(self):
        if not self.weapon_active:
            self.weapon_active = True
            self.weapon_timer = 6
            cx, cy = self.rect.center
            dx, dy = self.direction
            self.weapon_rect = Rect(0, 0, 45, 45)
            self.weapon_rect.center = (cx + dx*40, cy + dy*40)
            angle = 0
            if dx == 1: angle = -90
            elif dx == -1: angle = 90
            elif dy == 1: angle = 180
            self.current_img = pygame.transform.rotate(self.weapon_img, angle)

class Enemy:
    def __init__(self):
        self.rect = Rect(ran.randint(50, 550), ran.randint(50, 550), 18, 18)
        self.hp = 2
        self.vx, self.vy = ran.choice([-3, 3]), ran.choice([-3, 3])
        self.timer = ran.randint(20, 50)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.vx, self.vy = ran.choice([-3, 3]), ran.choice([-3, 3])
            self.timer = ran.randint(20, 50)
        self.rect.x = max(0, min(self.rect.x + self.vx, WIDTH-18))
        self.rect.y = max(0, min(self.rect.y + self.vy, HEIGHT-18))

class Boss:
    def __init__(self):
        self.rect = Rect(WIDTH//2-40, -100, 80, 80)
        self.hp = 30
        self.max_hp = 30
    def update(self, px, py):
        if self.rect.y < 60: self.rect.y += 2
        else:
            if self.rect.centerx < px: self.rect.x += 2
            if self.rect.centerx > px: self.rect.x -= 2
            if self.rect.centery < py: self.rect.y += 2
            if self.rect.centery > py: self.rect.y -= 2

# --- メインシステム ---
def main():
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font_lg = pygame.font.Font(None, 80)
    font_sm = pygame.font.Font(None, 40)
    
    # 武器画像生成
    sw = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(sw, (0, 255, 255), (18, 0, 4, 40))
    
    # ゲーム状態
    scene = SCENE_TITLE
    player = Player(sw)
    enemies = []
    boss = None
    score = 0

    while True:
        surface.fill((15, 15, 20))
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT: pygame.quit(); sys.exit()

        # --- シーン別ロジック ---
        if scene == SCENE_TITLE:
            msg = font_lg.render("SWORD ACTION", True, (255, 255, 255))
            sub = font_sm.render("Press SPACE to Start", True, (200, 200, 200))
            surface.blit(msg, (WIDTH//2-200, HEIGHT//2-50))
            surface.blit(sub, (WIDTH//2-130, HEIGHT//2+50))
            
            for event in events:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    # 初期化して開始
                    player.reset(sw)
                    enemies = [Enemy() for _ in range(5)]
                    boss = None
                    score = 0
                    scene = SCENE_PLAY

        elif scene == SCENE_PLAY:
            keys = pygame.key.get_pressed()
            player.update(keys)
            for event in events:
                if event.type == KEYDOWN and event.key == K_SPACE: player.attack()

            if score < 1000:
                for e in enemies[:]:
                    e.update()
                    if player.rect.colliderect(e.rect): player.hp -= 0.05
                    if player.weapon_active and player.weapon_rect.colliderect(e.rect):
                        e.hp -= 1
                        if e.hp <= 0:
                            score += 200
                            enemies.remove(e)
                            enemies.append(Enemy())
            else:
                if not boss: 
                    enemies.clear()
                    boss = Boss()
                boss.update(player.rect.centerx, player.rect.centery)
                if player.rect.colliderect(boss.rect): player.hp -= 0.1
                if player.weapon_active and player.weapon_rect.colliderect(boss.rect):
                    if player.weapon_timer == 5: boss.hp -= 1
                if boss.hp <= 0: scene = SCENE_CLEAR

            if player.hp <= 0: scene = SCENE_GAMEOVER

            # 描画
            pygame.draw.rect(surface, (255, 255, 255), player.rect)
            for e in enemies: pygame.draw.circle(surface, (200, 50, 50), e.rect.center, 9)
            if boss: 
                pygame.draw.rect(surface, (150, 0, 250), boss.rect)
                pygame.draw.rect(surface, (255, 0, 0), (boss.rect.x, boss.rect.y-15, (boss.hp/30)*80, 8))
            if player.weapon_active:
                r = player.current_img.get_rect(center=player.weapon_rect.center)
                surface.blit(player.current_img, r.topleft)
            surface.blit(font_sm.render(f"HP: {int(player.hp)}  SCORE: {score}", True, (255, 255, 255)), (10, 10))

        elif scene == SCENE_GAMEOVER:
            msg = font_lg.render("GAME OVER", True, (255, 50, 50))
            sub = font_sm.render("Press SPACE to Title", True, (255, 255, 255))
            surface.blit(msg, (WIDTH//2-160, HEIGHT//2-50))
            surface.blit(sub, (WIDTH//2-130, HEIGHT//2+50))
            for event in events:
                if event.type == KEYDOWN and event.key == K_SPACE: scene = SCENE_TITLE

        elif scene == SCENE_CLEAR:
            msg = font_lg.render("MISSION CLEAR!", True, (50, 255, 50))
            sub = font_sm.render("Press SPACE to Title", True, (255, 255, 255))
            surface.blit(msg, (WIDTH//2-220, HEIGHT//2-50))
            surface.blit(sub, (WIDTH//2-130, HEIGHT//2+50))
            for event in events:
                if event.type == KEYDOWN and event.key == K_SPACE: scene = SCENE_TITLE

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
