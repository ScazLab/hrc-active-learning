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

