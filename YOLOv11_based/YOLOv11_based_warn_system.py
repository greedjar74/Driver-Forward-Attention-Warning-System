import cv2
import numpy as np
import time
import pygame
from ultralytics import YOLO

classes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'eye']
font = cv2.FONT_HERSHEY_PLAIN

# YOLO 모델 로드
model = YOLO('YOLOv11_based/YOLOv11s_epochs_250_batch_16_imgsz_224_best.pt')

# 경고 이미지 및 사운드 설정
warning = cv2.imread("YOLOv11_based/warn_image.png", cv2.IMREAD_UNCHANGED)
warning_resize = cv2.resize(warning, dsize=(1000, 1000))
warning_sound = "YOLOv11_based/warn_sound.mp3"

# OpenCV 캡처 객체 생성
capture = cv2.VideoCapture(1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

prevTime = time.time()
warning_time = 2
last_detect_time = time.time()
war = 0


# pygame 오디오 초기화
pygame.mixer.init()

while True:
    ret, frame = capture.read()
    if not ret:
        break

    # YOLOv8을 이용한 객체 탐지
    results = model.predict(frame, conf=0.5)  # 신뢰도 50% 이상

    # 눈 감지 확인
    eye_cnt = 0
    for result in results:
        boxes = result.boxes  # 탐지된 박스들
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 경계 박스 좌표
            conf = box.conf[0].item()  # 신뢰도
            cls = int(box.cls[0].item())  # 클래스 ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 감지된 눈 표시
            cv2.putText(frame, f'{conf:.4f}', (x1, y1-30), font, 2, (0, 255, 0), 2)
            eye_cnt += 1

    # FPS 계산
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / sec if sec > 0 else 0
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    print(fps)

    # 눈 감지 로직
    if eye_cnt >= 1:
        last_detect_time = time.time()  # 정상 시각 업데이트

    if time.time()-last_detect_time>warning_time:
        print(time.time()-last_detect_time, warning_time)
        print("경고 (종료: 2초)")
        pygame.mixer.init() # mixer생성
        pygame.mixer.music.load(warning_sound)
        pygame.mixer.music.play(-1)
        cv2.imshow("WARNING", warning_resize)
        cv2.waitKey(2000)  # 2초 동안 경고창 표시
        cv2.destroyWindow("WARNING") # 2초 후 창 닫기 -> 사용자의 피드백 필요 없음
        pygame.mixer.quit() # mixer삭제
        last_detect_time = time.time()
        detect_time2 = time.time()
        war = 1

    # 이전에 경고가 있었고 마지막으로 전방주시가 정상이었던 시각과 현재 시각의 차이가 1초를 넘어간 경우
    elif war == 1 and time.time() - last_detect_time > 1: # 2차 경고 출력
        print("경고 (종료: 사용자 피드백)")
        pygame.mixer.init() # mixer 생성
        pygame.mixer.music.load(warning_sound) # 경고음 파일 로드
        pygame.mixer.music.play(-1) # 경고음 재생 -> 무한반복

        cv2.imshow("WARNING", warning_resize) # 경고 이미지 출력
        key = cv2.waitKey(0)
        
        # 사용자의 피드백이 있는 경우 경고 종료
        if key == ord('t'):  # 키보드의 t 를 누르면 무한루프가 멈춤
            cv2.destroyWindow("WARNING")
            pygame.mixer.music.stop()
        war = 0
        last_detect_time = time.time()
        #앞선 경고에도 불구하고 다시 한번 더 걸렸기 때문에 운전자가 직접 특정 버튼을
        #눌러야 경고창이 사라지도록 함, 특정한 경고가 울리는 시간을 정하지 않고
        #운전자가 버튼을 누르면 경고가 꺼지도록 알고리즘을 정함

    # 이전에 경고가 있은 후 전방주시가 1초간 정상인 경우 -> 초기화
    if war == 1 and last_detect_time - detect_time2 > 1:
        war = 0
        detect_time2 = time.time()

    # 화면 출력
    cv2.imshow("Image", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
pygame.mixer.quit()