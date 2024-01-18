#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thinkpad E570
#
# Created:     20/01/2020
# Copyright:   (c) Thinkpad E570 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Hello
def main():
    pass
class InputOutString(object):
    def __init__(self):
        self.s=""
    def getString(self):
        self.s=input("Nhap chuoi: ")
    def printString(self):
        print(self.s.upper())
class Person:
    #Dinh nghia lop instance
    name="Person"
    def __init__(self,name=None):
        self.name=name

if __name__ == '__main__':
    main()
    input_str = input("Nhập X, Y: ")
    dimensions=[int(x) for x in input_str.split(',')]
    rowNum=dimensions[0]
    colNum=dimensions[1]
    multilist = [[0 for col in range(colNum)] for row in range(rowNum)]
    print (multilist)

    for row in range(rowNum):
        for col in range(colNum):
            multilist[row][col]= row*col
    print (multilist)

"""
    strObj=InputOutString()
    strObj.getString()
    strObj.printString()
==========================================

    s=input("Nhap vao day so: ")

    d=[]
    t=()
    for i in d:
        d[i]=s.split
    print(d)

    x=int(input("Nhập số cần tính giai thừa: "))
    def fact(x):
        if x==0:
            return 1
        return x*fact(x-1)
    print(fact(x))
"""

