
import csv
from datetime import datetime


class BatchProcessor:

    def __init__(self, fichier_csv):
        self.fichier_csv = fichier_csv
        self.csv_file = None
        self.journal = None

    # Ouverture des fichiers
    def __enter__(self):
        try:
            self.csv_file = open(
                self.fichier_csv, "r",
                encoding="utf-8", newline=""
            )

            self.journal = open(
                "journal.log", "a", encoding="utf-8"
            )

            self.journaliser("Début du traitement du fichier CSV")

            print("[LOG] Fichiers ouverts")

            return self

        except OSError:
            if self.csv_file is not None:
                self.csv_file.close()

            if self.journal is not None:
                self.journal.close()

            raise

    # Journalisation
    def journaliser(self, message):
        date = datetime.now()
        self.journal.write(f"[{date}] {message}\n")
        self.journal.flush()

    # Traitement des opérations
    def traiter(self):

        lecteur = csv.reader(self.csv_file)

        try:
            for numero, ligne in enumerate(lecteur, start=1):

                if not ligne or not ligne[0].strip():
                    continue

                operation = ligne[0].strip()

                self.journaliser(
                    f"Début traitement ligne {numero} : {operation}"
                )

                try:
                    if operation == "ERREUR":
                        raise RuntimeError("Erreur de traitement simulée")

                    resultat = operation.upper()

                    print(f"Opération : {operation}")
                    print(f"Résultat : {resultat}")

                finally:
                    self.journaliser(
                        f"Fin traitement ligne {numero} : {operation}"
                    )

        except (OSError, csv.Error) as erreur:
            raise RuntimeError(
                f"Erreur de lecture CSV : {erreur}"
            ) from erreur

    # Fermeture des ressources
    def __exit__(self, exc_type, exc_value, traceback):

        try:
            if self.journal is not None:
                if exc_type:
                    self.journaliser(
                        f"Fin du traitement avec erreur : {exc_value}"
                    )
                else:
                    self.journaliser("Fin du traitement avec succès")

        finally:
            try:
                if self.csv_file is not None:
                    self.csv_file.close()
            finally:
                if self.journal is not None:
                    self.journal.close()

        print("[LOG] Fichiers fermés")

        return False


# Programme principal
if __name__ == "__main__":

    try:
        with BatchProcessor("operations.csv") as batch:
            batch.traiter()

    except (OSError, RuntimeError, csv.Error) as erreur:
        print("Erreur :", erreur)
