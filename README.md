# Chatbot Modules

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Offline--First-238636?style=for-the-badge" />
  <img src="https://img.shields.io/badge/14_Modules-58a6ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active_Development-ff5e6c?style=for-the-badge" />
</p>

> **Modular offline-first multilingual chatbot engine — memory, intent, neural nets + optional LLM hybrid.**

This repository contains the modular source/runtime components of the offline-first multilingual chatbot.

The project is structured around independently understandable modules that are assembled by the main runtime. This keeps the system usable in constrained environments such as Pydroid 3 while also supporting a cleaner package interface elsewhere.

## What lives here

The modules cover areas such as:

- intent recognition
- conversation handling
- memory
- creative generation
- games
- utilities
- multilingual response data
- optional ML integrations
- optional voice and vision functionality

## Architecture

```text
Numbered modules
      │
      ▼
    main.py
      │
      ▼
Shared runtime
 ┌────┼────┬────┬────┐
 ▼    ▼    ▼    ▼    ▼
NLP  Chat  Memory Games Tools
      │
      ▼
Optional ML / voice / vision
```

The numbered execution model is deliberate rather than accidental: it preserves compatibility with the original Android/Pydroid workflow.

## Module map

| # | Module | Purpose |
|---|---|---|
| 01 | config_and_db | Configuration + SQLite persistence |
| 02 | memory_and_logging | Conversation memory + logging |
| 03 | datetime_engine | Time-aware responses |
| 04 | creative_writing | Poems, stories, jokes, riddles |
| 05 | fun_extras | Entertainment handlers |
| 06 | text_number_tools | Math, conversions, utilities |
| 07 | continuity_and_tone | Context tracking + tone |
| 08 | hangman | Game module |
| 09 | sklearn_tools | Classical ML integrations |
| 10 | neural_networks | Neural net components |
| 11 | llm_hybrid | Optional LLM fallback |
| 12 | intent_engine | Intent classification |
| 13 | response_banks_loader | Multilingual response data |
| 14 | chatbot_core | Core orchestration |

## Status

**Active development**

See the main chatbot repository for the complete project documentation, installation options, tests and architecture explanation.