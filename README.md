# cruX-inductions-round-3

link to original github repository: https://github.com/Sohum1/cruX_inductions

Hello!
My project is a pandemic simulation that illustrates how diseases spread across populations. It also shows how various measures like masks, lockdowns, and vaccinations affect this spread. This simulation is an agent-based model created using Object-Oriented Programming in Python.

Tasks completed:

Task 1) Added path-following to the simulation: Earlier, people in the simulation would randomly be assigned one place each day. Now each person has a fixed path it takes every day, which includes multiple locations. I did this by giving an additional attribute to each person object, a list containing randomly selected locations for the person to go everyday. This path remains fixed for a person for the entire simulation, except for weekends (as described in the next task).

Task 2) Added a weekly routine: Each person's path varies for weekdays and weekends; a person takes a fixed route every weekday and a different fixed route every weekend. The path taken by each person on weekends is stored in a different attribute of the object, created similarly to the weekday path.

Tasks 3 & 4) Improved simulation of transmission probabilities: Changed probability rules for transmission of disease between two people and removed commutativity of transmission between masked and unmasked people. I created two functions (calc_trans_prob() and calc_catch_prob()), one calculating how likely an infected person is to transmit a virus and the other calculating how likely an uninfected person is to catch a virus given he comes in contact with an infected person, given information like whether the person is wearing a mask, is vaccinated, etc. This ensures if an infected and uninfected person come in contact, which one is wearing a mask affects the probability of the uninfected person getting infected. Probability calculation of vaccinated people has also been changed through the functions, and an arbitrary number of extra variables can be added for calculating the probabilities just by adding new conditions to the functions.

Task 5) Allowing outbreaks: Now, instead of randomly infecting people to introduce the disease to the population, the disease arises when the maximum number of people possible in a place are present, thus simulating an outbreak.

Task 6) GUI (partial): Added an animation depicting locations, uninfected people, infected people, etc. It was done by animating a scatterplot in matplotlib.

demo output on running pandemic_simulation_round3.py: https://www.youtube.com/watch?v=7N6B7gSw1sA

Note: Graphs created in the previous simulation from past run data and visualisations comparing different measures are not a part of this program and can be found in the previous repository.
