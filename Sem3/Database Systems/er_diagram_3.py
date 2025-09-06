from graphviz import Digraph

er_b = Digraph("ER_6_2b", format="pdf")
er_b.attr(rankdir="LR", size="10")

# Entities
entity_style = {"shape": "rectangle", "fontsize": "18", "fontname": "Helvetica-Bold"}
rel_style = {"shape": "diamond", "fontsize": "18", "fontname": "Helvetica-Bold"}

er_b.node("Student", "Student\n(StudentID, Name, Major)", **entity_style)
er_b.node("Course", "Course\n(CourseID, Title, Credits)", **entity_style)
er_b.node("Section", "Section\n(SecID, Semester, Year)", **entity_style)
er_b.node("Exam", "Exam\n(ExamID, ExamType, Date, Marks)", **entity_style)

# Relationships
er_b.node("Takes", "Takes", **rel_style)

# Student–Takes–Section
er_b.edge("Student", "Takes", label="N", fontsize="14")
er_b.edge("Takes", "Section", label="N", fontsize="14")

# Course–Section
er_b.node("Offers", "Offers", **rel_style)
er_b.edge("Course", "Offers", label="1", fontsize="14")
er_b.edge("Offers", "Section", label="N", fontsize="14")

# Exam depends on Takes (weak entity style)
er_b.edge("Takes", "Exam", label="N", fontsize="14")

# Render
er_b.render("ER_6_2b", format="pdf", cleanup=True)
