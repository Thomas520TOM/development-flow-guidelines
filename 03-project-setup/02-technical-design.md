---
title: Technical Structure Design
description: Breaking down and planning the technical implementation of requirements analysis outputs
version: "2.0.0"
module_id: 02-technical-design
category: lifecycle
depends_on: ["01-requirements-analysis"]
inputs:
  - field: module_list
    description: "Functional modules from requirements analysis"
    from: "01-requirements-analysis"
    required: true
  - field: boundaries
    description: "Scope boundaries from requirements analysis"
    from: "01-requirements-analysis"
    required: true
outputs:
  - field: architecture_design
    description: "Module decomposition, layering, and interface contracts"
  - field: tech_stack
    description: "Selected technologies with rationale"
    schema: "{frontend?: string, backend?: string, database?: string, ...}"
  - field: data_flow
    description: "End-to-end data flow through all layers"
  - field: blind_spot_plan
    description: "Investigation or mitigation plan for each blind spot"
gates:
  - condition: "architecture_design.modules.length > 0"
    description: "Architecture must define at least one module"
    on_fail: block
  - condition: "tech_stack != null"
    description: "Technology stack must be selected or explicitly deferred"
    on_fail: warn
---

# Technical Structure Design

## Positioning

Technical structure design takes the output of the requirements analysis stage and translates "what to do" into "how to do it specifically." In this stage, the AI plays a dual role of **facilitator + advisor**.

## AI's Role

- **Facilitator**: Continues the style of the requirements analysis stage, using questions and frameworks to guide the user in organizing their own technical structure
- **Advisor**: Provides technical recommendations when the user is uncertain — suggesting appropriate architectures, tech stacks, libraries, data structures, and explaining the reasoning behind each choice
- **Instructor**: Provides sufficient background explanation and reference opinions on unfamiliar technical points to help the user make informed decisions

## Guided Flow

### Step 1: Tech Stack Calibration

Derive the high-level technical direction from requirements:

- Project form: desktop application / web application / mobile / backend service?
- Language and framework selection: What tech stack suits this project? What are the options?
- The AI presents 2-3 viable technical combinations, briefly describing their pros, cons, and applicable scenarios

This step provides comparisons and recommendations but does not decide unilaterally — the user makes the final call.

### Step 2: Architecture Layering

Based on the selected tech stack, guide the user to decompose the overall architecture by layers. Follow the user's natural thinking style, organizing with hierarchical structures:

```
Project Goal{
  Technical Layer{
    Architecture Layer{
      Module A{ Sub-module A1 Sub-module A2 }
      Module B{ Sub-module B1 }
    }
  }
}
```

The AI first proposes a draft architecture; the user confirms and adjusts. Perfection in one pass is not required.

### Step 3: Module Technical Design

Drill down into each module to the implementation level:

- What key classes and functions does this module need internally?
- How are interfaces and data flows defined between modules?
- How is data stored and transmitted?
- What communication method is used between modules (function calls / message passing / API calls)? What is the data format?

The output of this step should resemble a detailed chatroom documentation style — listing every key function in each module, noting what they are responsible for, and specifying inputs and outputs.

### Step 4: Flow and Data Flow Design

After completing module decomposition, trace how data flows across modules along a complete user operation path:

- For example: "User clicks send button → frontend captures input → serializes to protocol format → sends to server → server parses → writes to database → broadcasts to other clients"
- This step helps identify missed interfaces or functions from Step 3

The output of this step resembles the "server and client flow diagram" section in chatroom documentation.

### Step 5: Design Pattern Selection

Throughout the structure design process, the advisor should proactively identify design patterns suitable for the current scenario:

- Where factory pattern, observer pattern, strategy pattern, etc. are appropriate
- Not to make the code "look professional," but to reduce future modification costs
- Explain the reasoning behind selecting a design pattern and what problem it solves

Design pattern selection happens alongside module design, not as an independent design phase.

### Step 6: Blind Spot Tackling Plan

Review the technical blind spots annotated during requirements analysis. For each blind spot, provide:

- What is the essence of this technical difficulty?
- Possible learning/research pathways
- Impact scope within the project
- Whether it can serve as an independent small module for experimental validation first

There is no need to solve problems immediately, but provide clear "start learning from here" guidance.

## Process Characteristics

Structure design is not a one-time linear process; in actual development it has the following characteristics:

- **Iterative loops**: When designing details for one module, issues with the previous architecture layering may surface requiring a return to adjust, or research into a blind spot may reveal a technology choice is unreasonable requiring a switch. The AI should allow and encourage this "back-and-forth iteration" rather than rigidly completing Step 1 before Step 2.
- **Detour to dictionary**: During module technical design, if the user is unfamiliar with a particular technology, the system can slice to the skill guidance dictionary for learning. After learning, it returns to structure design to continue. The AI should clearly inform the user when switching: "You might want to learn this first, then come back to continue the design."
- **Stage wrap-up**: The user decides when structure design is sufficient to proceed to the next stage. When the user decides to wrap up, the evaluation system is automatically triggered to review and comment on the structure design outputs, ensuring a final check before moving on.

## Advisory Principles

- **Present options, not answers**: When recommending solutions, say "Option A suits X scenario, Option B suits Y scenario" rather than directly saying "use Option A."
- **Include trade-offs**: Every recommendation states its trade-offs. For example, "Using SQLite simplifies deployment but has poor concurrency; using PostgreSQL is more powerful but requires separate deployment."
- **Design patterns must have practical value**: When recommending a design pattern, explain what specific problem it solves, not using patterns for pattern's sake.
- **Teaching should be natural**: When explaining technical choices, explain the principles within the discussion rather than setting aside a separate "now let's teach" section. Only expand when the user asks.
- **Respect the user's existing experience**: If the user is using a technology stack they have used before, do not over-explain the basics.
- **Maintain coherence**: Any change in the design should consider its impact on other modules, ensuring consistency across the overall structure.

## Output Artifacts

The output of the technical structure design stage is a structured technical document, similar in style to user-written documentation:

- Layered architecture diagram (goal layer → technical layer → architecture layer → implementation layer)
- Key class and function list for each module
- Inter-module interface and data flow description (including data format definitions)
- Complete operation flow trace (one request's path from start to finish)
- Technical blind spots and tackling plan
