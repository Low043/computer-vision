from services.Reader import Reader
import warnings

# Ignora avisos de hardware
warnings.filterwarnings("ignore", category = UserWarning, message="Specified provider .* is not in available provider names.*")

class Monitoring:
    def __init__(self):
        self.reader = Reader(model_id="7-segment-display-gxhnj/2")

    def run(self):
        results = self.reader.read_image("teste.png")

        print(self.reader.get_json(results))
        self.reader.visualize("teste.png", results)

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()