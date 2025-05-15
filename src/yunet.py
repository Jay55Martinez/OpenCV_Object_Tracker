from picamera2 import Picamera2
import cv2 as cv
import numpy as np
# current implementation of yunet.py works only on pc not rpi
# file ment to demonstrate the use of the yunet face detector and not for actual implementation

def visualize(image, faces, print_flag=False, fps=None):
    output = image.copy()

    if fps:
        cv.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    for idx, face in enumerate(faces):
        if print_flag:
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))

        coords = face[:-1].astype(np.int32)
        # Draw face bounding box
        cv.rectangle(output, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), 2)
        # Draw landmarks
        cv.circle(output, (coords[4], coords[5]), 2, (255, 0, 0), 2)
        cv.circle(output, (coords[6], coords[7]), 2, (0, 0, 255), 2)
        cv.circle(output, (coords[8], coords[9]), 2, (0, 255, 0), 2)
        cv.circle(output, (coords[10], coords[11]), 2, (255, 0, 255), 2)
        cv.circle(output, (coords[12], coords[13]), 2, (0, 255, 255), 2)
        # Put score
        cv.putText(output, '{:.4f}'.format(face[-1]), (coords[0], coords[1]+15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    return output

def main():
    # takes input frames from camera (pc not rpi)
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={'format':'XRGB8888', 'size':(3280,2464)}))
    camera.start()
    
    # if not cap.isOpened():
    #     print("Error: Could not open camera.")
    #     return
    
    image = camera.capture_array()
    yunet = cv.FaceDetectorYN.create('../out/face_detection_yunet_2022mar.onnx',  '', (0, 0))
    tm = cv.TickMeter()
    frame_w = int(image.shape[1])
    frame_h = int(image.shape[0])
    yunet.setInputSize([frame_w, frame_h])
    
    while True:
            frame = camera.capture_array()
            rgb_image = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)

            tm.start()
            _, faces = yunet.detect(rgb_image) # faces: None, or nx15 np.array
            tm.stop()

            print(faces)
            if faces is not None:
                frame = visualize(frame, faces, fps=tm.getFPS())
            cv.imshow('libfacedetection demo', frame)

            tm.reset()
        
            
            
            if cv.waitKey(20) & 0xFF==ord('d'):
                break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()