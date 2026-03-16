# Fello Account Intelligence Engine - Easy Video Script
*Speak naturally, like you're explaining to a friend*

---

## PART 1: INTRO (1-2 minutes)

**What to say:**
"Hi everyone! Today I want to show you a project I built called the Fello Account Intelligence Engine.

Basically, here's the problem: When people visit your website, most of them are anonymous. You don't know who they are, what company they work for, or if they're actually interested in buying.

And here's the crazy part - by the time someone finally identifies themselves, they're already 70% through their buying journey. So you've missed all the early signals.

My solution takes those anonymous visitors and uses AI to figure out who they are and what they want - then sends that info directly to your sales team."

---

## PART 2: HOW IT WORKS (2-3 minutes)

**What to say:**
"So let me show you how it works.

The system has three main steps:

**Step 1: Signal Generation**
First, we capture visitor signals - things like which company domain they're coming from, what pages they're looking at, how long they're staying, and how often they visit.

**Step 2: AI Analysis**
This is where the magic happens. We send each signal to Groq's Llama-3 AI model, which does a deep dive on the company. It figures out:
- Who the decision-makers are
- What technology they're using
- Their company size and industry
- How likely they are to buy (we call this an 'intent score')
- Even personalized suggestions for how to approach them

**Step 3: Results**
All this information gets saved as a clean JSON file that can be imported directly into Salesforce or any other CRM system.

The whole thing runs automatically through GitHub Actions - no servers needed."

---

## PART 3: LIVE DEMO (3-4 minutes)

**What to say:**
"Let me show it running right now.

*I'll switch to my browser and open GitHub Actions*

Here's my repository. I'll click on the Actions tab, select the workflow, and just hit 'Run Workflow' with 10 records.

*Wait for it to start*

You can see it's running now. Each step is logged so you can see exactly what's happening.

While this runs, let me explain what's going on behind the scenes..."

---

## PART 4: THE OUTPUT (2 minutes)

**What to say:**
"*Once the workflow completes*

Okay, it finished in about 2 minutes. Now let me show you what it produced.

*I'll open the JSON file*

Here's a sample output. For each company, we get:

**Basic Info:** Company name, domain, industry, size, location

**Leadership:** Who's in charge - CTO, VP of Engineering, etc.

**Intent Score:** A number from 1 to 10 showing how ready they are to buy. An 8 or higher means they're really interested.

**Persona:** What kind of person is visiting - like 'VP of Engineering looking for scalability tools'

**AI Summary:** A complete paragraph about the company, their funding, what they're working on

**Sales Hook:** Something specific you can mention in your outreach - like 'They just raised $45 million and are hiring engineers'

**Action Item:** Exactly what to do next - like 'Send them fintech case studies'

This is gold for sales teams. Instead of spending hours researching, they get everything they need in seconds."

---

## PART 5: SUMMARY (1-2 minutes)

**What to say:**

"To summarize, here's what this system does:

**Before:** Sales teams are flying blind - they don't know who's visiting their website or which companies are actually interested. They waste hours doing manual research.

**After:** Anonymous visitors become qualified leads. Sales teams get:
- Company names and details automatically
- Intent scores showing who's hottest
- Personalized outreach suggestions
- All delivered to their CRM

**The best part?**
- It's fully automated with GitHub Actions
- Uses free AI from Groq
- No infrastructure costs
- Completely open source

**Use cases:**
- ABM campaigns - target accounts showing high intent
- Sales prioritization - focus on the best prospects first
- Competitive intelligence - see who's researching you versus competitors

That's it! Thanks for watching, and happy to answer any questions."

---

## CHEAT SHEET (Quick Reference)

**The Problem:**
- 70% of buying journey happens before prospects identify themselves
- Sales teams don't know who's visiting their website
- Hours wasted on manual research

**The Solution:**
- Visitor signals → AI analysis → Sales intelligence
- Uses Groq + Llama-3
- Automated via GitHub Actions
- Results in ~2 minutes

**What You Get:**
- Company identification
- Intent score (1-10)
- Decision-maker personas
- Personalized sales hooks
- All in Salesforce-ready JSON

**Key Stats:**
- 90% reduction in research time
- 17+ data points per account
- Zero infrastructure costs

---

## TIPS FOR RECORDING

**Before you start:**
- Have your GitHub repo open in a tab
- Have a sample JSON output ready to show
- Run the workflow once so it's fresh in your mind

**While recording:**
- Speak at a normal pace
- Use your mouse to point at things on screen
- If you mess up, just pause and start that sentence over
- You can edit out mistakes later

**If you forget something:**
- Glance at this script
- Or just keep going - it doesn't need to be perfect!

**Length target:**
- Aim for 8-10 minutes total
- Don't rush - better to be clear than quick
