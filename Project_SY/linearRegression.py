import numpy as np

x_train = np.array([1., 3., 4., 5., 2.]) #직원과 손님간의 거리
y_train = np.array([5., 10., 13., 16., 7.]) #걸리는 시간

# y = wx + b 예측함수의 공식

#0으로 초기화
W = 0.0 # weight
b = 0.0 # offset


n_data = len(x_train)
epochs = 5000
learning_rate = 0.01

for i in range(epochs):
    hypothesis = x_train * W + b
    cost = np.sum((hypothesis - y_train) ** 2) / n_data #평균제곱 오차 공식 1/n sum((예측값 - y값)^2)
    gradient_w = np.sum((W * x_train - y_train + b) * 2 * x_train) / n_data #w에 대하여 편미분하여 나온 계산값
    gradient_b = np.sum((W * x_train - y_train + b) * 2) / n_data #b에 대하여 편미분하여 나온 계산값

    W -= learning_rate * gradient_w 
    b -= learning_rate * gradient_b

    if i % 100 == 0:
        print('Epoch ({:10d}/{:10d}) cost: {:10f}, W: {:10f}, b:{:10f}'.format(i, epochs, cost, W, b))

print('W: {:10f}'.format(W))
print('b: {:10f}'.format(b))
print('result : ')

minV = input()

print(int(minV) * W + b) #input값