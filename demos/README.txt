Checkpoint 1: completed
	- Simulation for Part One - models assumptions for this project. Simulate feature selection to map real-world observations to task state in HTM.
	- Simulation for Part Two - models initial training interactions to build default mapping of task states to set of supportive behaviors. Can be extended to instead model initial training interactions to build default mapping of (task state, timestep) to set of supportive behaviors.
	- Basic uncertainty measure defined. Returns vector for whether or not to query user for supportive action label given a set of real-world observations.

Checkpoint 2: completed
	- Pushed to next checkpoint: use task_models instead of simpler HTM definition
	- fix assumptions as per 3/3/2018 meeting with Corina

Checkpoint 3: as per 3/12/2018 meeting with Corina
	- use task_models to define task
	- define what happens during the query - "Robot: What should I do now?" vs. "Should I do X?" 
	- based on this, play with uncertainty metric. May be more interesting to provide certain supportive actions at a given (task state, timestep) that have low uncertainty and query for others...but also may (1)incorrectly be assuming independence of supportive actions, (2) increase # of queries
	- how to decide whether query -> update to 'default' model or update to user-specific model. Would be interesting to have this depend on the query
	- if it works, add noise
	- spend time working with Baxter

Checkpoint4:
	- just stuck with my implementation of htm
	- completed query update
	- desc:
		part 1 - Oi:htmleaf dict
		part 2 - htmleaf:supportiveaction dict, htmleaf:query?TorF dict
		main - part1 dict, part2 dict
		        print default query dict
		        worker bob: 3 runs, print query dict now
		        worker carol: 3 runs, print query dict now
		part 3 - takes a starting htmleaf:supportiveaction dict and a starting htmleaf:query?TorF dict and update and return both

Checkpoint5:
	- uses real features (no model of task needed, but for the generation of simulated user preferences)
	- NOTE: environment features modeled slightly differently here as compared to the hrc_active_learning package, but still equivalent

Checkpoint6:
	- see final hrc_active_learning package in parent directory. 
	- desc:
		HTM
			The HTM class was only used to generated simulated user prefence label data. HTMs were defined to be trees, where inner nodes were ’parallel’ or ’sequential’ directives for the children, and the leaves are steps in the task.
		Chair Assembly Task
			This includes a class UserPrefEnvDemo which represents the state of the environment which can be updated given past successful actions. This file also includes sim user labels() which produces labels for given (timestep, environment features) based on some random variables and some reasonable heuristics.
		Model Framework
			This contains the UserPrefModel class that contains a dict of (timestep, environment features) keys and Counter objects keeping track of votes for supportive action lists.
		Other
			Utils.py contains an implementation of a prettyprint function I wrote useful for debugging.

Checkpoint6_extra
	- unfinished code to refactor simulation to use classes defined in hrc_active_learning, and some notes/data collected from robot experiments