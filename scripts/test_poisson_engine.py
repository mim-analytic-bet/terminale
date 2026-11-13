import json
import math

def poisson(k, l):
    p = math.exp(-l)
    for i in range(1, k + 1):
        p *= l / i
    return p

def calc_match_stats(lambda_c, mu_o):
    p_c = 0.0
    p_x = 0.0
    p_o = 0.0
    p_over = 0.0
    p_under = 0.0
    p_gg = 0.0
    p_ng = 0.0
    
    for i in range(10):
        for j in range(10):
            p = poisson(i, lambda_c) * poisson(j, mu_o)
            if i > j: p_c += p
            elif i == j: p_x += p
            else: p_o += p
            
            if (i + j) > 2.5: p_over += p
            else: p_under += p
            
            if i > 0 and j > 0: p_gg += p
            else: p_ng += p
            
    tot_1x2 = p_c + p_x + p_o
    p_c /= tot_1x2
    p_x /= tot_1x2
    p_o /= tot_1x2
    
    return {
        'p1': round(p_c, 3), 'px': round(p_x, 3), 'p2': round(p_o, 3),
        'p_over': round(p_over, 3), 'p_under': round(p_under, 3),
        'p_gg': round(p_gg, 3), 'p_ng': round(p_ng, 3),
        'q1': round(1 / p_c, 2), 'qx': round(1 / p_x, 2), 'q2': round(1 / p_o, 2),
        'q_over': round(1 / p_over, 2), 'q_under': round(1 / p_under, 2),
        'q_gg': round(1 / p_gg, 2), 'q_ng': round(1 / p_ng, 2),
    }

print('Poisson engine ready.')
