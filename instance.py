import numpy as np
import random

#np.random.seed(23)
#random.seed(23)

class Agent: 
    def __init__(self, id, skillCount):
        self.ID = id
        self.bias_variety = 0.0
        self.bias_patience = 0.0
        self.skills = [0 for i in range(skillCount)]

class Task:
    def __init__(self, id, num_skills):
        self.ID = id
        self.req_skills = [0 for _ in range(num_skills)]
        self.curr_skills = [0 for _ in range(num_skills)]  # Keep this if you need to track current skills separately
        self.assignment = []

    def inc_req_skill_at(self, index):
        self.req_skills[index] += 1

    def assign(self, agent, skill):
        self.assignment.append((agent, skill))
        self.curr_skills[skill] += 1

    def unassign(self, agent, skill):
        self.assignment.remove((agent, skill))
        self.curr_skills[skill] -= 1
            
        
class Instance:
    MIN_BIAS_VARIETY = -0.333
    MAX_BIAS_VARIETY = 0.333
    MIN_BIAS_PATIENCE = 0.0
    MAX_BIAS_PATIENCE = 1.0
    
    MEAN_SKILLS_PER_AGENT = 4
    STDV_SKILLS_PER_AGENT = 1
    MAX_SKILLS_PER_AGENT = 5
    MIN_SKILLS_PER_AGENT = 1
    
    AGENTS_PER_TASK = -1
    MIN_TASKS_PER_STEP = 3
    MAX_TASKS_PER_STEP = 5
    MEAN_TASKS_PER_STEP = -1 #made in constructor
    STDV_TASKS_PER_STEP = -1 #made in constructor

    MEAN_GROUP_SIZE = 5
    STDV_GROUP_SIZE = 2
    MAX_UTILITY = 1.0
    MIN_UTILITY = -1.0
    BREAK_PENALTY = MAX_UTILITY * 10 

    def __init__(self, num_agents, num_skills, schedule_length, biasDistID=0):
        self.num_agents = num_agents
        self.num_skills = num_skills
        self.agents = [Agent(i, num_skills) for i in range(num_agents)]
        self.schedule_length = schedule_length
        self.schedule = [[] for i in range(schedule_length)]  # Pass num_skills to Task
        self.preferences = np.zeros((num_agents, num_agents))
        self.break_room = []
        self.break_penalty = self.BREAK_PENALTY
        self.biasID = biasDistID
        self.bias_stdev = 1/8

        self.MAX_SKILLS_PER_AGENT = min(self.MAX_SKILLS_PER_AGENT, num_skills)
        self.MEAN_TASKS_PER_STEP = (self.MAX_TASKS_PER_STEP + self.MIN_TASKS_PER_STEP) / 2 if self.AGENTS_PER_TASK == -1 else self.num_agents / self.AGENTS_PER_TASK
        self.STDV_TASKS_PER_STEP = (self.MAX_TASKS_PER_STEP - self.MIN_TASKS_PER_STEP) / 4 if self.AGENTS_PER_TASK == -1 else num_agents / (4 * self.AGENTS_PER_TASK) 
    
        self.generated_assignment = -1
        self.generated_reward = -1

    def scale_bias(self, stdev):
        if self.bias_stdev == -1: self.bias_stdev = stdev 
        for agent in self.agents:
            agent.bias_variety *= stdev / self.bias_stdev
            agent.bias_variety = max(-1, min(1, agent.bias_variety))
        self.bias_stdev = stdev
            
    
    def save_assignment(self, timestep):
        assignment = [0 for i in range(self.num_agents)]
        for task in self.schedule[timestep]:
            for agent_id, skill in task.assignment:
                assignment[agent_id] = (task.ID, skill)
        return assignment

    def load_assignment(self, timestep, assignment):
        for task in self.schedule[timestep]:
            task.assignment = []
            task.curr_skills = [0 for _ in range(self.num_skills)]

        # Reset break room
        self.break_room = []

        for agent_id in range(self.num_agents):
            if assignment[agent_id]:
                task_ID = assignment[agent_id][0]
                skill = assignment[agent_id][1]
                self.schedule[timestep][task_ID].assign(agent_id, skill)
            else:
                self.break_room.append(self.agents[agent_id])
            
    def randomize_all(self):
        self.randomize_agents()
        self.randomize_timesteps()
        self.randomize_preferences()
        
    def generate_highUtil(self):
        self.randomize_agents()

        prePrefs = [[0 for i in range(self.num_agents)] for i in range(self.num_agents)]
        
        time = self.schedule_length * 2
        assignment = [[0 for i in range(self.num_agents)] for i in range(time)] #for each time step the assignment is given as a list of (projectID, skillID) tuples such that each tuple's index is its agents ID
        project_count = [max(self.MIN_TASKS_PER_STEP, min(int(np.random.normal(self.MEAN_TASKS_PER_STEP, self.STDV_TASKS_PER_STEP)), self.MAX_TASKS_PER_STEP)) for i in range(time)]
        
        for timestep in range(time):
            #make assignment from workers to projects based on preprefs
            currentAssignment = [[] for _ in range(project_count[timestep])]
            for i in random.sample(range(self.num_agents), self.num_agents):
                projectUtils = [sum([prePrefs[i][a] + prePrefs[a][i] for a in task]) for task in currentAssignment]
                projectChoice = random.choice([i for i, x in enumerate(projectUtils) if x == max(projectUtils)])
                currentAssignment[projectChoice].append(i)
                assignment[timestep][i] = (projectChoice, random.choice([i for i, x in enumerate(self.agents[i].skills) if x == 1]))
            
            #instantiate tasks
            tasks_in_step = []
            for i, project in enumerate(currentAssignment):
                if len(project) == 0:
                    tasks_in_step.append(Task(i, self.num_skills))
                    continue
                task = Task(i, self.num_skills)
                for agent in project:
                    task.req_skills[assignment[timestep][agent][1]] += 1
                tasks_in_step.append(task)
                
            if timestep >= time - self.schedule_length:
                self.schedule[timestep - (time - self.schedule_length)] = tasks_in_step
            
            #update pre-pref matrix
            for agent1 in self.agents: 
                for agent2 in self.agents:
                    if agent1.bias_variety > 0: 
                        prePrefs[agent1.ID][agent2.ID] += 1 if assignment[timestep][agent1.ID][0] == assignment[timestep][agent2.ID][0] else -1
                    else:
                        prePrefs[agent1.ID][agent2.ID] -= 1 if assignment[timestep][agent1.ID][0] == assignment[timestep][agent2.ID][0] else -1
                    
        #map preprefs to preferences
        min_val = np.min(prePrefs)
        max_val = np.max(prePrefs)
        for i, prePrefList in enumerate(prePrefs):
            self.preferences[i] = [(2 * (x - min_val) / (max_val - min_val)) - 1 for x in prePrefList]

        return assignment[-self.schedule_length:]

    def randomize_agents(self):
        #random.seed()
        for agent in self.agents:
            agent.skills = [0 for _ in range(self.num_skills)]
            agent.bias_variety = random.gauss(0, 1/8) #self.sample_bias() #random.uniform(self.MIN_BIAS_VARIETY, self.MAX_BIAS_VARIETY)
            agent.bias_patience = 0#self.sample_bias()
            num_skills_agent_has = max(self.MIN_SKILLS_PER_AGENT, min(int(np.random.normal(self.MEAN_SKILLS_PER_AGENT, self.STDV_SKILLS_PER_AGENT)), self.MAX_SKILLS_PER_AGENT))
            for _ in range(num_skills_agent_has):
                skill_index = random.randint(0, self.num_skills - 1)
                while agent.skills[skill_index] == 1:
                    skill_index = random.randint(0, self.num_skills - 1) #skill distribution
                agent.skills[skill_index] = 1

    def randomize_timesteps(self):
        #random.seed()
        for step in range(len(self.schedule)):
            tasks_in_step = []
            num_tasks_in_step = max(self.MIN_TASKS_PER_STEP, min(int(np.random.normal(self.MEAN_TASKS_PER_STEP, self.STDV_TASKS_PER_STEP)), self.MAX_TASKS_PER_STEP))
            
            task_partition = [0]
            task_partition += sorted(random.sample(range(1, self.num_agents), num_tasks_in_step - 1))
            task_partition.append(self.num_agents)
            #print(task_partition)
            for i in range(num_tasks_in_step):
                sum_skills_task = task_partition[i+1] - task_partition[i]
                task = Task(i, self.num_skills)
                for _ in range(sum_skills_task):
                    skill_index = random.randint(0, self.num_skills - 1)
                    task.req_skills[skill_index] += 1
                    
                tasks_in_step.append(task)
            
            self.schedule[step] = tasks_in_step
            
        #print('schedule: ' + str(self._timestep[0][0]._req_skills))

    def randomize_preferences(self):
        #random.seed()
        for i in range(self.num_agents):
            for j in range(self.num_agents):
                self.preferences[i, j] = 0.0 if i == j else random.uniform(self.MIN_UTILITY, self.MAX_UTILITY)

    def print_all(self):
        self.print_agents()
        self.print_tasks()
        self.print_utility_mat()

    def print_agents(self):
        print("\n--- AGENTS ---")
        for agent in self.agents:
            print(f"\nAgent [{agent.ID}]:")
            print(f"\tBias for Variety = {agent.bias_variety}")
            print(f"\tBias for Patience = {agent.bias_patience}")
            print("\tSkill Vector:")
            print("\t\t", end="")
            for j in range(self.num_skills):
                print(f"{1 if agent.skills[j] else 0:3}", end="")
            print()

    def print_tasks(self):
        print("\n--- TASKS ---")
        for i, timestep in enumerate(self.schedule):
            print(f"\n------------ Timestep: {i} ------------")
            for task in timestep:
                print(f"\nTask [{task.ID}]:")
                print(f"\tRequired Skill Vector:")
                print("\t\t", end="")
                for j in range(self.num_skills):
                    print(f"{task.req_skills[j]:3}", end="")
                print()

    def print_utility_mat(self):
        print("\n--- Utility Matrix ---")
        for i in range(self.num_agents):
            print()
            for j in range(self.num_agents):
                print(f"{self.preferences[i, j]:7.3f}", end="")
        print()
        
    def getString(self):
        st = ""
        for agent in self._all_agents:
            st += str(agent.ID())
            st += " "
            st += str(agent.bias_variety())
            st += " "
            for skill in agent._skills:
                st += str(skill) + " "
            st += "\n"
        st += "\n"
        
        for step in self._timestep:
            for task in step: 
                st += str(task.ID())
                st += " "
                for skill in task._req_skills:
                    st += str(skill) + " "
                st += "\n"
            st += "\n"
        
        for i in range(len(self._utility_mat)):
            for j in range(len(self._utility_mat[0])):
                st += str(self._utility_mat[i][j]) + " "
            st += "\n"
        st += "\n"

        
        return st