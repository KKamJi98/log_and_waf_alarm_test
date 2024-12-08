# Traffic Generator

## frontend_traffic_generator.py

```bash
python frontend_traffic_generator.py --requests_per_interval 400 --interval_seconds 60 --duration_seconds 300
```

`--url`: target url  
`--request_per_interval`: interval당 요청을 몇 회 보낼건지  
`--interval_seconds`: interval 간격  
`--duration_seconds`: 몇 분 동안 traffic을 생성할건지  

## backend_traffic_generator.py

```bash
python backend_traffic_generator.py --api_endpoint https://xxxxxx.execute-api.ap-northeast-2.amazonaws.com/prod --duration_seconds 300
```

`--api_endpoint`: 테스트할 Backend 혹은 API Gateway의 Invoke URL 지정
`--duration_seconds`: 몇 초 동안 traffic을 발생시킬 것인지
