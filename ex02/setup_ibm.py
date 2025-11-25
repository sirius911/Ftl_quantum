from qiskit_ibm_runtime import QiskitRuntimeService

# ATTENTION : Remplace la ligne ci-dessous par ta VRAIE CLÉ API IBM !
VRAIE_CLE_API = "Ma_Cle_API_IBM_Quantum_Personnelle"

print("Tentative de sauvegarde du compte IBM (V_1.0+)...")
try:
    # La dernière version ne nécessite plus de forcer l'URL
    QiskitRuntimeService.save_account(
        token=VRAIE_CLE_API,
        overwrite=True
    )
    print("✅ Sauvegarde locale réussie ! Votre token est enregistré pour Qiskit Runtime.")
except Exception as e:
    print(f"❌ Erreur lors de la sauvegarde du token local: {e}")

# Tentative de chargement du service (test de la connexion réseau)
print("\nTentative de connexion au serveur IBM Quantum...")
try:
    service = QiskitRuntimeService()
    print(f"✅ Connexion finale à IBM Quantum réussie. Utilisateur actif: {service.active_account()}")
except Exception as e:
    print("="*60)
    print(f"❌ ÉCHEC DE LA CONNEXION: {e}\n Le problème est DNS. Veuillez changer de réseau (4G/VPN).")
    print("="*60)
