"""
	Ce code est basé sur la méthode de Quine-McCluskey (aussi appelée "Méthode Tabulaire") qui est elle même basée sur la méthode du
tableau de Karnaugh mais est cependant une version plus simple à implémentée que la méthode originale surtout pour un nombre élevée de 
variables (au delà de 4 variables, la méthode classique de Karnaugh est difficile à mettre en oeuvre).
 	Cette méthode vient des recherches de Willard V. Quine sur la simplification des fonctions logiques via le tableau de Karnaugh. Il 
réussira à traduire cette méthode (celle de Karnaugh) dans un algorithme qu'il est possible d'implémenter sur ordinateur et plus tard la 
méthode sera étendue par Edward J. McCluskey.
	En bref, cette méthode est en fait une variation algorithmique du tableau de Karnaugh.
"""

# Retourne la liste des variables
def get_variables(expression):
	return sorted(set(filter(str.isalpha, expression)))

# Evalue la fonction pour des valeurs données
def evaluate(expression, var_dict):
	expression = expression.replace("+", " or ")
	expression = expression.replace(".", " and ")
	expression = expression.replace("!", " not ")
	expression = expression.replace("~", " not")
	for var, val in var_dict.items():
		expression = expression.replace(var, val)
	return eval(expression)

# Récupère les mintermes sous la forme d'une liste. Ex: A + B => [1, 2, 3]
def get_minterms(expression):
	minterms = []
	variables = get_variables(expression)
	var_count = len(variables)
	tab = []
	for i in range(2 ** var_count):
		b = bin(i)[2:].zfill(var_count)
		tab.append(list(b))

	for c in tab:
		var_dict = dict(zip(variables, c))
		result = evaluate(expression, var_dict)
		if result == 1:
			minterms.append(c)
	return minterms

# Renvoi la liste des implicants premiers
def get_prime_implicants(minterms):
	prime_implicants = []
	used = [0 for i in range(len(minterms))]
	for i in range(len(minterms)):
		for j in range(len(minterms)):
			if minterms[i] != minterms[j]:
				idxs = [k for k in range(len(minterms[i])) if (minterms[i][k] != minterms[j][k])]
				if len(idxs) == 1:
					tmp = minterms[i].copy()
					tmp[idxs[0]] = "*"
					used[i] = 1
					if tmp not in prime_implicants:
						prime_implicants.append(tmp)

	if used.count(0) == len(used):
		return []

	for u in range(len(used)):
		if used[u] == 0:
			prime_implicants.append(minterms[u])

	return prime_implicants

# Renvoie la liste des valeurs couvertes par un implicant premier appelé "subsets"
def get_subset(implicant):
	subset = []
	star_count = implicant.count("*")
	tab = []
	for i in range(2 ** star_count):
		b = list(bin(i)[2:].zfill(star_count))
		tab.append(b)

	for t in tab:
		star_counter = 0
		tmp = implicant.copy()
		for i in range(len(tmp)):
			if implicant[i] == "*":
				tmp[i] = t[star_counter]
				star_counter += 1
		subset.append(tmp)
	return subset

# Renvoie la liste des valeurs couvertes par une liste d'implicants premiers
def get_all_subsets(implicants):
	all_minterms = []
	for implicant in implicants:
		all_minterms.append(get_subset(implicant))

	return all_minterms

# Renvoie les minterms d'une liste de subsets
def get_all_minterms(subsets):
	all_minterms = []
	for subset in subsets:
		for s in subset:
			if s not in all_minterms:
				all_minterms.append(s)
	all_minterms = sorted(all_minterms)
	return all_minterms

# Minimise la fonction passée en paramètre
def minimize(expression):
	minterms = get_minterms(expression)
	variables = get_variables(expression)
	prime_implicants = get_prime_implicants(minterms)
	while len(prime_implicants) != 0:
		minterms.clear()
		minterms.extend(prime_implicants)
		prime_implicants = get_prime_implicants(prime_implicants)
	subsets = get_all_subsets(minterms)
	all_minterms = get_all_minterms(subsets)

	redundant_indexes = []
	for i in range(len(subsets)):
		tmp_subsets = []
		for j in range(len(subsets)):
			if (i != j) and (j not in redundant_indexes):
				tmp_subsets.append(subsets[j])
		if get_all_minterms(tmp_subsets) == all_minterms:
			redundant_indexes.append(i)

	for idx in reversed(range(len(redundant_indexes))):
		del minterms[redundant_indexes[idx]]

	output = str()
	for i in range(len(minterms)):
		for j in range(len(minterms[i])):
			if minterms[i][j] == "1":
				output += variables[j]
			elif minterms[i][j] == "0":
				output += "!" + variables[j]
			else:
				continue
			output += "."
		if output[-1] == ".":
			output = output[:-1]
		if i < len(minterms) - 1:
			output += " + "

	return output


def main():
	expression = input("Entrez l'expression à simplifier: ")
	print("Résultat:")
	output = minimize(expression)
	print("\t", output)


if __name__ == "__main__":
	main()
