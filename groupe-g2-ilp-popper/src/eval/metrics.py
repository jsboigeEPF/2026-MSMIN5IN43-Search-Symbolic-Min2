def calculer_metriques(confusion):
    """
    Calcule les métriques de classification à partir d'une matrice
    de confusion.

    Paramètre :
        confusion : dictionnaire contenant tp, fp, tn et fn.

    Retour :
        Dictionnaire contenant précision, rappel, exactitude,
        F1-score, spécificité et balanced accuracy.
    """

    tp = confusion["tp"]
    fp = confusion["fp"]
    tn = confusion["tn"]
    fn = confusion["fn"]

    def diviser(numerateur, denominateur):
        """Évite une division par zéro."""
        if denominateur == 0:
            return 0.0
        return numerateur / denominateur

    precision = diviser(tp, tp + fp)
    rappel = diviser(tp, tp + fn)
    exactitude = diviser(tp + tn, tp + fp + tn + fn)
    specificite = diviser(tn, tn + fp)

    f1 = diviser(
        2 * precision * rappel,
        precision + rappel
    )

    balanced_accuracy = (rappel + specificite) / 2

    return {
        "precision": precision,
        "rappel": rappel,
        "exactitude": exactitude,
        "f1": f1,
        "specificite": specificite,
        "balanced_accuracy": balanced_accuracy,
    }
