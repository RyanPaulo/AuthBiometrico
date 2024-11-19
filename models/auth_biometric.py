import cv2
import numpy as np
import os


#Class dedicada para as funções de reconhecimento e tratamento da biometria/ imagem

class Img_Biometric():
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = self.verification_img()

#Função para fazer o tratamento da imagem

    # Verificação da image
    def verification_img(self):
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

    # Função para fazer o processos nas imagem e a comparação
    def match_fingerprints(self, other_img):
        if self.img is None or other_img is None:
            print("Erro ao carregar a imagem,")
            return None


        # Convertendo a imagem para a escala de cinza
        if len(self.img.shape) == 3:
            pross_self_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            gray_self_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        else:
            pross_self_img = self.img

        if len(other_img.shape) == 3:
            pross_other_img = cv2.cvtColor(other_img, cv2.COLOR_BGR2GRAY)

        else:
            pross_other_img = other_img

        # Pré-processamento para redução de ruido
        pross_self_img = cv2.GaussianBlur(pross_self_img, (5, 5), 0)
        pross_other_img = cv2.GaussianBlur(pross_other_img, (5, 5), 0)

        # # Segmentação para realçar as caracteristicas
        _, segmented_self_img = cv2.threshold(pross_self_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, segmented_other_img = cv2.threshold(pross_other_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        intend_orb = cv2.ORB_create(nfeatures=20)

        kp1, des1 = intend_orb.detectAndCompute(pross_self_img, None)
        kp2, des2 = intend_orb.detectAndCompute(pross_other_img, None)

        estimate_bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = estimate_bf.knnMatch(des1, des2, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

                # Desenhando os postos parecidos
        img_matches = cv2.drawMatches(segmented_self_img, kp1, segmented_other_img, kp2, good_matches, None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('Imagem na escala de cinza', gray_self_img)
        cv2.imshow('Imagem Pre-processada', pross_self_img)
        cv2.imshow('Imagem Imagem original', self.img)
        cv2.imshow('Pontos Semelhantes  (Imagem adquirido) vs (imagem armazenada)', img_matches)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        if len(good_matches) > 15:

            print("Acesso concedido!")
            return True
        else:
            print("Acesso negado!")
            return False
        return







