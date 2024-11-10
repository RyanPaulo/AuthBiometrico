import cv2
import numpy as np
import os

#Class dedicada para as funções de reconhecimento e tratamento da biometria/ imagem

class Img_Biometric():
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = self.convert_img()

    #Função para fazer o tratamento da imagem
    #Converta para a escala de cinza
    def convert_img(self):
        if not os.path.exists(self.img_path):
            print(f"Erro: camonho da imagem '{self.img_path}' não encontrada")
            return None

        img = cv2.imread(self.img_path)
        if img is None:
            print(f"Erro ao carregar imagem: {self.img_path}")
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    #Converter a imagem em bytes, para ser armazenado no banco de dados
    def img_to_byte(self):
        if self.img is None:
            print("imagem não corregada")
            return None
        _, img_byte = cv2.imencode('.jpg', self.img)
        return img_byte.tobytes()

    #Função para fazer a conversao ds bytes para imagen
    def byte_to_img(self, blob):
        img_array = np.frombuffer(blob, np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    #Função para fazer a comparação das imagens
    def match_fingerprints(self, other_img):
        if self.img is None or other_img is None:
            print("Erro ao carregar a imagem,")
            return None
        difference = cv2.norm(self.img, other_img, cv2.NORM_L1)
        return difference
