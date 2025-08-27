""" Declaração da classe Reader"""
from ultralytics import YOLO
from typing import TypedDict

class ExtractedValue(TypedDict):
    text: str
    x1: float
    x2: float
    conf: float

class Reader:
    """Classe responsável por ler os frames da stream e processar o resultado"""
    def __init__(self):
        self.model = YOLO('balancaReader.pt')

    def get_frame_text(self, frame):
        """Extrai o texto da imagem usando o modelo YOLO e formata o resultado"""
        result = self.model.predict(frame, iou=0, verbose=False)[0]

        extracted_values = []
        for box in result.boxes:
            extracted_values.append(self.__get_box_values(box, result.names))

        final_result = self.__refine_values(extracted_values)

        return [final_result, result.plot()]
    
    def __get_box_values(self, box, names) -> ExtractedValue:
        return {
            'text': names.get(box.cls.item()),
            'x1': box.xyxy[0][0].item(),
            'x2': box.xyxy[0][2].item(),
            'conf': box.conf.item()
        }
    
    def __refine_values(self, values: list[ExtractedValue]):
        ordered_values = self.__order_values(values)
        no_overlap_values = self.__remove_overlaps(ordered_values)
        final_result = self.__join_values(no_overlap_values)

        return final_result
    
    def __order_values(self, values: list[ExtractedValue]):
        return sorted(values, key=lambda x: x['x1'])
    
    def __remove_overlaps(self, ordered_values: list[ExtractedValue]):
        for i in range(len(ordered_values) - 1):
            current = ordered_values[i]
            next = ordered_values[i + 1]

            if next['x1'] < current['x2']:
                minor_conf = current if current['conf'] < next['conf'] else next
                minor_conf['text'] = ''

        return ordered_values
    
    def __join_values(self, values: list[ExtractedValue]):
        return ''.join([value['text'] for value in values]).replace('.','')
