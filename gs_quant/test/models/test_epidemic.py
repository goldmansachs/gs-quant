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

from gs_quant.models.epidemic import *


def test_SIR():
    # Initialize a model
    beta_0 = 0.1
    gamma_0 = 0.2
    parameters, initial_conditions = SIR.get_parameters(99, 1, 0, 100,
                                                        beta=beta_0,
                                                        gamma=gamma_0,
                                                        S0_fixed=True,
                                                        I0_fixed=False,
                                                        R0_fixed=True,
                                                        S0_max=10e6,
                                                        I0_max=5e6,
                                                        R0_max=10e6)
    sir = PandemicModel(SIR, parameters=parameters, initial_conditions=initial_conditions)

    # Solve a problem with an independently checkable solution
    N = 100
    S0 = 99
    I0 = 1
    R0 = 0
    beta = 0.5
    gamma = 0.25
    days_ahead = 40  # days ahead to look at
    T = np.arange(days_ahead)
    forecast = sir.solve(T, (S0, I0, R0), (beta, gamma, N))

    # get the curve data as if it were our data
    S_data = forecast[:, 0]
    I_data = forecast[:, 1]
    R_data = forecast[:, 2]
    data = np.array([S_data, I_data, R_data]).T

    # slightly perturbed parameters, to check if the fitting finds the original (optimal) parameters
    parameters, initial_conditions = SIR.get_parameters(S_data[0], I_data[0], R_data[0], N, beta=beta + 0.4,
                                                        gamma=gamma + 0.2,
                                                        S0_fixed=True,
                                                        I0_fixed=True,
                                                        R0_fixed=True,
                                                        S0_max=10e6,
                                                        I0_max=5e6,
                                                        R0_max=10e6)
    sir = PandemicModel(SIR, parameters=parameters, data=data,
                        initial_conditions=initial_conditions)
    sir.fit()

    # check fitted parameters
    beta_fitted = sir.fitted_parameters['beta']
    gamma_fitted = sir.fitted_parameters['gamma']

    assert np.isclose(beta, beta_fitted)
    assert np.isclose(gamma, gamma_fitted)
