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

//Portions copyright Maximilian Boeck. Licensed under Apache 2.0 license
"""

from gs_quant.models.epidemiology import *

def test_SI():
    for incidence in ['mass_action', 'standard']:
        # Initialize a model
        beta_0 = 0.1
        parameters, initial_conditions = SI.get_parameters(99, 1, 100,
                                                           beta=beta_0,
                                                           beta_max=10,
                                                           S0_fixed=True,
                                                           I0_fixed=False,
                                                           S0_max=10e6,
                                                           I0_max=5e6)
        si = EpidemicModel(SI, parameters=parameters, initial_conditions=initial_conditions, incidence_type=incidence)

        # Solve a problem with an independently checkable solution
        N = 100
        S0 = 99
        I0 = 1
        beta = 0.5
        days_ahead = 40  # days ahead to look at
        T = np.arange(days_ahead)
        forecast = si.solve(T, (S0, I0), (beta, N))

        # Get the curve data as if it were our data
        S_data = forecast[:, 0]
        I_data = forecast[:, 1]
        data = np.array([S_data, I_data]).T

        # Slightly perturbed parameters, to check if the fitting finds the original (optimal) parameters
        beta_perturbed = beta + 0.4
        parameters, initial_conditions = SI.get_parameters(S_data[0], I_data[0], N, beta=beta_perturbed,
                                                           beta_max=10,
                                                           S0_fixed=True,
                                                           I0_fixed=True,
                                                           S0_max=10e6,
                                                           I0_max=5e6)
        si = EpidemicModel(SI, parameters=parameters, data=data,
                           initial_conditions=initial_conditions, incidence_type=incidence)
        si.fit()

        # Check fitted parameters
        beta_fitted = si.fitted_parameters['beta']

        assert np.isclose(beta, beta_fitted, rtol=5e-1)

        si = EpidemicModel(SI, parameters=parameters, data=data, initial_conditions=initial_conditions, fit_period=10, incidence_type=incidence)
        si.fit()

        # Check fitted parameters again
        beta_fitted = si.fitted_parameters['beta']

        assert np.isclose(beta, beta_fitted,rtol=5e-1)

def test_SIS():
    for incidence in ['mass_action', 'standard']:
        # Initialize a model
        beta_0 = 0.1
        delta_0 = 0.1
        parameters, initial_conditions = SIS.get_parameters(99, 1, 100,
                                                           beta=beta_0,
                                                           beta_max=10,
                                                           delta=delta_0,
                                                           delta_max=10,
                                                           S0_fixed=True,
                                                           I0_fixed=False,
                                                           S0_max=10e6,
                                                           I0_max=5e6)
        sis = EpidemicModel(SIS, parameters=parameters, initial_conditions=initial_conditions, incidence_type=incidence)

        # Solve a problem with an independently checkable solution
        N = 100
        S0 = 99
        I0 = 1
        beta = 0.5
        delta = 0.4
        days_ahead = 40  # days ahead to look at
        T = np.arange(days_ahead)
        forecast = sis.solve(T, (S0, I0), (beta,delta, N))

        # Get the curve data as if it were our data
        S_data = forecast[:, 0]
        I_data = forecast[:, 1]
        data = np.array([S_data, I_data]).T

        # Slightly perturbed parameters, to check if the fitting finds the original (optimal) parameters
        beta_perturbed = beta + 0.4
        delta_perturbed = delta + 0.3
        parameters, initial_conditions = SIS.get_parameters(S_data[0], I_data[0], N, beta=beta_perturbed,
                                                           beta_max=10,delta=delta_perturbed, delta_max=10,
                                                           S0_fixed=True,
                                                           I0_fixed=True,
                                                           S0_max=10e6,
                                                           I0_max=5e6)
        sis = EpidemicModel(SIS, parameters=parameters, data=data,
                           initial_conditions=initial_conditions, incidence_type=incidence)
        sis.fit()

        # Check fitted parameters
        beta_fitted = sis.fitted_parameters['beta']
        delta_fitted = sis.fitted_parameters['delta']

        assert np.isclose(beta, beta_fitted, rtol=5e-1)
        assert np.isclose(delta, delta_fitted, rtol=5e-1)

        sis = EpidemicModel(SIS, parameters=parameters, data=data, initial_conditions=initial_conditions, fit_period=10, incidence_type=incidence)
        sis.fit()

        # Check fitted parameters again
        beta_fitted = sis.fitted_parameters['beta']
        delta_fitted = sis.fitted_parameters['delta']

        assert np.isclose(beta, beta_fitted,rtol=5e-1)
        assert np.isclose(delta, delta_fitted, rtol=5e-1)

def test_SIR():
    for incidence in ['mass_action', 'standard']:
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
      sir = EpidemicModel(SIR, parameters=parameters, initial_conditions=initial_conditions, incidence_type=incidence)

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
      sir = EpidemicModel(SIR, parameters=parameters, data=data,
                          initial_conditions=initial_conditions, incidence_type=incidence)
      sir.fit()

      # check fitted parameters
      beta_fitted = sir.fitted_parameters['beta']
      gamma_fitted = sir.fitted_parameters['gamma']

      assert np.isclose(beta, beta_fitted)
      assert np.isclose(gamma, gamma_fitted)

      sir = EpidemicModel(SIR, parameters=parameters, data=data, initial_conditions=initial_conditions, fit_period=10, incidence_type=incidence)
      sir.fit()

      # check fitted parameters
      beta_fitted = sir.fitted_parameters['beta']
      gamma_fitted = sir.fitted_parameters['gamma']

      assert np.isclose(beta, beta_fitted)
      assert np.isclose(gamma, gamma_fitted)

def test_SIRS():
    for incidence in ['mass_action', 'standard']:
      # Initialize a model
      beta_0 = 0.1
      gamma_0 = 0.2
      delta_0 = 0.3
      parameters, initial_conditions = SIRS.get_parameters(99, 1, 0, 100,
                                                          beta=beta_0,
                                                          gamma=gamma_0,
                                                          delta=delta_0,
                                                          S0_fixed=True,
                                                          I0_fixed=False,
                                                          R0_fixed=True,
                                                          S0_max=10e6,
                                                          I0_max=5e6,
                                                          R0_max=10e6)
      sirs = EpidemicModel(SIRS, parameters=parameters, initial_conditions=initial_conditions, incidence_type=incidence)

      # Solve a problem with an independently checkable solution
      N = 100
      S0 = 99
      I0 = 1
      R0 = 0
      beta = 0.5
      gamma = 0.25
      delta = 0.25
      days_ahead = 40  # days ahead to look at
      T = np.arange(days_ahead)
      forecast = sirs.solve(T, (S0, I0, R0), (beta, gamma, delta, N))

      # get the curve data as if it were our data
      S_data = forecast[:, 0]
      I_data = forecast[:, 1]
      R_data = forecast[:, 2]
      data = np.array([S_data, I_data, R_data]).T

      # slightly perturbed parameters, to check if the fitting finds the original (optimal) parameters
      parameters, initial_conditions = SIRS.get_parameters(S_data[0], I_data[0], R_data[0], N, beta=beta + 0.4,
                                                          gamma=gamma + 0.2,
                                                          delta=delta + 0.2,
                                                          S0_fixed=True,
                                                          I0_fixed=True,
                                                          R0_fixed=True,
                                                          S0_max=10e6,
                                                          I0_max=5e6,
                                                          R0_max=10e6)
      sirs = EpidemicModel(SIRS, parameters=parameters, data=data,
                          initial_conditions=initial_conditions, incidence_type=incidence)
      sirs.fit()

      # check fitted parameters
      beta_fitted = sirs.fitted_parameters['beta']
      gamma_fitted = sirs.fitted_parameters['gamma']
      delta_fitted = sirs.fitted_parameters['delta']

      assert np.isclose(beta, beta_fitted)
      assert np.isclose(gamma, gamma_fitted)
      assert np.isclose(delta, delta_fitted, rtol=5e-1)

      sirs = EpidemicModel(SIRS, parameters=parameters, data=data, initial_conditions=initial_conditions, fit_period=5, incidence_type=incidence)
      sirs.fit()

      # check fitted parameters
      beta_fitted = sirs.fitted_parameters['beta']
      gamma_fitted = sirs.fitted_parameters['gamma']
      delta_fitted = sirs.fitted_parameters['delta']

      assert np.isclose(beta, beta_fitted, rtol=5e-1)
      assert np.isclose(gamma, gamma_fitted, rtol=5e-1)
      assert np.isclose(delta, delta_fitted, rtol=5e-1)

def test_SEIR():
    # Initialize a model
    beta_0 = 0.1
    gamma_0 = 0.2
    sigma_0 = 0.1
    parameters, initial_conditions = SEIR.get_parameters(99, 1, 1, 0, 100,
                                                         beta=beta_0,
                                                         gamma=gamma_0,
                                                         sigma=sigma_0,
                                                         S0_fixed=True,
                                                         E0_fixed=True,
                                                         I0_fixed=False,
                                                         R0_fixed=True,
                                                         S0_max=10e6,
                                                         I0_max=5e6,
                                                         R0_max=10e6)
    sir = EpidemicModel(SEIR, parameters=parameters, initial_conditions=initial_conditions)

    # Solve a problem with an independently checkable solution
    N = 100
    S0 = 99
    E0 = 1
    I0 = 1
    R0 = 0
    beta = 0.5
    gamma = 0.25
    sigma = 0.2
    days_ahead = 40  # days ahead to look at
    T = np.arange(days_ahead)
    forecast = sir.solve(T, (S0, E0, I0, R0), (beta, gamma, sigma, N))

    # get the curve data as if it were our data
    S_data = forecast[:, 0]
    E_data = forecast[:, 1]
    I_data = forecast[:, 2]
    R_data = forecast[:, 3]
    data = np.array([S_data, E_data, I_data, R_data]).T

    # slightly perturbed parameters, to check if the fitting finds the original (optimal) parameters
    parameters, initial_conditions = SEIR.get_parameters(S_data[0], E_data[0], I_data[0], R_data[0], N,
                                                         beta=beta + 0.4,
                                                         gamma=gamma + 0.2,
                                                         sigma=sigma + 0.1,
                                                         S0_fixed=True,
                                                         E0_fixed=True,
                                                         I0_fixed=True,
                                                         R0_fixed=True,
                                                         S0_max=10e6,
                                                         I0_max=5e6,
                                                         R0_max=10e6)
    seir = EpidemicModel(SEIR, parameters=parameters, data=data, initial_conditions=initial_conditions)
    seir.fit()

    # check fitted parameters
    beta_fitted = seir.fitted_parameters['beta']
    gamma_fitted = seir.fitted_parameters['gamma']
    sigma_fitted = seir.fitted_parameters['sigma']

    assert np.isclose(beta, beta_fitted)
    assert np.isclose(gamma, gamma_fitted)
    assert np.isclose(sigma, sigma_fitted)

    seir = EpidemicModel(SEIR, parameters=parameters, data=data, initial_conditions=initial_conditions, fit_period=10,)
    seir.fit()

    # check fitted parameters
    beta_fitted = seir.fitted_parameters['beta']
    gamma_fitted = seir.fitted_parameters['gamma']
    sigma_fitted = seir.fitted_parameters['sigma']

    assert np.isclose(beta, beta_fitted)
    assert np.isclose(gamma, gamma_fitted)
    assert np.isclose(sigma, sigma_fitted)