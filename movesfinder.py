import pdb
import chess
import chess.uci
import chess.engine

class MovesFinder:

    def __init__(self):
        self._engine = chess.uci.popen_engine('stockfish.exe')
        self._engine.uci()
        self._info_handler=chess.uci.InfoHandler()
        self._engine.info_handlers.append(self._info_handler)

    def get_list_moves(self, board):
        self._engine.position(board)
        reslist = list()
        moves = board.legal_moves
        for move in moves:
            self._engine.go(searchmoves=[move], depth=5)
            scr = self._info_handler.info['score'][1].cp
            scrf = round(float(scr)/1000, 2)
            reslist.append({'move' : move.uci(), 'score' : scrf})
        reslist.sort(key=lambda p:-p['score'])
        return reslist
    
    def how_best_move(self, board):
        return self.get_list_moves(board)[0]