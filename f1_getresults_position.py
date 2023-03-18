import fastf1 as ff1

# Skru på cache
ff1.Cache.enable_cache('cache')

# Load session data
session = ff1.get_session(2023, 'Saudi Arabia', 'Q1')
session.load()

# Get positions as floats
results = session.results['Position']

# Convert floats to ints
results = results.astype(int)

# Print positions
print(results)
