from picamera import PiCamera
from datetime import datetime

class Camera:

    def __init__(self):
        self.camera = PiCamera()

    def start_recording(self):
        path = 'records/record-{0}.h264'.format(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        self.camera.start_preview()
        self.camera.start_recording(path)

    def stop_recording(self):
        self.camera.stop_recording()
        self.camera.stop_preview()
