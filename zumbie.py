from dis import dis
from turtle import width
from collections import deque
import pygame
import re
from tkinter import messagebox
import sys
import random

black = (0, 0, 0)
white = (255, 255, 255)
green = (147, 241, 55)
lightGreen = (59, 255, 176)
blue = (0, 0, 255)
red = (192, 57, 43)
yellow = (255, 255, 0)

Personicon = pygame.image.load('images/Zumbie.png')
pygame.display.set_icon(Personicon)

# This class represents the bar at the bottom that the player controls


class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a green wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1


def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 6, 66],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], green)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list

# This class represents the ball
# It derives from the "Sprite" class in Pygame


class Path (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([x, y])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.rect(self.image, blue, [0, 0, x, y])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()


class Point (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([x, y])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.rect(self.image, red, [0, 0, x, y])
        self.rect = self.image.get_rect()


class Grafo:
    def __init__(self, vertices):
        pygame.sprite.Sprite.__init__(self)
        self.vertices = vertices
        self.grafo = [[0]*self.vertices for i in range(self.vertices)]

    def adiciona_aresta(self, u, v):
        self.grafo[u][v] = 1

    def mostra_lista(self):
        print("Inprimindo matrix de adjacencias: ....")
        for i in range(self.vertices):
            print(self.grafo[i])

    def retorna_grafo(self):
        return self.grafo


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = x

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls):
        # Get the old position, in case we need to go back to it

        old_x = self.rect.left
        new_x = old_x+self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y+self.change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
        else:
            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y


class Zumbie_Class(Player):
    # Change the speed of the ghost
    def changespeed(self, listPath, turn, steps, l):
        # l sempre vale 17
        try:
            z = listPath[turn][2]
            # print("Valor do z", steps)
            if steps < z:
                # print("Entrou no if do step menor que z", steps, z)
                self.change_x = listPath[turn][0]
                self.change_y = listPath[turn][1]
                steps += 1
            else:
                # print("Entrou no primeiro else")
                if turn < l:
                    # print("Entrou no if do TURN < L", turn, l)
                    turn += 1
                else:
                    # print("Entrou no ELSE do TURN = 0")
                    turn = 0
                self.change_x = listPath[turn][0]
                self.change_y = listPath[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


# propriedades de cada valor = [avanço em x, avanço em y, quantidade de passos]
# Cada item nesse array é um caminho em uma direção
# Quando a quantidade de passos acaba ele vai pra direção seguinte no array
Zumbie_directions = [
    [0, -30, 1],
    [15, 0, 2],
    [0, 15, 3],
    [-15, 0, 4],
    [0, 15, 5],
    [15, 0, 6],
    [0, -15, 7],
    [15, 0, 8],
    [0, 15, 9],
    [15, 0, 10],
    [0, 15, 11],
    [15, 0, 12],
    [0, -15, 13],
    [-15, 0, 14],
    [0, 15, 15],
    [-15, 0, 16],
    [0, -15, 17],
    [15, 0, 18]
]

Zumbie2_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 10],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 15],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [-15, 0, 11],
    [0, 15, 7],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 3],
    [0, -15, 15],
    [15, 0, 15],
    [0, 15, 3],
    [-15, 0, 15],
    [0, 15, 11],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 11],
    [0, 15, 3],
    [15, 0, 1],
]


pl = len(Zumbie_directions)-1
bl = len(Zumbie2_directions)-1

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 606x606 sized screen
size = (width, height) = 606, 606
screen = pygame.display.set_mode(size)


# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'

pygame.display.set_caption('Zumbie Competition')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
# Used for converting color maps and such
background = background.convert()
# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

# default locations for Person and zumbie


class Cell:
    def __init__(self, x, y, dist, prev):
        self.x = x
        self.y = y
        self.dist = dist
        self.prev = prev

class ShortestPathBetweenCellsBFS:
    def shortestPath(self, matrix, start, end):
        sx = start[0]
        sy = start[1]
        dx = end[0]
        dy = end[1]

        if matrix[sx][sy] == 0 or matrix[dx][dy] == 0:
            messagebox.showinfo("Sem solucao", "Nao ha solucao")
            return

        m = len(matrix)
        n = len(matrix[0])
        cells = []
        for i in range(0, m):
            row = []
            for j in range(0, n):
                if matrix[i][j] != 0:
                    row.append(Cell(i, j, sys.maxsize, None))
                else:
                    row.append(None)
            cells.append(row)

        queue = []
        listPath = []
        src = cells[sx][sy]
        src.dist = 0
        queue.append(src)
        dest = None
        p = queue.pop(0)
        while p != None:
            if p.x == dx and p.y == dy:
                dest = p
                break
            self.visit(cells, queue, p.x-1, p.y, p)
            self.visit(cells, queue, p.x, p.y-1, p)
            self.visit(cells, queue, p.x+1, p.y, p)
            self.visit(cells, queue, p.x, p.y+1, p)
            if len(queue) > 0:
                p = queue.pop(0)
            else:
                p = None

        if dest == None:
            messagebox.showinfo("Sem solucao", "Nao ha solucao")
            return
        else:
            path = []
            p = dest
            while p != None:
                path.insert(0, p)
                p = p.prev
            for i in path:
                listPath.append(i)
        return listPath

    def visit(self, cells, queue, x, y, parent):
        if x < 0 or x >= len(cells) or y < 0 or y >= len(cells[0]) or cells[x][y] == None:
            return

        dist = parent.dist + 1
        p = cells[x][y]
        if dist < p.dist:
            p.dist = dist
            p.prev = parent
            queue.append(p)


def startGame():

    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    zumbie_collide = pygame.sprite.RenderPlain()
    zumbie_list = pygame.sprite.RenderPlain()
    zumbie2_collide = pygame.sprite.RenderPlain()
    person_collide = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)
    g = Grafo(19)

    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    start = [0, 0]
    end = [0, 0]

    # Cria o caminho do grafo
    for row in range(19):
        for column in range(19):
            point = Point(5, 5)

            # Set a random location for the block
            point.rect.x = (30*column+6)+26
            point.rect.y = (30*row+6)+26

            w_collide = pygame.sprite.spritecollide(point, wall_list, False)
            if w_collide:
                continue
            else:
                g.adiciona_aresta(row, column)
                # Add the block to the list of objects

    # g.mostra_lista()
    grafo = g.retorna_grafo()

    invalidposition = True
    # Random location for Person
    while(invalidposition):
        x = random.randint(0, 18)
        y = random.randint(0, 18)
        per_x = (30*x+6)+12
        per_y = (30*y+6)+12
        start = [y, x]
        Person = Player(per_x, per_y, "images/Person.png")
        p_collide = pygame.sprite.spritecollide(Person, wall_list, False)
        if p_collide:
            continue
        else:
            all_sprites_list.add(Person)
            person_collide.add(Person)
            invalidposition = False

    invalidposition = True
    # Random location for Zumbie
    while(invalidposition):
        x = random.randint(0, 18)
        y = random.randint(0, 18)
        zumb_x = (30*x+6)+12
        zumb_y = (30*y+6)+12
        Zumbie = Zumbie_Class(zumb_x, zumb_y, "images/Zumbie.png")
        z_collide = pygame.sprite.spritecollide(Zumbie, wall_list, False)
        if z_collide:
            continue
        else:
            zumbie_collide.add(Zumbie)
            all_sprites_list.add(Zumbie)
            zumbie_list.add(Zumbie)
            invalidposition = False

    invalidposition = True
    # Random location for Zumbie
    while(invalidposition):
        x = random.randint(0, 18)
        y = random.randint(0, 18)
        zumb_x = (30*x+6)+12
        zumb_y = (30*y+6)+12
        Zumbie2 = Zumbie_Class(zumb_x, zumb_y, "images/Zumbie.png")
        z_collide = pygame.sprite.spritecollide(Zumbie2, wall_list, False)
        if z_collide:
            continue
        else:
            zumbie2_collide.add(Zumbie2)
            all_sprites_list.add(Zumbie2)
            invalidposition = False
            zumbie_list.add(Zumbie2)

    # Mostra a moedinha
    invalidposition = True
    while(invalidposition):
        column = random.randint(0, 18)
        row = random.randint(0, 18)
        block = Block(yellow, 10, 10)
        block.rect.x = (30*column+6)+26
        block.rect.y = (30*row+6)+26
        end = [row, column]
        b_collide = pygame.sprite.spritecollide(block, wall_list, False)
        z_collide = pygame.sprite.spritecollide(block, zumbie_collide, False)
        z2_collide = pygame.sprite.spritecollide(block, zumbie2_collide, False)
        p_collide = pygame.sprite.spritecollide(block, person_collide, False)
        if b_collide:
            continue
        elif p_collide:
            continue
        elif z_collide:
            continue
        elif z2_collide:
            continue
        else:
            # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)
            invalidposition = False

    matrix = ShortestPathBetweenCellsBFS()

    listPath = matrix.shortestPath(grafo, start, end)
    # Zumbie_directions = listPath

    for i in listPath:
        x = i.__dict__['x']
        y = i.__dict__['y']
        dist = i.__dict__['dist']
        path = Path(5, 5)
        path.rect.x = (30*y+6)+26
        path.rect.y = (30*x+6)+26
        all_sprites_list.add(path)

    bll = len(block_list)

    score = 0

    done = False

    while done == False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Person.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Person.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Person.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Person.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Person.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Person.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Person.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Person.changespeed(0, -30)

        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Person.update(wall_list)

        returned = Zumbie.changespeed(
            Zumbie_directions, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Zumbie.changespeed(Zumbie_directions, p_turn, p_steps, pl)
        Zumbie.update(wall_list)

        returned = Zumbie2.changespeed(
            Zumbie2_directions, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Zumbie2.changespeed(Zumbie2_directions, b_turn, b_steps, bl)
        Zumbie2.update(wall_list)

        # See if the Zumbie block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(Person, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list) > 0:
            score += len(blocks_hit_list)

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        all_sprites_list.draw(screen)
        zumbie_list.draw(screen)
        # zumbie_collide.draw(screen)

        if score == bll:
            doNext("Parabens, voce ganhou!", 145, all_sprites_list,
                   block_list, zumbie_collide, person_collide, wall_list)

        zumbie_hit_list = pygame.sprite.spritecollide(Zumbie, block_list, True)
        zumbie2_hit_list = pygame.sprite.spritecollide(Zumbie2, block_list, True)
        zumbie_hit_person = pygame.sprite.spritecollide(Person, zumbie_list, True)
        zumbie2_hit_person = pygame.sprite.spritecollide(Person, zumbie_list, True)

        if zumbie_hit_list or zumbie2_hit_list or zumbie2_hit_person or zumbie_hit_person:
            doNext("Voce perdeu", 235, all_sprites_list, block_list,
                   zumbie_collide, person_collide, wall_list)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, zumbie_list, person_collide, wall_list):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del zumbie_list
                    del person_collide
                    del wall_list
                    startGame()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)                # alpha level
        w.fill((128, 128, 128))           # this fills the entire surface
        screen.blit(w, (100, 200))    # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("Para jogar, aperte ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("Para sair, aperte ESC.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


startGame()

pygame.quit()
