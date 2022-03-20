def GetDTM(T1, T2, t1, t2, shell_passes):
    import math

    DTLM = ((T1 - t2) - (T2 - t1)) / math.log((T1 - t2) / (T2 - t1))

    R = (T1 - T2) / (t2 - t1)
    S = (t2 - t1) / (T1 - t1)

    if shell_passes == 1:
        # 1 shell pass and two or more even tube passes
        numerator = math.sqrt((R ** 2) + 1) * math.log((1 - S) / (1 - R * S))
        denom_1 = 2 - S * (R + 1 - math.sqrt((R ** 2) + 1))
        denom_2 = 2 - S * (R + 1 + math.sqrt((R ** 2) + 1))
        Ft = numerator / ((R - 1) * math.log(denom_1 / denom_2))

    else:
        # Equation: https://imgur.com/a/Q60laqU
        # 2 shell passes and four or multiples of 4 tube passes
        numerator = math.sqrt((R ** 2) + 1) * math.log((1 - S) / (1 - S * R))
        denom_1 = (2 / S) - 1 - R + (2 / S) * math.sqrt((1 - S) * (1 - R * S)) + math.sqrt((R ** 2) + 1)
        denom_2 = (2 / S) - 1 - R + (2 / S) * math.sqrt((1 - S) * (1 - R * S)) - math.sqrt((R ** 2) + 1)
        Ft = numerator / (2 * (R - 1) * math.log(denom_1 / denom_2))

    return [DTLM, Ft, DTLM * Ft]



