import pathlib
p=pathlib.Path("models/primarycare_model/app.py")
c=p.read_text(encoding="utf-8")
m="st.markdown("### Microeconomics lab 4: co-payment / access barrier")"
i=c.find(m)
le=c.find("
",i)
e="
    with st.expander("How this works"):
        st.markdown("#### Inputs")
        st.markdown("- Co-payment: out-of-pocket cost")
        st.markdown("- Local in-person capacity")
        st.markdown("- Digital access reach")
        st.markdown("- Equity protection")
        st.markdown("- Travel friction")
        st.markdown("#### Output: stacked bar of need met by route")
"
c=c[:le+1]+e+c[le+1:]
p.write_text(c,encoding="utf-8")
print("OK")
