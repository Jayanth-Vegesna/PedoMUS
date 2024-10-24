import streamlit as st

def simulation_page():
    st.subheader("Simulation Page")
    st.write("Here are the simulations:")
    iframe_code_gene_expression = """
    <iframe src="https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    iframe_code_beers_law = """
    <iframe src="https://phet.colorado.edu/sims/html/beers-law-lab/latest/beers-law-lab_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    iframe_code_keplers_laws = """
    <iframe src="https://phet.colorado.edu/sims/html/keplers-laws/latest/keplers-laws_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    st.components.v1.html(iframe_code_gene_expression, height=600)
    st.components.v1.html(iframe_code_beers_law, height=600)
    st.components.v1.html(iframe_code_keplers_laws, height=600)