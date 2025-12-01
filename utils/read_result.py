import sys
from qiskit_ibm_runtime import QiskitRuntimeService
from results_utils import afficher_resultats


def main(job_id: str):
    print(f"Récupération du job {job_id} ...")

    service = QiskitRuntimeService()
    try:
        job = service.job(job_id)

        print(f"Statut actuel : {job.status()}")

        print("\n--- ATTENTE DES RÉSULTATS ---")
        result = job.result()

        # result est un PrimitiveResult → on prend le premier SamplerPubResult
        pub_result = result[0]

        bitarray = pub_result.data.c

        # Récupération des comptages type {'0': 523, '1': 501}
        counts = bitarray.get_counts()

        print("\nCounts bruts :")
        print(counts)

        backend_name = job.backend().name

        afficher_resultats(
            counts,
            backend_name=backend_name,
            titre=f"Résultats EX02 (lecture différée) — {backend_name}",
            afficher_graphique=True,
        )
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération du job ou des résultats : {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python read_result.py <JOB_ID>")
        sys.exit(1)

    main(sys.argv[1])
