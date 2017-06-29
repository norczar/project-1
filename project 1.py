import cantera as ct
import matplotlib.pyplot as plt
# Simulation parameters
p = ct.one_atm # pressure [Pa]
Tin = 300.0  # unburned gas temperature [K]
reactants = 'H2:2, O2:2'  # premixed gas composition
width = 0.03  # m
loglevel = 1  # amount of diagnostic output (0 to 8)

# IdealGasMix object used to compute mixture properties, set to the state of the
# upstream oxyhydrogen mixture
gas = ct.Solution('h2o2.xml')
gas.TPX = Tin, p, reactants

# Set up flame object
f = ct.FreeFlame(gas, width=width)
f.set_refine_criteria(ratio=3, slope=0.06, curve=0.12)
f.show_solution()

# Solve with mixture-averaged transport model
f.transport_model = 'Mix'
f.solve(loglevel=loglevel, auto=True)

# Solve with the energy equation enabled
f.save('h2_adiabatic.xml', 'mix', 'solution with mixture-averaged transport')
f.show_solution()
print('mixture-averaged flamespeed = {0:7f} m/s'.format(f.u[0]))

# Solve with multi-component transport properties
f.transport_model = 'Multi'
f.solve(loglevel) # don't use 'auto' on subsequent solves
f.show_solution()
print('multicomponent flamespeed = {0:7f} m/s'.format(f.u[0]))
f.save('h2_adiabatic.xml','multi', 'solution with multicomponent transport')

# write the velocity, temperature, density, and mole fractions to a CSV file
f.write_csv('h2_adiabatic.csv', quiet=False)
plt.plot(f.grid,f.T)
plt.show
