from statsmodels.stats.multitest import multipletests


def correct_pvalues(p_values, method="none", alpha=0.05):
    """
    Parameters
    ----------
    p_values : array-like
        List of raw p-values.

    method : str
        'none'
        'bonferroni'
        'bh'

    alpha : float
        Significance level.

    Returns
    -------
    corrected_pvalues : list
        Corrected p-values.
    """

    method = method.lower()

    if method == "none":
        return list(p_values)

    elif method == "bonferroni":
        _, corrected, _, _ = multipletests(
            p_values,
            alpha=alpha,
            method="bonferroni",
        )
        return corrected

    elif method == "bh":
        _, corrected, _, _ = multipletests(
            p_values,
            alpha=alpha,
            method="fdr_bh",
        )
        return corrected

    else:
        raise ValueError(
            f"Unknown multiple-comparison correction method: '{method}'"
        )