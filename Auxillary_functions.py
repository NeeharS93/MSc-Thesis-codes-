import numpy as np 
import pybamm

def run_rate_capabilities(model, Parameter_values, C_rates): 
    var = pybamm.standard_spatial_vars
    var_pts = {var.x_n: 20, var.x_s: 20, var.x_p:400, var.r_n: 150, var.r_p: 20}
    sims = []
    for C_rate in C_rates:
        if C_rate < 2.1:
          t_eval = np.linspace(0, 4000 / C_rate, 500)
          dt_max = None
        elif C_rate < 4:
          t_eval = np.linspace(0, 3500 / C_rate, 1000)
          dt_max = 0.1
        elif C_rate < 8:
          t_eval = np.linspace(0, 3000 / C_rate, 500)
          dt_max = 0.001
        else:
          t_eval = np.linspace(0, 60, 500)
          dt_max = 0.001
        solver = pybamm.CasadiSolver(mode="safe", dt_max=dt_max, max_step_decrease_count= 15)
        sim = pybamm.Simulation(model, parameter_values=Parameter_values, var_pts=var_pts, solver=solver, C_rate=C_rate)
        sim.solve(t_eval)
        sims.append(sim)
    return sims