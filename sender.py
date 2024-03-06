import os, pickle, filelist, receiver

def send(who, sender, arg):
    len_who = len(pickle.dumps(who))
    os.write(sender, len_who.to_bytes(4, "big"))
    os.write(sender, pickle.dumps(who))

    if who == 'meow':
        # Longueur du message
        len_arg = len(arg)

        # Envoi de la longueur du message
        os.write(sender, len_arg.to_bytes(4, "big"))

        # Envoi du message
        os.write(sender, arg)
    else:
        # Longueur du message
        len_arg = len(pickle.dumps(arg))

        # Envoi de la longueur du message
        os.write(sender, len_arg.to_bytes(4, "big"))

        # Envoi du message
        os.write(sender, pickle.dumps(arg))

def sender(source, destination, recursive, server_read, client_read, client_write, server_write):
    # Fermeture des pipes inutiles
    os.close(server_write)
    os.close(server_read)


    # Liste des fichiers de la source

    files = filelist.creer_list(source, recursive)

    # Envoi de la liste des fichiers présents à la source
    send('', client_write, files)

    while True:
        # Attente du message du generator
        action, nom = receiver.receive(client_read)

        if action == 'creer':
            if os.path.isfile(source[0][0]):
                send('creer', client_write, 'file')
                send('creer', client_write, os.path.basename(source[0][0]))
                with open(source[0][0], 'rb') as f:
                    contenu = f.read()
                    send('creer', client_write, contenu)
                mod_time = os.path.getmtime(source[0][0])
                send('creer', client_write, mod_time)

            # Envoi du contenu du fichier au generator
            elif os.path.isfile(os.path.join(source[0][0], nom)):
                send('creer', client_write, 'file')
                send('creer', client_write, nom)
                with open(os.path.join(source[0][0], nom), 'rb') as f:
                    contenu = f.read()
                    send('creer', client_write, contenu)
                mod_time = os.path.getmtime(os.path.join(source[0][0], nom))
                send('creer', client_write, mod_time)

            elif os.path.isfile(nom) and not os.path.isdir(os.path.join(source[0][0], nom)):
                send('creer', client_write, 'file')
                send('creer', client_write, nom)
                with open(nom, 'rb') as f:
                    contenu = f.read()
                    send('creer', client_write, contenu)
                mod_time = os.path.getmtime(nom)
                send('creer', client_write, mod_time)

            else:

                send('creer', client_write, 'dir')
                send('creer', client_write, nom)

        elif action == 'update':
            if os.path.isfile(source[0][0]):
                send('update', client_write, 'file')
                send('update', client_write, os.path.basename(source[0][0]))
                with open(source[0][0], 'rb') as f:
                    contenu = f.read()
                    send('update', client_write, contenu)
                mod_time = os.path.getmtime(source[0][0])
                send('update', client_write, mod_time)

            # Envoi du contenu du fichier au generator
            elif os.path.isfile(os.path.join(source[0][0], nom)):
                send('update', client_write, 'file')
                send('update', client_write, nom)
                with open(os.path.join(source[0][0], nom), 'rb') as f:
                    contenu = f.read()
                    send('update', client_write, contenu)
                mod_time = os.path.getmtime(os.path.join(source[0][0], nom))
                send('update', client_write, mod_time)

            else:
                send('update', client_write, 'dir')
                send('update', client_write, nom)

        elif action == 'delete':
            if os.path.isfile(source[0][0]):
                send('delete', client_write, 'file')
                send('delete', client_write, os.path.basename(source[0][0]))

            # Envoi du contenu du fichier au generator
            elif os.path.isfile(os.path.join(destination, nom)):
                send('delete', client_write, 'file')
                send('delete', client_write, nom)

            else:
                send('delete', client_write, 'dir')
                send('delete', client_write, nom)

        elif action == 'end':
            send('end', client_write, None)
            # Le sender n'a plus rien à faire.

        else:
            break



    # Fermeture des pipes restants
    os.close(client_write)
    os.close(client_read)
