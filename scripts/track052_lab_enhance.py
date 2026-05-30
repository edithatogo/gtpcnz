import pathlib
p = pathlib.Path("models/primarycare_model/app.py")
c = p.read_text(encoding="utf-8")

# Helper to add how-this-works expander
def add_expander(marker, content):
    global c
    old = marker
    new = marker + "
" + content
    if old in c:
        c = c.replace(old, content + "
" + old, 1)
        print(f"Added expander after {marker[:50]}...")
        return True
    else:
        print(f"NOT FOUND: {marker[:60]}...")
        return False

# Micro lab 3: scheduled payment
doc3 = """    with st.expander("How this works - inputs, assumptions, calculation, output"):
        st.markdown("#### Inputs")
        st.markdown("- **Eligible activity units:** volume of claimable activity."
            "\n- **Scheduled payment rate (NZD/unit):** per-unit payment."
            "\n- **Control strength (0-100):** audit and rule intensity."
            "\n- **Scope flexibility (0-100):** breadth of eligible workforce.")
        st.markdown("#### Assumptions")
        st.markdown("1. Gross payment = units * rate."
            "\n2. Controls reduce net payment via sigmoid (strategic_response)."
            "\n3. Scope expands net payment via diminishing_return."
            "\n4. Illustrative NZD values, not calibrated.")
        st.markdown("#### Calculation")
        st.latex(r"\text{gross} = \text{units} \times \text{rate}")
        st.latex(r"\text{net} = \text{gross} - \text{control} + \text{scope_bonus}")
        st.markdown("#### Output")
        st.markdown("- **Gross, control adjustment, net payment** in illustrative NZD."
            "\n- **Interpretation:** shows how controls reduce effective payment.")
"""
add_expander('    st.markdown("### Microeconomics lab 3: scheduled activity payment")', doc3)

p.write_text(c, encoding="utf-8")
print("Done")
