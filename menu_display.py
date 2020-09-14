# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 17:38:19 2019

@author: DELL
"""

import curses as cs
import time
import os
import ctypes
import msvcrt
import subprocess

from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)
    
maximize_console() 
menu = ['DARKNET TERROR','PARAGRAF 22','O MNIE','WYJŚCIE']

def center(ekr, menu, current_raw_ix):
    h, w = ekr.getmaxyx()
#    for ix, text in enumerate(menu):
#        if text == menu[current_raw_ix]:
#            idx = ix
    x = w//2 - len(menu[current_raw_ix])//2 - 4
    y = h//2 - len(menu)//2 + current_raw_ix
    return [y, x]

def print_menu(ekr, current_raw_ix):
    ekr.clear()
    h, w = ekr.getmaxyx()
    
    for ix, text in enumerate(menu):
        x = w//2 - len(text)//2
        y = h//2 - len(menu)//2 + ix
        if ix == current_raw_ix:
            ekr.attron(cs.color_pair(1))
            ekr.addstr(y, x, text)
            ekr.attroff(cs.color_pair(1))
        else: 
            ekr.addstr(y, x, text)
        
    ekr.refresh()
    
    
def main(ekr):
    cs.curs_set(0)
    cs.init_pair(1, cs.COLOR_BLACK, cs.COLOR_WHITE)
    current_raw_ix = 0

    print_menu(ekr, current_raw_ix)
    #ryj = open("asciiRyj80.txt", 'r')
    ryj = open("temp.txt", 'r')
    ryj2 = "".join(ryj.readlines())
    while True:
        key = ekr.getch()
        ekr.clear()
        if key == cs.KEY_UP and current_raw_ix > 0: 
            current_raw_ix -= 1
        elif key == cs.KEY_DOWN and current_raw_ix < len(menu) - 1:
            current_raw_ix += 1
        elif key == cs.KEY_ENTER or key in [10,13]:
            if current_raw_ix == len(menu) - 1:
                break
            y, x = center(ekr, menu, current_raw_ix)
            if current_raw_ix == len(menu) - 2:
                #num_lines = sum(1 for line in ryj)   
                ekr.addstr(y, x, ryj2)
            if current_raw_ix == len(menu) - 3:
                os.startfile("Animacja2.mp4")
                time.sleep(5)
                
            if current_raw_ix == len(menu) - 4:
                os.startfile("Animacja.wmv")
                time.sleep(3)
                
            ekr.getch()

        print_menu(ekr, current_raw_ix)

cs.wrapper(main)