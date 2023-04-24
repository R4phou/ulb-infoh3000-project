POPULATION = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
SCORES = [["a", "b"], ["c", "d"], ["e", "f"]]
# # print(zip(POPULATION, SCORES))


def from_list_to_dict(liste1, liste2):
    dico = []
    for i in range(len(liste1)):
        dico.append((liste1[i], liste2[i]))
    return dico


DICO_POPU_SCORE = from_list_to_dict(POPULATION, SCORES)

print(DICO_POPU_SCORE)
# dico = {[1, 2, 3]: ["a", "b"], [4, 5, 6]: ["c", "d"], [7, 8, 9]: ["e", "f"]}
# print(dico)
