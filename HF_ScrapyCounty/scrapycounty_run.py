import subprocess
import os
import normal_mode

def main():
    print "-----------------------------------------"
    print "         Welcome to Scrapy County!"
    print "Choose county:"
    print "              -- Essex (E)"
    print "              -- MiddleSex (S)"
    print "              -- Union (U)"
    print "-----------------------------------------"
    num = raw_input("your choice?")
    tab_no = -1
    tab_name = ""
    if num.upper() == 'E':
        tab_no = 0
    elif num.upper() == 'S':
        tab_no = 1
    elif num.upper() == 'U':
        tab_no = 2
    else:
        print "NOT FOUND! "

    print  "Please enter the recent tab name"
    tab_name = raw_input(":")

    normal_mode.normal_mode(tab_no, tab_name)

if __name__ == "__main__":
    main()