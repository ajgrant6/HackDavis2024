import lgbtPolicy as lp

states_to_test = ["CA", "NY", "TX", "FL", "OH", "PR"]
for state in states_to_test:
    print(f"{state}: {lp.lgbtPolicy(state)}")
