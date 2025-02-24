# Driver-Forward-Attention-Warning-System
'운전자 전방주시 알림 시스템 구현'

# 전방주시 미흡 판단 알고리즘
![Image](https://github.com/user-attachments/assets/2e1b7654-041f-4056-9d94-5b900119ddcd)
- 눈 객체 탐지
- 눈 객체 1개 이상: 정상
- 눈 객체 없음: 비정상
- 첫 미흡 알림: 2초간 지속 후 자동 정지
- 첫 알림 후 1초간 정상 유지: 리셋
- 첫 알림 후 지속적으로 비정상: 알림 무한재생, 사용자 피드백을 통해 중단

# YOLO version
- YOLO v3
- YOLO v8
- YOLO v11

# 결과
## FPS
- YOLO v3: 약 10FPS
- YOLO v8: 약 25~35FPS
- YOLO v11: 약 25~35FPS
- YOLOv3의 경우 v8, v11에 비해 처리속도가 많이 느리다.

## 정확도
- v3, v8, v11 모두 정확도는 높은 수준
