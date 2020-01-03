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
    #Sort and delete duplicate value
    vlans_new=[vlan for i,vlan in enumerate(vlans) if vlan not in vlans[i+1:]]
    pass

#a = [{'a': 123}, {'b': 123}, {'a': 123}]
#b = []
#for i in range(0, len(a)):
#    if a[i] not in a[i+1:]:
#        b.append(a[i])



if __name__ == '__main__':
    main()
