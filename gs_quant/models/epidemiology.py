"""
Copyright 2020 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from abc import ABC, abstractmethod
from typing import Type

import numpy as np
from scipy.integrate import odeint
from lmfit import minimize, Parameters, report_fit

"""
Statistical models for the transmission of infectious diseases
"""


class CompartmentalModel(ABC):

    @classmethod
    @abstractmethod
    def calibrate(cls, xs, t, parameters) -> tuple:
        """ Should be of form callable(y, t, ...)
            See https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_parameters(cls, *args, **kwargs) -> tuple:
        raise NotImplementedError


class SIR(CompartmentalModel):
    """SIR Model"""

    @classmethod
    def calibrate(cls, xs: tuple, t: float, parameters: [Parameters, tuple]) -> tuple:
        """
        SIR model derivatives at t.

        :param xs: variables that we are solving for, i.e. [S]usceptible, [I]nfected, [R]emoved
        :param t: time parameter, inactive for this model
        :param parameters: parameters of the model (not including initial conditions), i.e. beta, gamma, N
        :return: tuple, the derivatives dSdt, dIdt, dRdt of each of the S, I, R variables
        """
        s, i, r = xs

        if isinstance(parameters, Parameters):
            beta = parameters['beta'].value
            gamma = parameters['gamma'].value
            N = parameters['N'].value
        elif isinstance(parameters, tuple):
            beta, gamma, N = parameters
        else:
            raise ValueError("Cannot recognize parameter input")

        dSdt = - beta * s * i / N
        dIdt = beta * s * i / N - gamma * i
        dRdt = gamma * i

        return dSdt, dIdt, dRdt

    @classmethod
    def get_parameters(cls, S0: float, I0: float, R0: float, N: float, beta: float = 0.2, gamma: float = 0.1,
                       beta_max: float = 10, gamma_max: float = 1, S0_fixed: bool = True, S0_max: float = 1e6,
                       beta_fixed: bool = False, gamma_fixed: bool = False, R0_fixed: bool = True, R0_max: float = 1e6,
                       I0_fixed: bool = True, I0_max: float = 1e6)\
            -> tuple:
        """
        Produce a set of parameters for the SIR model.

        :param S0: initial number of susceptible in the population
        :param I0: initial number of infected in the population, usually set to 1
        :param R0: initial number of recovered/removed in the population, usually set to 0
        :param N: size of the population
        :param beta: transmission rate parameter
        :param gamma: recovery rate parameter
        :param beta_max: maximum value to consider for beta during parameter fitting
        :param gamma_max: maximum value of gamma to consider during parameter fitting
        :param S0_fixed: whether to keep S0 fixed during fitting
        :param S0_max: maximum value of S0 to consider during parameter fitting
        :param R0_fixed: whether to keep R0 fixed during fitting
        :param R0_max: maximum value of R0 to consider during parameter fitting
        :param I0_fixed: whether to keep I0 fixed during fitting
        :param I0_max: maximum value of I0 to consider during parameter fitting
        :return: tuple[Parameters, list]: (parameters, a list of the names of the variables for initial conditions)
        """
        parameters = Parameters()
        parameters.add('N', value=N, min=0, max=N, vary=False)
        parameters.add('S0', value=S0, min=0, max=S0_max, vary=not S0_fixed)
        parameters.add('I0', value=I0, min=0, max=I0_max, vary=not I0_fixed)
        parameters.add('R0', value=R0, min=0, max=R0_max, vary=not R0_fixed)
        parameters.add('beta', value=beta, min=0, max=beta_max, vary=not beta_fixed)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max, vary=not gamma_fixed)
        initial_conditions = ['S0', 'I0', 'R0']

        return parameters, initial_conditions


class SEIR(CompartmentalModel):
    """SEIR Model"""

    @classmethod
    def calibrate(cls, xs: tuple, t: float, parameters: [Parameters, tuple]) -> tuple:
        """
        SEIR model derivatives at t.

        :param xs: variables that we are solving for, i.e. [S]usceptible, [E]xposed, [I]nfected, [R]emoved
        :param t: time parameter, inactive for this model
        :param parameters: parameters of the model (not including initial conditions), i.e. beta, gamma, sigma, N
        :return: tuple, the derivatives dSdt, dEdt, dIdt, dRdt of each of the S, E, I, R variables
        """
        s, e, i, r = xs

        if isinstance(parameters, Parameters):
            beta = parameters['beta'].value
            gamma = parameters['gamma'].value
            sigma = parameters['sigma'].value
            N = parameters['N'].value
        elif isinstance(parameters, tuple):
            beta, gamma, sigma, N = parameters
        else:
            raise ValueError("Cannot recognize parameter input")

        dSdt = -beta * s * i / N
        dEdt = beta * s * i / N - sigma * e
        dIdt = sigma * e - gamma * i
        dRdt = gamma * i

        return dSdt, dEdt, dIdt, dRdt

    @classmethod
    def get_parameters(cls, S0: float, E0: float, I0: float, R0: float, N: float, beta: float = 0.2, gamma: float = 0.1,
                       sigma: float = 0.2, beta_max: float = 10, gamma_max: float = 1, sigma_max: float = 1,
                       beta_fixed: bool = False, gamma_fixed: bool = False, sigma_fixed: bool = False,
                       S0_fixed: bool = True, S0_max: float = 1e6, R0_fixed: bool = True, R0_max: float = 1e6,
                       I0_fixed: bool = True, I0_max: float = 1e6, E0_fixed: bool = True, E0_max: float = 1e6) -> tuple:
        """
        Produce a set of parameters for the SIR model.

        :param S0: initial number of susceptible in the population
        :param E0: initial number of exposed in the population
        :param I0: initial number of infected in the population, usually set to 1
        :param R0: initial number of recovered/removed in the population, usually set to 0
        :param N: size of the population
        :param beta: transmission rate parameter
        :param gamma: recovery rate parameter
        :param sigma: parameter controlling transition from exposed to infectious
        :param beta_max: maximum value to consider for beta during parameter fitting
        :param gamma_max: maximum value of gamma to consider during parameter fitting
        :param sigma_max: maximum value of gamma to consider during parameter fitting
        :param S0_fixed: whether to keep S0 fixed during fitting
        :param S0_max: maximum value of S0 to consider during parameter fitting
        :param E0_fixed: whether to keep E0 fixed during fitting
        :param E0_max: maximum value of E0 to consider during parameter fitting
        :param R0_fixed: whether to keep R0 fixed during fitting
        :param R0_max: maximum value of R0 to consider during parameter fitting
        :param I0_fixed: whether to keep I0 fixed during fitting
        :param I0_max: maximum value of I0 to consider during parameter fitting
        :return: tuple[Parameters, list]: (parameters, a list of the names of the variables for initial conditions)
        """
        parameters = Parameters()
        parameters.add('N', value=N, min=0, max=N, vary=False)
        parameters.add('S0', value=S0, min=0, max=S0_max, vary=not S0_fixed)
        parameters.add('E0', value=E0, min=0, max=E0_max, vary=not E0_fixed)
        parameters.add('I0', value=I0, min=0, max=I0_max, vary=not I0_fixed)
        parameters.add('R0', value=R0, min=0, max=R0_max, vary=not R0_fixed)
        parameters.add('beta', value=beta, min=0, max=beta_max, vary=not beta_fixed)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max, vary=not gamma_fixed)
        parameters.add('sigma', value=sigma, min=0, max=sigma_max, vary=not sigma_fixed)
        initial_conditions = ['S0', 'E0', 'I0', 'R0']

        return parameters, initial_conditions


def switch(t: float, T: float, eta: float = 0, xi: float = 0.1, nu: float = 0) -> float:
    """
    Return a time-dependent factor that decreases exponentially, to scale parameters that are affected at some
    time point T.

    Ex. quarantine control measures were instated at some point T > t0, where t0 is the first day in available data.
    After this point, transmission rate was effectively reduced. This is modeled as a time-varying exponential decrease
    from 1 (no effect) to some fixed coefficient eta (the full effect) (ie. at time t0 it is 1 * beta, and by
    time T + nu, it is around eta * beta). If quarantine reduces transmission rate by 60%, eta would be 0.4. The
    paramater xi controls the steepness of this decrease, the nu controls the shift relative to time T at which the
    decrease peaks (ie. effects from quarantine measures at time T are visible at T+5 so nu=5). If nu=0, steepest
    point is at time T.

    To disable the 'switch', set eta = 1.0

    :param t: current time step
    :param T: some fixed time step at which the regime 'switches' - T is relative to t0, which is positioned at 0
              NOTE: this is not necessarily the steepest point of decrease. That is controlled by nu.
    :param eta: optional - the proportional reduction in transmission rate after control measures (ie. quarantine)
    :param xi: optional - the slope of the exponential decrease
    :param nu: optional - the shift of the exponential decrease
    :return:
    """
    return eta + (1 - eta) / (1 + np.exp(xi * (t - T - nu)))


class SEIRCM(CompartmentalModel):
    """ SEIR Model from https://www.medrxiv.org/content/10.1101/2020.03.04.20031104v1.full.pdf
        with cumulative cases (C) and cumulative fatalities (M) """

    @classmethod
    def calibrate(cls, xs: tuple, t: float, parameters: [Parameters, tuple]) -> tuple:
        """
        SEIRCM model derivatives at t.

        :param xs: variables that we are solving for
                   i.e. [S]usceptible, [E]xposed, [I]nfected, [R]emoved, [C]ases, [M]ortality
        :param t: time parameter
        :param parameters: parameters of the model (not including initial conditions)
                           i.e. beta, gamma, sigma, eta, epsilon
        :return: the derivatives of each of the S, E, I, R, C, M variables
        """
        s, e, i, r, c, m = xs

        if isinstance(parameters, Parameters):
            beta = parameters['beta'].value  # transmission rate
            gamma = parameters['gamma'].value  # removal rate
            sigma = parameters['sigma'].value  # infection rate
            eta = parameters['eta'].value  # control measure redux
            epsilon = parameters['sigma'].value  # case fatality rate
            T_quarantine = parameters['T'].value  # time of quarantine policy, relative to t=0 (first reported case)
        elif isinstance(parameters, tuple):
            beta, gamma, sigma, eta, epsilon, T_quarantine = parameters
        else:
            raise ValueError("Cannot recognize parameter input")

        # total population
        N = s + e + i + r

        # if T_quarantine is 0, we are not considering effect of quarantine policy so scale factor is fixed at 1
        quarantine_factor = switch(t, T_quarantine, eta=eta) if T_quarantine else 1

        dSdt = -(quarantine_factor * beta) * s * i / N  # susceptible -> exposed
        dEdt = (quarantine_factor * beta) * s * i / N - sigma * e  # exposed -> infected AND recorded cases
        dIdt = sigma * e - gamma * i  # infected -> removed (recovered AND dead)
        dRdt = (1 - epsilon) * gamma * i  # recovered (from removed)
        dCdt = sigma * e  # recorded cases (from infected)
        dMdt = epsilon * gamma * i  # dead (from removed)

        return dSdt, dEdt, dIdt, dRdt, dCdt, dMdt

    @classmethod
    def get_parameters(cls,
                       S0: float, E0: float, I0: float, R0: float, C0: float, M0: float,
                       T_quarantine: float = 0,
                       beta: float = 0.2, gamma: float = 0.1, sigma: float = 0.2,
                       eta: float = 0.6, epsilon: float = 0.02,
                       beta_max: float = 10, gamma_max: float = 1, sigma_max: float = 1,
                       eta_max: float = 1, epsilon_max: float = 1,
                       beta_fixed: bool = False, gamma_fixed: bool = False, sigma_fixed: bool = False,
                       eta_fixed: bool = False, epsilon_fixed: bool = False,
                       S0_fixed: bool = True, S0_max: float = 1e6,
                       R0_fixed: bool = True, R0_max: float = 1e6,
                       I0_fixed: bool = True, I0_max: float = 1e6,
                       E0_fixed: bool = True, E0_max: float = 1e6,
                       C0_fixed: bool = True, C0_max: float = 1e6,
                       M0_fixed: bool = True, M0_max: float = 1e6) -> tuple:
        """
        Produce a set of parameters for the SIERCM model.

        :param S0: initial number of susceptible in the population
        :param E0: initial number of exposed in the population
        :param I0: initial number of infected in the population, usually set to 1
        :param R0: initial number of recovered/removed in the population, usually set to 0
        :param C0: initial number of cumulative infected cases
        :param M0: initial number of cumulative fatalities
        :param T_quarantine: relative time at which quarantine policy goes in effect. If 0, not used.
        :param beta: transmission rate parameter
        :param gamma: recovery rate parameter
        :param sigma: parameter controlling transition from exposed to infectious
        :param eta: parameter controlling proportion by which quarantine measure reduces rate of transmission
        :param epsilon: parameter controlling rate of death
        :param beta_max: maximum value to consider for beta during parameter fitting
        :param gamma_max: maximum value of gamma to consider during parameter fitting
        :param sigma_max: maximum value to consider for sigma during parameter fitting
        :param eta_max: maximum value to consider for eta during parameter fitting
        :param epsilon_max: maximum value to consider for epsilon during parameter fitting
        :param beta_fixed: whether to keep beta fixed during fitting
        :param gamma_fixed: whether to keep gamma fixed during fitting
        :param sigma_fixed: whether to keep sigma fixed during fitting
        :param eta_fixed: whether to keep eta fixed during fitting
        :param epsilon_fixed: whether to keep epsilon fixed during fitting
        :param S0_fixed: whether to keep S0 fixed during fitting
        :param S0_max: maximum value of S0 to consider during parameter fitting
        :param E0_fixed: whether to keep E0 fixed during fitting
        :param E0_max: maximum value of E0 to consider during parameter fitting
        :param R0_fixed: whether to keep R0 fixed during fitting
        :param R0_max: maximum value of R0 to consider during parameter fitting
        :param I0_fixed: whether to keep I0 fixed during fitting
        :param I0_max: maximum value of I0 to consider during parameter fitting
        :param C0_fixed: whether to keep C0 fixed during fitting
        :param C0_max: maximum value of C0 to consider during parameter fitting
        :param M0_fixed: whether to keep M0 fixed during fitting
        :param M0_max: maximum value of M0 to consider during parameter fitting
        :return: tuple[Parameters, list]: (parameters, a list of the names of the variables for initial conditions)
        """
        parameters = Parameters()
        parameters.add('T', value=T_quarantine, min=0, max=T_quarantine, vary=False)
        parameters.add('S0', value=S0, min=0, max=S0_max, vary=not S0_fixed)
        parameters.add('E0', value=E0, min=0, max=E0_max, vary=not E0_fixed)
        parameters.add('I0', value=I0, min=0, max=I0_max, vary=not I0_fixed)
        parameters.add('R0', value=R0, min=0, max=R0_max, vary=not R0_fixed)
        parameters.add('C0', value=C0, min=0, max=C0_max, vary=not C0_fixed)
        parameters.add('M0', value=M0, min=0, max=M0_max, vary=not M0_fixed)
        parameters.add('beta', value=beta, min=0, max=beta_max, vary=not beta_fixed)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max, vary=not gamma_fixed)
        parameters.add('sigma', value=sigma, min=0, max=sigma_max, vary=not sigma_fixed)
        parameters.add('eta', value=eta, min=0, max=eta_max, vary=not eta_fixed)
        parameters.add('epsilon', value=epsilon, min=0, max=epsilon_max, vary=not epsilon_fixed)

        initial_conditions = ['S0', 'E0', 'I0', 'R0', 'C0', 'M0']

        return parameters, initial_conditions


class SEIRCMAgeStratified(CompartmentalModel):
    """ Age-structured SEIRCM Model from https://www.medrxiv.org/content/10.1101/2020.03.04.20031104v1.full.pdf """

    @classmethod
    def calibrate(cls, y: list, t: float, parameters: Parameters) -> list:
        """
        SEIR model derivatives at t.

        :param y: variables that we are solving for
                  i.e. [S]usceptible, [E]xposed, [I]nfected, [R]emoved, [C]ases, [M]ortality
        :param t: time parameter
        :param parameters: parameters of the model (not including initial conditions)
                           i.e. beta, gamma, sigma, eta, epsilon
        :return: the derivatives dydt of each of the variable in y
        """
        beta = parameters['beta'].value  # transmission rate
        gamma = parameters['gamma'].value  # removal rate
        sigma = parameters['sigma'].value  # infection rate
        eta = parameters['eta'].value  # control measure redux
        T_quarantine = parameters['T'].value  # time of quarantine policy, relative to t=0 (first reported case)
        K = parameters['K'].value  # number of age groups

        # y is of dimension (6 * K) x 1, where the first K are 'S', next K are 'E', and so on for each age group...
        assert len(y) == 6 * K, f'Error: SEIRCM states not organized into {K} age groups!'
        dydt = [0] * len(y)

        def epsilon(k):  # case fatality rate per age group
            return parameters[f'epsilon_{k}'].value

        N = sum(y[:4 * K])  # sum(S) + sum(E) + sum(I) + sum(R) where sum is over age groups
        I_total = sum(y[2 * K:3 * K])  # total number of infectious people across age groups
        s, e, i = lambda k: y[k], lambda k: y[K + k], lambda k: y[2 * K + k]

        # if T_quarantine is 0, we are not considering effect of quarantine policy so scale factor is fixed at 1
        quarantine_factor = switch(t, T_quarantine, eta=eta) if T_quarantine else 1

        for k in range(K):
            dydt[k] = -(quarantine_factor * beta) * s(k) * I_total / N  # susceptible -> exposed
            dydt[K + k] = (quarantine_factor * beta) * s(k) * I_total / N - sigma * e(k)  # exposed -> infected
            dydt[2 * K + k] = sigma * e(k) - gamma * i(k)  # infected -> removed
            dydt[3 * K + k] = (1 - epsilon(k)) * gamma * i(k)  # -> cumulative recovered (from removed)
            dydt[4 * K + k] = sigma * e(k)  # -> cumulative recorded cases (from infected)
            dydt[5 * K + k] = epsilon(k) * gamma * i(k)  # -> cumulative fatalities (from removed)

        return dydt

    @classmethod
    def get_parameters(cls,
                       S0: np.ndarray, E0: np.ndarray, I0: np.ndarray, R0: np.ndarray, C0: np.ndarray, M0: np.ndarray,
                       K: int, T_quarantine: float = 0,
                       beta: float = 0.2, gamma: float = 0.1, sigma: float = 0.2,
                       eta: float = 0.6, epsilon: np.ndarray = None,
                       beta_max: float = 10, gamma_max: float = 1, sigma_max: float = 1,
                       eta_max: float = 1, epsilon_max: float = 1,
                       beta_fixed: bool = False, gamma_fixed: bool = False, sigma_fixed: bool = False,
                       eta_fixed: bool = False, epsilon_fixed: bool = False,
                       S0_fixed: bool = True, S0_max: float = 1e6,
                       R0_fixed: bool = True, R0_max: float = 1e6,
                       I0_fixed: bool = True, I0_max: float = 1e6,
                       E0_fixed: bool = True, E0_max: float = 1e6,
                       C0_fixed: bool = True, C0_max: float = 1e6,
                       M0_fixed: bool = True, M0_max: float = 1e6) -> tuple:
        """
        Produce a set of parameters for the age-stratified SIERCM model.

        :param S0: initial number of susceptible in the population per age group
        :param E0: initial number of exposed in the population per age group
        :param I0: initial number of infected in the population per age group
        :param R0: initial number of recovered/removed in the population  per age group
        :param C0: initial number of cumulative infected cases per age group
        :param M0: initial number of cumulative fatalities per age group
        :param K: number of age groups
        :param T_quarantine: relative time at which quarantine policy goes in effect. If 0, not used.
        :param beta: transmission rate parameter
        :param gamma: removal rate parameter
        :param sigma: parameter controlling transition from exposed to infectious
        :param eta: parameter controlling proportion by which quarantine measure reduces rate of transmission
        :param epsilon: parameter controlling rate of death per age group. Recovery rate == 1 - epsilon
        :param beta_max: maximum value to consider for beta during parameter fitting
        :param gamma_max: maximum value of gamma to consider during parameter fitting
        :param sigma_max: maximum value to consider for sigma during parameter fitting
        :param eta_max: maximum value to consider for eta during parameter fitting
        :param epsilon_max: maximum value to consider for epsilon during parameter fitting
        :param beta_fixed: whether to keep beta fixed during fitting
        :param gamma_fixed: whether to keep gamma fixed during fitting
        :param sigma_fixed: whether to keep sigma fixed during fitting
        :param eta_fixed: whether to keep eta fixed during fitting
        :param epsilon_fixed: whether to keep epsilon fixed during fitting
        :param S0_fixed: whether to keep S0 fixed during fitting
        :param S0_max: maximum value of S0 to consider during parameter fitting
        :param E0_fixed: whether to keep E0 fixed during fitting
        :param E0_max: maximum value of E0 to consider during parameter fitting
        :param R0_fixed: whether to keep R0 fixed during fitting
        :param R0_max: maximum value of R0 to consider during parameter fitting
        :param I0_fixed: whether to keep I0 fixed during fitting
        :param I0_max: maximum value of I0 to consider during parameter fitting
        :param C0_fixed: whether to keep C0 fixed during fitting
        :param C0_max: maximum value of C0 to consider during parameter fitting
        :param M0_fixed: whether to keep M0 fixed during fitting
        :param M0_max: maximum value of M0 to consider during parameter fitting
        :return: tuple[Parameters, list]: (parameters, a list of the names of the variables for initial conditions)
        """
        parameters = Parameters()
        parameters.add('K', value=K, min=0, max=K, vary=False)
        parameters.add('T', value=T_quarantine, min=-1, max=T_quarantine, vary=False)
        parameters.add('beta', value=beta, min=0, max=beta_max, vary=not beta_fixed)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max, vary=not gamma_fixed)
        parameters.add('sigma', value=sigma, min=0, max=sigma_max, vary=not sigma_fixed)
        parameters.add('eta', value=eta, min=0, max=eta_max, vary=not eta_fixed)

        # add parameters that vary by age group
        for k in range(K):
            parameters.add(f'epsilon_{k}', value=epsilon[k], min=0, max=epsilon_max, vary=not epsilon_fixed)

        # add initial state conditions that vary by age group
        initial_conditions = []
        for param in ['S0', 'E0', 'I0', 'R0', 'C0', 'M0']:
            for k in range(K):
                parameters.add(f'{param}_{k}', value=eval(param)[k], min=0, max=eval(f'{param}_max'),
                               vary=not eval(f'{param}_fixed'))
                initial_conditions.append(f'{param}_{k}')

        return parameters, initial_conditions


class EpidemicModel:

    """Class to perform solutions and parameter-fitting of epidemic models"""

    def __init__(self, model: Type[CompartmentalModel], parameters: tuple = None, data: np.array = None,
                 initial_conditions: list = None, fit_method: str = 'leastsq', error: callable = None,
                 fit_period: float = None):
        """
        A class to standardize fitting and solving epidemiological models.

        :param model: the model to use, currently a class in the form of SIR, SEIR above
        :param parameters: tuple, parameters to use for the model, defaults to the output of [model].get_parameters
        :param data: np.array, data that can be used to calibrate the model
        :param initial_conditions: list, initial conditions for the model
        :param fit_method: str, the method to use to minimize the (given) error. Available methods are those in the
                           lmfit.minimizer.minimize function. Default is Levenberg-Marquardt least squares minimization.
        :param error: callable, control which residuals (and in what form) to minimize for fitting.
        :param fit_period: float, how far back to fit the data, defaults to fitting all data
        """
        self.model = model
        self.parameters = parameters
        self.data = data
        self.initial_conditions = initial_conditions
        self.fit_method = fit_method
        self.error = error
        self.fit_period = fit_period
        self.result = None
        self.fitted_parameters = None

    def solve(self, time_range: np.ndarray, initial_conditions: [list, tuple], parameters) -> np.ndarray:
        """
        Integrate the model ODEs to get a solution.

        :param time_range: the time range to solve for
        :param initial_conditions: the initial conditions for the solution
        :param parameters: the parameters for the solution
        :return:
        """
        x = odeint(self.model.calibrate, initial_conditions, time_range, args=(parameters,))
        x = np.array(x)
        return x

    def residual(self, parameters: Parameters, time_range: np.arange, data: np.ndarray) -> np.ndarray:
        """
        Obtain fit error (to minimize).

        :param parameters: parameters to use (which we are usually minimizing the residual for)
        :param time_range: time range for solution (over which we obtain the residual)
        :param data: data to fit the models too (i.e. compute residuals in terms of)
        :return:
        """
        initial_conditions = []
        for variable in self.initial_conditions:
            initial_conditions.append(parameters[variable].value)

        # obtain solution given current initial conditions and parameters
        solution = self.solve(time_range, initial_conditions, parameters)

        # compute residual, using custom error function if it has been passed in
        residual = solution - data if self.error is None else self.error(solution, data, parameters)

        if self.fit_period is not None:
            residual = residual[-self.fit_period:]

        return residual.ravel()

    def fit(self, time_range: np.arange = None, parameters: [Parameters, tuple] = None, initial_conditions: list = None,
            residual=None, verbose: bool = False, data: np.array = None, fit_period: float = None):
        """
        Fit the model based on data in the form np.array([X1,...,Xn])
        """
        if data is None:
            if self.data is None:
                raise ValueError("No data to fit the model on!")
            data = self.data
        if initial_conditions is not None:
            self.initial_conditions = initial_conditions
        if self.initial_conditions is None:
            raise ValueError("No initial conditions to fit the model with!")
        if parameters is None:
            if self.parameters is None:
                raise ValueError("No parameters to fit the model with!")
            parameters = self.parameters
        if time_range is None:
            time_range = np.arange(data.shape[0])
        if fit_period is not None:
            self.fit_period = fit_period
        if residual is None:
            residual = self.residual

        result = minimize(residual, parameters, args=(time_range, data), method=self.fit_method)
        self.result = result
        self.fitted_parameters = result.params.valuesdict()

        if verbose:
            report_fit(result)

        return result
