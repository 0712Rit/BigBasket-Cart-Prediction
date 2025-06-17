import streamlit as st
import random
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from main import load_data
from recommender import create_similarity_matrix, recommend_products

# Page Config and Custom CSS
st.set_page_config(page_title="Smart Cart Predictor", layout="wide")

def local_css():
    st.markdown("""
        <style>
        body {
            background-color: #f7f9fc;
            color: #333;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stSelectbox > div {
            border-radius: 8px;
        }
        .stAlert {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_cart = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")
lottie_sidebar = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_HpFqiS.json")

# Sidebar
with st.sidebar:
    st_lottie(lottie_sidebar, height=120)
    st.markdown("## 🛒 Smart Cart Predictor")
    st.write("Discover products related to your shopping habits!")
    st.markdown("---")

@st.cache_data
def load_clean_data():
    return load_data()

df_full = load_clean_data()

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "prices" not in st.session_state:
    st.session_state.prices = {}
if "quantities" not in st.session_state:
    st.session_state.quantities = {}

st.title("💡 BigBasket Product Recommender")

st_lottie(lottie_cart, height=150)

# Dropdowns in columns
category_list = sorted(df_full["category"].unique())
colA, colB = st.columns(2)
with colA:
    selected_category = st.selectbox("📂 Choose a category", category_list)

df = df_full[df_full["category"] == selected_category].reset_index(drop=True)
product_list = df["product"].sort_values().unique()

with colB:
    selected_product = st.selectbox("🔍 Choose a product", product_list)

brand = df[df["product"] == selected_product]["brand"].values
if len(brand) > 0:
    st.info(f"🏷️ Brand: **{brand[0]}**")

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🛒 Add to Cart"):
        if selected_product not in st.session_state.cart:
            st.session_state.cart.append(selected_product)
            st.session_state.prices[selected_product] = random.randint(20, 200)
            st.session_state.quantities[selected_product] = 1
            st.success(f"Added **{selected_product}** to cart!")
        else:
            st.warning("Already in cart. You can update quantity below.")

with col2:
    if st.button("🎯 Recommend Similar Products"):
        sim_matrix = create_similarity_matrix(df)
        recommendations = recommend_products(df, sim_matrix, selected_product)
        st.info("Here are some products you might like:")
        for rec in recommendations:
            st.markdown(f"- 🛍️ **{rec}**")

with col3:
    if st.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.session_state.prices = {}
        st.session_state.quantities = {}
        st.warning("Cart has been cleared.")

# Cart View
if st.session_state.cart:
    st.markdown("---")
    st.subheader("🛍️ Your Shopping Cart")
    cart_data = []
    for item in st.session_state.cart:
        price = st.session_state.prices[item]
        qty = st.number_input(f"{item} (₹{price})", 1, 10,
                              value=st.session_state.quantities[item],
                              key=item)
        st.session_state.quantities[item] = qty
        cart_data.append((item, price, qty, price * qty))

    df_cart = pd.DataFrame(cart_data, columns=["Product", "Price", "Qty", "Subtotal"])
    st.dataframe(df_cart.style.format({"Price": "₹{}", "Subtotal": "₹{}"}), use_container_width=True)
    st.markdown(f"### 💰 Total: ₹{sum(row[3] for row in cart_data)}")

    if st.button("✅ Checkout"):
        st.balloons()
        st.success("Thank you for shopping with us!")
        st.markdown("Your order has been placed. 🧾")
        st.session_state.cart = []
        st.session_state.prices = {}
        st.session_state.quantities = {}
else:
    st.info("🛒 Your cart is empty.")

# Popular products
st.markdown("---")
st.subheader("🔥 Popular Products in This Category")
popular = df["product"].value_counts().head(5)
for prod, count in popular.items():
    st.markdown(f"- 📦 {prod} ({count} entries)")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
