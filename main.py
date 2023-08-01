import pygame, random

class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range (1, 6):
      img = pygame.image.load(f"imgs/Explosion{num}.png")
      img = pygame.transform.scale(img, (30, 30))
      self.images.append(img)
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.counter = 0
    self.animation_time = 0

  def update(self):
    delta_time = clock.get_time()
    self.animation_time += delta_time
    clock.tick()
    print(delta_time) 
    explosion_speed = 4
    self.counter = self.animation_time * 5/40
    if self.counter >= explosion_speed and self.index < len(self.images) - 1:
      self.counter = 0
      self.index += 1
      self.image = self.images[self.index]
    
    if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
      self.kill()
    


class Target(pygame.sprite.Sprite):
  def __init__ (self,picture_path,pos_x,pos_y):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.rect.center=[pos_x,pos_y]
      
class Hitbox(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    self.gunshot = pygame.mixer.Sound("gunshot.wav")
  def shoot(self):
    self.gunshot.play()
    pygame.sprite.spritecollide(hitbox,target_group,True)
  def update(self):
    self.rect.center=pygame.mouse.get_pos()
      
class Crosshair(pygame.sprite.Sprite):
  def __init__ (self,picture_path):
    super().__init__()
    self.image=pygame.image.load(picture_path)
    self.rect=self.image.get_rect()
    
  def update(self):
    self.rect.center=pygame.mouse.get_pos()
    
pygame.init()
screen = pygame.display.set_mode((580, 409))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
background = pygame.image.load("bg.jpg")

target_group = pygame.sprite.Group()
for target in range(15):
  new_target = Target("target.png",random.randrange(10,590),random.randrange(10,390))
  target_group.add(new_target)

crosshair = Crosshair("crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

hitbox = Hitbox("hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)
hitbox.shoot()

explosion_group = pygame.sprite.Group()
run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False   
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      explosion = Explosion(pos[0], pos[1])
      explosion_group.add(explosion)
      print("shoot")
      hitbox.shoot()
 
  #Shooting sound when the game launched

  pygame.display.flip()
  screen.blit(background,(0,0))
  target_group.draw(screen)
  crosshair_group.draw(screen)
  crosshair_group.update()

  hitbox_group.draw(screen)
  hitbox_group.update()

  explosion_group.draw(screen)
  explosion_group.update()
  clock.tick(60)
pygame.quit()