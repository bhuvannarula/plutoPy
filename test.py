import cv2 as cv

class video:
    def __init__(self) -> None:
        self.dim = (960, 540)
        self.video = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.video.set(cv.CAP_PROP_FPS, 40)
        self.video.set(cv.CAP_PROP_FRAME_WIDTH, self.dim[0])
        self.video.set(cv.CAP_PROP_FRAME_HEIGHT, self.dim[1])
        #self.video.set(cv.CAP_PROP_BUFFERSIZE, 1)
        #self.video.set(cv.CAP_PROP_FRAME_COUNT, 1)
        #self.video.set(cv.CAP_PROP_ISO_SPEED, 1/10000)
        self.video.set(cv.CAP_PROP_ISO_SPEED, -11)
        #print(self.video.get(cv.CAP_PROP_ISO_SPEED))
    def read(self):
        ret, frame = self.video.read()
        if not ret:
            raise ValueError
        frame = cv.rotate(frame, cv.ROTATE_180)
        return frame

vid = video()

while True:
    cv.imshow("frame", vid.read())
    key = cv.waitKey(1)