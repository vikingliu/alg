# coding=utf-8
def softmax(xi, x):
    return e ^ xi / sum([e ^ xj for xj in x])

# dyi/dxj = yi(1-yj)    i==j
# dyi/dxj = -yiyj    i!=j
def softmax_dx(x):
    dx = 0
    for i in range(len(x)):
        for j in range(len(x)):
            if i == j:
                dx += softmax(x[i], x) * (1 - softmax(x[i], x))
            if i != j:
                dx += softmax(x[i], x) * softmax(x[j], x)
    return dx


# loss func  L = - ΣΣtki log(yki)
# dL/dxi = dL/dyj * dyj/dxi = yi - xi
def loss_dx(p, x):
    return [softmax(x[i]) - p[i] for i in range(len(x))]