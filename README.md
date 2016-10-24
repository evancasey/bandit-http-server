# bandit-http-server

A Python/Flask REST API for the bandit algorithms. Uses [redis](http://redis.io) under the hood.

Currently supports e-greedy and softmax action selection.

## Getting Started

Each Bandit has up to 8 parameters associated with it. These include:

* `name`: Can be any string

* `arm_count`: Must be a positive integer 

* `algo_type`: Only "egreedy" or "softmax" (will add more later)

* `budget_type`: Only "trials" (will add more later)

* `budget`: Must be a positive integer

* `epsilon`: Must be a float between 0 and 1

* `temperature`: Must be a float between 0 and infinity

* `reward_type`: Only "click" (will add more later)


## Making API Calls


#### Creating a Bandit:

```
$ curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test","arm_count":4,"algo_type":"egreedy","budget_type":"trials", "budget":1000, "epsilon":0.1,"reward_type":"click"}' http://localhost:5000/api/v1.0/bandits
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
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"test","algo_type":"egreedy","budget_type":"trials", "budget":1000, "epsilon":0.1}' http://localhost:5000/api/v1.0/bandits/1
```

#### Updating a Bandit's Arm:

For "click" reward type, reward must be either 0 (no click) or 1 (click)

```
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"reward":1}' http://localhost:5000/api/v1.0/bandits/1/arms/1
```

#### Deleting a Bandit:

```
$ curl -i -H "Content-Type: application/json" -X DELETE -d http://localhost:5000/api/v1.0/bandits/1
```


