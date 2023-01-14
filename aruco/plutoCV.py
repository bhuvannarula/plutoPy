import cv2 as cv
import numpy as np
from time import sleep
from .common import *

calib_path = "aruco/calib_data/MultiMatrix.npz"

FRAME_DELAY = 0

class video:
    def __init__(self) -> None:
        self.thresh = 80
        self.dim2 = (960, 540)
        self.dim1 = (1280, 720)
        self.dim = (1920, 1080)
        self.video = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.video.set(cv.CAP_PROP_FPS, 40)
        #self.video.set(cv.CAP_PROP_AUTOFOCUS, 0)
        self.video.set(cv.CAP_PROP_FRAME_WIDTH, self.dim[0])
        self.video.set(cv.CAP_PROP_FRAME_HEIGHT, self.dim[1])
        self.video.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        #self.video.set(cv.CAP_PROP_BUFFERSIZE, 1)
        #self.video.set(cv.CAP_PROP_FRAME_COUNT, 1)
        #self.video.set(cv.CAP_PROP_ISO_SPEED, 1/10000)
        self.video.set(cv.CAP_PROP_EXPOSURE, -6)
        self.video.set(cv.CAP_PROP_ISO_SPEED, -7)
        #_t_br = int(self.video.get(cv.CAP_PROP_BRIGHTNESS))
        #self.thresh = _t_br-30
        #self.video.set(cv.CAP_PROP_BRIGHTNESS, _t_br+10)
    def read(self):
        ret, frame = self.video.read()
        if not ret:
            raise ValueError
        frame = cv.rotate(frame, cv.ROTATE_180)
        
        return frame

class arucoGPS:
    def __init__(self, state : arucoState) -> None:
        calib = np.load(calib_path)
        self.video = video()

        self.target_id = 42

        self.cam_mat = calib["camMatrix"]
        self.dist_coef = calib["distCoef"]
        r_vectors = calib["rVector"]
        t_vectors = calib["tVector"]

        self.MARKER_SIZE_1 = 6 # cm
        self.MARKER_SIZE_2 = 6.5 # cm

        self.marker_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50)
        self.param_markers = cv.aruco.DetectorParameters_create()

        self.coord_data = {}

        self.dronePos = state

    def loop(self):
        #sleep(FRAME_DELAY)
        frame = self.video.read()
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #gray_frame = cv.bilateralFilter(gray_frame, 11, 17, 17)
        ret, gray_frame = cv.threshold(gray_frame, self.video.thresh, 255, cv.THRESH_BINARY)
        #gray_frame = cv.adaptiveThreshold(gray_frame, self.video.thresh, adaptiveMethod= cv.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType= cv.THRESH_BINARY, blockSize= 1, C= 2)
        marker_corners, marker_IDs, reject = cv.aruco.detectMarkers(
            gray_frame, self.marker_dict, parameters=self.param_markers
        )

        if marker_corners:
            rVec, tVec, _ = cv.aruco.estimatePoseSingleMarkers(
                marker_corners, self.MARKER_SIZE_2, self.cam_mat, self.dist_coef
            )
            total_markers = range(0, marker_IDs.size)
            for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left =  corners[3].ravel()

                distance = np.sqrt(
                    tVec[i][0][2]**2 + tVec[i][0][0]**2 + tVec[i][0][1]**2
                )

                _t_X = int((top_left[0] + bottom_right[0])/2)
                _t_Y = int((top_left[1] + bottom_right[1])/2)

                _t_x = int(tVec[i][0][0]*4)/4
                _t_y = int(tVec[i][0][1]*4)/4
                _t_z = int(tVec[i][0][2]*4)/4
                self.coord_data[ids[0]] = [_t_X, _t_Y, _t_z]
                #point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                cv.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                    bottom_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
            #print(self.coord_data)
            if self.target_id in self.coord_data:
                self.dronePos.update(self.coord_data[self.target_id])

        cv.imshow("frame", cv.resize(frame, self.video.dim2, cv.INTER_LINEAR))
        cv.imshow("gray", cv.resize(gray_frame, self.video.dim2, cv.INTER_LINEAR))
        key = cv.waitKey(1)
        if key == ord("q"):
            return self.stop()
        return 0

    def stop(self):
        self.video.video.release()
        cv.destroyAllWindows()
        return 1


if __name__ == "__main__":
    state = arucoState()
    aruco = arucoGPS(state)
    while True:
        _err = aruco.loop()