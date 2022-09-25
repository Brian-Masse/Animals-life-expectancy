import sys
sys.path.append( "." ) 
import pygame
import pandas as pd
import numpy as np
import random
from independent_work.colors import color

pygame.init()

width = 1000
height = 500

screen = pygame.display.set_mode((width, height))

running = True

xls = pd.ExcelFile(
    "independent_work/Animal Distributions/data/data.xlsx"
)

data = pd.read_excel( xls, "AZA_MLE_Jul2018" )

def render_text(message, position, color, size):
    font = pygame.font.Font( "freesansbold.ttf", size )
    text = font.render(message, True, color)
    textRect = text.get_rect()
    textRect.center = ( position[0], height - position[1] )
    screen.blit( text, textRect )

def render_point( pos, color, radius ):
    pygame.draw.circle(screen, color, (pos[0], height - pos[1]), radius)

def render_line( start_pos, end_pos, color ):
    pygame.draw.line(screen, color, (start_pos[0], height - start_pos[1]), (end_pos[0], height - end_pos[1]))

class Series:
    def __init__( self, series, gender, color ):
        self.series = series 
        self.gender = gender
        self.name = series + ", " + gender
        self.color = color
        self.data = self.get_data()
    
    def get_data(self):
        rows = (data["TaxonClass"] == self.series)
        selection = data.loc[ rows, self.gender ]
        return selection

    def render(self, graph, index):
        space = (graph.size[1] / len(graph.series)) - 10 

        render_text( self.name, ( graph.pos[0] - 70, (index * space) + graph.pos[1] + 10), self.color, 10)

        for age in self.data:   
        
            y = ((index * space ) + graph.pos[1] + 10) + random.uniform(0, space / 2)
            x = (age * graph.interval) + graph.pos[0]

            if not np.isnan( x ):
                render_point( ( x, y ), self.color, 2 )
        

class Graph:
    def __init__(self, size, position, series, title):
        self.size = size
        self.pos = position 
        self.top_right = self.return_top_right()
        self.series = series
        self.interval = self.return_interval()
        self.title = title

    def return_interval(self):
        return self.size[0] / 50

    def return_top_right(self):
        x = self.pos[0] + self.size[0]
        y = self.pos[1] + self.size[1]
        return (x, y)

    def render(self ):
        render_text( self.title, ( self.pos[0] + (self.size[0] / 2), self.top_right[1] ), dark, 20 )

        render_line( self.pos, (self.top_right[0], self.pos[1]), dark )
        render_line( self.pos, (self.pos[0], self.top_right[1]), dark )

        self.render_series()

        num = 0 
        while ( num < int(self.size[0] / self.interval) ):

            x = (num * self.interval) + self.pos[0]
            y = self.pos[1] - 10
            render_text(str(num), (x, y), dark, 10 )
            num += 2

            


    def render_series(self):
        for i in range(0, len(self.series)):
            self.series[0].render(self, i)
    
    

types = [ "Mammalia", "Reptilia", "Aves", "Amphibia", "Chondrichthyes" ]
genders = ["Male MLE", "Female MLE"]

def create_series():
    master = []
    i = 0
    for type in types:
        for gender in genders:

            base = color(200, 86 - i, 90 - i)

            series = Series(type, gender, base.return_RGB())
            master.append(series)
            i += 100 /  (len(types) * len(gender))
    return master


dark =color(200, 86, 70).return_RGB()
back = color( 150, 2, 100 ).return_RGB()

screen.fill(back)

graph = Graph( ( 800, 400 ), ( 150, 50 ), create_series(), "The maximum life span for certain classifications of animals")
graph.render()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()


