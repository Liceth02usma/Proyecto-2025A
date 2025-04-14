from src.funcs.base import ABECEDARY, LOWER_ABECEDARY
from src.constants.base import VOID_STR


def fmt_biparticion(
    parte_one: list[tuple[int, ...], tuple[int, ...]],
    parte_two: list[tuple[int, ...], tuple[int, ...]],
) -> str:
    # Extraer mecanismo y purview de cada parte
    mech_p, pur_p = parte_one
    mech_d, purv_d = parte_two

    # Convertir índices a letras o símbolo vacío si no hay elementos
    purv_prim = ",".join(ABECEDARY[j] for j in pur_p) if pur_p else VOID_STR
    mech_prim = ",".join(LOWER_ABECEDARY[i] for i in mech_p) if mech_p else VOID_STR

    purv_dual = ",".join(ABECEDARY[i] for i in purv_d) if purv_d else VOID_STR
    mech_dual = ",".join(LOWER_ABECEDARY[j] for j in mech_d) if mech_d else VOID_STR

    width_prim = max(len(purv_prim), len(mech_prim)) + 2
    width_dual = max(len(purv_dual), len(mech_dual)) + 2

    return (
        [f"⎛{purv_prim:^{width_prim}}⎞⎛{purv_dual:^{width_dual}}⎞\n"
        f"⎝{mech_prim:^{width_prim}}⎠⎝{mech_dual:^{width_dual}}⎠\n",
        f"[[{purv_prim}t+1,{mech_prim}t],[[{purv_dual}t+1],[{mech_dual}t]]"]
    )


def fmt_biparte_q(
    prim: list[tuple[int, int]],
    dual: list[tuple[int, int]],
    order: bool = True,
) -> str:
    top_prim, bottom_prim = fmt_parte_q(prim, order)[0]
    top_dual, bottom_dual = fmt_parte_q(dual, order)[0]

    top_prim2, bottom_prim2 = fmt_parte_q(prim, order)[1]
    top_dual2, bottom_dual2 = fmt_parte_q(dual, order)[1]


    return [f"{top_prim}{top_dual}\n{bottom_prim}{bottom_dual}\n", f"[[{top_prim2}t+1,{bottom_prim2}t],[[{top_dual2} t+1],[{bottom_dual2} t]]"]


def fmt_parte_q(parte: list[tuple[int, int]], order: bool = True) -> tuple[str, str]:
    if order:
        parte.sort(key=lambda x: x[1])  # Ordenar por índice

    purv, mech = [], []
    for time, idx in parte:
        purv.append(ABECEDARY[idx]) if time else mech.append(LOWER_ABECEDARY[idx])

    width = max(len(purv), len(mech)) + 2
    str_purv = "".join(purv) if purv else VOID_STR
    str_mech = "".join(mech) if mech else VOID_STR

    return [[f"⎛{str_purv:^{width}}⎞", f"⎝{str_mech:^{width}}⎠"],[str_purv, str_mech]]
