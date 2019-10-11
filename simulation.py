import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, virus , initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        
        
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, self.pop_size, self.vacc_percentage, self.initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self.population = self._create_population(self.initial_infected) # List of Person objects
        self.total_vaccinated = 0

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        population_list = []

        # Vaccination calculated using defined vacc percentage and population size

        self.total_vaccinated = round(self.pop_size * self.vacc_percentage)

        for person_id in range(self.pop_size):


            # Handles if person is infected

            if person_id < initial_infected:
                population_list.append(Person(person_id, False, self.virus))
                self.total_infected += 1

            # Handles if person is vaccinated

            elif person_id < initial_infected + self.total_vaccinated:
                population_list.append(Person(person_id, False))
                # self.total_vaccinated += 1

            # Handles if person is not vaccinated
            else:

                population_list.append(Person(person_id, False))

        return population_list
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

    def get_infected_people(self):

        infected_list = []

        self.current_infected = 0

        for person in self.population:
            # print("person is alive", person.is_alive)
            # print("person infection", person.infection)
            if person.is_alive and person.infection != None:
                infected_list.append(person)
                self.current_infected += 1

        return infected_list

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.
        return len(self.get_infected_people()) is 0


    def run(self):
        """
        This method should run the simulation until all requirements for ending
        the simulation are met.
        """
        counter = 0
        should_continue = True

        while should_continue:
            counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()

        print("The simulation has ended after " + str(counter) + " turns" )



    def time_step(self):
        """
        This method should contain all the logic for computing one time step
        in the simulation.
        This includes:
            1. 100 total interactions with a randon person for each infected
            person in the population
            2. If the person is dead, grab another random person from the
            population.
                Since we don't interact with dead people, this does not count
                as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
        """
        # Create list of infected people
        self.new_deaths = 0
        self.new_vaccinations = 0
        infected_list = self.get_infected_people()

        #  Hainvg each infecter person interact with 100 other people
        for person in infected_list:
            interaction_count = 0
            while interaction_count != 100:

                # Makes sure the random person is alive

                random_person = random.choice(self.population)
                while not random_person.is_alive:
                    random_person = random.choice(self.population)

                # If alive interact with the random person
                self.interaction(person, random_person)
                interaction_count += 1

        # Check if infected people are dead or vaccinated
        for person in infected_list:
            survived = person.did_survive_infection()

            # Handles if person is alive
            if survived:
                self.new_vaccinations += 1
                self.total_vaccinated += 1
                self.logger.log_infection_survival(person, False)

            # Handles if person died lol
            else:
                self.new_deaths += 1
                self.total_dead += 1
                self.logger.log_infection_survival(person, True)


        self._infect_newly_infected()
        self.get_infected_people()

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.

        #   Nothing happens to random person because they are vaccinated
        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person, False, True, False)

        #   Nothing happens to random person because they are already infected
        elif random_person.infection is not None:
            self.logger.log_interaction(person, random_person, True, False, False)

        # Handles if random person is healthy but unvaccinated
        else:
            infected_chance = random.random()
            if (infected_chance < person.infection.repro_rate
               and self.newly_infected.count(random_person._id) == 0):
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person,
                                            False, False, True)
            else:
                self.logger.log_interaction(person, random_person,
                                            False, False, False)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for person_id in self.newly_infected: 
            # Get infected yo
            self.population[person_id].infection = self.virus
            self.total_infected += 1

        self.newly_infected.clear()




if __name__ == "__main__":
    params = sys.argv[1:]

    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    repro_num = float(params[4])
    
    
    

    
    

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
