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

    def convert_move(self, inp):
        k0 = ord(inp['move'][0]) - ord('a')
        k1 = ord(inp['move'][1]) - ord('1')
        k2 = ord(inp['move'][2]) - ord('a')
        k3 = ord(inp['move'][3]) - ord('1')
        return [[k0, k1], [k2, k3]]

    def get_list_moves(self, sboard):
        board = chess.Board(sboard)        
        self._engine.position(board)
        res = list()
        moves = board.legal_moves
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
            res.append({'move' : move.uci(), 'score' : scrf})
        res.sort(key=lambda p:-p['score'])
        reslist = list()
        for el in res:
            vel = self.convert_move(el)
            if vel[0] not in reslist:
                reslist.append(vel[0])
            if vel[1] not in reslist:
                reslist.append(vel[1])        
        return reslist
    
    def how_best_move(self, sboard):
        res = self.get_list_moves(sboard)
        return [res[0], res[1]]

class CheckFunc:

    def check_castling(self, sboard):
        board = chess.Board(sboard)
        notate = sboard.split(' ')[2]
        req1 = {'K':False, 'Q':False}
        for c in notate:
            req1[c]=True
        if not (req1['K'] or req1['Q']):
            return None
        req2 = {'K':False, 'Q':False}
        for move in board.legal_moves:
            if 'e1c1'==move.uci():
                req2['K'] = True
            elif 'e1g1'==move.uci():
                req2['Q'] = True
        reslist = list()
        if req1['K'] and req2['K']:
             reslist.append([[4, 0], [0, 0]])
        if req1['Q'] and req2['Q']:
             reslist.append([[4, 0], [7, 0]])
        return reslist

    def get_crit(self, sboard):
        figures = sboard.split(' ')[0]
        white = 0.0
        black = 0.0
        for ch in figures:
            if ch == 'R':
                white = white + 5
            elif ch == 'r':
                black = black + 5
            elif ch == 'N':
                white = white + 3
            elif ch == 'n':
                black = black + 3
            elif ch == 'B':
                white = white + 3.5
            elif ch == 'b':
                black = black + 3.5
            elif ch == 'Q':
                white = white + 10
            elif ch == 'q':
                black = black + 10
            elif ch == 'K':
                white = white + 4
            elif ch == 'k':
                black = black + 4
            elif ch == 'P':
                white = white + 1
            elif ch == 'p':
                black = black + 1
        return [white, black]