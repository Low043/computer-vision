import numpy as np
import cv2

class Watcher:
    def __init__(self, streamUrl: str, saveFolder: str):
        self.streamUrl = streamUrl
        self.saveFolder = saveFolder
        
    def getMultipleFrames(self, numFrames: int) -> list[np.ndarray]:
        frames = []
        cap = cv2.VideoCapture(self.streamUrl)

        for _ in range(numFrames):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()
        
        return frames
        
    def stackFrames(self, frames: list[np.ndarray], saveFrame: bool = False):
        stackedFrame = np.mean(frames, axis=0).astype(np.uint8)
        if saveFrame:
            cv2.imwrite(f'{self.saveFolder}/stackedFrame.png', stackedFrame)

        return stackedFrame