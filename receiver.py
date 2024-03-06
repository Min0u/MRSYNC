import os, pickle, filelist, receiver, shutil, sys

import sender


def receive(receiver):
    len_what = int.from_bytes(os.read(receiver, 4), "big")
    what = pickle.loads(os.read(receiver, len_what))


    # si c'est un message
    if what == 'meow':
        # longueur du message
        len_arg = int.from_bytes(os.read(receiver, 4), "big")
        # recupere le message
        arg = os.read(receiver, len_arg)

    else:
        # longueur du message
        len_arg = int.from_bytes(os.read(receiver, 4), "big")
        # recupere le message
        arg = pickle.loads(os.read(receiver, len_arg))

    return what, arg

def receiver(delete, quiet, force, verbose, source, destination, server_read, client_write, client_read, server_write):
    # ferme les pipes inutiles
    os.close(client_read)

    while True:
        # recupere las info de sender
        reponse = receive(server_read)
        action = reponse[0]

        if action == 'creer':
            type = reponse[1]

            # type
            if type == 'file':
                # recupere le nom du fichier
                _,nom = receive(server_read)

                # recupere le contenu du fichier
                _,contenu = receive(server_read)

                # recupere la date de modification
                _,mod_time = receive(server_read)

                # cree le fichier
                if os.path.isfile(nom):
                    if os.path.isdir(destination):
                        if os.path.isfile(nom) and os.path.isdir(os.path.join(destination, os.path.basename(nom))):
                            try:
                                os.rmdir(os.path.join(destination, nom))
                                if verbose:
                                    print('Directory deleted : ' + nom)
                                with open(os.path.join(destination, nom), 'wb') as f:
                                    f.write(contenu)
                                if verbose:
                                    print('File created : ' + nom)
                                a_time = os.path.getatime(os.path.join(destination, nom))
                                os.utime(os.path.join(destination, nom), (a_time, mod_time))
                            except:
                                if force:
                                    shutil.rmtree(os.path.join(destination, nom))
                                    if verbose:
                                        print('Directory deleted : ' + nom)
                                    with open(os.path.join(destination, nom), 'wb') as f:
                                        f.write(contenu)
                                    if verbose:
                                        print('File created : ' + nom)
                                    a_time = os.path.getatime(os.path.join(destination, nom))
                                    os.utime(os.path.join(destination, nom), (a_time, mod_time))
                                else:
                                    if not quiet:
                                        print('cannot delete non-empty directory: ' + nom + '\ncould not make way for new regular file: ' + nom)
                        else:
                            with open(os.path.join(destination, nom), 'wb') as f:
                                f.write(contenu)
                            if verbose:
                                print('File created : ' + nom)
                            a_time = os.path.getatime(os.path.join(destination, nom))
                            os.utime(os.path.join(destination, nom), (a_time, mod_time))

                    else:
                        with open(destination, 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File created : ' + destination)
                        a_time = os.path.getatime(destination)
                        os.utime(destination, (a_time, mod_time))
                else:
                    print(nom)
                    if (os.path.isfile(os.path.join(source[0][0],nom)) or os.path.isfile(nom)) and os.path.isdir(os.path.join(destination, os.path.basename(nom))):
                        try:
                            os.rmdir(os.path.join(destination, nom))
                            if verbose:
                                print('Directory deleted : ' + nom)
                            with open(os.path.join(destination, nom), 'wb') as f:
                                f.write(contenu)
                            if verbose:
                                print('File created : ' + nom)
                            a_time = os.path.getatime(os.path.join(destination, nom))
                            os.utime(os.path.join(destination, nom), (a_time, mod_time))
                        except:
                            if force:
                                shutil.rmtree(os.path.join(destination, nom))
                                if verbose:
                                    print('Directory deleted : ' + nom)
                                with open(os.path.join(destination, nom), 'wb') as f:
                                    f.write(contenu)
                                if verbose:
                                    print('File created : ' + nom)
                                a_time = os.path.getatime(os.path.join(destination, nom))
                                os.utime(os.path.join(destination, nom), (a_time, mod_time))
                            else:
                                if not quiet:
                                    print('cannot delete non-empty directory: ' + nom + '\ncould not make way for new regular file: ' + nom)

                    elif os.path.isfile(os.path.join(destination, os.path.basename(nom))) and os.path.isdir(nom):

                        os.remove(os.path.join(destination, os.path.basename(nom)))
                        if verbose:
                            print('File deleted : ' + nom)
                        os.mkdir(nom)
                        if verbose:
                            print('Directory created : ' + nom)

                    else:
                        with open(os.path.join(destination, nom), 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File created : ' + nom)
                        a_time = os.path.getatime(os.path.join(destination, nom))
                        os.utime(os.path.join(destination, nom), (a_time, mod_time))

            elif type == 'dir':
                # recupere le nom du dossier
                _,nom = receive(server_read)


                if os.path.isfile(os.path.join(destination, os.path.basename(nom))) and os.path.isdir(os.path.join(source[0][0], os.path.basename(nom))):
                    os.remove(os.path.join(destination, os.path.basename(nom)))
                    if verbose:
                        print('File deleted : ' + nom)
                    os.mkdir(os.path.join(destination, nom))
                    if verbose:
                        print('Directory created : ' + nom)
                else:
                    try:
                        os.mkdir(os.path.join(destination, nom))
                        if verbose:
                            print('Directory created : ' + nom)
                    except:
                        if os.path.isfile(os.path.join(destination, nom)):
                            os.remove(os.path.join(destination, nom))
                            if verbose:
                                print('File deleted : ' + nom)
                        else:
                            try:
                                os.rmdir(os.path.join(destination, nom))
                                if verbose:
                                    print('Directory deleted : ' + nom)
                            except:
                                shutil.rmtree(os.path.join(destination, nom))
                                if verbose:
                                    print('Directory deleted : ' + nom)
                        os.mkdir(os.path.join(destination, nom))
                        if verbose:
                            print('Directory created : ' + nom)

        elif action == 'update':
            type = reponse[1]

            # type
            if type == 'file':
                # recupere le nom du fichier
                _,nom = receive(server_read)

                # recupere le contenu du fichier
                _,contenu = receive(server_read)

                # recupere la date de modification
                _,mod_time = receive(server_read)

                # cree le fichier
                if os.path.isfile(nom):
                    if os.path.isdir(destination):
                        with open(os.path.join(destination, nom), 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File updated : ' + nom)
                        a_time = os.path.getatime(os.path.join(destination, nom))
                        os.utime(os.path.join(destination, nom), (a_time, mod_time))

                    else:
                        with open(destination, 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File updated : ' + destination)
                        a_time = os.path.getatime(destination)
                        os.utime(destination, (a_time, mod_time))

                else:
                    if os.path.isfile(destination):
                        with open(destination, 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File updated : ' + destination)
                        a_time = os.path.getatime(destination)
                        os.utime(destination, (a_time, mod_time))
                    else:
                        with open(os.path.join(destination, nom), 'wb') as f:
                            f.write(contenu)
                        if verbose:
                            print('File updated : ' + nom)
                        a_time = os.path.getatime(os.path.join(destination, nom))
                        os.utime(os.path.join(destination, nom), (a_time, mod_time))

        elif action == 'delete':
            type = reponse[1]

            # type
            if type == 'file':
                # recupere le nom du fichier
                _,nom = receive(server_read)

                if not os.path.exists(destination) or not os.path.exists(os.path.join(destination, nom)):
                    pass

                # supprime le fichier
                elif os.path.isfile(nom):
                    os.remove(os.path.join(destination, nom))
                    if verbose:
                        print('File deleted : ' + os.path.join(destination, nom))

                else:
                    os.remove(os.path.join(destination, nom))
                    if verbose:
                        print('File deleted : ' + nom)

            elif type == 'dir':
                # recupere le nom du dossier
                _,nom = receive(server_read)

                if not os.path.exists(os.path.join(destination, nom)):
                    pass

                else:
                    try:
                        os.rmdir(os.path.join(destination, nom))
                        if verbose:
                            print('Directory deleted : ' + nom)
                    except:
                        if force or delete:
                            shutil.rmtree(os.path.join(destination, nom))
                            if verbose:
                                print('Directory deleted : ' + nom)

        else:
            sender.send('fini', server_write, None)
            break

    # ferme les pipes restants
    os.close(server_write)
    os.close(server_read)
    os.close(client_write)
