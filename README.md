# log_and_waf_alarm_test

frontend_traffic_generator.py

```bash
python frontend_traffic_generator.py --requests_per_interval 400 --interval_seconds 60 --duration_seconds 300
```

`--url`: target url  
`--request_per_interval`: interval당 요청을 몇 회 보낼건지  
`--interval_seconds`: interval 간격  
`--duration_seconds`: 몇 분 동안 traffic을 생성할건지  
