# 지하철 봇

#### 이 프로그램은 서울메트로가 관리하는 1 ~ 4호선 역의 혼잡도를 알려주는 카카오톡 자동응답 봇입니다
###### (좋은 이름 추천받습니다)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/005798da067e4185a15f09b6413875e2)](https://www.codacy.com/app/parksjin01/Kor_subway?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=parksjin01/Kor_subway&amp;utm_campaign=Badge_Grade)

#### Version 0.1.1(Minor update)
> 카카오톡 플러스 친구를 맺으면 현재 시간 특정 지하철 역의 혼잡한 정도를 알 수 있습니다.
![](https://github.com/parksjin01/Kor_subway/blob/master/Image/Example.jpeg?raw=true)

#### Dependency
> Flask

#### Data source
> [Data](https://www.data.go.kr/dataset/15003169/fileData.do)

#### Preprocessing
> 날짜 호선 역명 구분 시간대(00 ~ 01, 01 ~ 02, 02 ~ 03 ... 23 ~ 24)  
> :arrow_down:
> 호선 역명 시간대 -> input
> 혼잡도(승하차 인원의 합이 2000을 넘으면 1, 넘지 않으면 0) -> output