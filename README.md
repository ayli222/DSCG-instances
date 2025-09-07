# DSCG-instances
Instances used in Dr. Judy Goldsmith's research group on **Dynamic Skill Coalition Formation Games (DSCG)**.  

These instances were created to support experiments in **Temporal Team Formation Games (TTFG)** and related coalition formation research.  
They provide reproducible benchmarks for evaluating algorithms that assign agents with heterogeneous skills, preferences, and histories to dynamic tasks over time.  

This repository is intended to:
- Publish the exact **instances** used in grant proposals and research experiments.  
- Provide a minimal **Python scaffold** (`usage.py` + `objectLoader.py`) so others can load, inspect, and extend these instances.  
- Serve as a **foundation for future algorithmic extensions**, where researchers can add their own schedulers, learning agents, or evaluation pipelines.  

## Repository Structure
```
.
├── instance.py # Definition of the instance data structure, including tasks and agents
├── usage.py # Example usage of loading an instance
├── objectLoader.py # Lightweight save/load of instances
├── Instances/ # Contains published instances
│ └── M-PREF2025_instances/
│ ├── 10-agents-biasSTDEV-0/
│ ├── 15-agents-biasSTDEV-0.25/
│ └── ...
├── LICENSE # MIT License (for code)
└── LICENSE-DATA # CC-BY 4.0 License (for instances)
```
## Requirements

- Python >= 3.9  
- [NumPy](https://numpy.org/)

## Usage
Load a directory of instances and print a simple summary:
```
python usage.py --instances-dir "./Instances/M-PREF2025_instances/10-agents-biasSTDEV-0" --index 0
```

example output:
```
==== TTFG Minimal Scaffold ====
Loaded instance from: C:\Users\aaron\Documents\DSCG-instances\Instances\M-PREF2025_instances\10-agents-biasSTDEV-0
Instance index: 0
Instance object summary:

--- AGENTS ---

Agent [0]:
        Bias for Variety = 0.0
        Bias for Patience = 0
        Skill Vector:
                  0  1  0  1  0

Agent [1]:
        Bias for Variety = 0.0
        Bias for Patience = 0
        Skill Vector:
                  1  1  1  1  0

...

Agent [9]:
        Bias for Variety = -0.0
        Bias for Patience = 0
        Skill Vector:
                  1  1  1  1  1

--- TASKS ---

------------ Timestep: 0 ------------

Task [0]:
        Required Skill Vector:
                  0  0  0  2  1

Task [1]:
        Required Skill Vector:
                  1  1  1  0  0

Task [2]:
        Required Skill Vector:
                  0  1  1  1  1

------------ Timestep: 1 ------------

Task [0]:
        Required Skill Vector:
                  0  1  4  1  1

Task [1]:
        Required Skill Vector:
                  0  0  0  0  0

Task [2]:
        Required Skill Vector:
                  0  1  1  0  0

Task [3]:
        Required Skill Vector:
                  0  0  1  0  0
...

------------ Timestep: 11 ------------

Task [0]:
        Required Skill Vector:
                  0  0  0  0  0

Task [1]:
        Required Skill Vector:
                  0  0  1  1  0

Task [2]:
        Required Skill Vector:
                  0  1  1  2  1

Task [3]:
        Required Skill Vector:
                  0  2  1  0  0

--- Utility Matrix ---

  1.000 -1.000 -0.500 -1.000 -0.500 -1.000 -0.667  1.000 -0.333 -0.333
 -1.000  1.000 -0.250 -1.000 -0.417  1.000 -0.500 -1.000 -0.500 -0.583
  0.500  0.250 -1.000  0.250  0.000  0.250  0.000  0.500  0.000  0.083
 -1.000 -1.000 -0.250  1.000 -0.167 -1.000 -0.250 -1.000 -0.500 -0.167
  0.500  0.417  0.000  0.167 -1.000  0.417  0.000  0.500  0.000  0.000
 -1.000  1.000 -0.250 -1.000 -0.417  1.000 -0.500 -1.000 -0.500 -0.583
  0.667  0.500  0.000  0.250  0.000  0.500 -1.000  0.667  0.000  0.083
  1.000 -1.000 -0.500 -1.000 -0.500 -1.000 -0.667  1.000 -0.333 -0.333
  0.333  0.500  0.000  0.500  0.000  0.500  0.000  0.333 -1.000  0.000
  0.333  0.583  0.083  0.167  0.000  0.583  0.083  0.333  0.000 -1.000

Done.
```

## License

- **Code**: [MIT License](LICENSE)  
- **Instances (datasets)**: [CC BY 4.0](LICENSE-DATA)  

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a  
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
