"""Declaração da classe Messager"""
import requests
import os
from utils.converter import ndarray_to_base64

class Messager:
    """Classe responsável por enviar mensagens para a API do WhatsApp"""
    def __init__(self, api_url):
        self.api_url = api_url
        self.process_id = os.getpid()

    def send_message(self, message, image=None, weight=None):
        """Envia uma mensagem para a API do WhatsApp"""
        if image is not None:
            image = ndarray_to_base64(image)
        try:
            requests.post(self.api_url, json = { 'image': image, 'weight': weight, 'message': message, 'pid': self.process_id }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

    def send_start_message(self):
        """Define uma mensagem de inicio para a API do WhatsApp"""
        message = "🤖 Iniciando monitoramento de peso no guincho"
        self.send_message(message)

    def send_stop_message(self, image, max_weight_detected):
        """Define uma mensagem de fim para a API do WhatsApp"""
        message = f'''🤖 Encerrando monitoramento de peso no guincho
⚠ Peso máximo detectado: {max_weight_detected}kg
🔎 Confirme o peso na imagem em anexo'''
        self.send_message(message, image)

    def send_weight_exceeded_message(self, weight_trigger, detected_weight, image, timestamp):
        """Define uma mensagem de alerta para a API do WhatsApp"""
        message = f'''⚠ POSSÍVEL EXCESSO DE PESO NO GUINCHO
🔎 Confirme o peso na imagem em anexo
🕒 Horário: {timestamp}
🔴 Situação: Valor pode exceder o limite de {weight_trigger}kg
📍 Local: Área de Carga - *Elevador Principal* - Extração 2 - Acesso B1
👥 Notificação enviada a Central de monitoramento, Corpo técnico e Supervisores'''
        self.send_message(message, image, detected_weight)
