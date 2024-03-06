import os, pickle, filelist, sender, receiver, checksums

def generator(update, size_only, ssh, source, files, destination, dirs, recursive, delete, server_read, client_write, client_read, server_write):

    # Fermeture des pipes inutiles
    os.close(client_write)
    os.close(client_read)

    # Fichier de la destination
    if os.path.isfile(source[0][0]):
        if os.path.isdir(destination):
            dest_file = filelist.creer_list([[destination]], recursive)

            if os.path.basename(source[0][0]) not in dest_file or os.path.isdir(os.path.join(destination, os.path.basename(source[0][0]))):
                sender.send('creer', server_write, source[0][0])

            elif size_only:
                if int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination + '/' + os.path.basename(source[0][0]))):
                    sender.send('update', server_write, source[0][0])

            elif update:
                if int(os.path.getmtime(source[0][0])) > int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) or (int(os.path.getmtime(source[0][0])) == int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) and int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination + '/' + os.path.basename(source[0][0])))):
                    sender.send('update', server_write, source[0][0])

            elif int(os.path.getmtime(source[0][0])) != int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) or os.path.getsize(source[0][0]) != os.path.getsize(destination + '/' + os.path.basename(source[0][0])):
                sender.send('update', server_write, source[0][0])

        elif os.path.isdir(destination + '/'):
            dest_file = filelist.creer_list([[destination + '/']], recursive)

            if source[0][0] not in dest_file or (os.path.basename(source[0][0]) not in dest_file):
                sender.send('creer', server_write, source[0][0])

            elif size_only:
                if int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination + '/' + os.path.basename(source[0][0]))):
                    sender.send('update', server_write, source[0][0])

            elif update:
                if int(os.path.getmtime(source[0][0])) > int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) or (int(os.path.getmtime(source[0][0])) == int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) and int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination + '/' + os.path.basename(source[0][0])))):
                    sender.send('update', server_write, source[0][0])

            elif int(os.path.getmtime(source[0][0])) != int(os.path.getmtime(destination + '/' + os.path.basename(source[0][0]))) or os.path.getsize(source[0][0]) != os.path.getsize(destination + '/' + os.path.basename(source[0][0])):
                sender.send('update', server_write, source[0][0])

        elif not os.path.exists(destination):
            sender.send('creer', server_write, source[0][0])

        elif size_only:
            if int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination)):
                sender.send('update', server_write, source[0][0])

        elif update:
            if int(os.path.getmtime(source[0][0])) > int(os.path.getmtime(destination)) or (int(os.path.getmtime(source[0][0])) == int(os.path.getmtime(destination)) and int(os.path.getsize(source[0][0])) != int(os.path.getsize(destination))):
                sender.send('update', server_write, source[0][0])

        # Si le fichier est dans la source mais pas dans la destination, il va demander au client de créer le fichier en question
        elif os.path.isfile(destination) and int(os.path.getmtime(source[0][0])) != int(os.path.getmtime(destination)) or os.path.getsize(source[0][0]) != os.path.getsize(destination):
            sender.send('update', server_write, source[0][0])

    else:
        if dirs or recursive or (source[0][0] == '.') or ssh:
        # Liste des fichiers de la destination
            if destination.endswith('/'):
                dest_files = filelist.creer_list([[destination]], recursive)

            else:
                dest_files = filelist.creer_list([[destination + '/']], recursive)

        if (dirs and os.path.isdir(source[0][0])) or recursive or ssh:
            for f in files:
                if f not in dest_files or((os.path.isfile(os.path.join(source[0][0],f)) and os.path.isdir(os.path.join(destination, f)))) or ((os.path.isdir(os.path.join(source[0][0],f)) and os.path.isfile(os.path.join(destination, f)))) or not os.path.exists(os.path.join(destination, f)):
                    # Si le fichier est dans la source mais pas dans la destination, il va demander au client de créer le fichier en question
                    sender.send('creer', server_write, f)

                elif os.path.isdir(os.path.join(destination, f)):
                    pass

                elif size_only:
                    if int(os.path.getsize(os.path.join(source[0][0], f))) != int(os.path.getsize(os.path.join(destination, f))):
                        sender.send('update', server_write, f)

                elif update:
                    if source[0][0].endswith('/'):
                        if int(os.path.getmtime(os.path.join(source[0][0], f))) > int(os.path.getmtime(os.path.join(destination, f))) or (int(os.path.getmtime(os.path.join(source[0][0], f))) == int(os.path.getmtime(os.path.join(destination, f))) and os.path.getsize(os.path.join(source[0][0], f)) != os.path.getsize(os.path.join(destination, f))):
                            sender.send('update', server_write, f)
                    else:
                        if int(os.path.getmtime(f)) > int(os.path.getmtime(os.path.join(destination, f))) or (int(os.path.getmtime(f)) == int(os.path.getmtime(os.path.join(destination, f))) and os.path.getsize(f) != os.path.getsize(os.path.join(destination, f))):
                            sender.send('update', server_write, f)

                # Si fichier présent dans la source et dans la destination, il va demander au client de mettre à jour le fichier en question si la date de modification ou la taille est différente
                elif source[0][0].endswith('/'):
                    if int(os.path.getmtime(os.path.join(source[0][0], f))) != int(os.path.getmtime(os.path.join(destination, f))) or os.path.getsize(os.path.join(source[0][0], f)) != os.path.getsize(os.path.join(destination, f)):
                        sender.send('update', server_write, f)

                elif int(os.path.getmtime(f)) != int(os.path.getmtime(os.path.join(destination, f))) or os.path.getsize(f) != os.path.getsize(os.path.join(destination, f)):
                    sender.send('update', server_write, f)

                else:
                    if dirs:
                        if not os.path.exists(os.path.join(destination,files[0])):
                            sender.send('creer', server_write, files[0])

        if ((delete and recursive) or (delete and dirs)) and source[0][0].endswith('/'):
            if destination.endswith('/'):
                dest_file2 = filelist.creer_list([[destination]], recursive)
            else:
                dest_file2 = filelist.creer_list([[destination + '/']], recursive)
            files2 = filelist.creer_list(source, recursive)
            for f in dest_file2:
                if f not in files2:
                    if f != destination:
                        sender.send('delete', server_write, f)

    # Préviens le sender, que le generator à finis
    sender.send('end', server_write, None)

    # Fermeture des pipes restants
    os.close(server_read)
    os.close(server_write)
