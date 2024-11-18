import cv2
import numpy as np
import os


#Class dedicada para as funções de reconhecimento e tratamento da biometria/ imagem

class Img_Biometric():
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = self.convert_img()

#Função para fazer o tratamento da imagem

    # Convertendo a image para a escala de cinza e fazendo o pré-processamento
    def convert_img(self):
        if not os.path.exists(self.img_path):
            print(f"Erro: camonho da imagem '{self.img_path}' não encontrada")
            return None

        img = cv2.imread(self.img_path)
        if img is None:
            print(f"Erro ao carregar imagem: {self.img_path}")
            return None

        # Convertendo a imagem para a escala de cinza
        if len(img.shape) == 3:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = img

        # Pré-processamento para redução de ruido
        gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

        # Segmentação para realçar as caracteristicas
        _, segmented_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY +
                                         cv2.THRESH_OTSU)

        return segmented_img


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

        if len(self.img.shape) == 3:
            gray_self_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            gray_self_img = self.img

        if len(other_img.shape) == 3:
            gray_other_img = cv2.cvtColor(other_img, cv2.COLOR_BGR2GRAY)

        else:
            gray_other_img = other_img

        # Pré-processamento
        gray_self_img = cv2.GaussianBlur(gray_self_img, (5, 5), 0)
        gray_other_img = cv2.GaussianBlur(gray_other_img, (5, 5), 0)

        # Segmentação
        _, segmented_self_img = cv2.threshold(gray_self_img, 0, 255, cv2.THRESH_BINARY +
                                              cv2.THRESH_OTSU)
        _, segmented_other_img = cv2.threshold(gray_other_img, 0, 255, cv2.THRESH_BINARY +
                                               cv2.THRESH_OTSU)



        intend_orb = cv2.ORB_create(nfeatures=20)

        kp1, des1 = intend_orb.detectAndCompute(gray_self_img, None)
        kp2, des2 = intend_orb.detectAndCompute(gray_other_img, None)

        estimate_bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = estimate_bf.knnMatch(des1, des2, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)



        if len(good_matches) > 15:
            # Desenhando os postos parecidos
            img_matches = cv2.drawMatches(self.img, kp1, other_img, kp2, good_matches, None,
                                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imshow('Pontos semelhantes', img_matches)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Acesso concedido!")
            return True
        else:
            print("Acesso negado!")
            return False
        return







