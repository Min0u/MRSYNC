import os, pickle, receiver, generator, filelist

# Fils (serveur, FILS DU 1ER FORK) : sender
def serveur(update, quiet, size_only, force, verbose, ssh, source, destination, dirs, recursive, delete, server_read, client_write, client_read, server_write):
    # Attend de recevoir la liste du client
    _,files = receiver.receive(server_read)


    # Serveur = Père : reciever, Fils : generator
    pid2 = os.fork()

    # Si on est dans le processus fils, generator
    if pid2 == 0:
        generator.generator(update, size_only, ssh, source, files, destination, dirs, recursive, delete, server_read, client_write, client_read, server_write)
    # Si on est dans le processus père, receiver
    else:
        receiver.receiver(delete, quiet, force, verbose, source, destination, server_read, client_write, client_read, server_write)
