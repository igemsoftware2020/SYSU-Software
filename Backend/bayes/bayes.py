from bayes_opt import BayesianOptimization

gene_num = int(input(""))
axes = ['x', 'y', 'z', 'w', 'u'][:gene_num]

optimizer = BayesianOptimization(
    f=None,
    pbounds={k:(0, 50) for k in axes},
    verbose=2,
    random_state=1,
)

from bayes_opt import UtilityFunction

iter_num = int(input(""))

utility = UtilityFunction(kind="ei", kappa=2.5, xi=0.0)

next_point_to_probe = optimizer.suggest(utility)
print(*[next_point_to_probe[k] for k in axes])

target = float(input(""))

optimizer.register(
    params=next_point_to_probe,
    target=target,
)

for _ in range(iter_num):
    next_point = optimizer.suggest(utility)
    print(*[next_point[k] for k in axes])
    R = input("")
    target = float(R)
    optimizer.register(params=next_point, target=target)
    # print("Target:", target, next_point)
#tmp = round(optimizer.max['x'])
#optimizer.max['x'] = tmp
print(optimizer.max['target'], *[optimizer.max['params'][k] for k in axes])
