import cv2
import dlib
import subprocess

#鯉の動画（input.mp4）をキャプチャーする.
cap = cv2.VideoCapture("test2.mov")

detector_stop_sign = dlib.simple_object_detector("detector_stop_sign.svm")
detector_do_not_park_sign = dlib.simple_object_detector("detector_do_not_park_sign.svm")

counter1 = 0
find_flag1 = 0
counter2 = 0
find_flag2 = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    dets1 = detector_stop_sign(frame, 0)
    dets2 = detector_do_not_park_sign(frame, 0)
    print('Stop sign: ', end='')
    print(dets1)
    print('Do not park sign: ', end='')
    print(dets2)
    if len(dets1) > 0:
        counter1 += 1
    else:
        counter1 = 0
        find_flag1 = 0
    if len(dets2) > 0:
        counter2 += 1
    else:
        counter2 = 0
        find_flag2 = 0

    if counter1 >= 10:
        for det in dets1:
            cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), (255, 0, 0), 3)
        if find_flag1 == 0:
            subprocess.Popen(['say', '前方に一時停止標識があります'])
            find_flag1 = 1
    if counter2 >= 10:
        for det in dets2:
            cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), (0, 255, 0), 3)
        if find_flag2 == 0:
            subprocess.Popen(['say', '駐車禁止エリアです'])
            find_flag2 = 1
    
    cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == 27: # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()