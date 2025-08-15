from services.Watcher import Watcher
from services.Reader import Reader
import warnings
import os

# Ignora avisos de hardware
warnings.filterwarnings("ignore", category=UserWarning, message="Specified provider .* is not in available provider names.*")

class Monitoring:
    def __init__(self):
        self.watcher = Watcher(stream_url=os.getenv("STREAM_URL"), save_folder="images")
        self.reader = Reader(model_id="7-segment-display-gxhnj/2")

    def run(self):
        frame = self.watcher.get_frame(save_frame=True)
        results = self.reader.read_image(image=frame)
        json = self.reader.get_json(results=results)

        self.reader.visualize(image=frame, results=results)

if __name__ == "__main__":
    monitoring = Monitoring()

    while True:
        monitoring.run()