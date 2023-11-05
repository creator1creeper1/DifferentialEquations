class TermType:
    X = 0
    ApplyF = 1
    ApplyFPrime = 2
    Sum = 3
    Product = 4

class Term:
    def __init__(self, t, **kwargs):
        self.t = t
        self.__dict__.update(kwargs)

    def differentiate(self):
        if self.t == TermType.X:
            raise Exception
        if self.t == TermType.ApplyF:
            if self.inner.t == TermType.X:
                return Term(TermType.ApplyFPrime, inner=Term(TermType.X))
            else:
                return Term(TermType.Product, lhs=self.inner.differentiate(), rhs=Term(TermType.ApplyFPrime, inner=self.inner))
        if self.t == TermType.ApplyFPrime:
            raise Exception
        if self.t == TermType.Sum:
            return Term(TermType.Sum, lhs=self.lhs.differentiate(), rhs=self.rhs.differentiate())
        if self.t == TermType.Product:
            return Term(TermType.Sum,
                        lhs=Term(TermType.Product, lhs=self.lhs, rhs=self.rhs.differentiate()),
                        rhs=Term(TermType.Product, lhs=self.lhs.differentiate(), rhs=self.rhs))
        raise Exception

    def reduce(self):
        if self.t == TermType.X:
            return Term(TermType.X)
        if self.t == TermType.ApplyF:
            return Term(TermType.ApplyF, inner=self.inner.reduce())
        if self.t == TermType.ApplyFPrime:
            return Term(TermType.ApplyF, inner=Term(TermType.ApplyF, inner=self.inner.reduce()))
        if self.t == TermType.Sum:
            return Term(TermType.Sum, lhs=self.lhs.reduce(), rhs=self.rhs.reduce())
        if self.t == TermType.Product:
            return Term(TermType.Product, lhs=self.lhs.reduce(), rhs=self.rhs.reduce())
        raise Exception

    def eval_at_1(self):
        if self.t == TermType.X:
            return 1
        if self.t == TermType.ApplyF:
            return self.inner.eval_at_1()
        if self.t == TermType.ApplyFPrime:
            raise Exception
        if self.t == TermType.Sum:
            return self.lhs.eval_at_1() + self.rhs.eval_at_1()
        if self.t == TermType.Product:
            return self.lhs.eval_at_1() * self.rhs.eval_at_1()
        raise Exception

    def repr(self):
        if self.t == TermType.X:
            return "x"
        if self.t == TermType.ApplyF:
            return "f(" + self.inner.repr() + ")"
        if self.t == TermType.ApplyFPrime:
            return "f'(" + self.inner.repr() + ")"
        if self.t == TermType.Sum:
            return self.lhs.repr() + " + " + self.rhs.repr()
        if self.t == TermType.Product:
            return self.lhs.repr() + " * " + self.rhs.repr()
        raise Exception

    def repr_at_1(self):
        if self.t == TermType.X:
            return "1"
        if self.t == TermType.ApplyF:
            return "f(" + self.inner.repr_at_1() + ")"
        if self.t == TermType.ApplyFPrime:
            return "f'(" + self.inner.repr_at_1() + ")"
        if self.t == TermType.Sum:
            return self.lhs.repr_at_1() + " + " + self.rhs.repr_at_1()
        if self.t == TermType.Product:
            return self.lhs.repr_at_1() + " * " + self.rhs.repr_at_1()
        raise Exception

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def power_series_from_coefficients(coefs):
    s = ""
    first = True
    for i in range(len(coefs)):
        if first:
            first = False
        else:
            s += " + "
        s += str(coefs[i]) + "/" + str(factorial(i)) + " * (x - 1)^" + str(i)
    return s

functions = [Term(TermType.ApplyF, inner=Term(TermType.X))]
coefs = [1]
for i in range(1, 6 + 1):
    b = functions[-1].differentiate()
    c = b.reduce()
    d = c.eval_at_1()
    functions.append(c)
    coefs.append(d)
    print(f"{i}.")
    print("")
    print("Wir berechnen die " + str(i) + "-te Ableitung:")
    print("f" + "'"*i + "(x) = " + b.repr() + " = " + c.repr())
    print("")
    print("Die " + str(i) + "-te Ableitung ausgewertet bei 1 ist:")
    print("f" + "'"*i + "(1) = " + c.repr_at_1() + " = " + str(d))
    print("")
    print("Die bisher berechneten Koeffizienten lauten:")
    print(coefs)
    print("")
    print("Es ergibt sich die Potenzreihe:")
    print(power_series_from_coefficients(coefs))
    print("")
