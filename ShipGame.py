# Project Name: ShipGame

class ShipGame:
    """
    Creates an instance of a game of Battleship.
    """

    def __init__(self):
        """
        Initializes all of the data members for the ShipGame class.
        """
        self._players = {'first': Player(), 'second': Player()}
        self._current_player = "first"
        self._game_state = "UNFINISHED"
        self._board_dim = 9
        self._game_started = False

    def get_players(self):
        """
        Returns the dictionary of players.
        """
        return self._players

    def get_players_board(self, player):
        """
        Returns the board of player requested.
        """
        return self.get_players()[player].display_grid()

    def get_coordinates(self, game_square):
        """
        Returns the coordinates of a given game square as a tuple.
        """
        # determine x-coordinate
        row_coord = ord(game_square[0].lower()) - 97
        # determine y-coordinate
        column_coord = int(game_square[1]) - 1

        # return coordinate
        # row_coord is the row for the letter in the game square
        # column_coord is the number in the game square
        return row_coord, column_coord

    def get_current_player(self):
        """
        Returns the player to which the current turn belongs.
        """
        return self._current_player

    def get_opponent(self):
        """
        Returns the current player's opponent.
        """
        if self.get_current_player() == "first":
            return "second"
        else:
            return "first"

    def update_current_player(self):
        """
        Updates the current player at the end of a turn.
        """
        if self.get_current_player() == "first":
            self._current_player = "second"
        else:
            self._current_player = "first"

    def get_game_state(self):
        """
        Returns the current state of the game.
        """
        return self._game_state

    def update_game_state(self):
        """
        Updates the current state of the game.
        """
        # update winner to player 1 if player 2 has no more ships remaining
        if self.get_num_ships_remaining('second') == 0:
            self._game_state = 'FIRST_WON'
            print("The first player has won!")

        # update winner to player 2 if player 1 has no more ships remaining
        elif self.get_num_ships_remaining('first') == 0:
            self._game_state = 'SECOND_WON'
            print("The second player has won!")

    def place_ship(self, player, ship_length, game_square, orientation):
        """
        Places a ship on the board for the specified player.
        """
        # get the current player's grid
        grid = self.get_players()[player].get_grid()

        # do not allow Players to place ships if a torpedo has been fired
        if self._game_started:
            print("The game has already started! You can't place more ships now.")
            return False

        # return False if ship is too long
        if ship_length > self._board_dim:
            return False

        # get row coordinate
        row_coord = self.get_coordinates(game_square)[0]
        column_coord = self.get_coordinates(game_square)[1]

        # return False if game square is invalid
        if row_coord > self._board_dim or column_coord > self._board_dim:
            print("The game square provided is not valid.")
            return False

        # return False if it is not the current player's turn
        if player != self.get_current_player():
            print("It is not this player's turn.")
            return False

        # return False if ship's length is less than 2
        if ship_length < 2:
            print("The input for the ship's length is invalid.")
            return False

        # check if path for ship placement is clear
        for i in range(ship_length):
            if grid[row_coord][column_coord] == 'x':
                print("You cannot place a ship here; there is another ship placed along this path.")
                return False

        if orientation == 'C':

            # return False if ship would not fit
            if row_coord + ship_length > self._board_dim + 1:
                return False

            # add to Player's roster of ships
            self.get_players()[player].get_ships()[(row_coord, column_coord)] = (ship_length, orientation)

            # place ship on the player's grid
            for i in range(ship_length):
                grid[row_coord][column_coord] = 'x'
                row_coord += 1

        elif orientation == 'R':

            # return False if ship would not fit
            if column_coord + ship_length > self._board_dim + 1:
                return False

            # add to Player's roster of ships
            self.get_players()[player].get_ships()[(row_coord, column_coord)] = (ship_length, orientation)

            # place ship on the player's grid
            for i in range(ship_length):
                grid[row_coord][column_coord] = 'x'
                column_coord += 1

        # add to Player's ship count
        self.get_players()[player].add_ship()

        # update to the next player's turn
        self.update_current_player()

    def get_current_state(self):
        """
        Returns the current state of the game.
        """
        return self._game_state

    def fire_torpedo(self, player, game_square):
        """
        Fires a torpedo at the given coordinate.
        """
        # return False if it is not the player's turn
        if player != self.get_current_player():
            print("Hey -- it's not this player's turn yet!")
            return False

        # return False if the game has already been won
        if self.get_game_state() != "UNFINISHED":
            print("The game has already been won!")
            return False

        # indicate that the game has started
        self._game_started = True

        # get the grid of the opposing player
        opponent_grid = self.get_players()[self.get_opponent()].get_grid()

        # break down the coordinates
        coordinates = self.get_coordinates(game_square)
        x_coord = coordinates[0]
        y_coord = coordinates[1]

        # check if it's a hit and update grid if so
        if opponent_grid[x_coord][y_coord] == 'x':
            print("It's a hit!")
            opponent_grid[x_coord][y_coord] = 'o'

            # check if a torpedo fired results in a ship being sunk
            if self.sunk_ship_check(opponent_grid):
                self.get_players()[self.get_opponent()].delete_ship()
                print("You've sunk a ship!")

        # let player know if they've missed
        elif opponent_grid[x_coord][y_coord] == ' ':
            print("It's a miss!")

        elif opponent_grid[x_coord][y_coord] == 'o':
            print("This spot has already been hit.")

        # update whose turn it is
        self.update_current_player()

        # update the game state
        self.update_game_state()

    def get_num_ships_remaining(self, player):
        """
        Returns the number of ships the specified player has.
        """
        return self.get_players()[player].get_ships_remaining()

    def sunk_ship_check(self, grid):
        """
        Checks if a hit results in a sunken ship.
        """

        # get the dictionary of the opponent's ships
        opponent_ships = self.get_players()[self.get_opponent()].get_ships()

        # check through each of the opponent's ships
        for i in opponent_ships:
            row_coord = i[0]
            column_coord = i[1]
            ship_length = opponent_ships[i][0]
            orientation = opponent_ships[i][1]
            hit_count = 0

            if orientation == 'C':
                # return False if there is still a spot on the ship that hasn't been hit
                for j in range(ship_length):
                    if grid[row_coord][column_coord] == 'o':
                        hit_count += 1
                    row_coord += 1

                if hit_count == ship_length:
                    del opponent_ships[(row_coord - ship_length, column_coord)]
                    return True

            if orientation == 'R':
                # return False if there is still a spot on the ship that hasn't been hit
                for j in range(ship_length):
                    if grid[row_coord][column_coord] == 'o':
                        hit_count += 1
                    column_coord += 1

                if hit_count == ship_length:
                    del opponent_ships[(row_coord, column_coord - ship_length)]
                    return True


class Player:
    """
    Creates an instance of a Player in ShipGame.
    """

    def __init__(self):
        """
        Contains data for the Player's ships remaining, ships lost, ships' positions, and grid.
        """
        self._ships_remaining = 0
        self._ships = {}
        self._grid = [[' '] * 10 for i in range(10)]

    def get_grid(self):
        """
        Returns the game board for manipulation.
        """
        return self._grid

    def display_grid(self):
        """
        Displays the game board for visualization.
        """

        def format_row(row):
            return '|' + '|'.join('{0:^3s}'.format(x) for x in row) + '|'

        def format_board(board):
            return '\n'.join(format_row(row) for row in board)

        print(format_board(self.get_grid()))

    def get_ships_remaining(self):
        """
        Returns the remaining number of ships the player has.
        """
        return self._ships_remaining

    def add_ship(self):
        """
        Increases the number of ships a player has.
        """
        self._ships_remaining += 1

    def delete_ship(self):
        """
        Decreases the number of ships a player has and increases the number of ships lost.
        """
        self._ships_remaining -= 1

    def get_ships(self):
        """
        Returns a dictionary of each ship the player has placed on the board with the game square
        closest to A1 that it occupies as the key and the ship's orientation as its value.
        """
        return self._ships
