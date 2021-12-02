from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    
    def binarisation(self, S):
		# creation d'une image vide
        im_bin = Image()
        
        # affectation a l'image im_bin d'un tableau de pixels de meme taille
        # que self dont les intensites, de type uint8 (8bits non signes),
        # sont mises a 0
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))

        # TODO: boucle imbriquees pour parcourir tous les pixels de l'image im_bin
        # et calculer l'image binaire
        for i in range(self.H):
            for j in range(self.W):
                if self.pixels[i,j] >= S:
                    im_bin.pixels[i,j] = 255
                else:
                    im_bin.pixels[i,j] = 0
        
        return im_bin


    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        
        cmin = self.W
        cmax = 0
        lmin = self.H
        lmax = 0

        for i in range (self.H):
            for j in range (self.W):
                if self.pixels[i,j] == 0:
                    if i <= lmin:
                        lmin = i
                    if i >= lmax:
                        lmax = i
                    if j <= cmin:
                        cmin = j
                    if j >= cmax:
                        cmax = j
        img=self.pixels[lmin:lmax+1,cmin:cmax+1]
        imagette = Image()
        imagette.set_pixels(img)
        return imagette
    

    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        im_resized = Image()
        im_resized.H = new_H
        im_resized.W = new_W
        im_resized.pixels = resize(self.pixels, (new_H,new_W), 0)
        im_resized.pixels = np.uint8(im_resized.pixels*255)
        return im_resized
        
    



    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, im):
        im_bin = self.binarisation(127)
        nb_similitude = 0
        nb_pixels = 0
        res = 0
        self.resize(60, 60)
        im.resize(60, 60)
        for i in range (im_bin.H):
            for j in range (im_bin.W):
                if self.pixels[i][j] == im.pixels[i][j] :
                    nb_similitude = nb_similitude+1
                nb_pixels = nb_pixels+1
        res = nb_similitude / nb_pixels             
        return res
    
    
