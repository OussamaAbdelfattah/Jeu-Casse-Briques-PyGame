import pygame
import random
import sys

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)

# Ajout d'une police de caractères pour le texte
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu de casse-briques")

# Horloge pour contrôler les images par seconde
horloge = pygame.time.Clock()

# Dimensions de la barre
barre_largeur = 100
barre_hauteur = 10

# Position de départ de la barre
barre_x = (largeur_fenetre - barre_largeur) // 2
barre_y = hauteur_fenetre - 50

# Vitesse de déplacement de la barre
barre_vitesse = 5

# Dimensions de la balle
balle_rayon = 10

# Position de départ de la balle
balle_x = largeur_fenetre // 2
balle_y = barre_y - balle_rayon

# Vitesse de déplacement de la balle
balle_vitesse_x = 3
balle_vitesse_y = -3

# Dimensions des briques
brique_largeur = 60
brique_hauteur = 20

# Nombre de briques par rangée et nombre de rangées
nb_briques_x = largeur_fenetre // (brique_largeur + 10)
nb_briques_y = 5

# Liste pour stocker les briques
briques = []
for i in range(nb_briques_y):
    for j in range(nb_briques_x):
        brique = pygame.Rect(j * (brique_largeur + 10) + 50, i * (brique_hauteur + 10) + 50, brique_largeur, brique_hauteur)
        briques.append(brique)

# Variables pour gérer l'état du jeu
jeu_termine = False
victoire = False

# Boucle principale du jeu
while not jeu_termine:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_termine = True

    # Déplacement de la barre
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT] and barre_x > 0:
        barre_x -= barre_vitesse
    if touches[pygame.K_RIGHT] and barre_x < largeur_fenetre - barre_largeur:
        barre_x += barre_vitesse

    # Déplacement de la balle
    balle_x += balle_vitesse_x
    balle_y += balle_vitesse_y

    # Rebond de la balle sur les bords de l'écran
    if balle_x <= 0 or balle_x >= largeur_fenetre - balle_rayon:
        balle_vitesse_x = -balle_vitesse_x
    if balle_y <= 0:
        balle_vitesse_y = -balle_vitesse_y

    # Rebond de la balle sur la barre
    if balle_y + balle_rayon >= barre_y and balle_x + balle_rayon >= barre_x and balle_x - balle_rayon <= barre_x + barre_largeur:
        balle_vitesse_y = -balle_vitesse_y

    # Gestion de la collision entre la balle et les briques
    for brique in briques:
        if pygame.Rect(balle_x - balle_rayon, balle_y - balle_rayon, 2 * balle_rayon, 2 * balle_rayon).colliderect(brique):
            briques.remove(brique)
            balle_vitesse_y = -balle_vitesse_y
            break

    # Vérification de la fin du jeu
    if balle_y >= hauteur_fenetre - balle_rayon:
        jeu_termine = True

    # Vérification de la victoire
    if len(briques) == 0:
        jeu_termine = True
        victoire = True

    # Affichage des éléments du jeu
    fenetre.fill(NOIR)
    pygame.draw.rect(fenetre, BLANC, (barre_x, barre_y, barre_largeur, barre_hauteur))
    pygame.draw.circle(fenetre, ROUGE, (balle_x, balle_y), balle_rayon)

    for brique in briques:
        pygame.draw.rect(fenetre, VERT, brique)

    pygame.display.flip()

    # Limite les images par seconde
    horloge.tick(60)

# Affichage du message de fin
if victoire:
    message = font.render("Félicitations, Vous avez gagné !!", True, ROUGE)
    fenetre.blit(message, (50, hauteur_fenetre // 2 - 15))
else:
    message = font.render("Vous avez perdu !!", True, ROUGE)
    fenetre.blit(message, (50, hauteur_fenetre // 2 - 15))

    pygame.display.flip()

    # Attente avant de quitter
    pygame.time.delay(3000)  # Attendre 3 secondes (3000 millisecondes)
    pygame.quit()
    sys.exit()
