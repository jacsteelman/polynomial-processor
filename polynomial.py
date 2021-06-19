# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13, 2020 by Jim Carlson.
Last edited on 8 June 2021.

This file is stand-alone and runs under Spyder IDE and IPython.

First, 'Run' this file to activate and when prompted enter

        1    to process multiple pre-defined polynomials - do_mult()

        or

        2    to process user-defined polynomial - do_poly()

Every result of this file has been checked using Wolfram Alpha and
SageMath.

Note: Enter polynomial powers  as  ^  not  ** ; for example enter   x^9 ,
      not   x**9. Enter a number multipled by a variable as  19x  ,
      not   19*x . The replace function transforms the polynomial into
      proper Python format.
      A simple example entry is:   2x^3+25x+2
      which converts to:           2*x**3+25*x+2   for use by Python.
      Spaces are ignored. See more complex entries in function do_mult.

Search for texts    eval(   and   .replace(   to examine instances and
usage of these functions. The coding uses 10 instances of eval and
41 instances of replace. These two functions are critical to processing.

The file contains two global variables:

   flag_elliptic - sets whether or not to process the polynomial as
                   an elliptic curve if 3 is the highest power.

   flag_minor - sets whether or not to display minor grids.
"""
#### set flag_elliptic
flag_elliptic = 1 # = 0, do not process elliptic; = 1, process elliptic
                  # declared global variable in do_mult() and proc_poly()

#### set flag_minor
flag_minor = 0 # = 0, do not show minor grids; = 1, show minor grids
               # declared global variable in proc_poly(), elliptic(),
               # and poly()
               # displaying minor grids adds to processing time

from math import floor #floor() used in elliptic section 'xxx min x, ...'
import numpy as np
import matplotlib.pyplot as plt
from sympy import diff, expand

def do_mult(): #process multiple pre-defined polynomials
    #### global flag_elliptic
    global flag_elliptic #was set outside this function - do_mult()

    poly_list = [
                # ['x^10-25x^9',-2.5,2.5],
                # ['x^3',-4,4],
                # ['x^3-27x+64',-8,5],
                # ['x^3-25x+25',-7.5,9],
                # ['x(2x^2+4x+1+6/x)/3',-4,4],
                # ['x(x+1)(2x+1)/6',-6,6],
                # ['2x^3+25x^2+27',-3.5,3.5],
                # ['(x-1)^2(x+6)^3(x+1)',-3.8,1.5],
                # ['x^6-2x^5-26x^4+28x^3+145x^2-26x-80',-4,4],
                # ['x^5-x-1',-4,4],
                # ['(x-1)^2(x+6)^3(x+1)',-3.8,1.5],
                # ['x^3+17',-6,9.5],
                # ['x^3-150x+64',-10,15],
                # ['x^3-x+1',-6,8],
                # ['(2x^3+4x^2+x+6)/3',-4,5],
                # ['(1/5)(x^3-25x)',-6, 5.5],
                # ['(2x^3+3x^2+x)/6', -3, 1],
                # ['(x+1)(x-1)(x+1)/6',-4,3], #next 2 functions are actually the same
                # ['(1/6)(x+1)(x-1)(x+1)',-2,1.5], #when expanded using 'sympy expand'
                # ['x(2x^2+2500x+1+6/x)/3',-20,50], #300 for 3
                # ['x^11-25x^10-1000',-2.5,30],
                # ['2x+6',-4,4],
                ['x^2',-4,4],
                ['x^3-27x+64',-4,5],
                ['(1/20)(x^5+3x^4-11x^3-27x^2+10x+64)',-4.2,2.7],
                ['x^3-25x+25',-6,7.5],
                ['(2x^3+4x^2+x+6)/3',-2,1],
                ['x(x+1)(2x+1)/6',-1.5,0.5], #next 2 functions are actually the same
                ['(x+3x^2+2x^3)/6',-1.5,0.5], #when expanded using 'sympy expand'
                ['(3/10)(x^6-2x^5-26x^4+28x^3+145x^2-26x-80)', -4, 4],
                ['2x^3+25x^2',-3.5,4.2],
                ['2x^3+25(x+3)',-3,3],
                ['2x^3(x^2)-10(x+2)',-2,2],
                ['(2x^3)(x^2+1)x-10(x+2)',-2,2],
                ['x^5-30x^3+50x',-5,5],
                ]

    #### set flag_time
    flag_time = 1   # = 1, timing, = 0, no timing
    if flag_time == 1:
        from time import process_time

    #### time start
    if flag_time == 1:
        t1_start = process_time()

    #### initialize counts
    count_poly = 0
    count_deriv = 0
    count_poly_deriv = 0
    count_elliptic = 0 #remains at 0 if flag_elliptic == 0

    #### process polynomials
    for poly_item in poly_list:
        count_poly += 1
        count_deriv += 1
        count_poly_deriv += 1
        #### check flag_elliptic
        if flag_elliptic == 1:
            #### chk_elliptic - apply func01_02 and then slice
            chk_elliptic = func01_02(poly_item[0])
            chk_elliptic = chk_elliptic[chk_elliptic.index('x'):]
            if chk_elliptic.startswith('x**3'):
                count_elliptic += 1
        #### call function proc_poly(...)
        proc_poly(poly_item[0], poly_item[1], poly_item[2])

    #### print elapsed time
    if flag_time == 1:
        t1_stop = process_time()
        print()
        print('=================')
        print('Processing time: {:,.2f} seconds'.format(t1_stop-t1_start))
        print()
        print('Number of polynomial plots and results: {}'.format(count_poly))
        print('          derivative plots: {}'.format(count_deriv))
        print('          polynomial with derivative plots: {}'.format(count_poly_deriv))
        if flag_elliptic == 1:
            print('          elliptic plots and results: {}'.format(count_elliptic))
            print('          (If Elliptic has singular point, plotted but technically not elliptic)')
        print('Total number of plots: {}'.format(count_poly+count_deriv+count_poly_deriv+count_elliptic))

    #### end do_mult

def do_poly(): #process default polynomial or user-defined polynomial
    print()
    print('Enter polynomial in any order of powers, but descending powers is best')
    print('All powers must be integers')
    print('A beginning fraction or number can be type int or float')
    print('Sample polynomial: x^3+25x+25 or (1/6)(x^3+25x+25) or 2/5(x^3+25x+25) ')
    print()
    print('or, press Enter key to create: (3/10)(x^6-2x^5-26x^4+28x^3+145x^2-26x-80)')
    errors = 1 #set to 1 so 'while' runs
    while errors > 0:
        errors = 0 #reset to 0
        func01 = input('Polynomial function: ')
        if func01 == '':
            print('Default polynomial: (3/10)(x^6-2x^5-26x^4+28x^3+145x^2-26x-80)')
            func01 = '(3/10)(x^6-2x^5-26x^4+28x^3+145x^2-26x-80)'
        func01 = func01.replace(' ','')
        print('Function entered: {}'.format(func01))
        if func01.count('(') != func01.count(')'):
            print('Function entered: {}'.format(func01))
            print('Error: unmatched ()')
            print('Re-enter polynomial function')
            errors += 1
        for i in range(len(func01)):
            if func01[i] not in 'x+-./^()0123456789':
                print('Function entered: {}'.format(func01))
                print('Illegal character "{}" in polynomial'.format(func01[i]))
                print('Re-enter polynomial function')
                errors += 1
                break
    errors = 1
    while errors > 0:
        errors = 0
        xs = input('Enter starting x value (xs) or press Enter key for xs = -4: ')
        xs = xs.replace(' ','')
        if xs == '':
            xs = '-4'
        for i in range(len(xs)):
            if xs[i] not in '+-.0123456789':
                print('Starting x range (xs) is not a number')
                print('xs entered: {}'.format(xs))
                print('Re-enter xs')
                errors += 1
                break
    xs = float(xs)
    errors = 1
    while errors > 0:
        errors = 0
        xe = input('Enter ending x value (xe) or press Enter key for xe = 4: ')
        xe = xe.replace(' ','')
        if xe == '':
            xe = '4'
        for i in range(len(xe)):
            if xe[i] not in '+-.0123456789':
                print('Ending x range (xe) is not a number')
                print('xe entered: {}'.format(xe))
                print('Re-enter xe')
                errors += 1
                break
    xe = float(xe)
    print()
    if xs >= xe:
        print('Error: xs {} > xe {}; not valid'.format(xs, xe))
        xe = xs + 2
        print('xe reset to xs+2: {}; check plot and redo entries '.format(xe))

    #### entries for proc_poly()
    proc_poly(func01, xs, xe)

    #### end do_poly

def proc_poly(func01, xs, xe):  #controls polynomial processing
    #### flag_elliptic
    global flag_elliptic #was set outside this function - proc_poly()
    #### flag_minor
    global flag_minor #was set outside this function - proc_poly()
    flag_poly_no_deriv = 1  # = 0, no; = 1, yes; (process polynomial without derivative)
    flag_deriv = 1  # = 0, no; = 1, yes; (process derivative of polynomial)
    flag_poly_deriv = 1  # = 0, no; = 1, yes (polynomial with derivative)
    flag_zeros = 1 # = 0, no; = 1, yes and automatically set flag_poly = 0)

    #### end user inputs ###################
    #### DO NOT ENTER ANYTHING BELOW THIS LINE!!! ###################

    if flag_elliptic == 1:   #do not change
        elliptic(func01, xs, xe)

    if flag_zeros == 1:
        zeros(func01, xs, xe)

    if flag_poly_deriv == 1:   #do not change
        poly(func01,xs,xe,flag_poly=0,flag_deriv=0,flag_poly_deriv=1)

    if flag_deriv == 1:   #do not change
        poly(func01,xs,xe,flag_poly=0,flag_deriv=1,flag_poly_deriv=0)

    if flag_poly_no_deriv == 1:   #do not change
        poly(func01,xs,xe,flag_poly=1,flag_deriv=0,flag_poly_deriv=0)

    #### end proc_poly

def elliptic(func01, xs, xe):
    #### global flag_minor
    global flag_minor #was set outside this function - elliptic()

    #### reset xe if xe < 0
    if xe < 0:
        print()
        print('Warning')
        print('For the following Elliptic Curve:')
        print('   xs = {}, xe = {} are the input values.'.format(xs,xe))
        print('   xe = {} is < 0, does not always process correctly, reset to 0.'.format(xe))
        xe = 0

    #### set flag_print, user sets here and in polynomial.py
    flag_print = 0 # = 0, print normal, = 1 print z_box

    #### call function func01 to func02
    func02 = func01_02(func01)

    #### func03
    func03 = func02.replace('x','i')

    #### if elliptic
    ellip00 = func02[func02.index('x'):]
    if ellip00.startswith('x**3'):
        #### fig,ax
        fig,ax = plt.subplots(facecolor = 'white')
        ax.set_facecolor(color = 'lightgreen')

        #### ttt for plot
        ttt = '$y^2='+func01+'$'

        if len(ttt) < 22:
            ax.set_title('Contour Plot for Elliptic Curve: '+ ttt, fontsize = 12, color = 'blue')
        else:
            ax.set_title('Contour Plot for Elliptic Curve: '+ ttt, fontsize = 11, color = 'blue')
        ax.set_xlabel('x',fontsize = 12, color = 'blue')
        ax.set_ylabel('y',fontsize = 12, color = 'blue')

        #### set y_label rotation
        ax.set_ylabel('y',rotation=0)

        #### set xs = 0, then reset to capture beginning of elliptic
        xs = 0
        func03_box = []
        func04 = func02.replace('x','xs')
        while eval(func04) >= 0:
            xs -= 1
        #print('xs before refine: {}'.format(xs))
        #### refine xs
        xs_xe_range = np.linspace(xs, xe, 300)   #can increase to 400, ..
        for i in xs_xe_range:
            xs_xe_val = eval(func03)
            func03_box.append(xs_xe_val)
            if xs_xe_val >= 0:
                xs = floor(i)-0.2   #floor function was imported from math
                break
        #print('xs after refine: {}'.format(xs))
        if xs < -13:
            xs = xs*1.05

        #### y limits (yy_sqroot)
        x = xe
        yy_sqroot = (eval(func02))**0.5 #evaluate str func02 with x = xe
        yy_sqroot = yy_sqroot * 1.05

        #### set 0,0 grid line color yellow
        ax.axhline(0, color='yellow', linewidth=1)
        if xs <= 0:
            ax.axvline(0, color='yellow', linewidth=1)

        #### ogrid
        y, x = np.ogrid[-yy_sqroot:yy_sqroot:100j, xs:xe:100j]
        #### y_squared
        y_squared = eval(func02) #eval function
        #### reset yy_sqroot if necessary
        if max(y_squared[0])**0.5 > yy_sqroot:
            yy_sqroot = max(y_squared[0])**0.5
            yy_sqroot = yy_sqroot * 1.05
            y, x = np.ogrid[-yy_sqroot:yy_sqroot:100j, xs:xe:100j]
        #### ogrid contour
        #### zorder = 4 puts plot line on top of yellow 0,0 grid line
        ax.contour(x.ravel(),y.ravel(),y**2-(y_squared),[0],zorder=4,colors = 'blue')

        #### major, minor grid
        ax.grid(b=True, which='major', color='blue', linestyle='-', alpha=0.9)
        if flag_minor == 1:
            ax.grid(b=True, which='minor', color='blue', linestyle='-', alpha=0.3)
            ax.minorticks_on()
        ax.tick_params(axis='both',labelsize = 10, colors = 'blue')

        #### spines
        ax.spines['bottom'].set_color('blue')
        ax.spines['top'].set_color('blue')
        ax.spines['left'].set_color('blue')
        ax.spines['right'].set_color('blue')

        #### elliptic plot already processed in Spyder without using plt.show().
            #If using IPython and command line - run polynomial_elliptic, then
            #IPython needs a plt.show() somewhere. By invoking plt.show() after
            #printing, IPython prints and appears simultaneously with plot in a
            #separate window.

        #### start
        start = int(xs)
        #### set stop
        stop =  int(300)  #<= user can set this

        if flag_print == 0:
            #### print normal results (integer results only)
            number_solutions = 0
            print()
            print('=================')
            #### ttt for normal results
            ttt = func01.replace('+',' + ')
            ttt = ttt.replace('-',' - ')
            ttt = ttt.replace('( + ','(+')
            ttt = ttt.replace('( - ','(-')
            ttt = 'f(x) = ' + ttt
            print('Integer results for Elliptic Curve: {} '.format(ttt))
            print()
            print('{:>6}'.format('x'), '{:>11}'.format('y^2'), '{:>10}'.format('y'), '{:>10}'.format('-y'))
            print('{:>6}'.format('---'), '{:>11}'.format('----'), '{:>10}'.format('----'), '{:>10}'.format('----'))
            #### x_val
            func05 = func02.replace('x','j')
            for j in range(start, stop+1): #x_val type float needed for .is_integer
                x_val = float(eval(func05))
                if x_val >= 0 and (x_val**0.5).is_integer():
                    print('{:>6,d}'.format(int(j)), '{:>11,d}'.format(int(x_val)), '{:>10,d}'.format(int(x_val**0.5)), '{:>10,d}'.format(int(-x_val**0.5)))
                    number_solutions += 1
            print()
            print('Number of integer results = {} ({} <= x <= {})'.format(number_solutions,int(xs),int(stop)))
            print()
        else:
            #### print z_box results (integer results only)
            number_solutions = 0
            print()
            print('=================')
            #### z_box
            z_box = np.array([], dtype=int)
            #### ttt for z_box results
            ttt = func01.replace('+',' + ')
            ttt = ttt.replace('-',' - ')
            ttt = ttt.replace('( + ','(+')
            ttt = ttt.replace('( - ','(-')
            ttt = 'f(x) = ' + ttt
            print('Elliptic Curve: {} '.format(ttt))
            #### x_val
            func05 = func02.replace('x','j')
            for j in range(start, stop+1): #x_val type float needed for .is_integer
                x_val = float(eval(func05))
                if x_val >= 0 and (x_val**0.5).is_integer():
                    number_solutions += 1
                    z_box01 = np.array([int(j),int(x_val),int(x_val**0.5),-int(x_val**0.5)])
                    z_box = np.concatenate((z_box,z_box01))
            z_box = z_box.reshape(number_solutions,4)
            if z_box.size > 0:
                zbw = len(str(z_box[-1][1]))
                #print('zbw = {}'.format(zbw))
            print()
            print('Results for integer x:')
            print()
            if zbw == 1:
                print('  x y^2 y -y')
                print('  - --- - --')
            elif zbw == 2:
                print('   x  y^2  y  -y')
                print('   -  ---  -  --')
            elif zbw == 3:
                print('    x   y^2   y   -y')
                print('    -   ---   -   --')
            elif zbw == 4:
                print('     x    y^2    y    -y')
                print('     -    ---    -    --')
            elif zbw == 5:
                print('      x   y^2     y     -y')
                print('      -   ---     -     --')
            elif zbw == 6:
                print('       x    y^2      y      -y')
                print('       -    ---      -      --')
            elif zbw == 7:
                print('        x     y^2       y       -y')
                print('        -     ---       -       --')
            else:
                print('         x      y^2        y        -y')
            #print()
            print(z_box)
            print()
            print('Number of integer results = {} ({} <= x <= {})'.format(number_solutions,int(xs),int(stop)))
            #print('z_box: (rows, columns): {}'.format(z_box.shape))

        #### plt.show() - need for IPython but not for Spyder
        plt.show()

    #### if not elliptic
    else:
        print('=================')
        print('f(x) = {} is not Elliptic, no Elliptic plot.'.format(func01))

    #### end elliptic

def poly(func01, xs, xe, flag_poly, flag_deriv, flag_poly_deriv):
    #### global flag_minor
    global flag_minor #was set outside this function - poly()

    #### call function func01 to func02
    func02 = func01_02(func01)

    from sympy.abc import x   #used with func04 and diff
    #### func04 is derivative of func02
    if flag_deriv == 1 or flag_poly_deriv == 1:
        func04 = diff(func02, x)
        func04 = '{}'.format(func04)

        #### func05 for deriv text in plot
        func05 = func04.replace(' ','')
        func05 = func05.replace('**','^')
        func05 = func05.replace('*','')

        #### func06, to position deriv text on plot
        func06 = func04.replace('x','xs')

    #### x, y, y_deriv
    x = np.arange(xs, xe + 0.02, 0.02)
    x = np.round(x, 2)
    y = [eval(func02) for x in x]
    y = np.array(y)
    if flag_deriv == 1 or flag_poly_deriv == 1:
        y_deriv = [eval(func04) for x in x]
        y_deriv = np.array(y_deriv)

    #### fig, ax
    fig, ax = plt.subplots(facecolor = 'white')
    ax.set_facecolor(color = 'lightgreen')

    #### set 0,0 grid line color yellow
    ax.axhline(0, color='yellow', linewidth=1)
    if xs <= 0: #if x range includes 0, display yellow vertical line
        ax.axvline(0, color='yellow', linewidth=1)

    #### plot function and derivative
    if flag_poly == 1 or flag_poly_deriv == 1:
        ax.plot(x, y, color = 'blue', zorder = 4)
    if flag_deriv == 1 or flag_poly_deriv == 1:
        ax.plot(x, y_deriv, color = 'red')

    #### ttt if pwr < 10
    ttt = r'$f(x)='+func01+'$' # 'r' indicates raw text

    #### deriv text if pwr < 10
    if flag_deriv == 1 or flag_poly_deriv == 1:
        deriv_txt = '$'+"slope="+func05+'$'

    #### reset ttt and deriv_txt if max power >= 10 in func
    if '^' in func01:
        ttt_test =  func01[func01.index('^')+1:func01.index('^')+3]
        if ttt_test[-1] in '0123456789': #key step, works in all cases pwr >= 10
            if int(ttt_test) > 9:
                ttt1 = func01.replace('+',' + ')
                ttt1 = ttt1.replace('-',' - ')
                ttt1 = ttt1.replace('( + ','(+')
                ttt1 = ttt1.replace('( - ','(-')
                ttt = 'f(x) = ' + ttt1
                if flag_deriv == 1 or flag_poly_deriv == 1:
                    deriv_txt1 = func05.replace('+',' + ')
                    deriv_txt1 = deriv_txt1.replace('-',' - ')
                    deriv_txt1 = deriv_txt1.replace('( + ','(+')
                    deriv_txt1 = deriv_txt1.replace('( - ','(-')
                    if deriv_txt1[:3] == ' - ':
                        deriv_txt1 = '-' + deriv_txt1[3:]
                    deriv_txt = 'slope = ' + deriv_txt1

    #### title fontsize
    if len(ttt) < 43:
        ax.set_title(ttt, fontsize = 12, color = 'blue')
    else:
        ax.set_title(ttt, fontsize = 11, color = 'blue')

    #### position deriv_txt on plot
    if flag_deriv == 1 or flag_poly_deriv == 1:
        pos_y0 = eval(func06)
        #### deriv_txt fontsize
        if len(deriv_txt) < 43:
            ax.text(xs+0.25, int(pos_y0)*0.93,deriv_txt, zorder=5, horizontalalignment='left', fontsize=12,color='red')
        else:
            ax.text(xs+0.25, int(pos_y0)*0.93,deriv_txt, zorder=5, horizontalalignment='left', fontsize=11,color='red')

    #### major, minor grid
    ax.grid(b=True, which='major', color='blue', linestyle='-', alpha=0.6)
    if flag_minor == 1:
        ax.grid(b=True, which='minor', color='blue', linestyle='-', alpha=0.3)
        ax.minorticks_on()
    ax.tick_params(axis='both',labelsize = 10, colors = 'blue')

    #### thousands separator -- bool code
    #### yy_lim
    yy_lim = ax.get_ylim()
    #print('yy_lim = {}'.format(yy_lim))
    if abs(yy_lim[0]) <= 0.1 or abs(yy_lim[1]) <= 0.1 :
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(round(x,15))))
    elif abs(yy_lim[1] <= 1 and abs(yy_lim[0] <= 1)):
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(round(x,4))))
    elif abs(yy_lim[1] <= 10**10 and abs(yy_lim[0] <= 10**10)):
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    #### spines
    ax.spines['bottom'].set_color('blue')
    ax.spines['top'].set_color('blue')
    ax.spines['left'].set_color('blue')
    ax.spines['right'].set_color('blue')

    plt.show()

    #### end poly

def zeros(func01, xs, xe):
    #### call function func01 to func02
    func02 = func01_02(func01)

    #### x, y
    x = np.arange(xs, xe, 0.01)
    x = np.round(x, 2)
    y = [eval(func02) for x in x]
    y = np.array(y)

    #### f(x) = 0
    x_zeros = []
    y_zeros = []
    #### f'(x) = 0
    x_slope0 = []
    y_slope0 = []
    y_slope0_val = []

    for i in list(range(len(y)-2)):
        #### find points where f(x) = 0
        if y[i] < 0 and (y[i+1] == 0 or y[i+1] > 0):
            y_zeros.append(i+1)
        if y[i] > 0 and (y[i+1] == 0 or y[i+1] < 0):
            y_zeros.append(i+1)
        #### produces same results as f'(x) = 0
        if y[i] < y[i+1] and y[i+1] > y[i+2]: #relative maximum
            y_slope0.append(i+1)
        if y[i] > y[i+1] and y[i+1] < y[i+2]: #relative minimum
            y_slope0.append(i+1)
    #### sort y_zeros
    y_zeros.sort()
    #### create x_zeros
    for i in y_zeros:
        x_zeros.append(x[i])
    for i in list(range(len(x_zeros))):
        if x_zeros[i] == -0.0:
            x_zeros[i] = 0
    #### format x_zeros
    x_zeros = str(x_zeros)
    x_zeros = x_zeros[1:-1]

    #### sort y_slope0
    y_slope0.sort()
    #### create x_slope0, y_slope0_val
    for i in y_slope0:
        x_slope0.append(x[i])
        y_slope0_val.append(y[i])
    for i in range(len(y_slope0_val)):
        y_slope0_val[i] = round(y_slope0_val[i],2)
    for i in list(range(len(x_slope0))):
        if x_slope0[i] == -0.0:
            x_slope0[i] = 0
    #### format x_slope0, y_slope0_val
    x_slope0_str = str(x_slope0)
    x_slope0_str = x_slope0_str[1:-1]
    y_slope0_val_str = str(y_slope0_val)
    y_slope0_val_str = y_slope0_val_str[1:-1]

    #### print function and x range
    #### ttt
    ttt1 = func01.replace('+',' + ')
    ttt1 = ttt1.replace('-',' - ')
    ttt1 = ttt1.replace('( + ','(+')
    ttt1 = ttt1.replace('( - ','(-')
    ttt = 'f(x) = ' + ttt1
    print()
    print('=================')
    print('Results for {} and x_range({}<=x<={}):'.format(ttt, xs, xe))
    print()
    if len(x_zeros) == 0:
        print('f(x) does not cross the x axis at any point.')
    else:
        print('       f(x) = 0 at x: {}'.format(x_zeros))

    #### print f'(x) information
    if '**' not in  func02 and 'x' in func01:
        print("            is a straight line")
    elif '**' in func02 and len(x_slope0) == 0 and len(y_slope0) == 0:
        print("            has no relative maximum or minimum over the specified x range")
    else:
        print("      f'(x) = 0 at x: {}".format(x_slope0_str))
        print('                f(x): {}'.format(y_slope0_val_str))
        if len(y_slope0_val) > 1:
            y_slope0_val_max = max(y_slope0_val)
            y_slope0_val_min = min(y_slope0_val)
            x_at_y_slope0_val_max = x_slope0[y_slope0_val.index(y_slope0_val_max)]
            x_at_y_slope0_val_min = x_slope0[y_slope0_val.index(y_slope0_val_min)]
            print('       f(x) has relative maximum  of {} at x = {}'.format(y_slope0_val_max,x_at_y_slope0_val_max))
            print('                relative minimum  of {} at x = {}'.format(y_slope0_val_min,x_at_y_slope0_val_min))

    #### end zeros

def func01_02(func01):
    func01 = func01.replace(' ','')
    func02 = list(func01)
    for i in range(len(func02)-1):
        if func02[i] in '0123456789' and func02[i+1]=='(':
            func02[i] = func02[i]+'*'
    func02 = ''.join(func02)
    func02 = func02.replace('^','**')
    func02 = func02.replace(')(',')*(')
    func02 = func02.replace('x','*x')
    func02 = func02.replace('(*','(')
    func02 = func02.replace('+*','+')
    func02 = func02.replace('-*','-')
    if func02[0] == '*':
        func02 = func02[1:]
    if '(' in func02 and func02.index('(')>0 and func02[func02.index('(')-1]!='*':
        func_find = func02.index('(')
        func_temp = func02[func_find:]
        func02 = func02[:func02.index('(')] + '*' + func_temp
    if ')' in func02 and func02.rindex(')') < (len(func02)-1):
        func03 = func02[:func02.rindex(')')] + ')*'
        func02 = func03 + func02[func02.rindex(')')+1:]
    func02 = func02.replace('***','**')
    func02 = func02.replace('*/','/')
    func02 = func02.replace('/*','/')
    func02 = '{}'.format(expand(func02))
    return func02

    #### end func01_02

#### run do_mult() or do_poly()
if __name__ == '__main__':
    print()
    print('Press 1  to process multiple pre-defined polynomials - do_mult()')
    print('      2  to input user-defined polynomial - do_poly()')
    poly_input = input('Enter: ')
    if poly_input == '1': do_mult()
    else:  do_poly()

#### end polynomial