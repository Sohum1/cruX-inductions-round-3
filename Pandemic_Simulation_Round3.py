import random
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

"""Initial Conditions"""

total_population = 600 # Total Starting Population of people
percent_masked = 50 # Percentage of people wearing masks
population_density = 30 # Percent of capacity of places filled by people
num_of_generations = 80 # Number of days to run the simulation
with_mask_prob_infect = 0.10 # probability of getting infected with people weating masks
without_mask_prob_infect = 0.90 # probability of getting infected without anyone wearing a mask

change_vaccination_rate_on = False
change_lockdown_on = False
lockdown_intensity = 3.0
vaccinate_percent = 0.0 # percent of people to vaccinated everyday
incubation_period = 14 # How many days does the virus live
fatality = 2 # What percent of population dies on acquiring the disease

"""##Running the Simulation"""

persons = [] # list of human (person) objects
masks = [] # list of masked objects
maskless = [] # list of unmasked objects
places = [] # list of place objects
persons2 = [] # list of quarantined people

count_quarantined = [] # Counts current number of quarantined people
num_mask = round((percent_masked*total_population)/100) # Starting number of mask objects
num_maskless = total_population - num_mask # Starting number of maskless objects
num_place = round(total_population/(population_density*0.05)) # Number of different places people can be at GIVEN MAX PEOPLE IN ONE PLACE IS 5

vaccinate_frequency = round((vaccinate_percent*total_population))/100 # number of people to vaccinated everyday
# mask_prob_infect = with_mask_prob_infect

total_mask_infected = 0
total_maskless_infected = 0
cumulative_infected = 0
total_vaccinated_people = 0

# Functions used later
def less_than_num_prob(probability):
  """returns True, with the probability of returning True equal to the parameter, returns False otherwise"""
  return random.randint(1, 100) <= probability

def pinv(num):
  """returns 1 - num as long as parameter is between 0 and 1"""
  if num >= 0.0 and num <= 1.0:
    return 1 - num

def calc_trans_prob(i):
  """Calculate disease transmission probability of a person given a person object"""
  base = 0.9
  if isinstance(i, Mask):
    base *= 0.15
  if i.is_vaccinated:
    base *= 0.15
  return base

def calc_catch_prob(i):
  """Calculate disease catching probability of a person given a person object."""
  base = 0.9
  if isinstance(i, Mask):
    base *= 0.11
  if i.is_vaccinated:
    base *= 0.12
  return base

# probability of an uninfected person catching the disease if he comes in contact with an infected person is
# calc_trans_prob(infected person) * calc_catch_prob(uninfected person)

## CREATING LOCATION CLASS
class Place:
  def __init__(self, value, person1, person2, person3, person4, person5):
    self.value = value # How many additional people this place can occupy
    self.person1 = person1 # Type of person on place object
    self.person2 = person2 # Type of person on place object
    self.person3 = person3 # Type of person on place object
    self.person4 = person4 # Type of person on place object
    self.person5 = person5 # Type of person on place object

  def get_value():
    print(self.value)
x_lim = 21
y_lim = 21
x1 = [i for i in range(1, x_lim)]
y1 = [i for i in range(1, y_lim)]
coords = [[], []]
for i in range(1, len(x1) + 1):
    for j in range(1, len(y1) + 1):
        coords[0].append(i)
        coords[1].append(j)
xcoords, ycoords, colorsl, sizes = [], [], [], []
xcoords = coords[0][:]
ycoords = coords[1][:]
for i in range(num_place):
    colorsl.append('grey')
    sizes.append(50)

## CREATE LOCATION OBJECTS
for i in range(num_place):
  places.append(Place(5.0, None, None, None, None, None))

for i in range(len(places)):
    places[i].pcoord = [coords[0][i], coords[1][i]]

def all_place_occupied():
  """Checks if all place objects have been completely occupied by persons"""
  temp = True
  for place in places:
    if None in [place.person1, place.person2, place.person3, place.person4, place.person5]:
      temp = False
  return temp


def all_people_vaccinated():
  """Checks if all people have been vaccinated"""
  temp = True
  for person in persons:
    if not person.is_vaccinated:
      temp = False
  return temp

## CREATE PERSON CLASSES
class Person:
  def __init__(self, place_num, place_received, protection_rate, is_infected, is_vaccinated):
    self.place_num = place_num
    self.place_received = place_received
    self.protection_rate = protection_rate
    self.is_infected = is_infected
    self.is_vaccinated = is_vaccinated

  def assign_path(self):
    x = random.randint(0, len(places) - 1)
    y = random.randint(0, len(places) - 1)
    z = random.randint(0, len(places) - 1)
    blob_assigned = False
    while blob_assigned == False and not all_place_occupied():
      if not (places[x].value == 0 or places[y].value == 0 or places[z].value == 0):
        self.path = [x, y, z]
        self.pathw = [y, z]
        blob_assigned = True


  def assign_place(self, n):
    """Assigns available place object to the person. Person remains unassigned if all place objects are occupied"""
    setattr(places[n], 'person' + str(int(6 - (places[n].value))), self)
    self.bcoord = [places[n].pcoord[0] + np.random.uniform(-0.25, 0.25), places[n].pcoord[1] + np.random.uniform(-0.25, 0.25)]
    places[n].value -= 1.0

  def person_die(self):
    """Has a probability of 2% of killing infected people"""
    if self.is_infected and less_than_num_prob(fatality):
      persons.remove(self)

class Mask(Person):
  pass

class Maskless(Person):
  pass

## CREATE People OBJECTS
for i in range(num_mask):
  persons.append(Mask(0, -1.0, with_mask_prob_infect, False, False))
for i in range(num_maskless):
  persons.append(Maskless(0, -1.0, 1, False, False))

shuffle(persons)
for person in persons: #Assigns a place to each person
  person.trans_prob = calc_trans_prob(person)
  person.catch_prob = calc_catch_prob(person)
  person.assign_path()

def update_graph(x, which):
  index = persons.index(x) + (len(places)-1)
  xcoords[index] = x.bcoord[0]
  ycoords[index] = x.bcoord[1]
  colorsl[index] = which

def get_prob(list1):
  result = 1
  for l in list1:
    result *= pinv(l)
  return round(pinv(result), 3)

def sick_countdown():
  """Manages recovery from disease after a particular number of days"""
  for person in persons:
    if person.is_infected:
      person.days_left -= 1
      if person.days_left == 0:
        person.is_infected = False
        update_graph(person, 'green')
        person.is_vaccinated = True

def transmit_disease():
  """Distributes disease viruses at each generation"""

  global total_mask_infected
  global total_maskless_infected

  for place in places:
    temp = True
    place_persons = [place.person1, place.person2, place.person3, place.person4, place.person5]
    if lockdown_intensity != 0:
      del(place_persons[:int(lockdown_intensity)])
    for i in place_persons:
      if i is None:
        temp = False
    infected = []
    non_infected = []
    mask_rates = 1
    if temp:
      for i in place_persons:
        if i.is_infected:
          infected.append(i)
        else:
          non_infected.append(i)

  ###################
    # Calculating probabilities of people getting infected
    for i in non_infected:
      values = []
      for j in infected:
        values.append(j.trans_prob * i.catch_prob) # Creates list with probability of person getting infected values.
        # Putting in all these values in the get_prob function returns total probability of person getting infected
        # by everyone around them.

      if less_than_num_prob(get_prob(values) * 100) and not i.is_vaccinated:
        i.is_infected = True
        update_graph(i, 'red')
        if isinstance(i, Mask):
          total_mask_infected += 1
        elif isinstance(i, Maskless):
          total_maskless_infected += 1
        i.days_left = incubation_period


def vaccinate_people():
  """Vaccinates 'vaccinate_frequency' number of people every day"""
  global total_vaccinated_people
  num = len(persons)
  i = 0
  j = 0
  while i < vaccinate_frequency and not all_people_vaccinated() and j < total_population:
    x = random.randint(0, num - 1)
    if persons[x].is_vaccinated or persons[x].is_infected:
      i -= 1
    else:
      persons[x].is_vaccinated = True
      total_vaccinated_people += 1
    i += 1
    j += 1



def reset_values():
  for place in places: # Resetting place object values for next iteration
    place.value = 5.0 - lockdown_intensity
    place.person1 = None
    place.person2 = None
    place.person3 = None
    place.person4 = None
    place.person5 = None
  for person in persons: # Resetting person object values for next iteration
    person.place_num = 0
    person.place_received = -1.0
    # person.assign_place()

def count_masks():
  count = 0
  for person in persons:
    if isinstance(person, Mask):
      count += 1
  return count

def count_maskless():
  count = 0
  for person in persons:
    if isinstance(person, Maskless):
      count += 1
  return count

def count_infected_people():
  """Counts the number of infected people"""
  num_infected = 0
  for person in persons:
    if person.is_infected:
      num_infected += 1
  return num_infected

def count_infected_people_by_mask():
  mask_infect = 0
  for person in persons:
    if person.is_infected and isinstance(person, Mask):
      mask_infect += 1
  return mask_infect

def count_infected_people_by_maskless():
  maskless_infect = 0
  for person in persons:
    if person.is_infected and isinstance(person, Maskless):
      maskless_infect += 1
  return maskless_infect

def count_cumulative_infected():
  global cumulative_infected
  for person in persons:
    if person.is_infected and person.days_left == 14:
      cumulative_infected += 1



"""**Main Block**"""

total_num_infected = []
vaccinations = []
mask_infected = []
maskless_infected = []
dead_masked_people = []
dead_maskless_people = []
cumulative_infected_list = []
pop_vs_generation = {} # Dictionary containing generation number and number of persons alive

for person in persons:
  person.assign_place(person.path[0])


for person in persons:
    xcoords.append(person.bcoord[0])
    ycoords.append(person.bcoord[1])
    sizes.append(10)
    if person.is_infected:
        colorsl.append('red')
    else:
        colorsl.append('black')



# First People Infected

v = 0
for place in places:
  v += 1
  if place.value == 0:
    pblobs = [place.person1, place.person2, place.person3, place.person4, place.person5]
    for pblob in pblobs[round(len(pblobs)/2):]:
      pblob.is_infected = True
      pblob.days_left = 14
    if v == 3:
      break

for i in range(num_of_generations): # Each iteration is one generation

  # Set path for people based on whether it is a weekday or a weekend
  if i%7 == 0 or (i+1)%7 == 0:
    for k in range(3):
      for person in persons:
        person.assign_place(person.path[k])
      transmit_disease()
  else:
    for k in range(2):
      for person in persons:
        person.assign_place(person.pathw[k])
      transmit_disease()
  count_cumulative_infected()
  sick_countdown()


  cumulative_infected_list.append(cumulative_infected)
  vaccinate_people()
  vaccinations.append(total_vaccinated_people)

  for person in persons:
    person.person_die()

  dead_masked_people.append(num_mask - count_masks())
  dead_maskless_people.append(num_maskless - count_maskless())
  infected_people = count_infected_people()
  total_num_infected.append(infected_people)
  mask_infected.append(count_infected_people_by_mask())
  maskless_infected.append(count_infected_people_by_maskless())
  count_quarantined.append(len(persons2))


  pop_vs_generation[i+1] = infected_people


  reset_values()
  if change_lockdown_on:
    if infected_people/total_population >= 0.20:
      lockdown_intensity = 0.0
    elif infected_people/total_population < 0.2 and infected_people/total_population >= 0.1:
      lockdown_intensity = 2.0
    elif infected_people/total_population < 0.1:
      lockdown_intensity = 3.0
  if change_vaccination_rate_on:
    if i == 15:
      vaccinate_percent = 0.4
      vaccinate_frequency = round((vaccinate_percent*total_population))/100
  counti, countu = 0, 0
  for p in persons:
    if not p.is_infected:
      counti += 1
    elif p.is_infected:
      countu += 1
  plt.title('Spread of Viruses')
  plt.axis('off')
  plt.xlim(-1, x_lim+1)
  plt.ylim(-5, y_lim+1)
  plt.annotate('Day: ' + str(i+1), xy=(3.3, 1), xytext=(0.5, -1))
  plt.annotate('Number of uninfected people is ' + str(counti), xy=(3.3, 1), xytext=(0.5, -2))
  plt.annotate('"GREY": Places', xy =(3.3, 1), xytext =(0.5, -3))
  plt.annotate('"RED": infected', xy=(3.3, 1), xytext=(0.5, -4))
  plt.annotate('"BLACK": uninfected', xy=(3.3, 1), xytext=(0.5, -5))
  plt.annotate('"GREEN": recovered', xy=(3.3, 1), xytext=(0.5, -6))
  # plt.annotate('"BLACK" dots show uninfected people', xy =(3.3, 1), xytext =(0.5, -7))
  # plt.annotate('"RED" dots show infected people', xy =(3.3, 1), xytext =(0.5, -5))
  # plt.annotate('"GREEN" dots show recovered people', xy =(3.3, 1), xytext =(0.5, -7))
  sc = plt.scatter(xcoords, ycoords, sizes, colorsl)
  if i == num_of_generations - 1:
    plt.pause(4)
  else:
    plt.pause(0.1)
  plt.close()

print("A total of", total_mask_infected+total_maskless_infected, 'people were infected in this run')
print("Total masked people who got infected is", total_mask_infected)
print("Total maskless people who got infected is", total_maskless_infected)
