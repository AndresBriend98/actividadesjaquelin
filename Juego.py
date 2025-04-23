import numpy as np
import time
import os

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
        
        # Verificar si la casilla destino está vacía
        if self.board[new_pos] != 0:
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

# Ejecutar el juego
if __name__ == "__main__":
    game = EscapeGame()
    game.solve_with_custom_turns()