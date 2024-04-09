from itertools import product


def evaluate(expression, variables_dict):
	# Remplacer chaque symbole par l'opérateur associé
	expression = expression.replace("+", " or ")
	expression = expression.replace(".", " and ")
	expression = expression.replace("!", " not ")
	expression = expression.replace("~", " not ")

	# Remplacer chaque variable par la valeur qui lui est associée dans le dictionnaire
	for variable, value in variables_dict.items():
		expression = expression.replace(variable, str(value))

	# Évaluer l'expression
	return int(eval(expression))


def parse_expression(expression):
	# Renvoi l'ensemble des variables trouvées dans l'expression sans répétition
	return set(filter(str.isalpha, expression))


def truth_table(expression):
	# Modifier l'expression pour ignorer les minuscules et les espaces
	expression = expression.upper()
	expression = expression.replace(" ", "")

	# Liste contenant les résultats
	results = []
	variables = parse_expression(expression)
	variables_sorted = sorted(list(variables))		# Arranger l'ordre des variables
	print(" | ".join(variables_sorted + ["f = " + expression]))		# Affiche une en-tête
	print("-" * (len(expression) + 3 * (len(variables) + 2)))

	# Évaluer l'expression pour chaque combinaison de 0 et de 1 sachant que l'on a n variable dans la fonction
	for values in product([0, 1], repeat=len(variables)):
		value_dict = dict(zip(variables_sorted, values))		# Dictionnaire des {variable: valeur}
		result = evaluate(expression, value_dict)				# Résultat
		results.append(result)									# Ajouter à la liste
		value_str = " | ".join(str(v) for v in values)			# Affiche la ligne correspondante à l'opération
		print(f" | ".join([value_str, str(int(result))]))

	return results, variables									# Renvoi la liste des résultats et des variables


def disjonctive_canon(results, variables):
	variables = sorted(list(variables))						# Variables ordonnées
	products = product([0, 1], repeat=len(variables))		# Combinaison de 0 et 1 pour les n variables
	products = list(products)								# Convertir en liste (product() renvoi une union)
	tmp = str()												# Variable temporaire
	dcf = str()												# La forme canonique disjonctive

	# Pour chaque résultat
	for i in range(len(results)):
		if results[i]:					# On vérifie s'il vaut 1
			for j in range(len(variables)):		# Pour chaque variable
				tmp += str(products[i][j])		# On récupère la combinaison correspondant au résultat
				if j < len(variables) - 1:				# On sépare par des "." (on forme les mintermes)
					tmp += "."							# On aura par exemple: 0.1.1

			if i < len(results) - 1:					# On somme les mintermes
				tmp += " + "							# On aura par exemple 0.1.1 + 1.0.1 + 1.1.0

	tmp = tmp.split(" + ")								# On sépare les mintermes
	for i in range(len(tmp)):							# Pour chaque mintermes
		t = tmp[i]
		tmp2 = "("										# On ajoute une parenthese ouvrante
		tsize = len(t)
		for j in range(tsize):
			if t[j] == '1':								# Si on a '1', on remplace par sa variable correspondante
				tmp2 += variables[(j >> 1)]
			elif t[j] == '0':							# Si on a '0', on remplace par son complément
				tmp2 += variables[(j >> 1)] + "\u0304"
			else:										# Sinon c'est qu'il s'agit d'un '.'
				tmp2 += "."
		dcf += tmp2 + ")"								# On ferme la parenthèse
		if i != len(tmp) - 1:							# On somme les mintermes
			dcf += " + "

	dcf = dcf.replace("+ ()", "")						# Il se peut que la fonction split() ajoute une chaine vide et donc que dcf se termine par "+ ()". Il suffit de le retirer.
	print("\t" + dcf)


def conjonctive_canon(results, variables):
	# Presque identique à disjonctive_canon
	variables = sorted(list(variables))
	products = product([0, 1], repeat=len(variables))
	products = list(products)
	tmp = str()
	ccf = str()

	for i in range(len(results)):
		if results[i] == 0:
			for j in range(len(variables)):
				tmp += str(products[i][j])
				if j != len(variables) - 1:
					tmp += "+"

			if i < len(results) - 1:
				tmp += " . "

	tmp = tmp.split(" . ")
	for i in range(len(tmp)):
		t = tmp[i]
		tmp2 = "("
		tsize = len(t)
		for j in range(tsize):
			if t[j] == '1':
				tmp2 += variables[(j >> 1)] + "\u0304"		# Si '1', on complémente
			elif t[j] == '0':
				tmp2 += variables[(j >> 1)]					# Si '0', on laisse
			else:											# Sinon c'est un '+'
				tmp2 += " + "
		ccf += tmp2 + ")"
		if i != len(tmp) - 1:
			ccf += "."

	ccf = ccf.replace(".()", "")
	print("\t" + ccf)


def main():
	expression = input("Entrez l'expression de votre fonction (ex: A + !(B.C)): ")
	print("\nTable de vérité")
	results, variables = truth_table(expression)

	print("\nForme canonique disjonctive:")
	disjonctive_canon(results, variables)
	print("\nForme canonique conjonctive:")
	conjonctive_canon(results, variables)

if __name__ == "__main__":
	main()
