import pandas as pd
import CustomerBehaviourModels as CBM
import utility as utility
import warnings
warnings.filterwarnings("ignore")


I = pd.read_csv('dataDemand.dat', header=None, delimiter=' ', names=['Long', 'Lat', 'Pop'])
J = pd.read_csv('dataExisting.dat', header=None, delimiter=' ', names=['Long', 'Lat', 'Quality'])
X = pd.read_csv('dataCandidate.dat', header=None, delimiter=' ', names=['Long', 'Lat', 'Quality'])


# Example usage:
best_combinations, best_utility_percentage = utility.find_best_combinations(I, J, X, 1/3, "result.txt",5, CBM.utilityParettoHuff, 1)

CBM.utilityBinary(I, J, X, 1)
CBM.utilityHuff(I, J, X, 1)
CBM.utilityParettoHuff(I, J, X, 1)


