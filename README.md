# CIFO_project_group_A Spring Semester 2024/2025

## The project aims at:  apply‬ing the Genetic‬‭ Algorithms‬‭ to‬‭ solve‬‭ an‬‭ optimization‬‭ problem.
### The optimization problem
‭ Sports League Optimization‬
‭ In‬‭ a‬‭ fantasy‬‭ sports‬‭ league,‬‭ the‬‭ objective‬‭ is‬‭ to‬‭ assign‬‭ players‬‭ to‬‭ teams‬‭ in‬‭ a‬‭ way‬‭ that‬‭ ensures‬
‭ a balanced distribution of talent while staying within salary caps.‬
‭
‭
‬
‭ 1‬
‭ Each player is defined by the following attributes:‬
●
‬‭ Skill rating: Represents the player's ability.‬
●
‬‭ Cost: The player's salary.‬
●
‭ Position:‬‭ One‬‭ of‬‭ four‬‭ roles:‬‭ Goalkeeper‬‭ (GK),‬‭ Defender‬‭ (DEF),‬‭ Midfielder‬‭ (MID),‬‭ or‬
‭ Forward (FWD).‬
‭ A‬‭ solution‬‭ is‬‭ a‬‭ complete‬‭ league‬‭ configuration,‬‭ specifying‬‭ the‬‭ team‬‭ assignment‬‭ for‬‭ each‬
‭ player.‬‭ These‬‭ are‬‭ the‬‭ constraints‬‭ that‬‭ must‬‭ be‬‭ verified‬‭ in‬‭ every‬‭ solution‬‭ of‬‭ the‬‭ search‬‭ space‬
‭ (no object is considered a solution if it doesn’t comply with these):‬
●
‭ Each‬‭ team‬‭ must‬‭ consist‬‭ of:‬‭ 1‬‭ Goalkeeper,‬‭ 2‬‭ Defenders,‬‭ 2‬‭ Midfielders‬‭ and‬‭ 2‬
‭ Forwards.‬
●
‬‭ Each player is assigned to exactly one team.‬
‭ Impossible‬‭ Configurations:‬‭ Teams‬‭ that‬‭ do‬‭ not‬‭ follow‬‭ this‬‭ exact‬‭ structure‬‭ (e.g.,‬‭ a‬‭ team‬‭ with‬
‭ 2‬‭ goalkeepers,‬‭ or‬‭ a‬‭ team‬‭ where‬‭ the‬‭ same‬‭ defender‬‭ is‬‭ assigned‬‭ twice)‬‭ are‬‭ not‬‭ part‬‭ of‬‭ the‬
‭ search‬‭ space‬‭ and‬‭ are‬‭ not‬‭ considered‬‭ solutions.‬‭ It‬‭ is‬‭ forbidden‬‭ to‬‭ generate‬‭ such‬‭ an‬
‭ arrangement during evolution.‬
‭ Besides‬‭ that,‬‭ each‬‭ team‬‭ should‬‭ not‬‭ exceed‬‭ a‬‭ 750€‬‭ million‬‭ total‬‭ budget.‬‭ If‬‭ it‬‭ does,‬‭ it‬‭ is‬‭ not‬‭ a‬
‭ valid solution and the fitness value should reflect that.‬
‭ The‬‭ objective‬‭ is‬‭ to‬‭ create‬‭ a‬‭ balanced‬‭ league‬‭ that‬‭ complies‬‭ with‬‭ the‬‭ constraints.‬‭ A‬‭ balanced‬
‭ league‬‭ a‬‭ is‬‭ a‬‭ league‬‭ where‬‭ the‬‭ average‬‭ skill‬‭ rating‬‭ of‬‭ the‬‭ players‬‭ is‬‭ roughly‬‭ the‬‭ same‬‭ among‬
‭ the‬‭ teams.‬‭ This‬‭ can‬‭ be‬‭ measured‬‭ by‬‭ the‬‭ standard‬‭ deviation‬‭ of‬‭ the‬‭ average‬‭ skill‬‭ rating‬‭ of‬‭ the‬
‭ teams.

## Team Members 

| Name              | Student Number | 
|:------------------|:----------------|
| Alexandra Pinto   | 20211599        | 
| Julia Karpienia   | 20240514        | 
| Steven Carlson  | 20240554   | 
| Tim Straub | 20240505   | 
