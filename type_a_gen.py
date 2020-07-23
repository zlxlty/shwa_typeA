'''
@Author: Tianyi Lu
@Description: 
@Date: 2020-07-23 14:08:33
@LastEditors: Tianyi Lu
@LastEditTime: 2020-07-23 17:12:04
'''
import random
import xlrd

branch_to_index = {
    'morphology' : 1,
    'pragmatics' : 2,
    'language philosophy' : 3,
    'phonetics' : 4,
    'phonology' : 4,
    'syntax' : 5,
    'historical linguistics' : 6,
    'linguistic typology' : 7,
    'psycholinguistics' : 8,
    'applied linguistics - second language acquisition' : 9,
    'rhetorics' : 10,
    'neuro' : 11,
    'semantics' : 12,
}

class Problem(object):

    def __init__(self, id, diff, branch_list, discrib):
        self.id = id
        self.diff = diff
        self.branch_list = branch_list  # This is a list
        self.discrib = discrib

    def __repr__(self):
        return str(self.id)

def readExcel():
    wb = xlrd.open_workbook(r'A.xlsx')
    sheet1 = wb.sheet_by_index(0)
    branches = [x.strip() for x in sheet1.col_values(6)[1:]]
    diffs = [int(x) for x in sheet1.col_values(13)[1:]]
    discribs = sheet1.col_values(9)[1:]

    if len(branches) != len(diffs):
        print('[error]: Unmatch Numbers of Items!')    

    branch_lists = []
    for i in range(len(branches)):
        branch_lists.append([branch_to_index[x.strip().lower()] for x in branches[i].split('/')])

    return diffs, branch_lists, discribs

def initProblemSet():
    diffs, branch_lists, discribs = readExcel()
    problem_set = []
    for i in range(len(diffs)):
        problem_set.append(Problem(i+1, diffs[i], branch_lists[i], discribs[i]))

    return problem_set

def divideDiffs(problem_set):
    easy_problems = []
    medium_problems = [] 
    hard_problems = []

    for problem in problem_set:
        if problem.diff == 1:
            easy_problems.append(problem)
        elif problem.diff == 2:
            medium_problems.append(problem)
        elif problem.diff == 3:
            hard_problems.append(problem)
        else:
            print("[error]: Unexpected Difficulties")

    return easy_problems, medium_problems, hard_problems

def chooseProblem(num, problems):
    random.shuffle(problems)
    final_choices = []
    exist_branch = []

    for i in range(len(problems)):
        if len(final_choices) >= num:
            break
        if not set(problems[i].branch_list) & set(exist_branch):
            final_choices.append(problems[i])
            for branch in problems[i].branch_list:
                exist_branch.append(branch)

    # print(final_choices)
    # print(exist_branch)

    return final_choices

if __name__ == "__main__":
    problem_set = initProblemSet()
    easy, medium, hard = divideDiffs(problem_set)
    easy_num = round(len(easy)*10/26)
    medium_num = round(len(medium)*10/26)
    hard_num = round(len(hard)*10/26)
    print(easy_num, medium_num, hard_num)

    
    final_problem_sets = []
    for i in range(99):
        final_problems = []
        final_problems.extend(chooseProblem(easy_num, easy))
        final_problems.extend(chooseProblem(medium_num, medium))
        final_problems.extend(chooseProblem(hard_num, hard))

        if problem_set[15] in final_problems:
            if set(final_problems)&set([problem_set[0], problem_set[3], problem_set[9]]):
                continue

        if problem_set[0] in final_problems and problem_set[9] in final_problems:
            continue

        if problem_set[6] in final_problems and problem_set[7] in final_problems:
            continue

        if problem_set[11] in final_problems and problem_set[12] in final_problems:
            continue

        if problem_set[18] in final_problems and problem_set[21] in final_problems:
            continue

        existed = 0
        for final in final_problem_sets:
            if len(set(final)&set(final_problems)) == 10:
                existed = 1

        if not existed:
            final_problem_sets.append(final_problems)

    for final in final_problem_sets:
        final = [x.id for x in final]
        print(final)



    # readExcel()
    # print(branch_to_index['linguistic'])