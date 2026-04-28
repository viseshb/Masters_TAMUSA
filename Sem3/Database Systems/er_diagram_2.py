from graphviz import Digraph

er_a = Digraph("ER_6_2a", format="pdf")
er_a.attr(rankdir="LR", size="10")

# Entities
entity_style = {"shape": "rectangle", "fontsize": "18", "fontname": "Helvetica-Bold"}
rel_style = {"shape": "diamond", "fontsize": "18", "fontname": "Helvetica-Bold"}

er_a.node("Student", "Student\n(StudentID, Name, Major)", **entity_style)
er_a.node("Course", "Course\n(CourseID, Title, Credits)", **entity_style)
er_a.node("Section", "Section\n(SecID, Semester, Year)", **entity_style)
er_a.node("Exam", "Exam\n(ExamID, ExamType, Date)", **entity_style)

# Relationships
er_a.node("TakesExam", "TakesExam\n(Marks)", **rel_style)

# Connections
er_a.edge("Student", "TakesExam", label="N", fontsize="14")
er_a.edge("Section", "TakesExam", label="N", fontsize="14")
er_a.edge("Exam", "TakesExam", label="N", fontsize="14")

# Course–Section
er_a.node("Offers", "Offers", **rel_style)
er_a.edge("Course", "Offers", label="1", fontsize="14")
er_a.edge("Offers", "Section", label="N", fontsize="14")

# Render
er_a.render("ER_6_2a", format="pdf", cleanup=True)
