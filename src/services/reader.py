""" Declaração da classe Reader"""
from ultralytics import YOLO

class Reader:
    """Classe responsável por ler os frames da stream e processar o resultado"""
    def __init__(self):
        self.model = YOLO('balancaReader.pt')

    def get_frame_text(self, frame):
        """Extrai o texto da imagem usando o modelo YOLO e formata o resultado"""
        result = self.model.predict(frame, iou=0, verbose=False)[0]

        extracted_values = []
        for box in result.boxes:
            text_value = result.names.get(box.cls.item())
            x1 = box.xyxy[0][0].item()
            extracted_values.append([text_value, x1])

        ordered_values = sorted(extracted_values, key=lambda x: x[1])
        final_result = ''.join([value[0] for value in ordered_values]).replace('.','')

        return [final_result, result.plot()]
