#Thêm các thư viện cần thiết
import pygame, random, time, sys
pygame.init()
#Tạo cửa sổ game
gameSF = pygame.display.set_mode((840, 540))
pygame.display.set_caption('Snake')

#Hình ảnh
n = 20
imgbody = pygame.transform.scale(pygame.image.load('body.png'), (n, n))
imghead = pygame.transform.scale(pygame.image.load('head.jpg'), (n, n))
imgfood = pygame.transform.scale(pygame.image.load('food.jpg'), (n, n))
imgwall = pygame.transform.scale(pygame.image.load('wall.png'), (400, 20))

#Màu sắc
red = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(65, 105, 255)
purple = pygame.Color(128, 0, 128)

#Khai báo các biến
snakepos = [100, 60]
snakebody = [[100, 60], [80, 60]]
foodx = random.randrange(2, 80)
foody = random.randrange(2, 50)
if foody == 14 or foody == 38:
    foody = 22
if foodx % 2 != 0:
    foodx += 1
if foody % 2 != 0:
    foody += 1
foodpos = [foodx*10, foody*10]
foodflat = True
direction = 'RIGHT'
changeto = direction
score = 0

#Hàm gameover
def game_over():
    gfont = pygame.font.SysFont('consolas', 40)
    gsurf = gfont.render('Game over!', True, red)
    grect = gsurf.get_rect()
    grect.midtop = (400, 180)
    gameSF.blit(gsurf, grect)
    show_score(0)
    pygame.display.flip()
    time.sleep(3) #thoi gian thoat
    pygame.quit()
    sys.exit()

#Hàm show_score
def show_score(choice = 1):
    sfont = pygame.font.SysFont('consolas', 20)
    ssurf = sfont.render('Score: {0}'.format(score), True, black)
    srect = ssurf.get_rect()
    if choice == 1:
        srect.midtop = (70, 20)
    else:
        srect.midtop = (400, 260)
    gameSF.blit(ssurf, srect)

#Thêm nhạc nền
pygame.mixer.init()
pygame.mixer.music.load("musictheme.wav") 
pygame.mixer.music.play(-1,0.0)

#Vòng lặp chính
while True:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        #Xử lý phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT:
                changeto = 'LEFT'
            if event.key == pygame.K_UP:
                changeto = 'UP'
            if event.key == pygame.K_DOWN:
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    #Hướng đi
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    
    #Cập nhật vị trí mới
    if direction == 'RIGHT':
        snakepos[0] += n
    if direction == 'LEFT':
        snakepos[0] -= n
    if direction == 'UP':
        snakepos[1] -= n
    if direction == 'DOWN':
        snakepos[1] += n
    
    #Cơ chế dài thêm
    snakebody.insert(0, list(snakepos))
    if snakepos[0] == foodpos[0] and snakepos[1] == foodpos[1]:
        score += 1
        foodflat = False
    else:
        snakebody.pop()
    
    #Sinh thức ăn
    if foodflat == False:
        foodx = random.randrange(2, 80)
        foody = random.randrange(2, 50)
        if foody == 14 or foody == 38:
            foody = 22
        if foodx % 2 != 0:
            foodx += 1
        if foody % 2 != 0:
            foody += 1
        foodpos = [foodx*10, foody*10]
    foodflat = True
    
    #Giao diện cửa sổ
    gameSF.fill(white)
    for pos in snakebody:
        gameSF.blit(imgbody, pygame.Rect(pos[0], pos[1], n, n))
    gameSF.blit(imghead, pygame.Rect(snakebody[0][0], snakebody[0][1], n, n))
    gameSF.blit(imgfood, pygame.Rect(foodpos[0], foodpos[1], n, n))
    gameSF.blit(imgwall, pygame.Rect(220, 140, 400, 20))
    gameSF.blit(imgwall, pygame.Rect(220, 380, 400, 20))
    pygame.draw.rect(gameSF, purple, (10, 10, 820, 520), 10)
    
    #Xử lý chạm viền
    if snakepos[0] >=820 or snakepos[0] <= 0:
        game_over()
    if snakepos[1] >= 520 or snakepos[1] <= 0:
        game_over()
    if (snakepos[0] >= 220 and snakepos[0] <= 600) and snakepos[1] == 140:
        game_over()
    if (snakepos[0] >= 220 and snakepos[0] <= 600) and snakepos[1] == 380:
        game_over()
    
    #Xử lý ăn chính mình
    for b in snakebody[1:]:
        if snakepos[0] == b[0] and snakepos[1] == b[1]:
            game_over()
    
    #Hiển thị điểm
    show_score()
    pygame.display.flip()