# B4 assessment

Answer before consulting the instructor guide. Each question is worth 4 points: 2 for the correct behavior and 2 for its mechanism and limits (20 total). Explain predictions; a bare result is incomplete evidence.

1. What row does `SELECT id FROM containers WHERE fee > 100` return for C1=100, C2=200? What changes with >=, and why does the output shape remain unchanged?
2. Why does binding `C1' OR 1=1 --` as a parameter not return every row? Can a placeholder represent a table name?
3. C1 has two events and C2 has one. Explain why summing fees after the join returns 400 instead of 300. Why is SUM(DISTINCT fee) not a general solution?
4. A query executes successfully and returns 300. What additional questions must you ask about business meaning and caller access? Explain what the scoped capability and query_only each establish.
5. Why can a query returning one row still be expensive? Contrast a fetch limit with a SQLite progress callback and identify one limitation of cooperative deadlines.
