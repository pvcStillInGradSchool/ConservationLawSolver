import abc

import numpy as np

import equation


class RiemannSolver(abc.ABC):

  def set_initial(self, U_L, U_R):
    self._U_L = U_L
    self._U_R = U_R
    self._solve()
  
  @abc.abstractmethod
  def _solve(self):
    # Determine boundaries of constant regions and elementary waves,
    # as well as the constant states.
    pass

  @abc.abstractmethod
  def U(self, x, t):
    pass

  def F(self, U):
    return self._equation.F(U)

  def F_on_t_axis(self, U_L, U_R):
    # F is always unique on t-axis
    self.set_initial(U_L=U_L, U_R=U_R)
    U_on_t_axis = self.U(x=0, t=1)
    return self._equation.F(U_on_t_axis)


class LinearAdvection(RiemannSolver):

  def __init__(self, a_const):
    self._equation = equation.LinearAdvection(a_const)

  def U(self, x, t):
    U = 0.0
    if x < t * self._equation.A(U):
      U = self._U_L
    else:
      U = self._U_R
    return U


class InviscidBurgers(RiemannSolver):

  def __init__(self):
    self._equation = equation.InviscidBurgers()

  def U(self, x, t):
    if self._U_L < self._U_R:
      return self._rarefaction(x, t)
    else:
      return self._shock(x, t)

  def _rarefaction(self, x, t):
    U = 0.0
    if t == 0.0:
      if x < 0:
        U = self._U_L
      else:
        U = self._U_R
    else:
      slope = x / t
      if  slope < self._U_L:
        U = self._U_L
      elif slope > self._U_R:
        U = self._U_R
      else:
        U = slope
    return U

  def _shock(self, x, t):
    U = (self._U_L + self._U_R) / 2
    if x < t * U:
      U = self._U_L
    else:
      U = self._U_R
    return U


if __name__ == '__main__':
  pass
