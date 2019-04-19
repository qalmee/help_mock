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

    def get_list_moves(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        reslist = list()
        moves = board.legal_moves
        print(board)
        for move in moves:
            self._engine.go(searchmoves=[move], depth=10)
            scr = self._info_handler.info['score'][1].cp
            mate = self._info_handler.info['score'][1].mate
            if mate == 1:
                scrf = 5
            elif mate == -1:
                continue 
            elif scr != None:
                scrf = round(float(scr)/1000, 2)
            reslist.append({'move' : move.uci(), 'score' : scrf})
        reslist.sort(key=lambda p:-p['score'])
        return reslist
    
    def how_best_move(self, sboard):
        return self.get_list_moves(sboard)[0]