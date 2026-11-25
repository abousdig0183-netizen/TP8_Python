
from pathlib import Path
from contextlib import contextmanager, ExitStack


# PARTIE 1 : Gestion manuelle
class TempFileWriter:

    def __enter__(self):
        self.filepath = Path("temp.txt")
        self.f = self.filepath.open("w", encoding="utf-8")
        print("[LOG] Fichier ouvert")
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        print("[LOG] Fichier fermé")

        if self.filepath.exists():
            self.filepath.unlink()
            print("[LOG] Fichier supprimé")

        if exc_type is not None:
            print("[ERREUR]", exc_val)

        return False


# PARTIE 2 : contextmanager
@contextmanager
def temp_file():

    path = Path("temp.txt")
    f = path.open("w", encoding="utf-8")

    print("[LOG] Fichier ouvert avec contextmanager")

    try:
        yield f
    finally:
        f.close()
        print("[LOG] Fichier fermé")

        if path.exists():
            path.unlink()
            print("[LOG] Fichier supprimé")


# PARTIE 3 : ExitStack
def gerer_fichiers():

    paths = ["a.txt", "b.txt", "c.txt"]

    with ExitStack() as stack:

        files = [
            stack.enter_context(open(p, "w", encoding="utf-8"))
            for p in paths
        ]

        for f in files:
            f.write("Test de gestion des ressources\n")

    print("[LOG] Tous les fichiers sont fermés")


# MAIN
if __name__ == "__main__":

    print("===== PARTIE 1 =====")

    with TempFileWriter() as f:
        f.write("Contenu temporaire\n")

    print("\n===== PARTIE 2 =====")

    with temp_file() as f:
        f.write("Autre test\n")

    print("\n===== PARTIE 3 =====")

    gerer_fichiers()
