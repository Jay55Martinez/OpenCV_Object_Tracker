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
    cap = cv.VideoCapture(0) 
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    yunet = cv.FaceDetectorYN.create('../out/face_detection_yunet_2022mar.onnx',  '', (0, 0))
    tm = cv.TickMeter()
    frame_w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    yunet.setInputSize([frame_w, frame_h])
    
    while True:
            has_frame, frame = cap.read()
            if not has_frame:
                print('No frames grabbed!')

            tm.start()
            _, faces = yunet.detect(frame) # faces: None, or nx15 np.array
            tm.stop()

            frame = visualize(frame, faces, fps=tm.getFPS())
            cv.imshow('libfacedetection demo', frame)

            tm.reset()
        
            
            
            if cv.waitKey(20) & 0xFF==ord('d'):
                break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()