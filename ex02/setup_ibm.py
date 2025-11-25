import sys
from qiskit_ibm_runtime import QiskitRuntimeService


def load_api(path="api"):
    """
    Charge la clé API IBM Quantum depuis un fichier texte.
    Le fichier doit contenir uniquement la clé sur une ligne.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            cle = f.read().strip()
            if not cle:
                raise ValueError("Le fichier 'api' est vide.")
            return cle
    except FileNotFoundError:
        raise FileNotFoundError("❌ Fichier 'api' introuvable. Assure-toi qu’il existe à côté du script.")
    except Exception as e:
        raise RuntimeError(f"❌ Erreur lors du chargement de la clé API : {e}")


# ATTENTION : Remplace la ligne ci-dessous par ta VRAIE CLÉ API IBM !
try:
    CLE_API = load_api()

except Exception as e:
    print(e)
    sys.exit(1)

print("Tentative de sauvegarde du compte IBM (V_1.0+)...")
try:
    # La dernière version ne nécessite plus de forcer l'URL
    QiskitRuntimeService.save_account(
        token=CLE_API,
        overwrite=True
    )
    print("✅ Sauvegarde locale réussie ! Votre token est enregistré pour Qiskit Runtime.")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde du token local: {e}")

# # Tentative de chargement du service (test de la connexion réseau)
# print("\nTentative de connexion au serveur IBM Quantum...")
# try:
#     service = QiskitRuntimeService()
#     print(f"✅ Connexion finale à IBM Quantum réussie. Utilisateur actif: {service.active_account()}")
# except Exception as e:
#     print("="*60)
#     print(f"❌ ÉCHEC DE LA CONNEXION: {e}\n Le problème est DNS. Veuillez changer de réseau (4G/VPN).")
#     print("="*60)
