import re

def FindParenthesis(input: str):
    s = input.find(r"\left(")
    while s != -1:
        ParenStart = s
        ParenCount = 0
        while True:
            lefts = input.find(r"\left(",s)
            rights = input.find(r"\right)",s)
            print(lefts,rights)
            s = min(lefts,rights,key=lambda x: x if x != -1 else 99999)
            if s == lefts:
                print("found left")
                ParenCount += 1 
            else:
                print("found rights")
                ParenCount -= 1
            print(ParenCount)
            print("~~~~~~~~~~~~~~~")
            if ParenCount == 0:
                break
            s += 1
        #InnerPeren = input[ParenStart+6:s]
        InnerPeren = input[ParenStart:s+7]
        #5+3+\left(1+0.5\right)^{\left(3+5^{2}\right)}
        print("yeeoo", InnerPeren)
        print(input[:ParenStart],input[ParenStart+6:s],input[s+7:],input)
        input = input[:ParenStart] + str(CalcLatex(input[ParenStart+6:s])) + input[s+7:]
        #input = input.replace(InnerPeren,str(CalcLatex(InnerPeren))) # might need to be replace by removing the text and adding the new value in like input = input[:ParenStart] + str(CalcLatex(input[ParenStart+6:s])) + input[-s:]
        print("Back to parentheses", input)
        s = input.find(r"\left(")
    return input

def TokenizeInput(input: str, index: int = 0):
    print(input,index)
    tokenlist = []
    substring = ""
    while True:
        substring += input[index]
        print(substring, index,input)
        if re.fullmatch(r'\d+(\.\d+)?[^\d\.]',substring): # Look for numbers 5.23242 
            print("dding number", float(substring[:-1]))
            tokenlist.append(float(substring[:-1]))
            substring = ""
            continue
        elif re.fullmatch(r'[\+\-\^]',substring): # Look for simple tokens + or - or ^
            tokenlist.append(substring)
            substring = ""
        elif re.fullmatch(r'\\\w+[\\ \{]',substring): # Look for work function \cdot
            tokenlist.append(substring[:-1])
            substring = ""
            continue
        elif substring == '{': # Find curly start
            print("Found Curly Start")
            tokeneess, index = TokenizeInput(input,index+1)
            print("Printererrr",tokeneess)
            tokenlist.append(tokeneess)
            print(substring,input[index])
            substring = ""
        elif substring == '}': # Curly end
            print("returning tokenlist", input, tokenlist, index)
            return tokenlist, index
        index += 1
        if index == len(input):
            print("done finding tokens", input)
            return tokenlist

TokenArrangement = [
    "", # This is for praenthesis i can change this later
    r"\^", # expontents
    r"(\\cdot)|(\\frac)|[\*\/]", # Mult
    r"\\sin", # Here goes all functions
    r"[\+-]" # ddition
]
5/3
def EvaluteTokens(tokenlist: list, index: int):
    token = tokenlist[index]
    print(tokenlist,token,index)
    if token == "^":
        tokenlist[index] = pow(tokenlist[index-1],tokenlist[index+1])
        del tokenlist[index-1]
        del tokenlist[index]
    if token == "+":
        tokenlist[index] = tokenlist[index-1] + tokenlist[index+1]
        del tokenlist[index-1]
        del tokenlist[index]
    return tokenlist

def DoMath(tokenlist: list):
    # PEMDAS
    #look for lists
    index = 0
    tokentype = 0
    while True:
        #for index,token in enumerate(tokenlist):
        token = tokenlist[index]
        if type(token) == list:
            tokenlist[index] = DoMath(token)
            index -= 1
        elif type(token) != float and re.fullmatch(TokenArrangement[tokentype],token):
            tokenlist = EvaluteTokens(tokenlist, index)
            index -= 1
            print(tokenlist)
        index += 1
        print(tokentype, index, tokenlist, token, end = " ")
        if type(token) == str:
            print(re.fullmatch(TokenArrangement[tokentype],token))
        else:
            print("")
        if index >= len(tokenlist):
            index = 0
            tokentype += 1
        if tokentype == len(TokenArrangement):
            return tokenlist[0]

def CalcLatex(input: str):
    # Look for perentheseseses
    #5+3\cdot\frac{1}{x}\cdot\frac{1}{x}\cdot\sqrt{\frac{1}{x}}\cdot8+3\cdot5^{3}+8^{2+3}
    #4\cdot t
    input = FindParenthesis(input)
    
    input = TokenizeInput(input + " ")
    #input = [8.0, '+', 9.0, '+', 3.0, "^", [2.0, "+", 3.0]]
    print("Finliereroutput", input)
    input = DoMath(input)
    print("Done doin math", input)
    return input
    # turn this 5+3\cdot\frac{1}{x}\cdot\frac{1}{x}\cdot\sqrt{\frac{1}{x}}\cdot8+3\cdot5^{3}+8^{2+3}
    # ? could be sqrt or maybe we can just use words
    # Words is prob better
    #splitt up as each item like this [5,"+",3,"*",["/",[1],["x"]],"*","sqrt", ["/", [1], ["x"]], "*", 8, "+", 3, "*", 5, "^", [3]]
    # and then clean up the lists inside of lists with a CalcLatex recursion AGAIN.
    # to clean up to [5,"+",3,"*","/",1,"x","*","sqrt", "1/x", "*", 8, "+", 3, "*", 5, "^", 3]
    # I guess the 1/x means that i cant reuse a equation just with it simplified like that cause that would be to complicated to keep the 1/x as a piece because the whole point is that it just become a single value... Or not
    # And then i go through pemdas style looking for ^ first and doing it to the previous thing and the one afterwords. Going all the way through with 3 while loops for each part left to right until its a final number
    # I also might need some stuff for nonspecified multiplicated examples 4a becoming [4, "*", "a"] and 4\left(3\right) becoming [4, "*", 3] this wont work with my parenthesis thing. Unless i turn parenthesis into arrays and then go through those
    # or maybe i could add the "\cdot" by detecting it which might work better with like a regex looking for a number next to \left( or a number next to a letter (which wouldnt include opperators cause of the \) or a \right)\left( which would have a mult added inbetween. Or all the other ways it could add one
    # integral would become ["int_",2, "^", 3, [5+3]dx] idk too complicated
    # \int_{2}^{3}5+3dx
    # \cos^{-1}\left(3\right) so we could also look for \cos^{-1} at the start or becuase the {} would go away just look for \cos^-1. But as usual at the start might be easier
    # \sum_{n=1}^{5+3}5n+2 I just realize sum might be a problem cause it cant solve for n so we might need some stuff for that too.
    # \sum_{n=1}^{5+3}\left(5n+2\right)+3
    # WE actualy might need to add a way for it to store the variable so "1/x" would work and we might be able to use that to reuse a equation very quickly
    # But that actualy might get insane with the summation function cause thats like simplifing
    # I also could take a function path where i turn it all into functions

    #input.split()
    #[r"5+3\cdot\frac{1}{x}\cdot",[r"frac{1}{x}"],r"\cdot\sqrt{\frac{1}{x}}\cdot"]
    #[5,"+",3,"*",[[1],"/",["x"]],"*",]


#print(CalcLatex(r"8+9+\left(\left(1+2\right)\left(3+\left(4+5\right)\right)+6+7\right)+10"))
"""substring = "9.\\"
print(re.fullmatch(r'\d+(\.\d+)?[+-\\]',substring))
print(re.fullmatch(r'[\+\-\^]',substring))
print(re.fullmatch(r'\\\w+[\\ \{]',substring))"""
#print(CalcLatex(r"8+9+3^{2+3}+1"), "Final answer")
#print(CalcLatex(r"5+3+\left(1+0.5\right)^{\left(3+5^{2}\right)}"), "Final answer")
print(CalcLatex(r"2+5-6\cdot2\cdot\frac{3^{2}}{2}\cdot\sin\left(5\right)\cdot\cos^{-1}\left(.2\right)\cdot\log\left(3\right)\cdot\log_{4}\left(4\right)\cdot\sqrt[3]{8}"), "Final answer")
#print(CalcLatex(r"2+5-6\cdot2\cdot\frac{3^{2}}{2}\cdot\sin\left(5\right)\cdot\cos^{-1}\left(.2\right)\cdot\log\left(3\right)\cdot\log_{4}\left(4\right)\cdot\sqrt[3]{8}"), "Final answer")
