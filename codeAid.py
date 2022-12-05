import numpy as np
import os


def help(filename):  # receives file name, identifies mistakes in the code, and returns a clear explanation for the user

    # extract code from py file
    filename = str(os.path.dirname(os.path.abspath(__file__))) + "\\" + filename + ".py"
    file = open(filename, 'r')
    body = file.read().split('\n')
    del body[0]
    del body[0]
    body = "\n".join(body)
    if checkStartFinish(body):
        body = startfinish(body)

    # test code for errors
    go = False
    try:
        exec(body)
    except:
        go = True

    # if the code has errors, proceed to error identification

    # divide code into lines, create 2d array which allows for labeling of lines and error description if needed

    if go:
        body2 = body.split('\n')
        lines = np.array([])
        for i in body2:
            if i != '':
                lines = np.append(lines, [i])
        length = len(lines)
        for i in range(length):
            lines = np.append(lines, [False])
        for i in range(length):
            lines = np.append(lines, ["x"])
        lines = np.reshape(lines, (3, length))
        # row 1 - lines of code, row 2 - labeling (true/false = error/not error), line 3 - description if errors exist

        # check each line for errors, label each line according to results
        for i in range(len(lines)):
            try:
                exec(lines[0][i])
            except:
                lines[1][i] = True  # labels true if the code has mistakes
        # use identify_error function to describe the errors in each line of code in which errors exist
        for i in range(len(lines)):
            if lines[1][i]:
                lines[2][i] = identify_error(lines[0][i])

    # add clear print-out of errors


def identify_error(line):  # identifies type of error in a line of code and returns a clear explanation of the error
    ans = ''  # will contain description of error in the given line of code
    try:
        exec(line)
    except NameError:
        ans = ""  # write explanations
    # add additional exception possibilities
    return ans


# in development
def isforloop(lines,
              index):  # if there is a for loop, function finds iteration variable, adds variable definition where the variable is used to avoid redundant NameError identifications
    lst = lines[0][index].split(" ")
    add = np.array(["", False, ""])
    if lst[0] == "for":
        add[0] = str(lst[1]) + "= 0"

    for i in range(index, len(lines)):
        temp = lines[0][i].split(" ")
        for a in temp:
            if a == add[0]:
                lines[0][i] = add + "\n" + lines[0][i]


def startfinish(body):  # receives block of code from file, returns code between start and finish
    index = 0
    body = body.split("\n")
    newbody = np.array([])
    copy = False
    for i in body:
        if i == "# finish":
            copy = False
        if copy:
            newbody = np.append(newbody, [i])
        if i == "# start":
            copy = True
    newbody = "\n".join(newbody)
    return newbody


def checkStartFinish(body):  # checks if start and finish exist
    start = False
    finish = False
    body = body.split("\n")
    for i in body:
        if (i == "# start"):
            start = True
            if (i == "# finish"):
                finish = True
    if start and finish:
        return True


# example for use of function in regular code
# import codeAid
# help()
# your code
