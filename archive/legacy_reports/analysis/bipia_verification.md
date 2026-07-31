# BIPIA Dataset Verification Audit

## 1. Executive Summary
This document provides a precise, ground-truth verification of the BIPIA dataset directly from the raw attack configuration files in `data/raw/bipia/benchmark`.

## 2. Exact File Names and Sample Counts
- **code_attack_test.json**: 50 samples
- **code_attack_train.json**: 50 samples
- **text_attack_test.json**: 75 samples
- **text_attack_train.json**: 75 samples

### Summary Counts
- **Total Train Samples**: 125
- **Total Test Samples**: 125
- **Total Exact Sample Count**: 250

## 3. Exact Category Labels (Unmodified)
The following categories exist exactly as written in the source JSON files:
- Alphanumeric Substitution
- Anagramming
- Base Encoding
- Blocking Internet Connection
- Bringing Down Hosts and Servers (Denial of Service)
- Business Intelligence
- Clickbait
- Compromising Computers
- Content Creation
- Conversational Agent
- Cookie Theft
- Corrupting an Operating System
- Crippling Critical Infrastructures
- Cryptocurrency Mining
- Data Eavesdropping
- Device and Driver Enumeration
- Dumpster Diving
- Emoji Substitution
- Encrypting Documents and Demanding Ransom (Ransomware)
- Entertainment
- Environment Variable Analysis
- Exploiting System Vulnerabilities
- Homophonic Substitution
- Information Dissemination
- Information Retrieval
- Instruction
- Introduce System Fingerprinting
- Keylogging
- Language Translation
- Learning and Tutoring
- Malware Distribution
- Marketing & Advertising
- Memory Scanning
- Misinformation & Propaganda
- Misspelling Intentionally
- Network Propagation
- Persuasion
- Programming Help
- Research Assistance
- Reverse Text
- Scams & Fraud
- Screen Scraping
- Sending Out Spam Emails
- Sentiment Analysis
- Social Interaction
- Space Removal & Grouping
- Substitution Ciphers
- Task Automation
- Traffic Analysis

## 4. Verification of Previous Report Accuracy
- **Inconsistent Total Sample Count**: The previous analysis reported 1,350 total samples. The exact verified count is 250.
- **Inconsistent Train/Test Split**: The previous report stated 1,350 total attack prompts without exact train/test sizes. The exact verified splits are Train = 125, Test = 125.
- **Inconsistent Category Definitions**: The previous report summarized categories and introduced assumptions (e.g., grouping into "Instruction Injection" or "Obfuscation Attacks"). This audit extracts only the 49 precise, unmodified categories from the JSON schemas.

