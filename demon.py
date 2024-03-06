import socket
import sys
import signal
import os
import time
import logging
import daemon

###A FINIR

DEFAULT_PORT = 10873
PID_FILE = "/var/run/mrsync.pid" 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def handle_signal(signum, ignore):
    # On ferme la socket de service
    logger.info("Arrêt du démon")
    if server_socket:
        server_socket.close()
    # On ferme toutes les connexions en cours
    for conn in connections:
        conn.close()
    # On supprime le fichier PID
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    sys.exit(0)

# Fonction qui initialise la socket et se met en attente de demandes de connexion
def init_socket(port):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    while True:
        conn, addr = server_socket.accept()
        connections.append(conn)
        data = conn.recv(1024)
        # synchronisation

        conn.close()
        connections.remove(conn)

def run(port, detach):
    if os.path.exists(PID_FILE):
        raise Exception("Le démon est déjà en cours d'exécution.")
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    log_file = open('/var/log/mrsync.log', 'a')
    err_file = open('/var/log/mrsync.err', 'a')
    with daemon.DaemonContext(stdout=log_file, stderr=err_file):
        # Initialise la liste des connexions en cours
        global connections
        connections = []
        # Initialise la socket
        init_socket(port)
        # Intercepte le signal SIGTERM
        signal.signal(signal.SIGTERM, handle_signal)
