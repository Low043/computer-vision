import base64
import cv2

def ndarray_to_base64(image) -> str:
    """Converte uma imagem em formato ndarray para base64"""
    if image is str:
        return image

    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
