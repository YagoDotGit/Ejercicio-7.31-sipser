
class Clausula:
	def __init__(self, x: str, y: str, z: str):
		self.x = Clausula.format(x)
		self.y = Clausula.format(y)
		self.z = Clausula.format(z)

		self._x = x
		self._y = y
		self._z = z

	def format(x: str) -> str:
		if x.startswith("!"):
			return "(1-" + x.strip("!") + ")"
		return x

	def get_or(self) -> str:
		return "(" + self.x + "+" + self.y + "+" + self.z + "-" + self.x + "*" + self.y + "-" + self.y + "*" + self.z + "-" + self.x + "*" + self.z + "+" + self.x + "*" + self.y + "*" + self.z + ")"

class Sat3():
	def __init__(self, lista_clausulas: list, vars: str):
		self.clausulas = lista_clausulas
		self.vars = vars.split(",")

		self.equivalent_polynomial = self._calculate_equivalent_polynomial()

	def _clausulas_2_diophantine_expression(self) -> str:
		builder = ""
		for i in range(len(self.clausulas) - 1):
			builder += self.clausulas[i].get_or() + "*"
		
		builder += self.clausulas[len(self.clausulas) - 1].get_or()

		return builder

	def _calculate_equivalent_polynomial(self) -> str:
		q = self._clausulas_2_diophantine_expression()
		diophantine_pol = "(" + q + " - 1)**2"
		for var in self.vars:
			diophantine_pol += f" + ({var}*(1-{var}))**2"
		return diophantine_pol

	def get_equivalent_polynomial(self) -> str:
		return self.equivalent_polynomial

	def _get_polynomial_roots(self) -> list:
		valores_de_verdad = 2**len(self.vars)
	
		asignacion = {}
		roots = []
	
		for i in range(valores_de_verdad):
			asignacion_valores = format(i, '0'+str(len(self.vars))+'b')
			# print(f"Asignacion valores: {asignacion_valores}")
			for j in range(len(self.vars)):
				asignacion[self.vars[j]] = asignacion_valores[j]
			# print(asignacion)
	
			eq_sust = self.equivalent_polynomial
			for var in self.vars:
				eq_sust = eq_sust.replace(var, asignacion[var])
	
			# print(f"EVAL: {eq_sust}")
	
			if eval(eq_sust) == 0:
				roots.append(asignacion.copy())
	
		return roots

	def print_roots(self, roots: list):
		head = "  " + self.vars[0]
		sep = " --"
		for i in range(1, len(self.vars)):
			head += " | " + self.vars[i]
			sep += "----"
		print(head)
		print(sep + "-")
	
		for s in roots:
			assig = "  "
			for key in s:
				assig += s[key] + "   "
			print(assig)

	def get_polinomial_roots(self, show_results: bool = False) -> list:
		roots = self._get_polynomial_roots()
		if show_results:
			self.print_roots(roots)
		
	def to_string(self):
		l = self.clausulas
		if len(l) == 1:
			return "(" + l[0]._x + " V " + l[0]._y + " V " + l[0]._z + ")"
		res = ""
		for i in range(len(l) - 1):
			res += "(" + l[i]._x + " V " + l[i]._y + " V " + l[i]._z + ") Λ "
		i += 1
		res += "(" + l[i]._x + " V " + l[i]._y + " V " + l[i]._z + ")"
		return res


clausulas = [Clausula("x", "y", "z"), Clausula("x", "!y", "!z")]
vars = "x,y,z"
formula = Sat3(clausulas, vars)

print("\nFormula 3Sat: " + formula.to_string())
print(f"\nPolinomio equivalente:\np({vars}) = {formula.get_equivalent_polynomial()}")
print("\nRaices del polinomio:")
formula.get_polinomial_roots(show_results=True)