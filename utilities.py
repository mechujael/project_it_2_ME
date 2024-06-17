import pygame, sys
import main

pygame.init()
#button
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/mainmenu/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/mainmenu/font.ttf", size)

def play():
    while True:
        main.main(window=SCREEN)

        pygame.display.update()


#difficulty level 
class Difficulty():
    def __init__(self):
        super(Difficulty,self).__init__()        
        self.diflev=2
        self.diff=1


    def dl(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("antiquewhite")

            OPTIONS_TEXT = get_font(45).render("Set Your Difficulty Level", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
            #setting diffculty level

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()
                    if OPTIONS_EASY.checkForInput(OPTIONS_MOUSE_POS):
                        self.diflev=1
                    if OPTIONS_MEDIUM.checkForInput(OPTIONS_MOUSE_POS):
                        self.diflev=2
                    if OPTIONS_HARD.checkForInput(OPTIONS_MOUSE_POS):
                        self.diflev=3
            self.diff=self.diflev
            if self.diff==1:
                OPTIONS_EASY = Button(image=None, pos=(640, 160),
							    text_input="Easy", font=get_font(45), base_color="Palegreen", hovering_color="Palegreen")
                OPTIONS_MEDIUM = Button(image=None, pos=(640, 260),
		    				    text_input="Medium", font=get_font(45), base_color="Black", hovering_color="Gold")
                OPTIONS_HARD = Button(image=None, pos=(640, 360),
			    				text_input="Hard", font=get_font(45), base_color="Black", hovering_color="Tomato")
            if self.diff==2:
                OPTIONS_EASY = Button(image=None, pos=(640, 160),
		    					text_input="Easy", font=get_font(45), base_color="Black", hovering_color="Palegreen")
                OPTIONS_MEDIUM = Button(image=None, pos=(640, 260),
			    				text_input="Medium", font=get_font(45), base_color="Gold", hovering_color="Gold")
                OPTIONS_HARD = Button(image=None, pos=(640, 360),
			    				text_input="Hard", font=get_font(45), base_color="Black", hovering_color="Tomato")
            if self.diff==3:
                OPTIONS_EASY = Button(image=None, pos=(640, 160),
		    					text_input="Easy", font=get_font(45), base_color="Black", hovering_color="Palegreen")
                OPTIONS_MEDIUM = Button(image=None, pos=(640, 260),
			    				text_input="Medium", font=get_font(45), base_color="Black", hovering_color="Gold")
                OPTIONS_HARD = Button(image=None, pos=(640, 360),
			    				text_input="Hard", font=get_font(45), base_color="Tomato", hovering_color="Tomato")
        
            OPTIONS_BACK = Button(image=None, pos=(640, 560), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)
            OPTIONS_EASY.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_EASY.update(SCREEN)
            OPTIONS_MEDIUM.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_MEDIUM.update(SCREEN)
            OPTIONS_HARD.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_HARD.update(SCREEN)
            pygame.display.update() 

difficulty=Difficulty()
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        

        #Menu, Title on the top!
        MENU_TEXT = get_font(100).render("CALM BIRDS", True, "#16c780")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        #Options button is DIFFICULTY in this case!!!!!!!!!!!
        PLAY_BUTTON = Button(image=pygame.image.load("assets/mainmenu/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/mainmenu/Options Rect.png"), pos=(640, 400), 
                            text_input="DIFFICULTY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/mainmenu/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        #When mouse is over button (Najechanie na przycisk)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #clicked buttons
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    difficulty.dl()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()




