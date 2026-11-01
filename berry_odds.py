from ast import List
from itertools import product
import random


SAMPLE_SIZE: int = 5000


NONE_MUL: float = 0.85
POS_MUL: float = 0.06
NEG_MUL: float = 0.09

# True for positive, False for negative, None for none
traitOptions: List[bool] = [True, False, None]
traitWeights: List[float] = [POS_MUL, NEG_MUL, NONE_MUL]


NO_TRAIT_COMBINATIONS: int = 1
SINGLE_TRAIT_COMBINATIONS: int = 8
DOUBLE_TRAIT_COMBINATIONS: int = 24
TRIPLE_TRAIT_COMBINATIONS: int = 32
QUAD_TRAIT_COMBINATIONS: int = 16


def getCombosOfTraitCount(count: int) -> int:
    match count:
        case 0:
            return NO_TRAIT_COMBINATIONS
        case 1:
            return SINGLE_TRAIT_COMBINATIONS
        case 2:
            return DOUBLE_TRAIT_COMBINATIONS
        case 3:
            return TRIPLE_TRAIT_COMBINATIONS
        case 4:
            return QUAD_TRAIT_COMBINATIONS
        


def getOddsOfTraitCount(count: int) -> float:
    return 1/getCombosOfTraitCount(count=count)



class TraitSet:
    
    def __init__(self, traitCombo: List[bool]):
        self.traits: List[bool] = traitCombo
    
    def getOdds(self) -> float:
        odds: float = 1

        for tempTrait in self.traits:
            if(tempTrait == None):
                odds *= NONE_MUL
            elif(tempTrait):
                odds *= POS_MUL
            else:
                odds *= NEG_MUL
        
        return odds
    
    def getTraitCount(self) -> int:
        count: int = 0

        for tempTrait in self.traits:
            if(tempTrait != None):
                count += 1
        
        return count
    
    def __str__(self) -> str:
        return f"{self.traits}"



class BerryBush:
    def __init__(self, traits: TraitSet):
        self.traitSet: TraitSet = traits

    def getOdds(self) -> float:
        odds: float = self.traitSet.getOdds()
        return odds
    
    def __str__(self) -> str:
        return f"BerryBush({self.traitSet}, rarity = 1/{round(1/self.getOdds(), ndigits=1)})\n"
    
    def __eq__(self, other) -> bool:
        if(type(other) == type(self) and self.traitSet.traits == other.traitSet.traits):
            return True
        return False
    
    
def printAllBushes(bushes: List[BerryBush]):
    for bush in bushes:
        print(bush)

def getRandomTraitSet() -> BerryBush:
    return TraitSet(random.choices(population = traitOptions, weights = traitWeights, k = 4))


def getEveryBushCombo() -> List[BerryBush]:
    bushes: List[BerryBush] = [] 

    for combination in product(traitOptions, repeat = 4):
        bushes.append(BerryBush(TraitSet(combination)))
    
    return bushes
        

def printAllComboOdds() -> None:
    totalProb: float = 0

    for bush in getEveryBushCombo():
        print(bush)
        totalProb += bush.getOdds()

    print(f"\nTotal bush combinations = {len(getEveryBushCombo())}\nProbabilities add to = {totalProb}\n")


def bruteForceOddsOfTraitCount(traitCount: int, cycles: int):
    print(f"Starting search for {traitCount}-trait bushes:")
    listOfFoundCombos: List[TraitSet] = []

    pull: int = 0
    cycle: int = 0
    combinationsToFind = getCombosOfTraitCount(traitCount)
    tempTraits: TraitSet = None

    runningMean: float = 0
    accumulatedVariance: float = 0
    tempDelta:float = 0

    while cycle <= cycles:
        tempTraits = getRandomTraitSet()
        pull += 1

        print(f"\r  - [cycle = {cycle}/{cycles}, running mean = {round(runningMean,1)}, found = {len(listOfFoundCombos)}, pull = {pull}]     ", end="", flush=True)

        if(tempTraits.getTraitCount() != traitCount):
            continue

        if(tempTraits in listOfFoundCombos):
            continue

        listOfFoundCombos.append(tempTraits)

        if(len(listOfFoundCombos) == combinationsToFind):
            listOfFoundCombos = []

            # All needed for mean and stdev calculations
            cycle += 1 # == n
            tempDelta = pull - runningMean # delta = tempCount - oldMean
            runningMean += tempDelta / cycle # updates to the new mean
            accumulatedVariance += tempDelta * (pull - runningMean) # adds any leftover delta to variance

            pull = 0

    print(f"\nOn average over {cycles} cycles, it took {round(runningMean, 1)} (stdev = {round((accumulatedVariance / (cycle - 1)) ** 0.5, 2)}) findings to discover all {combinationsToFind} {traitCount}-trait berry bushes.\n")




def main() -> int:
    bruteForceOddsOfTraitCount(0, SAMPLE_SIZE)
    bruteForceOddsOfTraitCount(1, SAMPLE_SIZE)
    bruteForceOddsOfTraitCount(2, SAMPLE_SIZE)
    bruteForceOddsOfTraitCount(3, SAMPLE_SIZE)
    bruteForceOddsOfTraitCount(4, SAMPLE_SIZE)
    return 0
   

if __name__ == "__main__":
    main()