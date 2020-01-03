#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thinkpad E570
#
# Created:     03/01/2020
# Copyright:   (c) Thinkpad E570 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    num=407
    if num >1:
        for i in range(2,num):
            if ( num%i ) ==0:
                print(num,"is not a prime number")
                print(i,"times",num//i,"is",num)
                break
        else:
                print(num,"is a prime number")
    else:
        print(num,"is not a prime number")

if __name__ == '__main__':
    main()
