import numpy as np


def calculate_offset_and_bandwidth(riv : int, N_size_BWP: int) -> tuple[int, int]:
    result, reminder = divmod(riv, N_size_BWP)
    if result <= N_size_BWP / 2 + 1 and result + reminder < N_size_BWP:
        offset = reminder
        bandwidth = result + 1
    else:
        offset = N_size_BWP - reminder - 1
        bandwidth = N_size_BWP - result + 1
    return (offset, bandwidth)

def calculate_riv(RB_start : int, L_RBs : int, N_size_BWP : int) -> int:
    if (L_RBs - 1) < np.ceil(N_size_BWP / 2):
        riv = N_size_BWP * (L_RBs - 1) + RB_start
    else:
        riv = N_size_BWP * (N_size_BWP - L_RBs + 1) + (N_size_BWP - 1 - RB_start)
    return riv
