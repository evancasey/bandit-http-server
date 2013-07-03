Create Bandit

`
$ curl -i -H "Content-Type: application/json" -X POST -d '{"name":"test","arm_count":4,"algo_type":"egreedy","horizon_type":"time", "horizon_value":60, "epsilon":60}' http://localhost:5000/api/v1.0/bandits/
`

Get Bandit

`
curl -i http://localhost:5000/api/v1.0/bandits/1
`

Update Bandit

`
curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"test","arm_count":4,"algo_type":"egreedy","horizon_type":"time", "horizon_value":60, "epsilon":60}' http://localhost:5000/api/v1.0/bandits/1
`

Update Arm

`
curl -i -H "Content-Type: application/json" -X PUT -d '{"value":"5000"}' http://localhost:5000/api/v1.0/bandits/1/arms/1
`



