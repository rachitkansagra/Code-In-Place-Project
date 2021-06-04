import os , csv, random
from simpleimage import SimpleImage

image = SimpleImage('images/Basic Layout.png')

def image_update(box_num,human,old_move=False):

    str=""
    if human:
        str='images/circle.png'
    else:
        str='images/cross.png'
    shape = SimpleImage(str)

    with open("coordinates/boxnumber.csv") as box:
        next(box) 
        reader = csv.reader(box)
        for line in reader:
            if int(line[0])==box_num:
                x2 = x_location = int(line[1])
                y2 = y_location = int(line[2])

                if not old_move:
                    for y in range(shape.height):
                        x2=x_location
                        for x in range(shape.width):
                            pixel = shape.get_pixel(x,y)
                            if human:
                                if pixel.green<50:
                                    pixel.green=0
                                    pixel.blue=255
                                    pixel.red=0
                            else:
                                if pixel.green<128:
                                    pixel.green=215
                                    pixel.blue=0
                                    pixel.red=255

                            image.set_pixel(x2, y2, pixel)
                            x2+=1
                        y2+=1
                    break
                else:
                    for y in range(y2,60+y2):
                        for x in range(x2,60+x2):
                            pixel = image.get_pixel(x,y)
                            if pixel.green==215 and pixel.blue==0 and pixel.red==255 :
                                pixel.green=0
                                pixel.blue=0
                                pixel.red=255
                    break

def EnterMove(board):

    r=c=0
    flag=False
    print("")
    x = input("It's your move. Enter a number of an empty box : ")
    
    while True:
    
        if x.isnumeric() and int(x)>0 and int(x)<10:
            
            if x=="1":    
                r=c=0
            elif x=="2":
                r=0
                c=1
            elif x=="3":
                r=0
                c=2
            elif x=="4":
                r=1
                c=0
            elif x=="5":
                r=1
                c=1
            elif x=="6":
                r=1
                c=2
            elif x=="7":
                r=2
                c=0
            elif x=="8":
                r=2
                c=1
            elif x=="9":
                r=2
                c=2
            flag=True
        else:
            print("")
            x=input("Invalid Input. Enter again: ")
            continue

        if flag:        
            if board[r][c]=="X" or board[r][c]=="O":
                print("")
                x=input("Invalid Input. Enter again: ")
                continue
            else:
                board[r][c]="O"
                break
    image_update(int(x),True)
    return board

def DrawMove(board,bot_selection):

    if bot_selection == 1:
        r=c=0
        x = str(random.randint(1,9))
        flag=False
        while True:
            if x=="1":    
                r=c=0
            elif x=="2":
                r=0
                c=1
            elif x=="3":
                r=0
                c=2
            elif x=="4":
                r=1
                c=0
            elif x=="5":
                r=1
                c=1
            elif x=="6":
                r=1
                c=2
            elif x=="7":
                r=2
                c=0
            elif x=="8":
                r=2
                c=1
            elif x=="9":
                r=2
                c=2
            flag=True
            if flag:      
                if board[r][c]=="X" or board[r][c]=="O":
                    x= str(random.randint(1,9))
                    continue
                else:
                    board[r][c]="X"
                    break

    elif bot_selection == 2:
    
        bestMove = findBestMove(board)

        r = bestMove[0]
        c = bestMove[1]

        x = board[r][c]
        board[r][c]="X"

    image_update(int(x),False)
    lst = [board,int(x)]
    return lst

def isMovesLeft(board) :

    for i in range(3) :
        for j in range(3) :
            if (board[i][j] != 'X' and board[i][j] != "O") :
                return True
    return False

def evaluate(b) :

    for row in range(3) :	
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :	
            if (b[row][0] == "X") :
                return 10
            elif (b[row][0] == "O") :
                return -10

    for col in range(3) :
    
        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
        
            if (b[0][col] == "X") :
                return 10
            elif (b[0][col] == "O") :
                return -10

    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
    
        if (b[0][0] == "X") :
            return 10
        elif (b[0][0] == "O") :
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
    
        if (b[0][2] == "X") :
            return 10
        elif (b[0][2] == "O") :
            return -10

    return 0

def minimax(board, depth, isMax) :
    score = evaluate(board)

    if (score == 10) :
        return score

    if (score == -10) :
        return score

    if (isMovesLeft(board) == False) :
        return 0

    if (isMax) :	
        best = -1000

        for i in range(3) :
            for j in range(3) :
                
                g = board[i][j]

                if (board[i][j] != 'X' and board[i][j] != "O") :
                
                    board[i][j] = "X"
                    best = max( best, minimax(board,depth + 1,not isMax) )
                    board[i][j] = g
        return best

    else :
        best = 1000

        for i in range(3) :		
            for j in range(3) :
                
                g = board[i][j]

                if (board[i][j] != 'X' and board[i][j] != "O") :

                    board[i][j] = "O"
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = g
        return best

def findBestMove(board) :
    bestVal = -1000
    bestMove = (-1, -1)

    for i in range(3) :	
        for j in range(3) :
            
            g = board[i][j]

            if (board[i][j] != 'X' and board[i][j] != "O") :
            
                board[i][j] = "X"
                moveVal = minimax(board, 0, False)
                board[i][j] = g

                if (moveVal > bestVal) :			
                    bestMove = (i, j)
                    bestVal = moveVal

    return bestMove

def VictoryFor(board, sign):

    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]==sign:
            drawline("horizontal",i)
            return sign

    for i in range(3):
        if board[0][i]==board[1][i]==board[2][i]==sign:
            drawline("vertical",i)
            return sign

    if board[0][0]==board[1][1]==board[2][2]==sign:
        drawline("diagonal1",4)
        return sign
    elif  board[0][2]==board[1][1]==board[2][0]==sign :
        drawline("diagonal2",4)
        return sign

def drawline(direction,line_number):

    with open("coordinates/line.csv") as box:
        next(box) 
        reader = csv.reader(box)
        for line in reader:

            if line[0]==direction and line_number==4:
                if direction =="diagonal1":
                    x_location = int(line[1])
                    y_location = int(line[2])

                    for z in range(x_location-1,x_location+2):
                        y_location = int(line[2])
                        for x in range(z,int(line[3])-1):
                            pixel = image.get_pixel(x,y_location)
                            pixel.green=255
                            pixel.blue=pixel.red=0
                            y_location+=1
                
                else:
                    x_location = int(line[1])
                    y_location = int(line[2])

                    for z in range(x_location-1,x_location+2):
                        y_location = int(line[2])
                        for x in range(z,int(line[3])+1,-1):
                            pixel = image.get_pixel(x,y_location)
                            pixel.green=255
                            pixel.blue=pixel.red=0
                            y_location+=1
                        

            elif line[0]==direction and int(line[1])==line_number:
                x_location = int(line[2])
                y_location = int(line[3])

                if direction=="horizontal":
                    for y in range(y_location-1,y_location+2):        
                        for x in range(x_location,367+x_location):
                            pixel = image.get_pixel(x,y)
                            pixel.green=255
                            pixel.blue=pixel.red=0
                elif direction=="vertical":
                    for x in range(x_location-1,x_location+2):
                        for y in range(y_location,372+y_location):
                                pixel = image.get_pixel(x,y)
                                pixel.green=255
                                pixel.blue=pixel.red=0
                
                break

def final_message(board,winner):

    if winner == "human":

        win = SimpleImage('images/win.png')
        x2=y2=0
        for y in range(0,149):
            x2=0
            for x in range(image.width):
                pixel = win.get_pixel(x2,y2)
                image.set_pixel(x, y, pixel)
                x2+=1
            y2+=1

        for y in range(150,image.height):
            for x in range(image.width):
                pixel = image.get_pixel(x,y)
                if x<99 or x>499 or y<174 or y>574:
                    pixel.green=pixel.blue=pixel.red=0

    elif winner == "computer":

        lose = SimpleImage('images/lose.png')
        x2=y2=0
        for y in range(0,149):
            x2=0
            for x in range(image.width):
                pixel = lose.get_pixel(x2,y2)
                image.set_pixel(x, y, pixel)
                x2+=1
            y2+=1

        for y in range(150,image.height):
            for x in range(image.width):
                pixel = image.get_pixel(x,y)
                if x<99 or x>499 or y<174 or y>574:
                    pixel.green=pixel.blue=pixel.red=0
        
    else:
        tie = SimpleImage('images/tie.png')
        x2=y2=0
        for y in range(0,149):
            x2=0
            for x in range(image.width):
                pixel = tie.get_pixel(x2,y2)
                image.set_pixel(x, y, pixel)
                x2+=1
            y2+=1

        for y in range(150,image.height):
            for x in range(image.width):
                pixel = image.get_pixel(x,y)
                if x<99 or x>499 or y<174 or y>574:
                    pixel.green=pixel.blue=pixel.red=0

    for r in range(3):
        for c in range(3):
            if board[r][c]!= "X" and board[r][c]!= "O":

                box_number = int(board[r][c])
                with open("coordinates/boxnumber.csv") as box:
                    next(box) 
                    reader = csv.reader(box)
                    for line in reader:
                        if int(line[0])==box_number:
                            x2 = x_location = int(line[1])
                            y2 = y_location = int(line[2])
                            for y in range(y2,60+y2):
                                for x in range(x2,60+x2):
                                    pixel = image.get_pixel(x,y)

                                    pixel.green=255
                                    pixel.blue=255
                                    pixel.red=255

                            break

def main():
    board=[]
    board.append(["1","2","3"])
    board.append(["4","5","6"])
    board.append(["7","8","9"])

    winner = "tie"
    box_number = 0

    print("\n")
    print("➡ Welcome to the Game Of :")
    
    print(
        '''
    .___________. __    ______        .___________.    ___       ______        .___________.  ______    _______ 
    |           ||  |  /      |       |           |   /   \     /      |       |           | /  __  \  |   ____|
    `---|  |----`|  | |  ,----' ______`---|  |----`  /  ^  \   |  ,----' ______`---|  |----`|  |  |  | |  |__   
        |  |     |  | |  |     |______|   |  |      /  /_\  \  |  |     |______|   |  |     |  |  |  | |   __|  
        |  |     |  | |  `----.           |  |     /  _____  \ |  `----.           |  |     |  `--'  | |  |____ 
        |__|     |__|  \______|           |__|    /__/     \__\ \______|           |__|      \______/  |_______|
                                                                                                                
        '''
    )

    print("")

    gg = input("Press Enter to read the Rules of the Game : ")

    while True:
        if gg == "":
            print("")
            print("⭐ Rules Of The Game : ")
            print("")
            print("➡ You will be playing against the computer.")
            print("➡ Your symbol would be the Circle(O) and the computer's symbol would be the Cross(X).")
            print("➡ An Image will show the current position of the board. Type the box number in the console to input your next move.")
            print("➡ You will play the First Move.")
            print("➡ Computer's last move will be shown in a Yellow Cross, while the older computer moves will be in Red Crosses.")
            print("")
            print("⭐ It's your time to choose which computer you want to play against: The Random Bot or The AI Bot. ")
            
            bot_selection = input("➡ Type in 1 for the Random Bot Or 2 for the AI Bot (and then press Enter) : ")

            break
        else:
            print()
            gg = input("Wrong Input!! Please try again : ")

    while True:
        if  bot_selection.isnumeric() and (int(bot_selection) == 1 or int(bot_selection) == 2):
            bot_selection = int(bot_selection)
            break
        else:
            print()
            bot_selection = input("Wrong Input!! Please try again : ")
    
    print("")
    player_turn = input("⭐ Type in 1 to play the first move or 2 to play the second move (and then press Enter) : ")

    while True:
        if  player_turn.isnumeric() and (int(player_turn) == 1 or int(player_turn) == 2):
            player_turn = int(player_turn)
            break
        else:
            print()
            player_turn = input("Wrong Input!! Please try again : ")
    
    
    if player_turn == 1:
        image.show()

    while True:
        
        if player_turn == 1:

            board=EnterMove(board)
            z=VictoryFor(board, "O")
            
            if box_number!=0:
                image_update(box_number,False,True)
        
            if z=="O":
                winner = "human"
                break
            
            if not isMovesLeft(board):
                break

            lst=DrawMove(board,bot_selection)
            board= lst[0]
            box_number = lst[1]
        
            z=VictoryFor(board, "X")
            
            if z=="X":
                winner = "computer"
                image_update(box_number,False,True)
                break

            image.show()

        elif player_turn == 2:
            
            lst=DrawMove(board,bot_selection)
            board= lst[0]
            box_number = lst[1]
        
            z=VictoryFor(board, "X")
            
            if z=="X":
                winner = "computer"
                image_update(box_number,False,True)
                break

            if not isMovesLeft(board):
                image_update(box_number,False,True)
                break
            
            image.show()

            board=EnterMove(board)
            z=VictoryFor(board, "O")
            
            if box_number!=0:
                image_update(box_number,False,True)
        
            if z=="O":
                winner = "human"
                break

    final_message(board,winner)
    image.show()

if __name__ == '__main__':
    main()
