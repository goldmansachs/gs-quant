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

import numpy as np
from scipy.integrate import odeint
from lmfit import minimize, Parameters, report_fit

"""
Statistical models for the transmission of infectious diseases
"""


class SIR:
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
                       R0_fixed: bool = True, R0_max: float = 1e6, I0_fixed: bool = True, I0_max: float = 1e6) \
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
        parameters.add('beta', value=beta, min=0, max=beta_max)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max)
        initial_conditions = ['S0', 'I0', 'R0']

        return parameters, initial_conditions


class SEIR:
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
        parameters.add('beta', value=beta, min=0, max=beta_max)
        parameters.add('gamma', value=gamma, min=0, max=gamma_max)
        parameters.add('sigma', value=sigma, min=0, max=sigma_max)
        initial_conditions = ['S0', 'E0', 'I0', 'R0']

        return parameters, initial_conditions


class EpidemicModel:

    """Class to perform solutions and parameter-fitting of epidemic models"""

    def __init__(self, model, parameters: tuple = None, data: np.array = None, initial_conditions: list = None,
                 fit_method: str = 'leastsq', error: callable = None):
        """
        A class to standardize fitting and solving epidemiological models.

        :param model: the model to use, currently a class in the form of SIR, SEIR above
        :param parameters: tuple, parameters to use for the model, defaults to the output of [model].get_parameters
        :param data: np.array, data that can be used to calibrate the model
        :param initial_conditions: list, initial conditions for the model
        :param fit_method: str, the method to use to minimize the (given) error. Available methods are those in the
                           lmfit.minimizer.minimize function. Default is Levenberg-Marquardt least squares minimization.
        :param error: callable, control which residuals (and in what form) to minimize for fitting.
        """
        self.model = model
        self.parameters = parameters
        self.data = data
        self.initial_conditions = initial_conditions
        self.fit_method = fit_method
        self.error = error
        self.result = None
        self.fitted_parameters = None

    def solve(self, time_range: np.ndarray, initial_conditions: list, parameters):
        """
        Integrate the model ODEs to get a solution.

        :param time_range: the time range to solve for
        :param initial_conditions: the initial conditions for the solution
        :param parameters: the parameters for the solution
        :return:
        """
        x = odeint(self.model.calibrate, initial_conditions, time_range, args=(parameters,))
        return x

    def residual(self, parameters: Parameters, time_range: np.arange, data: np.array):
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
        residual = (solution - data).ravel() if self.error is None else self.error(solution, data, parameters)
        return residual

    def fit(self, time_range: np.arange = None, parameters: [Parameters, tuple] = None, initial_conditions: list = None,
            residual=None, verbose: bool = False, data: np.array = None):
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
        if residual is None:
            residual = self.residual

        result = minimize(residual, parameters, args=(time_range, data), method=self.fit_method)
        self.result = result
        self.fitted_parameters = result.params.valuesdict()

        if verbose:
            report_fit(result)

        return result
