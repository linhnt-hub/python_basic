#-------------------------------------------------------------------------------
# Name:        push
# Purpose:
#
# Author:      linhnt
#
# Created:     03/01/2020
# Copyright:   (c) Thinkpad E570 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def get_commands(vlan, name):
        """
        Get command to configure a VLAN
        Agrs:
            vlan(int): vlan id
            name(str): name of the vlan
        Returns:
            List of commands is returned
        """
        commands=[]
        commands.append('vlan '+vlan)
        commands.append('name '+name)
        return commands

