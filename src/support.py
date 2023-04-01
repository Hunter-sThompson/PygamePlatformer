from os import walk
import pygame
# import assets
def import_folder(path):
    surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path)
            surface_list.append(image_surf)
    if len(surface_list) == 0:
        print("Failure in import_folder support.py")
        print("From path: " + path)
        exit(-1)
    return surface_list
