from fuzzywuzzy import fuzz
from fuzzywuzzy import process

questions_global = [["все возможные ходы", "как я могу походить", "как я могу сходить"]
,["как лучше сходить", "какой лучший ход", "подскажи лучший ход", "как походить"]
,["как ходит конь", "как ходит пешка", "как ходит король"]
,["возможна ли рокировка", "можно ли сделать рокировку"]]

def find_max_ratio(questions, question):
    max = -1
    ans = ""
    for t in questions:
        ratio = fuzz.token_sort_ratio(t, question)
        print(t, ratio)
        if max < ratio:
            max = ratio
            ans = t
    return [questions.index(ans), max]

def find_best_match(question):
    ans = [0, -1]
    indx = 0
    for i in range(len(questions_global)):   
        ret = find_max_ratio(questions_global[i], question)
        if ret[1] > ans[1]:
            ans = ret
            indx = i
    return [indx, ans[1]]



#ans = find_best_match(questions, "рокировка")
#print(questions[ans[0]][ans[1]], ans[2])

@app.route('/get_help_test', methods=['POST'])
def get_help_test():
	json = request.get_json()
	movesfinder = MovesFinder()
	match = questions.find_best_match(json["question"])
	possible_moves = []
	if match[0] == 0:
		possible_moves = movesfinder.get_list_moves(json["board"])
	elif match[0] == 1:
		possible_moves = movesfinder.how_best_move(json["board"])
	answer = "haha"	
	print(possible_moves)
	#json_t = json.
	return ("123", "234")