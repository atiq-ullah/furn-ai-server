"Analyze the following input to identify individual tasks. Use conjunctions, punctuation, changes in context, dates, times, and action verbs as cues for different tasks. Treat actions as separate tasks unless explicitly linked. Consider these examples:

Example 1: Simple Task Separation
Input: "Remind me to call the dentist tomorrow at 10 AM and pick up groceries after work."
Expected Output:
Task 1: Call the dentist, Date/Time: Tomorrow at 10 AM.
Task 2: Pick up groceries, Date/Time: After work.

Example 2: Multiple Tasks with Different Contexts
Input: "Schedule a team meeting for next Monday and buy birthday presents for Alice on the weekend."
Expected Output:
Task 1: Schedule team meeting, Date/Time: Next Monday.
Task 2: Buy birthday presents for Alice, Date/Time: On the weekend.

Example 3: Ambiguous Input
Input: "Set an appointment with Dr. Smith and arrange my travel plans."
Expected Output:
Task 1: Set an appointment with Dr. Smith.
Task 2: Arrange travel plans.

Example 4: Complex Input with Multiple Elements
Input: "Email the project report by tomorrow evening, call the supplier next Wednesday, and check the inventory levels on Friday."
Expected Output:
Task 1: Email the project report, Date/Time: By tomorrow evening.
Task 2: Call the supplier, Date/Time: Next Wednesday.
Task 3: Check inventory levels, Date/Time: On Friday.

If an input is ambiguous, default to linking it with the previous task or flag it for clarification. Use past task data for context when available.
