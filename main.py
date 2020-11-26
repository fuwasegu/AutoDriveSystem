import cv2
import dlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from lauda import stopwatchcm

detector_stop_sign = dlib.simple_object_detector("detector_stop_sign.svm")
detector_do_not_park_sign = dlib.simple_object_detector("detector_do_not_park_sign.svm")
detector_do_not_park_and_stop = dlib.simple_object_detector("detector_do_not_park_and_stop.svm")


def main():
    cap = cv2.VideoCapture(0)

    counter1 = 0
    find_flag1 = 0
    counter2 = 0
    find_flag2 = 0
    counter3 = 0
    find_flag3 = 0
    # dets1 = []
    # dets2 = []
    # dets3 = []
    while True:
        ret, frame = cap.read()
        if ret == False:
            break


        with stopwatchcm():
            dets1 = detector_stop_sign(frame, 0)
            dets2 = detector_do_not_park_sign(frame, 0)
            dets3 = detector_do_not_park_and_stop(frame, 0)

            # executor = ThreadPoolExecutor(max_workers=3) # 3じゃなくてもよさそう
            # future1 = executor.submit(process_stop, frame)
            # future2 = executor.submit(process_do_not_park, frame)
            # future3 = executor.submit(process_do_not_park_and_stop, frame)

            # while future1.running() and future2.running() and future3.running():
            #     pass

            # dets1 = future1.result()
            # dets2 = future2.result()
            # dets3 = future3.result()

            print('getting 2 detses')

        with stopwatchcm():
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
            if len(dets3) > 0:
                counter3 += 1
            else:
                counter3 = 0
                find_flag3 = 0

            print('counting')

        with stopwatchcm():
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
            if counter3 >= 10:
                for det in dets3:
                    cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), (0, 0, 255), 3)
                if find_flag3 == 0:
                    subprocess.Popen(['say', '駐停車禁止エリアです'])
                    find_flag3 = 1
            
            print('prepare rectangle if detects')
        
        with stopwatchcm():
            cv2.imshow("frame", frame)

            print('showing image')

        if cv2.waitKey(1) == 27: # ESCキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()


def process_stop(frame):
    dets1 = detector_stop_sign(frame, 0)
    return dets1

def process_do_not_park(frame):
    dets2 = detector_do_not_park_sign(frame, 0)
    return dets2

def process_do_not_park_and_stop(frame):
    dets3 = detector_do_not_park_and_stop(frame, 0)
    return dets3

if __name__ == '__main__':
    main()
