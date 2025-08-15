from inference import get_model
import supervision as sv
import json
import cv2

class Reader:
    def __init__(self, model_id: str):
        self.model = get_model(model_id)

    def read_image(self, image_path: str):
        image = cv2.imread(image_path)

        results = self.model.infer(image)[0]
        return results
    
    def get_json(self, results):
        results_dict = results.model_dump()

        pretty_json = json.dumps(results_dict, indent=4)
        return pretty_json
    
    def visualize(self, image_path: str, results):
        image = cv2.imread(image_path)
        detections = sv.Detections.from_inference(results)

        # Caixas e labels
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # Adiciona as caixas e labels na imagem
        annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

        # Exibe a imagem em uma janela
        sv.plot_image(annotated_image)