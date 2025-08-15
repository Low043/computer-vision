from inference import get_model
from cv2.typing import MatLike
import supervision as sv
import json

class Reader:
    def __init__(self, model_id: str):
        self.model = get_model(model_id)

    def read_image(self, image: MatLike):
        results = self.model.infer(image)[0]
        return results
    
    def get_json(self, results):
        results_dict = results.model_dump()

        pretty_json = json.dumps(results_dict, indent=4)
        return pretty_json
    
    def visualize(self, image: MatLike, results):
        detections = sv.Detections.from_inference(results)

        # Caixas e labels
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # Adiciona as caixas e labels na imagem
        annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

        # Exibe a imagem em uma janela
        sv.plot_image(annotated_image)