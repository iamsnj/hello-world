#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sanjay
"""

# from __future__ import division
from flask import Flask, render_template, request
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

app = Flask(__name__)
app.secret_key = 'ud7we6^%t6yghg6%TGTGRt6ygvb6%6tgYYT6EYVEhf'

@app.route('/')
def index():
    return render_template('index.html')

def check_sign(expr):
    if expr[0] == '-':
        return 0
    return 1

@app.route('/quadratic/', methods = ['POST', 'GET'])
def quadratic():
    if request.method == 'GET':
        return render_template('quadratic.html')
    elif request.method == 'POST':
        q = symbols('q')
        equation = request.form['equation']
        profit = request.form['profit']
        init_printing(use_unicode=True)
        derivative = diff(equation, q)
        expr = derivative - parse_expr(profit)
        expr1 = factor(expr)
        factors = solve(expr1)

        sign = check_sign(str(derivative))
        tmp = factors[0]
        factors[0] = factors[1-sign]
        if not sign:
            factors[1] = tmp
        equation = parse_expr(equation)
        eq_val = equation.subs(q, factors[1])
        deri_val = derivative.subs(q, factors[1])
        ans = float(eq_val/(factors[1]*deri_val))
        return render_template('quadAns.html', equation=latex(equation), diff=latex(derivative), 
                                P=profit, expr=latex(expr), expr1=latex(expr1), factor0=latex(factors[0]),
                                factor1=latex(factors[1]), eq_val=latex(eq_val), deri_val=latex(deri_val), ans=latex(ans))
    return 'fail'

if __name__ == '__main__':
    app.run(debug=True)
