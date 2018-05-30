"""
@Project   : text-classification-cnn-rnn
@Module    : greedy.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/30/18 1:16 PM
@Desc      :
最近遇到了一个优化问题：一组结构化的数据包括N行M列，要从中抽取任意多行数据（不超过N），
这些数据要同时满足若干条件，如第一列的平均值在[a, b]之间，第二列的总和在[c, d]之间，
第三列的女性占比在[e, f]之间。

我自己试着想出了一个解决方法，因为最近在研究神经网络，受梯度下降法的启发，
不妨设计一个损失函数F，对所有数据与目标用MSE计算出一个平均损失，损失最小的数据被pop到结果集里，
再进行第二轮查找直至算法收敛，另外这个损失要做归一化处理，否则会导致各个约束条件之间的不平衡。

自己竟然自创了方法，很开心。后来自己一想，这不就是贪心算法么。哎，
这年头想有个什么创新比登天还难~
"""

"""
Created on Tue Oct 31 20:02:11 2017

@author: liuzimu
"""

import pandas as pd
import random, time
import numpy as np

"""
1. Establish a random dataset
The dataset contains the following columns:

Gender: randomly generate 'male' or 'female'
Age: random integers between 22 and 65
Salary: random integers between 3000 and 10000
"""

n_row = 1000
random.seed(50)

# create a series of gender
gender = pd.Series([random.choice(['male', 'female']) for i in range(n_row)])

# create a series of age
age_low = 22
age_high = 65
age = pd.Series([random.randint(age_low, age_high) for i in range(n_row)])

# create a series of salary
salary_low = 3000
salary_high = 10000
salary = pd.Series(
    [random.randint(salary_low, salary_high) for i in range(n_row)])

# create a dataframe by gender and salary
df = pd.DataFrame({"gender": gender, "age": age, "salary": salary})
df.head()

"""
2. Create a dictionary of strings and their corresponding functions
"average": numpy.mean function
"sum": numpy.sum function
"""


def str2func(x):
    func_dict = {"average": np.mean, "sum": np.sum}
    return func_dict[x]


"""
3. Calculate square error
Suppose we want the variable x to fall on the [a, b] interval, 
then the calculation of the squared error is as followed:

if x in [a, b], then  SE=0 
if x > b, then  SE=(x/b−1)^2 
if x < a，then  SE=(1−x/a)^2
"""


def get_se(x, rng):
    a, b = rng
    if a <= x <= b:
        res = 0
    elif x > b:
        # Normalization
        res = (x / b - 1) ** 2
    else:
        res = (1 - x / a) ** 2
    return res


"""
4. Calculate mean-square error
"""


def get_mse(data, rows, cols, funcs, rngs, n_cond):
    mse = 0.0
    for index, (col, func, rng) in enumerate(zip(cols, funcs, rngs)):
        se = func(data.loc[rows == 1, col])
        se = get_se(se, rng)
        mse += se * n_cond[index]
    return mse


"""
5. Search function
The variable rows is something like [1, 1, 0, 1, 0, 0, 0..., 0, 1, 0, 0, 0], 
in which 1 means the row number is selected.
Set the mse and min_mse as "infinite" initially to make the code more elegant.

a. Create an index array with n zeros.
b. Calculate the mse of indexes which are zeros.
c. Record the minimum mse as min_mse during step 2, 
and set the corresponding index as one.
d. Compare the mse and min_mse then update the value of mse.
e. Break the iteration if the mse cannot be lower anymore.
"""


def search(data, cols, funcs, rngs, threshold=10e-6):
    n_row = data.shape[0]
    # n_cond = len(cols)
    n_cond = [0.5, 0.5]
    # 求mse时用来给不同的列加权

    # create a series to show which rows are selected
    rows = pd.Series(np.zeros(n_row, dtype=np.int32))
    rows.index = data.index

    # get functions
    funcs = [str2func(x) for x in funcs]

    i = 0
    mse = float('inf')
    while mse > threshold:
        min_mse = float('inf')
        for idx in data.loc[rows == 0].index:
            rows.loc[idx] = 1
            tmp_mse = get_mse(data, rows, cols, funcs, rngs, n_cond)

            if tmp_mse < min_mse:
                min_mse = tmp_mse
                min_mse_idx = idx
            else:
                pass

            rows.loc[idx] = 0
        # 一个for循环下来，找到mse最小的那个样本，
        # 年龄最接近35到40，薪水最接近10万到12万

        # check if mse cannot be lower any more
        if min_mse > mse:
            break
            # 新加入的样本使得mse变大的话，就退出循环了，到此为止
        else:
            mse = min_mse
            # 更新mse
            rows.loc[min_mse_idx] = 1
            # 选中刚刚加入的这个样本
            # 是贪心算法，因为单独一个样本使得mse最小，不代表加入多个样本后也会使得mse最小
            # 贪心算法任务，单独一个样本使得mse最小时，各个样本有更大的概率在多样本中
            # 也使得mse最小

        # print loss
        print("%d times iteration, mse %.3f" % (i + 1, mse))
        i += 1

    return rows


"""
6. Test the search fucntion and show results.
"""
print("\n" * 3)
print("Test search:")

run_time = time.time()

idxs = search(data=df
              , cols=["age", "salary"]
              , funcs=["average", "sum"]
              , rngs=[[35, 40], [100000, 120000]])

search_result = df.loc[idxs == 1]
average_age = search_result.age.mean()
total_salary = search_result.salary.sum()

print()
print(
    "Target average age is 35 to 40 and target total salary is 100000 to 120000")
print(
    "Average age is %.2f and total salary is %d" % (average_age, total_salary))
print("Run time is %.2f s" % (time.time() - run_time))
