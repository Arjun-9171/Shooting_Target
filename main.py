import pygame, random, time

pygame.init()
pygame.mixer.init()
screen_width, screen_height = 580, 409

screen = pygame.display.set_mode((screen_width, screen_height))


background = pygame.image.load("Assets/bg.jpg")


class Button():
  def __init__(self,x,y,image,scale):
    width=image.get_width()
    height=image.get_height()
    self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    self.rect=self.image.get_rect()
    self.rect.topleft=(x,y)
    self.clicked=False
  def draw(self,surface):
    action=False
    pos=pygame.mouse.get_pos()
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
        self.clicked=True
        action=True
        print("start clicked")
        
  
    if pygame.mouse.get_pressed()[0]==0:
      self.clicked=False
    surface.blit(self.image,(self.rect.x,self.rect.y)) 
    return action
        
start_image = pygame.image.load("Assets/start.png")
start_button = Button(228, 190, start_image, 0.4)
#button_rect = start_button.get_rect(center = (screen_width/2, screen_height/2))


class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range (1, 6):
      img = pygame.image.load(f"Assets/explosions_imgs/Explosion{num}.png")
      img = pygame.transform.scale(img, (30, 30))
      self.images.append(img)
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.counter = 0
 

  def update(self):
    explosion_speed = 15
    self.counter += 1
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
    self.gunshot = pygame.mixer.Sound("Assets/gunshot.wav")
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

start_time = None
total_time = 8

in_menu = True

font_color = "black"
font_size = 50
font = pygame.font.Font(None, font_size)
play_option = font.render("play", True, font_color)
play_rect = play_option.get_rect(center = (screen_width/2, screen_height/2))

target_group = pygame.sprite.Group()
for target in range(15):
  new_target = Target("Assets/target.png",random.randrange(10,590),random.randrange(10,390))
  target_group.add(new_target)

crosshair = Crosshair("Assets/crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

hitbox = Hitbox("Assets/hitbox.jpg")
hitbox_group = pygame.sprite.Group()
hitbox_group.add(hitbox)
hitbox.shoot()

explosion_group = pygame.sprite.Group()

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False  
      exit() 
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      explosion = Explosion(pos[0], pos[1])
      explosion_group.add(explosion)
      print("shoot")
      hitbox.shoot()
      if in_menu:
        if play_rect.collidepoint(event.pos):
          in_menu = False
          start_time = time.time()
        

    if in_menu: 
      screen.blit(background, (0,0))
      #start_button.draw(screen)
      screen.blit(play_option, play_rect)
      pygame.display.flip()
    else: 
      pygame.mouse.set_visible(False)
      screen.blit(background, (0,0))
      target_group.draw(screen)
      crosshair_group.draw(screen)
      crosshair_group.update()
      hitbox_group.update()
      explosion_group.draw(screen)
      explosion_group.update()
      elapsed_time = time.time() - start_time if start_time else 0
      time_left = max(total_time - int(elapsed_time), 0)
      timer_text = font.render("time left: " + str(time_left), True, "red")
      screen.blit(timer_text, (10, 10))

      if time_left == 0:
        game_over_text = "Try again!"
        message_text = font.render(game_over_text, True, "white")
        screen.blit(message_text, (290, 204))
        pygame.display.flip()
        time.sleep(7)
        run = False
      pygame.display.flip()

  
pygame.quit()



  


