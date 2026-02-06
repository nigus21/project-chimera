# Project Chimera Skills Overview

| Skill Name               | Purpose                                          | Input/Output Contract                | Governance Notes                  |
|---------------------------|-------------------------------------------------|------------------------------------|----------------------------------|
| skill_trend_fetcher       | Fetch trends from social platforms             | See `specs/technical.md`           | Must respect platform API limits |
| skill_content_planner     | Convert trends into structured content plan   | See `specs/technical.md`           | Risk flags trigger HIL approval  |
| skill_publisher           | Publish approved content                       | See `specs/technical.md`           | Requires valid approval token    |

> All skills follow the canonical contracts in `specs/technical.md`.  
> Any implementation outside these contracts is prohibited.