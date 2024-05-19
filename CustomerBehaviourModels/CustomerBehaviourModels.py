import pandas as pd
pd.options.mode.chained_assignment = None
from utility import distance

# ==============================================================================
# Utility of the new locations given by X
# ==============================================================================
def utilityBinary(I, J, X, mode):
    AttrJ = []          # attractiveness of all preexisting facilities
    AttrX = []          # attractiveness of all new facilities
    utility = 0         # utility of the new facilties
    totalDemand = 0     # total demand of the whole population
    I["Dem_Preexisting"] = 0
    I["Dem_New"] = 0

    for i in range(len(I)):

        # Calculate AttrJ
        AttrJ.clear()
        for j in range(0, len(J)):
            AttrJ.append(J.iloc[j]['Quality'] / (distance(I.iloc[i], J.iloc[j])+1))


        # Calculate AttrX
        AttrX.clear()
        for j in range(0, len(X)):
            AttrX.append(X.iloc[j]['Quality'] / (distance(I.iloc[i], X.iloc[j])+1))

        # If the best of AttrX is better than the best of AttrJ
        if max(AttrX) > max(AttrJ):
            utility += I.iloc[i, 2]
            I["Dem_New"][i] = I.iloc[i, 2]
            I["Dem_Preexisting"][i] = 0

        elif max(AttrX) < max(AttrJ):
            I["Dem_Preexisting"][i] = I.iloc[i, 2]
            I["Dem_New"][i] = 0

        # If the best of Attr is equal to the best of AttrJ
        elif max(AttrX) == max(AttrJ):
            utility += I.iloc[i, 2] * 1/3
            I["Dem_New"][i] = I.iloc[i, 2] * 1/3
            I["Dem_Preexisting"][i] = I.iloc[i, 2] - (I.iloc[i, 2] * 1/3)

    if mode == 0:
        print(I.to_string())

    elif mode == 1:
        return utility


# ==============================================================================
# Utility of the new locations given by X
# ==============================================================================
def utilityHuff(I, J, X, mode):

    totalQualityJ = 0               # total quality of preexisting facilities
    totalQualityX = 0               # total quality of new facilities
    X["New_Demand"] = float(0)      # New demand of preexisting facilities
    J["New_Demand"] = float(0)      # New demand of new facilities
    utility = 0         # utility of the new facilties

    # calculate sum of quality of all preexisting facilities
    for i in range(0, len(J)):
        totalQualityJ += J.iloc[i, 2]

    # calculate sum of quality of all new facilities
    for i in range(0, len(X)):
        totalQualityX += X.iloc[i, 2]

    for i in range(len(I)):

        # Calculate new demand for each new facility depending on attraction proportion
        for j in range(len(J)):
            attractiveness_value = J.iloc[j, 2] / (totalQualityJ + totalQualityX)
            J["New_Demand"][j] += attractiveness_value * I.iloc[i, 2]

        # Calculate new demand for each preexisting facility depending on attraction proportion
        for j in range(len(X)):
            attractiveness_value = X.iloc[j, 2] / (totalQualityJ + totalQualityX)
            X["New_Demand"][j] += attractiveness_value * I.iloc[i, 2]
            utility = utility + attractiveness_value * I.iloc[i, 2]

    if mode == 0:
        print(X)
        print()
        print(J)

    elif mode == 1:
        return utility


# ==============================================================================
# Utility of the new locations given by X
# ==============================================================================
def utilityParettoHuff(I, J, X, mode):
    totalAttrX = 0               # total attractiveness of new facilities
    totalAttrJ = 0               # total attractiveness of preexisting facilities

    J["Distance"] = float(0)    # New demand of new facilities
    X["Distance"] = float(0)    # New demand of new facilities
    X["New_Demand"] = float(0)  # New demand of preexisting facilities
    J["New_Demand"] = float(0)  # New demand of new facilities
    utility = 0

    for i in range(len(I)):

        for j in range(0, len(J)):
            J["Distance"][j] = distance(J.iloc[j], I.iloc[i])

        for j in range(0, len(X)):
            X["Distance"][j] = distance(X.iloc[j], I.iloc[i])

        a = len(J)
        j = 0
        while j < a:
            dom = 0
            for z in range(0, len(J)):
                if j != z:
                    if ((J.iloc[z, 3] <= J.iloc[j, 3] and J.iloc[z, 2] >= J.iloc[j, 2])
                            and (J.iloc[z, 3] < J.iloc[j, 3] or J.iloc[z, 2] > J.iloc[j, 2])):
                        dom = 1
                        break
            for z in range(0, len(X)):
                if ((X.iloc[z, 3] <= J.iloc[j, 3] and X.iloc[z, 2] >= J.iloc[j, 2])
                        and (X.iloc[z, 3] < J.iloc[j, 3] or X.iloc[z, 2] > J.iloc[j, 2])):
                    dom = 1
                    break
            if dom == 1:
                J.drop(J.index[j], inplace=True)
                a -= 1
            else:
                j += 1

        a = len(X)
        j = 0
        while j < a:
            dom = 0
            for z in range(0, len(J)):
                if ((J.iloc[z, 3] <= X.iloc[j, 3] and J.iloc[z, 2] >= X.iloc[j, 2])
                        and (J.iloc[z, 3] < X.iloc[j, 3] or J.iloc[z, 2] > X.iloc[j, 2])):
                    dom = 1
                    break

            for z in range(0, len(X)):
                if j != z:
                    if ((X.iloc[z, 3] <= X.iloc[j, 3] and X.iloc[z, 2] >= X.iloc[j, 2])
                            and (X.iloc[z, 3] < X.iloc[j, 3] or X.iloc[z, 2] > X.iloc[j, 2])):
                        dom = 1
                        break
            if dom == 1:
                X.drop(X.index[j], inplace=True)
                a -= 1
            else:
                j += 1

        totalAttrX = 0
        for z in range(0, len(X)):
            totalAttrX += (X.iloc[z, 2])

        totalAttrJ = 0
        for z in range(0, len(J)):
            totalAttrJ += (J.iloc[z, 2])


        # Calculate new demand for each preexisting facility depending on attraction proportion
        for z in range(len(X)):
            X["New_Demand"].iloc[z] += I.iloc[i, 2] * (X.iloc[z, 2] / (totalAttrX + totalAttrJ))
            utility = utility + I.iloc[i, 2] * (totalAttrX / (totalAttrX + totalAttrJ))

        # Calculate new demand for each new facility depending on attraction proportion
        for z in range(len(J)):
            J["New_Demand"].iloc[z] += I.iloc[i, 2] * (J.iloc[z, 2] / (totalAttrX + totalAttrJ))

    if mode == 0:
        print(X)
        print()
        print(J)

    elif mode == 1:
        return utility

