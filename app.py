import streamlit as st
from main import load_data
from recommender import create_similarity_matrix, recommend_products

st.title("🛒 BigBasket Cart Predictor")

df = load_data()
sim_matrix = create_similarity_matrix(df)

product_list = df["product"].sort_values().unique()
selected_product = st.selectbox("Select a product:", product_list)

if st.button("Recommend Similar Products"):
    recommendations = recommend_products(df, sim_matrix, selected_product)
    st.subheader("🧠 You may also like:")
    for rec in recommendations:
        st.write("- " + rec)
