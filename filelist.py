import os, sys, options

def creer_list(source_paths, recursive):
    file_list = []
    args = options.parse_arguments()

    # On parcourt la liste des fichiers/dossiers
    for path in source_paths[0]:
        # Si le chemin est un fichier, on l'ajoute à la liste
        if os.path.isfile(path):
            file_list.append(os.path.basename(path))

        # Si le chemin est un dossier, on l'ajoute à la liste
        elif os.path.isdir(path):
            # Si le chemin se termine par un slash ou s'il est égal à un point
            if path.endswith('/') or path == ('.'):
                for root, dirs, files in os.walk(path):
                    # On parcourt les fichiers et dossiers
                    for dirs in dirs:
                        dir_path = os.path.join(root, dirs)
                        file_list.append(os.path.relpath(dir_path, path))
                    # On parcourt les fichiers
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_list.append(os.path.relpath(file_path, path))
                    # Si on ne veut pas parcourir récursivement
                    if not recursive:
                        break
            # Sinon, on ajoute le dossier à la liste
            else:
                file_list.append(os.path.basename(path))
                if recursive:
                    for root, dirs, files in os.walk(path):
                        # On parcourt les fichiers et dossiers
                        for dir_name in dirs:
                            dir_path = os.path.join(root, dir_name)
                            file_list.append(os.path.basename(path) + '/' + os.path.relpath(dir_path, path))
                        # On parcourt les fichiers
                        for file_name in files:
                            file_path = os.path.join(root, file_name)
                            file_list.append(os.path.basename(path) + '/' + os.path.relpath(file_path, path))
                        # Si on ne veut pas parcourir récursivement
                        if not recursive:
                            break

        # Sinon, on affiche un message d'erreur
        else:
            if not args.quiet:
                print(f"{path} is not a valid file or directory.")
            sys.exit(1)

    return file_list
