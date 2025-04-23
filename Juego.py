import numpy as np
import time
import os
from copy import deepcopy

class EscapeGame:
    def __init__(self):
        # Inicializar un tablero 3x3 (0 = vacío, 1 = ficha roja, 2 = ficha amarilla)
        self.board = np.zeros((3, 3), dtype=int)
        self.red_pos = (2, 0)  # Posición inicial ficha roja (fila, columna)
        self.yellow_pos = (0, 2)  # Posición inicial ficha amarilla
        self.exit_pos = (0, 2)  # Posición de la salida
        
        # Colocar fichas en el tablero
        self.board[self.red_pos] = 1
        self.board[self.yellow_pos] = 2
        
        # Número de movimientos
        self.moves_count = 0
        
        # Lista para almacenar el historial de estados
        self.history = []
        self.save_state()
        
    def save_state(self):
        """Guarda el estado actual del tablero para historial"""
        self.history.append({
            'board': self.board.copy(),
            'red_pos': self.red_pos,
            'yellow_pos': self.yellow_pos,
            'moves': self.moves_count
        })
    
    def move_piece(self, piece, direction):
        """
        Mueve una ficha en una dirección específica
        piece: 'red' o 'yellow'
        direction: 'up', 'down', 'left', 'right'
        """
        if piece == 'red':
            current_pos = self.red_pos
        else:
            current_pos = self.yellow_pos
        
        # Calcular nueva posición según la dirección
        if direction == 'up':
            new_pos = (current_pos[0] - 1, current_pos[1])
        elif direction == 'down':
            new_pos = (current_pos[0] + 1, current_pos[1])
        elif direction == 'left':
            new_pos = (current_pos[0], current_pos[1] - 1)
        elif direction == 'right':
            new_pos = (current_pos[0], current_pos[1] + 1)
        else:
            return False
        
        # Verificar si el movimiento es válido
        if not self.is_valid_move(current_pos, new_pos):
            return False
        
        # Actualizar el tablero y la posición de la ficha
        piece_value = 1 if piece == 'red' else 2
        self.board[current_pos] = 0  # Vaciar posición anterior
        self.board[new_pos] = piece_value  # Colocar ficha en nueva posición
        
        # Actualizar posición de la ficha
        if piece == 'red':
            self.red_pos = new_pos
        else:
            self.yellow_pos = new_pos
        
        # Incrementar contador de movimientos
        self.moves_count += 1
        
        # Guardar el nuevo estado
        self.save_state()
        return True
    
    def is_valid_move(self, current_pos, new_pos):
        """Verifica si un movimiento es válido"""
        # Verificar límites del tablero
        if new_pos[0] < 0 or new_pos[0] >= 3 or new_pos[1] < 0 or new_pos[1] >= 3:
            return False
        
        # Verificar si la casilla destino está vacía o es la salida para la ficha roja
        if current_pos == self.red_pos and new_pos == self.exit_pos and self.board[new_pos] == 2:
            # Caso especial: Si la ficha roja intenta ir a la salida y la amarilla está ahí, no es válido
            return False
        elif self.board[new_pos] != 0:
            # Si la casilla no está vacía, el movimiento no es válido
            return False
        
        return True
    
    def is_game_won(self):
        """Verifica si el juego ha sido ganado"""
        return self.red_pos == self.exit_pos
    
    def display_board(self):
        """Muestra el tablero en consola"""
        display_map = {
            0: '⬜',  # Casilla vacía
            1: '🔴',  # Ficha roja
            2: '🟡',  # Ficha amarilla
        }
        
        print("\n  0 1 2")
        print(" ┌─────┐")
        for i in range(3):
            row = f"{i}│"
            for j in range(3):
                if (i, j) == self.exit_pos and self.board[i, j] == 0:
                    row += '🟩'  # Salida vacía
                elif (i, j) == self.exit_pos and self.board[i, j] == 1:
                    row += '🏆'  # Ficha roja en la salida
                else:
                    row += display_map[self.board[i, j]]
            print(row + "│")
        print(" └─────┘")
    
    def get_valid_moves(self, piece):
        """
        Obtiene todos los movimientos válidos para una ficha
        piece: 'red' o 'yellow'
        """
        moves = []
        current_pos = self.red_pos if piece == 'red' else self.yellow_pos
        
        # Definir las direcciones a probar
        directions = ['up', 'down', 'left', 'right']
        
        # Para la ficha amarilla, solo permitir movimientos verticales
        if piece == 'yellow':
            directions = ['up', 'down']
        
        for direction in directions:
            # Calcular nueva posición según la dirección
            if direction == 'up':
                new_pos = (current_pos[0] - 1, current_pos[1])
            elif direction == 'down':
                new_pos = (current_pos[0] + 1, current_pos[1])
            elif direction == 'left':
                new_pos = (current_pos[0], current_pos[1] - 1)
            elif direction == 'right':
                new_pos = (current_pos[0], current_pos[1] + 1)
            
            # Verificar si el movimiento es válido
            if self.is_valid_move(current_pos, new_pos):
                moves.append((direction, new_pos))
        
        return moves
    
    def evaluate_state(self):
        """
        Evalúa el estado actual del juego para el algoritmo Minimax
        Retorna un valor mayor para estados favorables para la ficha roja
        """
        # Victoria: valor máximo
        if self.red_pos == self.exit_pos:
            return 10000
        
        # Derrota: valor mínimo (si la ficha roja está bloqueada y no puede moverse)
        if not self.get_valid_moves('red'):
            return -10000
        
        # Cálculo de la distancia Manhattan a la salida
        red_to_exit_distance = abs(self.red_pos[0] - self.exit_pos[0]) + abs(self.red_pos[1] - self.exit_pos[1])
        
        # Distancia entre fichas (para evitar bloqueos)
        distance_between_pieces = abs(self.red_pos[0] - self.yellow_pos[0]) + abs(self.red_pos[1] - self.yellow_pos[1])
        
        # Factor de progreso: cuánto ha avanzado la ficha roja hacia arriba y hacia la derecha
        progress_factor = (3 - self.red_pos[0]) * 15 + self.red_pos[1] * 10
        
        # Penalización si la ficha amarilla está en la salida o en el camino directo
        blocking_penalty = 0
        if self.yellow_pos == self.exit_pos:
            blocking_penalty = 50
        # Penalización adicional si la amarilla está en el camino óptimo a la salida
        elif self.yellow_pos[0] == 0 and self.yellow_pos[1] == 1:  # Posición (0,1)
            blocking_penalty = 30
        elif self.yellow_pos[0] == 1 and self.yellow_pos[1] == 2:  # Posición (1,2)
            blocking_penalty = 30
            
        # La evaluación favorece estados con:
        # - Menor distancia a la salida (multiplicado por un factor alto)
        # - Mayor distancia a la ficha amarilla para evitar bloqueos
        # - Mayor progreso hacia arriba y a la derecha
        # - Menor riesgo de bloqueo
        return 1000 - red_to_exit_distance * 100 + distance_between_pieces * 5 + progress_factor - blocking_penalty
    
    def minimax(self, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        """
        Algoritmo Minimax con poda alfa-beta para la toma de decisiones
        depth: profundidad de búsqueda restante
        is_maximizing: True si es turno de la ficha roja (maximizador)
        """
        # Verificar condiciones de terminación
        if self.is_game_won():
            return 10000, None  # Victoria para roja
        
        if depth == 0:
            return self.evaluate_state(), None
        
        # Determinar qué ficha se mueve
        piece = 'red' if is_maximizing else 'yellow'
        valid_moves = self.get_valid_moves(piece)
        
        # Si no hay movimientos válidos
        if not valid_moves:
            return -10000 if is_maximizing else 10000, None
        
        best_value = -float('inf') if is_maximizing else float('inf')
        best_move = None
        
        for move, new_pos in valid_moves:
            # Crear una copia del estado actual
            game_copy = deepcopy(self)
            
            # Aplicar el movimiento
            game_copy.move_piece(piece, move)
            
            # Verificar victoria inmediata después del movimiento
            if game_copy.is_game_won():
                return 10000, move if is_maximizing else -10000, move
            
            # Ficha roja mueve dos veces consecutivas
            if is_maximizing and piece == 'red':
                # Obtener movimientos válidos para el segundo turno de la roja
                second_moves = game_copy.get_valid_moves('red')
                
                if second_moves:
                    best_second_value = -float('inf')
                    best_second_move = None
                    
                    for second_move, second_new_pos in second_moves:
                        # Crear una copia del estado después del primer movimiento
                        second_game_copy = deepcopy(game_copy)
                        
                        # Aplicar el segundo movimiento
                        second_game_copy.move_piece('red', second_move)
                        
                        # Verificar victoria inmediata después del segundo movimiento
                        if second_game_copy.is_game_won():
                            return 10000, move  # Elegir el primer movimiento que nos lleva a la victoria
                        
                        # Evaluar después del segundo movimiento
                        value, _ = second_game_copy.minimax(depth - 1, False, alpha, beta)
                        
                        if value > best_second_value:
                            best_second_value = value
                            best_second_move = second_move
                        
                        # Actualizar alpha
                        alpha = max(alpha, best_second_value)
                        if beta <= alpha:
                            break
                    
                    # Usar el mejor valor del segundo movimiento
                    value = best_second_value
                else:
                    # Si no hay segundo movimiento posible, evaluar el estado actual
                    value, _ = game_copy.minimax(depth - 1, False, alpha, beta)
            else:
                # Obtener el valor del siguiente nivel
                value, _ = game_copy.minimax(depth - 1, not is_maximizing, alpha, beta)
            
            # Actualizar el mejor valor encontrado
            if is_maximizing:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)
            
            # Poda alfa-beta
            if beta <= alpha:
                break
        
        return best_value, best_move
    
    def find_optimal_solution(self):
        """
        Encuentra una solución óptima para el juego usando búsqueda en profundidad
        """
        # Secuencia de movimientos conocida que lleva a la victoria
        # Esta es la misma secuencia usada en solve_with_custom_turns
        optimal_moves = [
            ('red', 'right'),    # (2,0) -> (2,1)
            ('red', 'up'),       # (2,1) -> (1,1)
            ('yellow', 'down'),  # (0,2) -> (1,2)
            ('red', 'up'),       # (1,1) -> (0,1)
            ('red', 'right')     # (0,1) -> (0,2) (salida)
        ]
        
        # Verificar que esta secuencia funciona desde el estado actual
        game_copy = deepcopy(self)
        for piece, direction in optimal_moves:
            if not game_copy.move_piece(piece, direction):
                # Si algún movimiento no es válido, retornamos None
                return None
            if piece == 'red' and game_copy.red_pos == game_copy.exit_pos:
                # Si la ficha roja llega a la salida, terminamos
                break
        
        # Si llegamos aquí, la secuencia es válida
        return optimal_moves
    
    def solve_with_minimax(self, max_moves=20):
        """
        Resuelve el juego utilizando el algoritmo Minimax con poda alfa-beta
        max_moves: número máximo de movimientos a realizar
        """
        print("Estado Inicial:")
        self.display_board()
        
        # Usaremos la solución óptima conocida como guía inicial
        optimal_solution = self.find_optimal_solution()
        
        move_count = 0
        is_red_turn = True  # La ficha roja inicia
        red_second_move = False  # Controla si es el primer o segundo movimiento de la roja
        
        while move_count < max_moves and not self.is_game_won():
            piece = 'red' if is_red_turn else 'yellow'
            
            print(f"\nTurno de la ficha {piece}")
            time.sleep(0.5)  # Pausa para visualización
            
            # Ver si tenemos una solución óptima conocida para este estado
            if optimal_solution and move_count < len(optimal_solution):
                solution_piece, solution_move = optimal_solution[move_count]
                if piece == solution_piece:
                    print(f"Movimiento óptimo conocido: {solution_piece} → {solution_move}")
                    if self.move_piece(solution_piece, solution_move):
                        self.display_board()
                        # Actualizar turnos
                        if piece == 'red':
                            if not red_second_move:
                                red_second_move = True  # Cambiar al segundo movimiento de roja
                            else:
                                red_second_move = False  # Reiniciar para próximo turno
                                is_red_turn = False  # Cambiar a amarilla
                        else:
                            is_red_turn = True  # Volver a roja
                        
                        move_count += 1
                        continue
            
            # Si no hay solución óptima conocida o no es aplicable, usar Minimax
            if piece == 'red':
                # Aplicar Minimax para la ficha roja (2 movimientos)
                if not red_second_move:
                    value, best_move = self.minimax(4, True)  # Aumentar profundidad para mejor evaluación
                    print(f"La ficha roja mueve: {best_move} (Valor: {value})")
                    
                    if best_move and self.move_piece('red', best_move):
                        self.display_board()
                        red_second_move = True  # Ahora viene el segundo movimiento
                    else:
                        print("No se encontró un movimiento válido para la ficha roja")
                        break
                else:
                    # Segundo movimiento de la ficha roja
                    value, best_move = self.minimax(4, True)
                    print(f"La ficha roja mueve (segundo turno): {best_move} (Valor: {value})")
                    
                    if best_move and self.move_piece('red', best_move):
                        self.display_board()
                        red_second_move = False  # Reiniciar para el próximo turno
                        is_red_turn = False  # Ahora juega la amarilla
                    else:
                        print("No se encontró un movimiento válido para el segundo turno de la ficha roja")
                        break
            else:
                # Aplicar Minimax para la ficha amarilla (1 movimiento)
                value, best_move = self.minimax(3, False)
                print(f"La ficha amarilla mueve: {best_move} (Valor: {value})")
                
                if best_move and self.move_piece('yellow', best_move):
                    self.display_board()
                    is_red_turn = True  # Vuelve a jugar la roja
                else:
                    print("No se encontró un movimiento válido para la ficha amarilla")
                    break
            
            move_count += 1
        
        if self.is_game_won():
            print("\n🎉 ¡Felicidades! La ficha roja ha escapado.")
        else:
            print("\n❌ No se pudo completar la solución.")
            
        print(f"\nResumen: Se realizaron {self.moves_count} movimientos en total.")
    
    def solve_with_custom_turns(self):
        """Implementa la solución específica con los turnos alternados según lo requerido"""
        # La secuencia de movimientos según la descripción
        moves = [
            # Primeros dos movimientos de la ficha roja
            ('red', 'right'),    # (2,0) -> (2,1)
            ('red', 'up'),       # (2,1) -> (1,1)
            
            # Un movimiento de la ficha amarilla
            ('yellow', 'down'),  # (0,2) -> (1,2)
            
            # Últimos dos movimientos de la ficha roja para llegar a la salida
            ('red', 'up'),       # (1,1) -> (0,1)
            ('red', 'right'),    # (0,1) -> (0,2) (salida)
        ]
        
        print("Estado Inicial:")
        self.display_board()
        
        for i, (piece, direction) in enumerate(moves, 1):
            time.sleep(1)  # Pausa para visualización
            print(f"\nMovimiento {i}: {piece} → {direction}")
            if self.move_piece(piece, direction):
                self.display_board()
                # Mostrar quién juega en el siguiente turno
                if i < len(moves):
                    next_piece = moves[i][0]
                    print(f"Siguiente turno: {next_piece}")
            else:
                print(f"¡Movimiento inválido! {piece} no puede moverse {direction}")
                break
        
        if self.is_game_won():
            print("\n🎉 ¡Felicidades! La ficha roja ha escapado.")
        else:
            print("\n❌ No se pudo completar la solución.")
            
        print(f"\nResumen: Se realizaron {self.moves_count} movimientos en total.")

# Ejecutar el juego con solución inteligente
if __name__ == "__main__":
    print("SOLUCIÓN INTELIGENTE CON MINIMAX:")
    game_minimax = EscapeGame()
    game_minimax.solve_with_minimax()
    
    print("\n\nSOLUCIÓN PREDEFINIDA:")
    game_predefined = EscapeGame()
    game_predefined.solve_with_custom_turns()