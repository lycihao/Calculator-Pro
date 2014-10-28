#!/usr/bin/python
# FileName : calc.py

#constPi = [3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609,399]
pi = [31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679, 100]

def getVal(x):
    val = str(x[0])
    if x[1] == 0:
        return val
    length = len(val)
    if length <= x[1]:
        val = '0' * (x[1] + 1 - length) + val
    return val[:-x[1]] + '.' + val[-x[1]:]

def add(x, y):
    scale = max(x[1],y[1])
    y[0] *= 10**(scale - y[1])
    x[0] *= 10**(scale - x[1])
    return [x[0] + y[0], scale]

def sub(x, y):
    scale = max(x[1],y[1])
    y[0] *= 10**(scale - y[1])
    x[0] *= 10**(scale - x[1])
    return [x[0] - y[0], scale]

def mul(x, y, scale = 0):
    rs = [x[0] * y[0], x[1] + y[1]]
    if scale == 0:
        return rs
    length = len(str(rs[0]))
    if length <= scale:
        return rs
    rs[1] -= length - scale
    rs[0] /= 10**(length - scale)
    return rs

def div(x, y, scale = 100):
    if y[0] == 0:
        return 'Inf'
    if x[0] == 0:
        return [0, 0]
    xstr = str(x)
    ystr = str(y)
    if xstr[0] == '-':
        xstr = xstr[1:]
    if ystr[0] == '-':
        ystr = ystr[1:]
    if xstr < ystr:
        xx = scale - len(xstr) + len(ystr)
    else:
        xx = scale - len(xstr) + len(ystr) - 1
    if xx >= 0:
        return [x[0] * (10 ** xx) / y[0], x[1] - y[1] + xx]
    else:
        return [x[0] / y[0], x[1] - y[1]]

def mod(x, y):
    scale = max(x[1],y[1])
    y[0] *= 10**(scale - y[1])
    x[0] *= 10**(scale - x[1])
    return [x[0] % y[0], scale]

def exp(x):
    if x[0] == 0:
        return [1,0]
    rs = [1,0]
    xx = [1,0]
    index = 1
    loop = [1,0]
    while index <= 1000:
        xx = mul(xx, x)
        loop[0] = loop[0]*index
        rs = add(rs,div(xx, loop))
        index += 1
    return rs

def ln(x, scale = 32):
    if x[0] == 1 and x[1] == 0:
        return [0,0]
    elif x[0] <= 0:
        return 'error'
    y = div(sub(x,[1,0]),add(x,[1,0]))
    y2 = mul(y,y)
    yy = [1,0]
    rs = [1,0]
    loop = 1
    while loop < 100000:
        yy = mul(yy, y2, 100)
        rs = add(rs, div(yy,[loop*2+1,0]))
        loop += 1
    rs = mul(rs,[y[0]*2,y[1]],scale)
    return rs

def xy(x, y):
    if y[1] == 0:
        if x[0] == 1:
            return [1, x[1]*y[0]]
        rs = [1,0]
        while y[0] > 0:
            if y[0] % 2 == 1:
                rs = mul(rs, x)
            x = mul(x, x)
            y /= 2
        return rs
    return exp(mul(y,ln(x)))

def sin(x):
    x = mod(x,mul(pi,[2,0]))    
    x2 = mul(x,[-x[0],x[1]])
    rs = x
    xx = x
    loop = [1,0]
    index = 1
    while index < 100:
        xx = mul(xx, x2, 100)
        loop[0] *= 2*index*(2*index + 1)
        rs = add(rs, div(xx, loop))
        index += 1
    return rs

def cos(x):
    x = mod(x,mul(pi,[2,0]))
    x2 = mul(x,[-x[0],x[1]])
    rs = [1,0]
    xx = [1,0]
    loop = [1,0]
    index = 1
    while index < 100:
        xx = mul(xx, x2, 100)
        loop[0] *= 2*index*(2*index - 1)
        rs = add(rs, div(xx, loop))
        index += 1
    return rs

def tan(x):
    x = mod(x, pi)
    a = div(pi,x)
    if mul(a, a) == [4,0]:
        return 'inf'
    return div(sin(x),cos(x))
