# OKL-bandits

A Python/Flask REST API for the bandit algorithms.

## Getting Started

The OKL-bandits API has 5 different API calls, and each Bandit has 6 parameters associated with it. These include:

"name": This can be any string
"arm_count": Can be any positive integer (may change later)
"algo_type": Only "egreedy" or "softmax" (will add more later)
"budget_type": Only "trials" (will add more later)
"budget": Can be any positive integer
"epsilon": Must be a float between 0 and 1


'''

#### Creating a Bandit:

```
$ curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test","arm_count":4,"algo_type":"egreedy","budget_type":"time", "budget":60, "epsilon":0.1}' http://localhost:5000/api/v1.0/bandits
```

#### Looking up a Bandit:

```
$ curl -i http://localhost:5000/api/v1.0/bandits/1
```

#### Getting the "best" arm:

```
$ curl -i http://localhost:5000/api/v1.0/bandits/1/arms/current
```

#### Updating a Bandit:

```
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"test","algo_type":"egreedy","budget_type":"time", "budget":60, "epsilon":0.2}' http://localhost:5000/api/v1.0/bandits/1
```

#### Updating a Bandit's Arm:

```
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"reward":5000}' http://localhost:5000/api/v1.0/bandits/1/arms/1
```



