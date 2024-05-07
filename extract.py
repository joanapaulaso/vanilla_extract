import streamlit as st
import pandas as pd


# Define the function to calculate vanilla extract values
def vanilla_extract_calculator_df(
    bean_count, folds, base_price_per_oz_usd, usd_to_brl_exchange_rate
):
    # Constants
    bean_weight_per_bean_g = 3  # Each bean weighs 3 grams
    ounces_per_gallon = 128  # Fluid ounces per gallon
    grams_per_ounce = 28.3495  # Grams per ounce
    ml_per_gallon = 3785.41  # Milliliters per gallon

    # Cost calculations
    bean_cost_per_kg_usd = 150  # Cost for 1000 grams of vanilla beans
    bean_weight_per_kg_g = 1000
    cost_per_gram_usd = bean_cost_per_kg_usd / bean_weight_per_kg_g

    # Calculate weight of beans
    total_bean_weight_g = bean_count * bean_weight_per_bean_g

    # Determine weight of beans per gallon for 1-fold (from provided data)
    weight_per_gallon_1_fold_g = 378.47  # for 1-fold based on the table

    # Calculate required weight per gallon for the desired fold level
    required_weight_per_gallon_g = weight_per_gallon_1_fold_g * folds

    # Calculate the number of gallons needed to use the given number of beans for the specified fold level
    gallons_needed = total_bean_weight_g / required_weight_per_gallon_g

    # Calculate final volume in mL and ounces
    final_volume_ml = gallons_needed * ml_per_gallon
    final_volume_oz = gallons_needed * ounces_per_gallon

    # Calculate the volume of alcohol and water needed based on final volume
    alcohol_volume_ml = (
        0.35 * final_volume_ml
    )  # 35% of the final volume should be alcohol
    water_volume_ml = final_volume_ml - alcohol_volume_ml  # Rest is water

    # Calculate prices based on the user inputs
    base_price_per_oz_brl = base_price_per_oz_usd * usd_to_brl_exchange_rate
    price_usd = final_volume_oz * base_price_per_oz_usd
    price_brl = final_volume_oz * base_price_per_oz_brl

    # Calculate the cost of the beans used
    total_bean_cost_usd = total_bean_weight_g * cost_per_gram_usd

    # Calculate the added value (final price minus cost of beans)
    added_value_usd = price_usd - total_bean_cost_usd

    # Creating a DataFrame
    data = {
        "Parameter": [
            "Beans (count)",
            "Folds",
            "Bean Weight (g)",
            "Alcohol Volume (mL)",
            "Water Volume (mL)",
            "Final Volume (mL)",
            "Final Volume (oz)",
            "Extract Price (USD)",
            "Extract Price (BRL)",
            "Bean Cost (USD)",
            "Bean Cost per kg (USD)",
            "Added Value (USD)",
        ],
        "Value": [
            bean_count,
            folds,
            round(total_bean_weight_g, 2),
            round(alcohol_volume_ml, 2),
            round(water_volume_ml, 2),
            round(final_volume_ml, 2),
            round(final_volume_oz, 2),
            round(price_usd, 2),
            round(price_brl, 2),
            round(total_bean_cost_usd, 2),
            round(bean_cost_per_kg_usd, 2),
            round(added_value_usd, 2),
        ],
    }

    return pd.DataFrame(data)


# Streamlit App
st.title("Vanilla Extract Calculator")

# Display the logo image at the top
st.image("logo.png", use_column_width=True, caption="", output_format="PNG")

# Inputs
bean_count = st.number_input("Number of Beans", min_value=0, value=333, step=1)
folds = st.number_input("Number of Folds", min_value=1, value=1, step=1)
base_price_per_oz_usd = st.number_input(
    "Base Price of Extract per Ounce (USD)", min_value=0.0, value=1.0, step=0.1
)
usd_to_brl_exchange_rate = st.number_input(
    "USD to BRL Exchange Rate", min_value=1.0, value=5.0, step=0.1
)

# Calculate and display the results
if st.button("Calculate"):
    results_df = vanilla_extract_calculator_df(
        bean_count, folds, base_price_per_oz_usd, usd_to_brl_exchange_rate
    )
    st.table(results_df)

# Display the diagram image after the data frame
st.image(
    "diagram.png",
    use_column_width=True,
    caption="Vanilla Beans Price Projection",
    output_format="PNG",
)
