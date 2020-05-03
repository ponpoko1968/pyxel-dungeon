from enum import Enum
import numpy as np
import pyxel

class Direction(Enum):
    North = 1
    East = 2
    South = 3
    West = 4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
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

    def __str__(self):
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
        self.char_pos = Point(7,4)
        self.char_direction =  Direction.North
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
                    corners[2].lower_left,
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
                    corners[1].lower_left,
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
        self.wall_map = {
                        (1,0): [None, 'a'],
                        (2,0): [None, 'b'],
                        (3,0): [None,'c'],
                        (0,1): ['d',None],
                        (1,1): ['e', 'h'],
                        (2,1): [None,'i'],
                        (3,1): ['f', 'j'],
                        (4,1): ['g', None],
                        (1,2): ['k','m'],
                        (2,2): [None,'n'],
                        (3,2): ['l', 'o'],
                        (1,3): [None,'p'],
                        (3,3): [None,'q']
                    }
        self.dungeon = self.load_dungeon()
        print(self.dungeon)
        for direction in Direction:
            self.char_direction = direction
            window = self.update_window()
            print(direction)
            print(window)

        self.char_direction = Direction.North
        self.window = self.update_window()
        pyxel.init(256, 256, caption="dungeon")
        pyxel.load("my_resource.pyxres", False, False, True, False)
        pyxel.run(self.update, self.draw)

    def load_dungeon(self):
        return np.loadtxt('dungeon.csv', dtype = np.integer, delimiter=',')

            

    def update_window(self):

        dic = {Direction.North: (range(-2, 3), range(-3,1)),
               Direction.South: (range(-2, 3), range(0,4)),
               Direction.East:  (range(0,4), range(-2,3)),
               Direction.West:  (range(-3,1), range(-2,3)),
        }
        range_x = dic[self.char_direction][0]
        range_y = dic[self.char_direction][1]
        window = np.ndarray((range_y.stop-range_y.start,range_x.stop-range_x.start), dtype=np.integer)
        window.fill(-1)
        for relative_x in range_x:
            for relative_y in range_y:
                x = self.char_pos.x + relative_x
                y = self.char_pos.y + relative_y
                if x >= 0 and  y >= 0 and x < 16 and y < 16:
                    window[abs(range_y.start)+relative_y,abs(range_x.start)+relative_x] = self.dungeon[y,x]
                else:
                    window[abs(range_y.start)+relative_y,abs(range_x.start)+relative_x] = 1

        if self.char_direction == Direction.South:
            window = np.rot90(window,2)
        elif self.char_direction == Direction.East:
            window = np.rot90(window)
        elif self.char_direction == Direction.West:
            window = np.rot90(window,3)

        return window

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        diffs =  {
            Direction.North: Point(0, -1),
            Direction.West:  Point(-1, 0),
            Direction.South: Point(0, 1),
            Direction.East: Point(1,0)
        }
        directions = {
            Direction.North: {pyxel.KEY_A: Direction.West,  pyxel.KEY_D: Direction.East},
            Direction.West:  {pyxel.KEY_A: Direction.South, pyxel.KEY_D: Direction.North},
            Direction.South: {pyxel.KEY_A: Direction.East, pyxel.KEY_D: Direction.West},
            Direction.East: {pyxel.KEY_A: Direction.North, pyxel.KEY_D: Direction.South}
        }
        new_pos = Point(-1,-1)
        # north
        if pyxel.btnr(pyxel.KEY_W):
            diff = diffs[self.char_direction]
            new_pos = Point(self.char_pos.x + diff.x, self.char_pos.y + diff.y)
            if new_pos.x < 0 or new_pos.y < 0 or new_pos.x > 15 or new_pos.y > 15 \
                or self.dungeon[new_pos.y, new_pos.x] > 0:
                pyxel.play(0, 1)
            else:
                self.char_pos = new_pos
                self.window = self.update_window()
                print (self.window)
                print(self.draw_seq())

        # south
        if pyxel.btnr(pyxel.KEY_S):
            diff = diffs[self.char_direction]
            new_pos = Point(self.char_pos.x - diff.x, self.char_pos.y - diff.y)
            if new_pos.x < 0 or new_pos.y < 0 or new_pos.x > 15 or new_pos.y > 15 \
                or self.dungeon[new_pos.y, new_pos.x] > 0:
                pyxel.play(0, 1)
            else:
                self.char_pos = new_pos
                self.window = self.update_window()
                print (self.window)

        if pyxel.btnr(pyxel.KEY_A):
            self.char_direction = directions[self.char_direction][pyxel.KEY_A]
            self.window = self.update_window()

        if pyxel.btnr(pyxel.KEY_D):
            self.char_direction = directions[self.char_direction][pyxel.KEY_D]
            self.window = self.update_window()

    def draw_seq(self):
        seq = []
        for y in range(0,4):
            for x in range(0,5):
                if self.window[y, x] == 1 and (x,y) in self.wall_map and self.wall_map[(x,y)][0]:
                    seq.append(self.wall_map[(x,y)][0])
            for x in range(0,5):
                if self.window[y, x] == 1 \
                    and (x,y) in self.wall_map \
                    and len(self.wall_map[(x,y)]) >= 2 \
                    and self.wall_map[(x,y)][1]:
                    seq.append(self.wall_map[(x,y)][1])
        return seq

    def draw(self):
        pyxel.cls(0)
        for key in self.draw_seq():
            self.walls[key].draw()

App()