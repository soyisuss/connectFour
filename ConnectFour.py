import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((450,450))
pygame.display.set_caption("Connect4")

fondo = pygame.image.load('static/Board.jpg')
ficha1 = pygame.image.load('static/dona1.png')
ficha2 = pygame.image.load('static/dona2.png')

fondo = pygame.transform.scale(fondo,(450,450))
ficha1 = pygame.transform.scale(ficha1, (50,50))
ficha2 = pygame.transform.scale(ficha2, (50,50))

coor = [[(21,31),(81,31),(141,31),(201,31),(260,31),(320,31),(380,31)],
        [(21,99),(81,99),(141,99),(201,99),(260,99),(320,99),(380,99)],
        [(21,167),(81,167),(141,167),(201,167),(260,167),(320,167),(380,167)],
        [(21,235),(81,235),(141,235),(201,235),(260,235),(320,235),(380,235)],
        [(21,302),(81,302),(141,302),(201,302),(260,302),(320,302),(380,302)],
        [(21,369),(81,369),(141,369),(201,369),(260,369),(320,369),(380,369)]]

board = [['','','','','','',''],
         ['','','','','','',''],
         ['','','','','','',''],
         ['','','','','','',''],
         ['','','','','','',''],
         ['','','','','','','']]

turno = 'IA'
game_over = False
clock = pygame.time.Clock()

def graficarBoard():
    screen.blit(fondo, (0,0))
    for fila in range (6):
        for col in range (7):
            if board[fila][col] == 'x':
                dibujar_x(fila,col)
            elif board[fila][col] == 'IA':
                dibujar_o(fila,col)

def dibujar_x (fila,col):
    screen.blit(ficha1, coor[fila][col])

def dibujar_o (fila,col):
    screen.blit(ficha2, coor[fila][col])

def verificarGanador():
    # Verificar en horizontal
    for i in range(6):
        for j in range(4):  # Cambiado de 7 a 4 para evitar el desbordamiento de índice
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] != '':
                return True
    
    # Verificar en vertical
    for i in range(3):  # Cambiado de 6 a 3 para evitar el desbordamiento de índice
        for j in range(7):
            if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] != '':
                return True

    # Verificar diagonales descendentes
    for i in range(3):  # Cambiado de 6 a 3 para evitar el desbordamiento de índice
        for j in range(4):  # Cambiado de 7 a 4 para evitar el desbordamiento de índice
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] != '':
                return True

    # Verificar diagonales ascendentes
    for i in range(3):  # Cambiado de 6 a 3 para evitar el desbordamiento de índice
        for j in range(3, 7):  # Cambiado de 0 a 3 para evitar el desbordamiento de índice
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] != '':
                return True

    return False

def generarMovimientos():
    movimientos = []
    for col in range(7):
        for fila in range(6):
            if board[fila][col] == '':
                movimientos.append((fila, col))
                break
    return movimientos

def evaluarTablero():
    # Evaluación simple: contar el número de fichas en línea para cada jugador
    puntos = 0
    for i in range(6):
        for j in range(4):
            if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 'IA':
                puntos += 100
            elif board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 'x':
                puntos -= 100
    return puntos

def minimax(depth, maximizingPlayer):
    if depth == 0 or verificarGanador():
        return evaluarTablero()

    if maximizingPlayer:
        maxEval = -np.inf
        for movimiento in generarMovimientos():
            fila, col = movimiento
            board[fila][col] = 'IA'
            eval = minimax(depth - 1, False)
            board[fila][col] = ''
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = np.inf
        for movimiento in generarMovimientos():
            fila, col = movimiento
            board[fila][col] = 'x'
            eval = minimax(depth - 1, True)
            board[fila][col] = ''
            minEval = min(minEval, eval)
        return minEval

def encontrarMejorMovimiento():
    bestMove = None
    bestEval = -np.inf
    for col in range(7):
        for fila in range(5, -1, -1):  # Comenzar desde la parte inferior del tablero
            if board[fila][col] == '':
                board[fila][col] = 'IA'
                eval = minimax(4, False)  # Profundidad 3 para el ejemplo, puede ajustarse
                board[fila][col] = ''
                if eval > bestEval:
                    bestEval = eval
                    bestMove = (fila, col)
                break  # Salir del bucle interno para pasar a la siguiente columna
    return bestMove

while not game_over:
    clock_tick=(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if (mouseX >= 16 and mouseX < 436) and (mouseY >= 22 and mouseX < 428):
                col = (mouseX - 16) // 59

                # Actualizar el board con el jugador actual en la columna calculada
                for fila in range(6, 0, -1):  # Comenzar desde la parte inferior del board
                    if board[fila - 1][col] == '':
                        board[fila - 1][col] = turno
                        break
                
                if verificarGanador():
                    if turno == 'IA':
                        print("El ganador es la IA")
                    else:
                        print("El ganador es el usuario")

                    game_over = True
                # Cambiar el turno al siguiente jugador
                turno = 'IA' if turno == 'x' else 'x'

    if turno == 'IA' and not game_over:
        fila, col = encontrarMejorMovimiento()
        board[fila][col] = 'IA'
        if verificarGanador():
            print("El ganador es la IA")
            game_over = True
        turno = 'x'

    graficarBoard()
    pygame.display.update()

pygame.quit
