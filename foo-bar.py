from operator import attrgetter
import itertools


def foobar1(n):
    b = 2
    converted_n = ""

    while True:
        tmp_n = n
        while tmp_n != 0:
            n_d = tmp_n / b
            n_r = tmp_n % b
            tmp_n = n_d
            converted_n += str(n_r)
        if converted_n == converted_n[::-1]:
            print(b)
            return b
        else:
            converted_n = ""
            b += 1


def foobar2_1(meetings):
    m = [TimeSlot(n[0], n[1]) for n in meetings]

    # nl_1 = []
    # nl_2 = []
    # all_start_times = set([x.s for x in m])
    # all_end_times = set([x.e for x in m])
    #
    # for num in all_start_times:
    #     tmp_list = [t for t in m if t.s == num]
    #     min_duration_time = min(tmp_list, key=attrgetter('d'))
    #     nl_1.append(min_duration_time)
    # for num in all_end_times:
    #     tmp_list = [t for t in nl_1 if t.e == num]
    #     if len(tmp_list) > 0:
    #         min_duration_time = min(tmp_list, key=attrgetter('d'))
    #         nl_2.append(min_duration_time)

    m.sort(key=lambda x: x.e, reverse=False)

    if len(m) <= 1:
        return len(m)
    else:
        tmp_time_slot = m[0]
        final_list = []
        final_list.append(tmp_time_slot)
        for tslot in m[1:]:
            if check_times_overlap(tmp_time_slot, tslot):
                pass
            else:
                final_list.append(tslot)
                tmp_time_slot = tslot
        return len(final_list)


def check_times_overlap(t_1, t_2):
    # returns true if t_2 overlaps or is a subset/superset of t_1, and false if both times can fit in the same schedule
    if t_2.s in range(t_1.s, t_1.e):
        return True
    elif t_2.e in range(t_1.s + 1, t_1.e + 1):
        return True
    elif t_1.s in range(t_2.s, t_2.e):
        return True
    elif t_1.e in range(t_2.s + 1, t_2.e + 1):
        return True
    else:
        return False


class TimeSlot:
    def __init__(self, start, end):
        self.s = start
        self.e = end
        self.d = end - start


def foobar2_2(x):
    # Not knowing exactly how to combat this problem, I began by figuring out the formulas for x=1 until x=15 on paper and
    # seeing if I am able to find a pattern within these formulas. The list is as follows:

    # initial left weight		formula to balance
    # x=1						R
    # x=2						LR
    # x=3						-R
    # x=4						RR
    # x=5						LLR
    # x=6						-LR
    # x=7						RLR
    # x=8						L-R
    # x=9						--R
    # x=10					    R-R
    # x=11					    LRR
    # x=12					    -RR
    # x=13					    RRR
    # x=14					    LLLR
    # x=15					    -LLR

    # We can clearly see now the number of moves needed to balance out the scale is correlated with the given x. Counting moves
    # as either L, -, or R, there are 3^0 = 1 one-move movesets, 3^1 = 3 two-move movesets, 3^2 = 9 three-move movesets, etc.
    # We also can see a pattern involving the repetition of the pattern "L", "-", and "R", in that order. Each moveset also
    # seems to ALWAYS place the last weight on the right hand side (which intuitively makes sense - if you already have weight
    # initially on the left side, the last and heaviest weight MUST go to the right because otherwise the left will always be
    # heavier).

    # Thus, we can figure out, given an x, how many moves it'll take to balance out the scale. For example, given x=15, we know
    # it'll take 4 moves because x is greater than 3^0+3^1+3^2 = 13 but less than or equal to 3^0+3^1+3^2+3^3 = 40. Since we know
    # there are a possible 3^3 = 27 four-move movesets, the first of which starts at x=14, the moveset for x=15 is the second
    # in the list of the 27 possible four-move movesets as demonstrated in the list, because 15-(3^0+3^1+3^2) = 2.
    # Since x=15 has four moves, that means it'll utilize only the first four weights: 3^0, 3^1, 3^2, and 3^3.

    # Using the pattern, we work backwards until we obtain the final formula. Following our example of x=15, we first place "R"
    # as 4th in our character moveset. For the penultimate move, we divide our possible movesets (27) by 3 because we know the first
    # 27/3 = 9 has "L" as the 3rd char, the next 9 has "-" as the 3rd char, and the last 9 has "R" as the 3rd char as it follows
    # the pattern of balance in the list. Since x=15 is the 2nd of 27 possible, it's formula resides within the first 9, i/.e,
    # the penultimate move for x=15 is an "L". Then we move on to find the second character in the formula following the same
    # procedure -- this time dividing 9 into 3 subgroups of three each. Since 2 is within the first subgroup, the second character
    # in the formula is once again "L". Finally, we obtain the first character after dividing 3 into three subgroups and since 2
    # is simply in the second subgroup, we know the first character is a "-". Thus, our formula when read forwards is "-LLR".
    # We can follow the same procedure for any x because we'll always be able to divide into 3 subgroups evenly. We continue
    # until only 3 subgroups of 1 remain, which means we have finished.

    # print("Given number: {}".format(x))

    power = 0
    sum = 0
    while x > sum:
        sum += pow(3, power)
        power += 1

    relative_pos = x - (sum - pow(3, power - 1))
    char_movesets = pow(3, power - 1)
    chars = power
    # print("x ({}) is the {}th number in the list of {} {}-character formulas".format(x, relative_pos, char_movesets, chars))

    formula_backwards = ['R']

    subgroup_cardinal = char_movesets / 3
    while subgroup_cardinal != 0:

        # print(relative_pos)

        if relative_pos <= subgroup_cardinal:
            formula_backwards.append("L")
            subgroup_cardinal /= 3
        elif relative_pos > subgroup_cardinal * 2:
            formula_backwards.append("R")
            relative_pos -= subgroup_cardinal * 2
            subgroup_cardinal /= 3
        else:
            formula_backwards.append("-")
            relative_pos -= subgroup_cardinal
            subgroup_cardinal /= 3

    print(formula_backwards[::-1])
    return formula_backwards[::-1]


def foobar3_1(minions):
    t = []
    minion_count = 0
    for minion in minions:
        time = float(minion[0])
        num = float(minion[1])
        den = float(minion[2])
        calc = time / (num / den)
        t.append((minion_count, calc))
        minion_count += 1

    t.sort(key=lambda x: x[1])
    sorted_final = [mini[0] for mini in t]
    print(sorted_final)
    return sorted_final


def foobar3_2(words):
    letter_graph = []
    letter_map = {}  # dict
    l_word = r_word = ''
    val = position = 0

    if len(words) == 1:  # if there is only one word in the list, return the first letter of that word
        return words[0][0]

    for x in range(len(words) - 1):  # loop up to penultimate word, checking two words at a time (sliding window of n=2)
        l_word = words[x]
        r_word = words[x + 1]
        for y in range(min(len(l_word), len(r_word))):  # make both words the same length of shortest word
            l_letter = l_word[y]
            r_letter = r_word[y]
            if l_letter != r_letter:  # if both letters differ
                v_1 = Vertex(l_letter)
                v_2 = Vertex(r_letter)
                if l_letter not in letter_map and r_letter not in letter_map:  # if both letters not in map list, make vertices and edges for them
                    letter_map[l_letter] = position  # adds letter to dict
                    letter_map[r_letter] = position + 1  # adds letter to dict
                    v_1.edges.append(v_2)  # v_1 directs to v_2 because v_1 is alphabetically less than v_2
                    letter_graph.insert(position, v_1)  # inserts both vertices to graph for later use
                    letter_graph.insert(position + 1, v_2)
                    position += 2  # position increments by 2 because two new vertices added to graph

                elif r_letter in letter_map:  # if right side letter is in map list
                    val = letter_map[r_letter]
                    if l_letter not in letter_map:  # if ONLY right side letter is in map list
                        letter_map[l_letter] = position  # adds letter to dict
                        letter_graph.insert(position, v_1)  # inserts vertex to graph for later use
                        position += 1  # position increments by 1 because only 1 new vertex added to graph
                    letter_graph[letter_map[l_letter]].edges.append(
                        letter_graph[val])  # makes sure "left" vertex directs to "right" vertex

                elif l_letter in letter_map:  # if left side letter is in map list
                    val = letter_map[l_letter]
                    if r_letter not in letter_map:  # if ONLY left side letter is in map list
                        letter_map[r_letter] = position  # adds letter to dict
                        letter_graph.insert(position, v_2)  # inserts vertex to graph for later use
                        position += 1  # position increments by 1 because only 1 new vertex added to graph
                    letter_graph[val].edges.append(v_2)  # makes sure "left" vertex directs to "right" vertex

                # print('Adding {} to {}'.format(v_1.letter, v_2.letter))
                # print([g.letter for g in letter_graph])
                break

            else:
                pass  # if both letters are the same no information is given; move onto the the next respective letters

    # print([g.letter for g in letter_graph])
    return topological_sort_start(letter_graph)


class Vertex:
    visited = False

    def __init__(self, letter):
        self.letter = letter
        self.visited = False
        self.edges = []


def topological_sort(starting_vertex, tl, g):
    starting_vertex.visited = True
    for x in starting_vertex.edges:
        if not x.visited:
            topological_sort(x, tl, g)
    tl.append(starting_vertex.letter)
    return


def topological_sort_start(graph):
    tmp_list = []
    for i in range(len(graph)):
        if not graph[i].visited:
            topological_sort(graph[i], tmp_list, graph)

    # combine the characters of tmp_list and then reverse it because it's in reverse order:
    return ''.join(tmp_list)[::-1]


def foobar3_3(f, g):
    rooms_found = {}

    room_count = 1
    # for row in len(g):
    # tmp_rm = Room(room_count.)

    return


class Room:
    def __init__(self, num, food):
        self.num = num
        self.food = food
        self.visited = False
        self.east_door = None
        self.south_door = None
        self.values = []


if __name__ == "__main__":
    food = 7
    grid = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]
    l = foobar3_3(food, grid)
