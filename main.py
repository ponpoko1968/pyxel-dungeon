import numpy as np
import pyxel



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def str(self)->str:
        return 'x={0}, y={1}'.format(self.x, self.y)
        
class Trapezoid:
    def __init__(self, short_upper, short_lower, long_upper, long_lower):
        self.short_upper = short_upper
        self.short_lower = short_lower
        self.long_upper = long_upper
        self.long_lower = long_lower

    def draw(self):
        x =  self.short_upper.x if self.short_upper.x < self.long_upper.x else self.long_upper.x
        _x =  self.long_upper.x if self.short_upper.x < self.long_upper.x else self.short_upper.x
        y =  self.short_upper.y
        width = abs(x - _x)
        height = self.short_lower.y - self.short_upper.y
        pyxel.rect(x, y,
            width,
            height,            
            pyxel.COLOR_CYAN
        )
        pyxel.tri(
            self.short_upper.x, self.short_upper.y,
            self.long_upper.x, self.long_upper.y,
            self.long_upper.x, self.short_upper.y,
            pyxel.COLOR_CYAN
        )
        pyxel.tri(
            self.short_lower.x, self.short_lower.y,
            self.long_lower.x, self.long_lower.y,
            self.long_lower.x, self.short_lower.y,
            pyxel.COLOR_CYAN
        )

class Rect:
    def __init__(self, upper_left, lower_right,color):
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.color = color
        self.origin = upper_left
        self.width = self.lower_right.x - self.upper_left.x
        self.height =  self.lower_right.y - self.upper_left.y

    @property
    def upper_right(self):
        return Point(self.lower_right.x, self.upper_left.y)

    @property
    def lower_left(self):
        return Point(self.upper_left.x, self.lower_right.y)

    def str(self):
        return '{0},{1},width={2}, height={3}'.format(self.origin.x, self.origin.y, self.width, self.height)

    def draw(self):
        pyxel.rect(self.origin.x, # x
            self.origin.y, #y
            self.width,
            self.height,
            self.color)


origins = [(0,0),(37, 37),(74,74),(91,93),(29,93)]
corners = []


for origin in origins:
    x = origin[0]
    y = origin[1]
    corners.append(Rect( Point(x, y), 
        Point(256-x, 256-y),
        pyxel.COLOR_GREEN
    ))

class App:

    def __init__(self):
        self.walls = {
            'a' : Rect( corners[4].upper_left, 
            corners[3].lower_left,
            pyxel.COLOR_RED),
            'b' : Rect(
                corners[3].upper_left,
                corners[3].lower_right,
                pyxel.COLOR_BROWN
            ),
            'c' : Rect(
                corners[3].upper_right,
                corners[4].lower_right,
                pyxel.COLOR_CYAN
            ),
            'd' : Trapezoid(
                corners[4].upper_left,
                corners[4].lower_left,
                Point(corners[0].upper_left.x, corners[2].upper_left.y),
                Point(corners[0].upper_left.x, corners[2].lower_left.y)
            ),
            'e' :  Trapezoid(corners[3].upper_left, 
                corners[3].lower_left,
                corners[2].upper_left,
                corners[2].lower_left),
            'f' :  Trapezoid(corners[3].upper_right, 
                corners[3].lower_right,
                corners[2].upper_right,
                corners[2].lower_right),
            'g' : Trapezoid(
                corners[4].upper_right,
                corners[4].lower_right,
                Point(corners[0].upper_right.x, corners[2].upper_right.y),
                Point(corners[0].upper_right.x, corners[2].lower_right.y)),
            'h': Rect(Point(0, corners[2].upper_left.y),
                    corners[2].lower_right,
                    pyxel.COLOR_WHITE),
            'i' : Rect(corners[2].upper_left,
                    corners[2].lower_right,
                    pyxel.COLOR_WHITE),
            'j': Rect(corners[2].upper_right,
                        Point(corners[0].lower_right.x, corners[2].lower_right.y),
                        pyxel.COLOR_WHITE
                    ),
            'k' :  Trapezoid(corners[2].upper_left, 
                corners[2].lower_left,
                corners[1].upper_left,
                corners[1].lower_left),
            'l' :  Trapezoid(corners[2].upper_right, 
                corners[2].lower_right,
                corners[1].upper_right,
                corners[1].lower_right),   

            'm': Rect(Point(0, corners[1].upper_left.y),
                    corners[1].lower_right,
                    pyxel.COLOR_WHITE),
            'n' : Rect(corners[1].upper_left,
                    corners[1].lower_right,
                    pyxel.COLOR_WHITE),
            'o': Rect(corners[1].upper_right,
                        Point(corners[0].lower_right.x, corners[1].lower_right.y),
                        pyxel.COLOR_WHITE
                    ),                              
            'p' :  Trapezoid(corners[1].upper_left, 
                corners[1].lower_left,
                corners[0].upper_left,
                corners[0].lower_left),
            'q' :  Trapezoid(corners[1].upper_right, 
                corners[1].lower_right,
                corners[0].upper_right,
                corners[0].lower_right),                    
        } 
        for c in corners:
            print(c.str())
        print(self.walls['a'].str())
        pyxel.init(256, 256, caption="dungeon")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(0)
        # for c in corners:
        #     c.draw()
        self.walls['h'].draw()
        self.walls['i'].draw()
        self.walls['j'].draw()
        self.walls['m'].draw()
        self.walls['n'].draw()
        self.walls['o'].draw()
        self.walls['p'].draw()
        self.walls['q'].draw()


App()