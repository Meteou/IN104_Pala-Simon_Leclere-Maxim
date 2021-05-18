class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """
        # détermination des paramètres d'intégration nombre de pas 👎 et
        # intervalle entre deux pas (h)
        h = self.max_step_size
        n=(t-self.t0)/h
        # initialisation du vecteur de retour
        y =self.y0
        # calcul du vecteur de retour
        for i in range(n):
            y=y + self.f(y)*h
        return y
        




class DummySolver(ISolver):
    pass