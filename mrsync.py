import options, filelist, os, server, sender, sys, subprocess

if __name__ == '__main__':

    if "--help" in sys.argv or ("-h" in sys.argv and len(sys.argv) == 2):
        print(options.helptext)
        exit(0)

    ssh = False

    # Parsing de la ligne de commande
    args = options.parse_arguments()
    if args.list_only or args.destination == None:
        if (':' in args.source[0][0]) and not (args.server):
            index = args.source[0][0].index(":")
            args.source[0][0] = args.source[0][0][index + 1:]
            if args.source[0][0] == "":
                args.source[0][0] = "."
            os.execvp("ssh", ["ssh", "-e", "none", "-l", "distant", "localhost", "--", "python3", "./mrsync.py",
                              "--server"] + sys.argv[1:len(sys.argv) - 1] + args.source[0])
        else:
            # Récupération de la liste des fichiers de la source
            files = filelist.creer_list(args.source, args.recursive)
            if args.source[0][0] == '.' or args.source[0][0].endswith('/'):
                print('.')

            # Affichage de la liste des fichiers
            for f in files:
                print(f)

    elif len(args.source[0]) > 1 and not args.source[0][0] == '.' and not args.source[0][0] == '*':
        for src in args.source[0]:
            args_list = [f"--{attr}" for attr, arg in vars(args).items() if
                         arg and attr not in ['source', 'destination']]
            subprocess.run(["python3", "mrsync.py"] + args_list + [src, args.destination])

    else:
        if (':' in args.source[0][0] or (args.destination != None and ':' in args.destination)):
            ssh = True

        if args.server:
            with open('output.txt', 'w') as f:
                # rediriger la sortie standard vers le fichier
                sys.stdout = f
                server_read, client_write = os.pipe()
                client_read, server_write = os.pipe()
                #pull
                if ':' in args.source[0][0]:
                    #on récupère la bonne source (la partie après l'identification du serveur ssh)
                    index = args.source[0][0].index(":")
                    args.source[0][0] = args.source[0][0][index + 1:]
                    # on redirige l'entrée et sortie standart vers les tubes
                    os.dup2(0, client_read)
                    os.dup2(1, client_write)
                    sender.sender(args.source, args.destination, args.recursive, server_read, client_read, client_write, server_write)
                else:
                    index = args.destination.index(":")
                    args.destination = args.destination[index + 1:]
                    os.dup2(0, server_read)
                    os.dup2(1, server_write)
                    server.serveur(args.update, args.quiet, args.size_only, args.force, args.verbose, ssh, args.source, args.destination, args.dirs, args.recursive, args.delete, server_read, client_write, client_read, server_write)

        else:
            # Création de tubes
            server_read, client_write = os.pipe()
            client_read, server_write = os.pipe()

            # Création du processus fils
            pid1 = os.fork()

            # Si on est dans le processus fils
            if pid1 == 0:
                # push
                if ':' in args.destination:
                    if args.verbose:
                        print("SENDER")
                    sender.sender(args.source, args.destination, args.recursive, server_read, client_read, client_write, server_write)
                # pull/cas local on appelle serveur
                else:
                    server.serveur(args.update, args.quiet, args.size_only, args.force, args.verbose, ssh, args.source, args.destination, args.dirs, args.recursive, args.delete, server_read, client_write, client_read, server_write)


            # Si on est dans le processus père, sender / mrsync --server si ssh
            else:
                if ssh:
                    if args.verbose:
                        print("MODE SSH")
                    # pull
                    if (':' in args.source[0][0]):
                        #on récupère le user et le serv
                        distant, localhost = args.source[0][0].split("@")[0], args.source[0][0].split("@")[1].split(":")[0]
                        os.dup2(client_read, 0)
                        os.dup2(client_write, 1)
                    # push
                    elif ':' in args.destination:
                        distant, localhost = args.destination.split("@")[0], args.destination.split("@")[1].split(":")[0]
                        os.dup2(server_read, 0)
                        os.dup2(server_write, 1)
                    os.execvp("ssh", ["ssh", "-e", "none", "-l", distant, localhost, "--", "python3", "./mrsync.py", "--server"] + sys.argv[1:])
                else:
                    sender.sender(args.source, args.destination, args.recursive, server_read, client_read, client_write, server_write)
