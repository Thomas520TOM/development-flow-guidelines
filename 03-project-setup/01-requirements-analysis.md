---
title: Requirements Analysis
description: From vague ideas to clear requirements, guiding the user step by step
version: "2.0.0"
module_id: 01-requirements-analysis
category: lifecycle
depends_on: []
inputs:
  - field: user_idea
    description: "Vague or structured description of what the user wants to build"
    required: true
outputs:
  - field: module_list
    description: "Decomposed functional modules with responsibilities"
    schema: "[{name: string, responsibility: string}]"
  - field: boundaries
    description: "In-scope and out-of-scope items for current iteration"
    schema: "{in_scope: [string], out_of_scope: [string]}"
  - field: blind_spots
    description: "Identified unknown areas needing investigation"
    schema: "[{topic: string, label: 'needs_research' | 'accepted_risk'}]"
gates:
  - condition: "module_list.length > 0"
    description: "At least one module must be identified"
    on_fail: block
  - condition: "boundaries.in_scope.length > 0"
    description: "Scope must be explicitly defined"
    on_fail: block
---

# Requirements Analysis

## Positioning

This is the first stage of project setup. Users' initial ideas are often vague; the goal of requirements analysis is to transform fuzzy ideas into clear, actionable requirements through guided dialogue.

## AI's Role

The AI acts as a **facilitator**, not a surrogate:

- Does not make decisions for the user, but helps the user discover "questions they haven't thought of yet but need to consider"
- Does not directly output a complete requirements document for user review; instead guides the user to reach their own conclusions
- Respects the user's thinking process, leaving room for the user to add their own thoughts

## Guided Flow

### Step 1: Scenario Definition

Rather than directly asking "what features do you want," first help the user clarify:

- **Target users**: Who is this project for?
- **Core scenarios**: Under what circumstances will users use it?
- **Problem to solve**: What is the reason this project exists?

### Step 2: Module Discovery

Derive potentially needed modules from the scenarios. The AI proposes a module framework; the user decides whether to accept, modify, or reject it:

- The AI provides a "draft" module breakdown based on the description (listing possible functional modules)
- The user decides which modules to include, exclude, or adjust
- The user may also freely add modules the AI did not anticipate

### Step 3: Boundaries and Priorities

Refine each confirmed module further:

- **What to do / what not to do**: Clarify the module's boundaries
- **Priorities**: Which are must-haves, which can come later
- **Constraints**: Any limitations (performance, platform, timeline, etc.)

### Step 4: Technical Blind Spot Annotation

Based on the user's familiarity level, annotate current-stage technical blind spots and risk points:

- Which technologies has the user used before and is confident in?
- Which has the user not encountered and needs to learn or research?
- How large is the impact scope of these blind spots (affecting the entire project or limited to a single module)?

There is no expectation to solve these problems at this point; simply identify them and defer to the technical structure design stage for resolution.

## Guided Principles

- **Respect the user's layered thinking habits**: Organize discussions following the user's natural layering — first define the goal layer (what to do), then the technical layer (what to use), then the implementation layer (how to do it).
- **Derive requirements from scenarios, not the other way around**: discuss scenarios first, then features.
- **AI provides frameworks, user makes choices**: the AI offers options and structural ideas; the user judges and fills in.
- **Leave breathing room**: Do not pursue 100% precision during requirements analysis. Some problems only surface during coding. Allow for "we'll figure that out when we get there."

## Output Artifacts

The output of the requirements analysis stage is a structured checklist that serves as input for the next stage:

- Confirmed module list (module name + one-line description + priority)
- "What to do / what not to do" boundaries for each module
- Currently known technical blind spots and risk points
