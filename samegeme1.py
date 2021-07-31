import tkinter as tk
import math
import random
import queue
from tkinter import messagebox

canvas = None

SQUARE_LENGTH = 30
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 2
NUMBER = 20
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
open_cells = []
cells = []
BLUE = 1
YELLOW = 2
GREEN = 3

def set_field():
  global cells
  canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"], LENGTH + POSITION["y"], fill='snow', width=BORDER_WIDTH)

  for i in range(NUMBER - 1):
    x = POSITION["x"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    y = POSITION["y"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    canvas.create_line(x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH)
    canvas.create_line(POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH)
  cells = [[0]* NUMBER for i in range(NUMBER)]

def color_blocks(kind, x, y):
  center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
  center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2

  canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="#fff", width=0)

  if kind != None:
   if cells[x][y] == BLUE: 
      canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="deep sky blue", width=0)
      
   if cells[x][y] == YELLOW:
      canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="gold", width=0)
      
   if cells[x][y] == GREEN:
      canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="lawn green", width=0)


def color_blocks_set():
  count = 0
  while True:
    x = random.randint(0,NUMBER -1)
    y = random.randint(0,NUMBER -1)

    i = random.randint(1, 3)
    if cells[x][y] == 0:
    
      if i == 1:
        cells[x][y] = BLUE
        color_blocks("blue",x,y)

      if i == 2:
        cells[x][y] = YELLOW
        color_blocks("yellow",x,y)
      if i == 3:
        cells[x][y] = GREEN
        color_blocks("green",x,y)

      count += 1

      if count == 400:
          break
    #print(cells) 


# (i, j)を選択した時４方向を判定し続ける
def search(x, y):

  color = cells[x][y] #cellsの中に入っている数字をcolorに渡す
  
  q = queue.Queue()
  q.put((x, y))#基準を追加
  
  

  while not q.empty():#queueに何か入っている時
    x, y = q.get()
    color_blocks(None,x,y)
    cells[x][y] = 0#白くしてcellsに0を渡す

    #盤上にあってcellsの中身が基準と同じ時探索し続ける
    
    if 0 <= x < NUMBER and 0 <= y - 1 < NUMBER and cells[x][y - 1] == color:
      q.put((x, y - 1))

    if 0 <= x < NUMBER and 0 <= y + 1 < NUMBER and cells[x][y + 1] == color:
      q.put((x, y + 1))

    if 0 <= x - 1 < NUMBER and 0 <= y < NUMBER and cells[x - 1][y] == color:
      q.put((x - 1, y))

    if 0 <= x + 1 < NUMBER and 0 <= y < NUMBER and cells[x + 1][y] == color:
      q.put((x + 1, y))

  #print(cells)


# 上から詰める
# 新しい並びにする。行の中で白いマスをカウントして白いマスを上に、色付きのマスを下に配置し直す
def press_up():

  for col in range(NUMBER):

    new_color = [] # 行の新しい並びを作る
    white_count = 0 # 行の中で白いマスをカウントする

    for row in range(NUMBER):

      current_color = cells[col][row]#どこでもok👌

      if current_color == 0:
        white_count += 1
      else:
        new_color.append(cells[col][row])#色付きだったら並びに入れる
        
    new_color = [None] * white_count + new_color#上に今までカウントした白がきてしたには色付きブロックが配置される
    print(new_color)
    

    # new_colorの配置は数字だからそれぞれに色を付けていく
    for i in range(NUMBER): 

      if new_color[i] == BLUE:
        cells[col][i] = BLUE
        color_blocks("blue",col,i)
      if new_color[i] == YELLOW:
        cells[col][i] = YELLOW
        color_blocks("yellow",col,i)
      if new_color[i] == GREEN:
        cells[col][i] = GREEN
        color_blocks("green",col,i)
      if new_color[i] == None:
        cells[col][i] = 0
        color_blocks(None, col, i)



#　行に空きが出来たら左に詰める
#  NUMBER分真っ白な行が出来たらまるまる1行分右端に追加
def press_right():
  global cells

  new_cells = []
  white_col_count = 0
  # 行の白いマスをカウントしてNUMBER分揃ったらwhite_col_count += 1右端にプラスする

  for col in range(NUMBER):

    white_count = 0

    for row in range(NUMBER):

      if cells[col][row] == 0:
        white_count += 1

    if white_count == NUMBER:
      white_col_count += 1
    else:
      new_cells.append(cells[col])
  #print(new_cells)

  for _ in range(white_col_count):

    new_cells.append([0] * NUMBER)

  cells = new_cells

  for x in range(NUMBER):
    for y in range(NUMBER):
      if cells[x][y] == BLUE:
        color_blocks('blue', x, y)
      if cells[x][y] == GREEN:
        color_blocks('green', x, y)
      if cells[x][y] == YELLOW:
        color_blocks('yellow', x, y)
      if cells[x][y] == 0:
        color_blocks(None, x, y)

# ゲームオーバー時に表示(最後にブロックが残ってしまった時)
def game_over():
  messagebox.showinfo('Title','Game Over')
#　ゲームクリア時に表示（ブロックを全部消せた時)
def game_clear():
  messagebox.showinfo('Title','Game Clear')


#マスの中身が全部0
def game_clear_check():
  for x in range(NUMBER):
    for y in range(NUMBER):
      if not cells[x][y] == 0:
        return
      
  game_clear()  
#マスの中身が全部0ではない、４方向に同じ色がない、隣にマスがない場合調べなくていい (まだ探せる時return)
def game_over_check():
  for x in range(NUMBER):
    for y in range(NUMBER):
      if not cells[x][y] == 0:
        #if not(not cells[x][y] == cells[x - 1][y]) and ((x == (NUMBER - 1) or not cells[x][y] == cells[x + 1][y])) and (not cells[x][y] == cells[x][y - 1]) and ((y == (NUMBER - 1) or not cells[x][y] == cells[x][y + 1])):
        if (cells[x][y] == cells[x - 1][y]) or (x != NUMBER - 1 and cells[x][y] == cells[x + 1][y]) or (cells[x][y] == cells[x][y - 1]) or (y != NUMBER - 1 and cells[x][y] == cells[x][y + 1]) :
          return
  game_over()



def point_to_numbers(event_x, event_y):
    x = math.floor((event_x - POSITION["x"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    y = math.floor((event_y - POSITION["y"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    return x, y
 
def create_canvas():
  root = tk.Tk()
  root.geometry(f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
  root.title("samegame")
  canvas = tk.Canvas(root, width=(LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
  canvas.place(x=0, y=0)

  return root, canvas

#左クリックでマスが開く
def left_click(event):
  x, y = point_to_numbers(event.x, event.y)

  #　消えない時はどういう時か？　→　　4方向隣が違う色 or 隣にマスがない 左隣、右隣、上、下
  if (not cells[x][y] == cells[x - 1][y]) and ((x == (NUMBER - 1) or not cells[x][y] == cells[x + 1][y])) and (not cells[x][y] == cells[x][y - 1]) and ((y == (NUMBER - 1) or not cells[x][y] == cells[x][y + 1])):
        return
  

  search(x,y)
  press_up()
  press_right()
  game_over_check()
  game_clear_check()



def play():
  global canvas
  root, canvas = create_canvas()
  set_field()
  
  color_blocks_set()

  canvas.bind("<Button-1>", lambda event: left_click(event))#左クリック
  root.mainloop()
  
play()



