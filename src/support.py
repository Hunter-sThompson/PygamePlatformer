from os import walk
import pygame
# import assets
def import_folder(path):
    print("Importfolder: Path = " + path)
    surface_list = []
    for _, _, img_files in walk(path):
        print("Image")
        for image in img_files:
            full_path = path + '/' + image
            print("Imported asset: " + full_path)
            image_surf = pygame.image.load(full_path)
            surface_list.append(image_surf)
    if len(surface_list) == 0:
        print("Failure in import_folder support.py")
        exit(-1)
    return surface_list