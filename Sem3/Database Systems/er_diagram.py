from graphviz import Digraph

# Create ER diagram with larger font and vector output
er = Digraph("CarInsuranceER", format="pdf")
er.attr(rankdir="LR", size="10")

# Common styles
entity_style = {"shape": "rectangle", "fontsize": "20", "fontname": "Helvetica-Bold"}
rel_style = {"shape": "diamond", "fontsize": "20", "fontname": "Helvetica-Bold"}

# Entities with attributes
er.node("Customer", "Customer\n(CustomerID, Name, Address, Phone)", **entity_style)
er.node("Car", "Car\n(CarID, LicensePlate, Model, Year)", **entity_style)
er.node("Accident", "Accident\n(AccidentID, Date, Location, Description)", **entity_style)
er.node("InsurancePolicy", "InsurancePolicy\n(PolicyID, StartDate, EndDate, PolicyType)", **entity_style)
er.node("Payment", "Payment\n(PaymentID, Amount, Period, DueDate, PaymentDate)", **entity_style)

# Relationships
er.node("Owns", "Owns", **rel_style)
er.node("HasAccident", "Has_Accident", **rel_style)
er.node("Covers", "Covers", **rel_style)
er.node("HasPayment", "Has_Payment", **rel_style)

# Connections with cardinalities
# Customer - Car
er.edge("Customer", "Owns", label="1", fontsize="16")
er.edge("Owns", "Car", label="N", fontsize="16")

# Car - Accident
er.edge("Car", "HasAccident", label="1", fontsize="16")
er.edge("HasAccident", "Accident", label="N", fontsize="16")

# InsurancePolicy - Car (M:N)
er.edge("InsurancePolicy", "Covers", label="M", fontsize="16")
er.edge("Covers", "Car", label="N", fontsize="16")

# InsurancePolicy - Payment (1:N)
er.edge("InsurancePolicy", "HasPayment", label="1", fontsize="16")
er.edge("HasPayment", "Payment", label="N", fontsize="16")

# Render the diagram as PDF (vector-based, no blur on zoom)
er.render("car_insurance_er_diagram", format="pdf", cleanup=True)
