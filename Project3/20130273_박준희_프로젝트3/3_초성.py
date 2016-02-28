__author__ = 'JunHui'

"""
2015 Fall
Formal Languages and Automata

Project 3.
-- 한글 모아쓰기 오토마타 --
-- 초성 우선 방식 --


20130273 JunHui Park

2015.12.09
"""


class Mealy:    # mealy machine을 정의

    def __init__(self, state, symbol, out_symbol, trans, out_function, initial):
        self.state = state
        self.symbol = symbol
        self.out_symbol = out_symbol
        self.trans = trans
        self.out_function = out_function
        self.initial = initial

    def result(self, sigma):        # Mealy machine의 output들을 print하는 함수 (예비 프로젝트 1-2에서 사용되었다)
        current = self.initial      # current state
        next_state = self.initial   # next state
        dead = True                 # dead state

        for i in sigma:
            try:
                self.symbol.index(i)
            except ValueError as e:
                print(e)
                return

            for f in self.trans:
                if f[0][0] == current and f[0][1] == i:
                    next_state = f[1]
                    dead = False
                    break

            for o in self.out_function:
                if o[0][0] == current and o[0][1] == i:
                    print(o[1], end='')
                    break

            current = next_state

            if dead:
                print("not proper input")
                return

        print('')

    def display_hangul(self, sigma):    # 한글 모아쓰기 출력 함수; result()함수를 기반으로 한글 유니코드 계산에 대한 부분이 추가 되었음

        state_list = []
        value_list = []
        index_list = []
        cursor = 0

        current = self.initial          # current state
        next_state = self.initial       # next state
        dead = True                     # dead state

        jaeum_table = {0: 'ㄱ', 1: 'ㄲ', 2: 'ㄴ', 3: 'ㄷ', 4: 'ㄸ', 5: 'ㄹ', 6: 'ㅁ', 7: 'ㅂ',
                       8: 'ㅃ', 9: 'ㅅ', 10: 'ㅆ', 11: 'ㅇ', 12: 'ㅈ', 13: 'ㅉ', 14: 'ㅊ', 15: 'ㅋ', 16: 'ㅌ', 17: 'ㅍ', 18: 'ㅎ'}
        moeum_table = {0: 'ㅏ', 1: 'ㅐ', 2: 'ㅑ', 3: 'ㅒ', 4: 'ㅓ', 5: 'ㅔ', 6: 'ㅕ', 7: 'ㅖ',
                       8: 'ㅗ', 9: 'ㅘ', 10: 'ㅙ', 11: 'ㅚ', 12: 'ㅛ', 13: 'ㅜ', 14: 'ㅝ', 15: 'ㅞ', 16: 'ㅟ', 17: 'ㅠ', 18: 'ㅡ', 19: 'ㅢ', 20: 'ㅣ'}

        # 받침이었던 자음이 초성이 될 때, 초성의 테이블에 맞도록 인덱싱을 다시 해주기 위한 dictionary
        trd_fst = {1:0, 4:2, 7:3, 8:5, 16:6, 17:7, 19:9, 21:11, 22:12, 23:14, 24:15, 25:16, 26:17, 27:18, 2:1, 20:10, 30 : 9,
                   31 : 11, 32 : 2, 33 : 3, 34 : 11,
                   3:9, 5:12, 6:18, 9:0, 10:6, 11:7, 12:9, 13:16, 14:17, 15:18, 18:9}
        # 초성이 받침으로 들어갈 때, 다시 인덱싱 해주기 위한 dcitionary
        fst_trd = {0:1, 2:4, 3:4, 5:8, 6:16, 7:17, 9:19, 11:21, 12:22, 14:23, 15:24, 16:25, 17:26, 18:27, 1:2, 10:20, 30 : 4, 31 : 4, 32 : 8, 33 : 8, 34 : 8}


        # 겹받침이었던 자음이 초성이 될 때, 겹받침의 정보를 이용해 초성의 테이블에 맞도록 인덱싱 해주기 위한 dictionary ;ex) ㄹㅁ = 10(받침) --> ㅁ = 6(초성)
        double_single = {3:9, 5:12, 6:18, 9:0, 10:6, 11:7, 12:9, 13:16, 14:17, 15:18, 18:9}

        double = False                  # 겹받침인지 아닌지 표시
        result = []                     # 이미 완성된 글자들의 리스트

        # 초성, 중성, 받침의 인덱스; 상황에 따라 다름
        ppre_index = 0
        pre_index = 0
        index = 0

        # 지금까지 입력된 글자의 유니코드 값
        code_value = 0
        previous_value = 0

        code_value_temp = 0

        previous = 0

        first = -1
        middle = -1
        last = -1

        current_loc = 0

        result = []

        possible = False

        put_last = False
        double = False

        count = 0

        for i in sigma:

            count += 1
            # 'd' 심볼(delete)가 들어 왔을 때 delete기능을 수행한다
            if i == 'd':
                if current == 'S' or len(state_list) == 0:
                    if code_value != 0 and current == 'S':
                        code_value = 0
                        for k in result:
                            print(k, end='')
                        print(' ', end='')
                    elif len(result) > 1:
                        result.pop()
                        for k in result:
                            print(k, end='')
                        print(' ', end='')
                    elif len(result) == 1:
                        result[0] = []
                    continue

                state_list.pop()
                value_list.pop()
                index_list.pop()

                if current == 'V':
                    current = 'S'
                    code_value = 0
                    for k in result:
                        print(k, end='')
                    print(' ', end='')
                    continue

                if len(state_list) > 0:
                    current = state_list[len(state_list)-1]

                if len(value_list) > 0:
                    code_value = value_list[len(value_list)-1]
                if len(value_list) > 1:
                    previous_value = value_list[len(value_list)-2]

                if len(index_list) > 0:
                    index = index_list[len(index_list)-1]
                if len(index_list) > 1:
                    pre_index = index_list[len(index_list)-2]
                if len(index_list) > 2:
                    ppre_index = index_list[len(index_list)-3]

                for k in result:
                    print(k, end='')
                print(chr(code_value) + ' ', end='')

                continue

            # 알맞은 심볼인지 에러체크
            try:
                self.symbol.index(i)
            except ValueError as e:
                print(e)
                return

            # transition fucntion
            for f in self.trans:
                if f[0][0] == current and f[0][1] == i:
                    next_state = f[1]
                    state_list.append(f[1])
                    dead = False
                    break



            jaeum_table = {0: 'ㄱ', 1: 'ㄲ', 2: 'ㄴ', 3: 'ㄷ', 4: 'ㄸ', 5: 'ㄹ', 6: 'ㅁ', 7: 'ㅂ',
                       8: 'ㅃ', 9: 'ㅅ', 10: 'ㅆ', 11: 'ㅇ', 12: 'ㅈ', 13: 'ㅉ', 14: 'ㅊ', 15: 'ㅋ', 16: 'ㅌ', 17: 'ㅍ', 18: 'ㅎ'}

            first_table_plus = {0 : 15, 2 : 3, 3 : 16, 6 : 7, 7 : 15, 9 : 12, 11 : 18, 12 : 14}
            first_table_double = {0 : 1, 3 : 4, 7 : 8, 9 : 10, 12 : 13}

            middle_table_ee = {0 : 1, 4 : 5, 8 : 11, 6 : 7, 13 : 16, 18 : 19, 2 : 3, 9 : 10, 14 : 15}
            middle_table_plus = {0 : 2, 4 : 6, 8 : 12, 13 : 17}

            last_table_plus = {1 : 24, 4 : 7, 16 : 17, 17 : 26, 19 : 22, 21 : 27, 22 : 23, 30 : 5, 31 : 6 ,32 : 33,33 : 13, 34 : 15}

            last_table_first = {30 : 4, 31 : 4, 32 : 8, 33 : 8, 34 : 8}
            last_table_last = {30 : 19, 31 : 21, 32 : 4, 33 : 7, 34 : 21}
            fin = False

            # output function
            for o in self.out_function:
                if o[0][0] == current and o[0][1] == i:
                    if current_loc == 0 and (o[0][1] == '0' or o[0][1] == '3' or o[0][1] == '6' or o[0][1] == '9'):
                        current_loc = 1
                    elif current_loc == 1 and (o[0][1] == '1' or o[0][1] == '2' or o[0][1] == '4' or o[0][1] == '5' or o[0][1] == '7' or o[0][1] == '8'):
                        current_loc = 0
                        possible = True
                        code_value_temp = code_value

                    if (current_loc == 0) and not fin and not possible: ## 초성
                        if o[1] == 200:
                            fin = True
                        elif o[1] != 100 and o[1] != 99:
                            first = o[1]
                        elif o[1] == 100:  ## 획추가
                            first = first_table_plus[first]
                        elif o[1] == 99: ## 쌍자음
                            first = first_table_double[first]

                    elif (current_loc == 1) and not fin: ## 중성
                        if middle == -1: ## 초기 상태
                            middle = o[1]
                        elif o[1] == 101: ## 'ㅣ' 추가
                            middle = middle_table_ee[middle]
                        elif o[1] == 100: ##  획 추가
                            middle = middle_table_plus[middle]
                        elif o[1] == 200:
                            fin = True
                        else:
                            middle = o[1]

                    elif (current_loc == 0) and not fin and possible: ## 종성
                        if last == -1:
                            last = o[1]
                        elif o[1] == 100:
                            if not double:
                                last = last_table_plus[last]
                            else:
                                last = last_table_plus[previous]
                                put_last = True
                        elif o[1] == 200:
                            fin = True
                            possible = False
                        else:
                            last = o[1]
                        if not fin:
                            if not double:
                                if last == 30 or last == 31 or last == 32 or last == 33 or last == 34:
                                    code_value_temp = code_value_temp + fst_trd[last]
                                    double = True
                                previous = last
                                last = trd_fst[last]
                        if fin:
                            if not double:
                                last = fst_trd[last]

                    if current_loc == 0 and not possible and not fin:
                        code_value = ord(jaeum_table[first])
                    elif current_loc == 1:
                        code_value = (first * 588 + middle * 28) + 44032
                    elif current_loc == 0 and possible:
                        if put_last:
                            code_value = (first * 588 + middle * 28 + last) + 44032
                            code_value_temp = 0
                            put_last = False
                        else:
                            code_value = ord(jaeum_table[last])
                    elif current_loc == 0 and fin:
                        if last == 30 or last == 31 or last == 32 or last == 33 or last == 34:
                            code_value_temp = (first * 588 + middle * 28 + last_table_first[last]) + 44032
                            code_value = ord(jaeum_table[last_table_last[last]])
                        else :
                            if not double:
                                code_value = code_value_temp + last
                            code_value_temp = 0

                    if fin:
                        first = -1
                        middle = -1
                        last = -1
                        current_loc = 0
                        result.append(chr(code_value))
                        if count == len(sigma):
                            for i in result:
                                    print(i, end='')
                            print(' ', end='')
                        double = False
                        break

                    if last != 30 and last != 31 and last != 32 and last != 33 and last != 34:
                        for i in result:
                            print(i, end='')
                        if code_value_temp != 0:
                            print(chr(code_value_temp), end='')
                        print(chr(code_value) + ' ', end='')

            current = next_state

            if dead:
                print("not proper input")
                return


# define Hangul automata (mealy machine)
H = Mealy(
    # set of states
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    # input symbols
    ['#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'f', '~'],
    # output symbols
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    # transition function
    [[[0, '1'], 1], [[0, '2'], 2], [[0, '4'], 3], [[0, '5'], 2], [[0, '7'], 4], [[0, '8'], 5], [[1, '#'], 3],
     [[1, '0'], 6], [[1, '3'], 7], [[1, '6'], 8], [[1, '9'], 9], [[1, '~'], 3], [[2, '0'], 6], [[2, '3'], 7],
     [[2, '6'], 8], [[2, '9'], 9], [[2, '~'], 1], [[3, '0'], 6], [[3, '3'], 7], [[3, '6'], 8], [[3, '9'], 9],
     [[4, '#'], 3], [[4, '0'], 6], [[4, '3'], 7], [[4, '6'], 8], [[4, '9'], 9], [[4, '~'], 1], [[5, '0'], 6],
     [[5, '3'], 7], [[5, '6'], 8], [[5, '9'], 9], [[5, '~'], 3], [[6, '1'], 10], [[6, '2'], 11], [[6, '4'], 12],
     [[6, '5'], 13], [[6, '7'], 14], [[6, '8'], 15], [[6, '9'], 9], [[6, 'f'], 0], [[7, '1'], 10], [[7, '2'], 11],
     [[7, '3'], 16], [[7, '4'], 12], [[7, '5'], 13], [[7, '7'], 14], [[7, '8'], 15], [[7, '9'], 9], [[7, 'f'], 0],
     [[7, '~'], 6], [[8, '1'], 10], [[8, '2'], 11], [[8, '3'], 6], [[8, '4'], 12], [[8, '5'], 13], [[8, '6'], 17],
     [[8, '7'], 14], [[8, '8'], 15], [[8, '9'], 9], [[8, 'f'], 0], [[8, '~'], 9], [[9, '1'], 10], [[9, '2'], 11],
     [[9, '4'], 12], [[9, '5'], 13], [[9, '7'], 14], [[9, '8'], 15], [[9, 'f'], 0], [[10, '#'], 18], [[10, '7'], 18],
     [[10, 'f'], 0], [[10, '~'], 18], [[11, '7'], 19], [[11, '8'], 19], [[11, 'f'], 0], [[11, '~'], 15], [[12, '1'], 18],
     [[12, '2'], 20], [[12, '5'], 21], [[12, '7'], 18], [[12, '8'], 19], [[12, 'f'], 0], [[13, 'f'], 0], [[13, '~'], 22],
     [[14, '#'], 18], [[14, 'f'], 0], [[14, '~'], 15], [[15, 'f'], 0], [[15, '~'], 18], [[16, '1'], 10], [[16, '2'], 11],
     [[16, '4'], 12], [[16, '5'], 13], [[16, '7'], 14], [[16, '8'], 15], [[16, '9'], 9], [[16, 'f'], 0], [[16, '~'], 6],
     [[17, '1'], 10], [[17, '2'], 11], [[17, '3'], 6], [[17, '4'], 12], [[17, '5'], 13], [[17, '7'], 14], [[17, '8'], 15],
     [[17, '9'], 9], [[17, 'f'], 0], [[17, '~'], 9], [[18, 'f'], 0], [[19, '~'], 18], [[20, '~'], 19], [[21, 'f'], 0],
     [[21, '~'], 15], [[22, '7'], 18], [[22, 'f'], 0]],
    # output function
    [[[0, '1'], 0], [[0, '2'], 2], [[0, '4'], 5], [[0, '5'], 6], [[0, '7'], 9], [[0, '8'], 11], [[1, '#'], 99],
     [[1, '0'], 18], [[1, '3'], 0], [[1, '6'], 8], [[1, '9'], 20], [[1, '~'], 100], [[2, '0'], 18], [[2, '3'], 0],
     [[2, '6'], 8], [[2, '9'], 20], [[2, '~'], 100], [[3, '0'], 18], [[3, '3'], 0], [[3, '6'], 8], [[3, '9'], 20],
     [[4, '#'], 99], [[4, '0'], 18], [[4, '3'], 0], [[4, '6'], 8], [[4, '9'], 20], [[4, '~'], 100], [[5, '0'], 18],
     [[5, '3'], 0], [[5, '6'], 8], [[5, '9'], 20], [[5, '~'], 100], [[6, '1'], 1], [[6, '2'], 4], [[6, '4'], 8],
     [[6, '5'], 16], [[6, '7'], 19], [[6, '8'], 21], [[6, '9'], 101], [[6, 'f'], 200], [[7, '1'], 1], [[7, '2'], 4],
     [[7, '3'], 4], [[7, '4'], 8], [[7, '5'], 16], [[7, '7'], 19], [[7, '8'], 21], [[7, '9'], 101], [[7, 'f'], 200],
     [[7, '~'], 100], [[8, '1'], 1], [[8, '2'], 4], [[8, '3'], 9], [[8, '4'], 8], [[8, '5'], 16], [[8, '6'], 13],
     [[8, '7'], 19], [[8, '8'], 21], [[8, '9'], 101], [[8, 'f'], 200], [[8, '~'], 100], [[9, '1'], 1], [[9, '2'], 4],
     [[9, '4'], 8], [[9, '5'], 16], [[9, '7'], 19], [[9, '8'], 21], [[9, 'f'], 200], [[10, '#'], 2], [[10, '7'], 3],
     [[10, 'f'], 200], [[10, '~'], 24], [[11, '7'], 30], [[11, '8'], 31], [[11, 'f'], 200], [[11, '~'], 100], [[12, '1'], 9],
     [[12, '2'], 32], [[12, '5'], 10], [[12, '7'], 12], [[12, '8'], 34], [[12, 'f'], 200], [[13, 'f'], 200], [[13, '~'], 100],
     [[14, '#'], 20], [[14, 'f'], 200], [[14, '~'], 100], [[15, 'f'], 200], [[15, '~'], 100], [[16, '1'], 1], [[16, '2'], 4],
     [[16, '4'], 8], [[16, '5'], 16], [[16, '7'], 19], [[16, '8'], 21], [[16, '9'], 101], [[16, 'f'], 200], [[16, '~'], 100],
     [[17, '1'], 1], [[17, '2'], 4], [[17, '3'], 14], [[17, '4'], 8], [[17, '5'], 16], [[17, '7'], 18], [[17, '8'], 21],
     [[17, '9'], 101], [[17, 'f'], 200], [[17, '~'], 100], [[18, 'f'], 200], [[19, '~'], 100], [[20, '~'], 100], [[21, 'f'], 200],
     [[21, '~'], 100], [[22, '7'], 18], [[22, 'f'], 200]],
    0)

while True:
    print('####초성 우선 입력 방식 입니다####')

    a = input("입력 : ")
    H.display_hangul(a)
    print()


