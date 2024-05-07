import streamlit as st
import pandas as pd


def vanilla_extract_calculator_df(bean_count, folds):
    # Constants based on the table provided
    bean_weight_per_bean_g = 3  # each bean weighs 3 grams

    # Conversion constants
    ounces_per_gallon = 128  # fluid ounces per gallon
    grams_per_ounce = 28.3495  # grams per ounce
    ml_per_gallon = 3785.41  # milliliters per gallon

    # Calculate weight of beans
    total_bean_weight_g = bean_count * bean_weight_per_bean_g

    # Determine weight of beans per gallon for 1-fold (from provided data)
    weight_per_gallon_1_fold_g = 378.47  # for 1-fold based on table

    # Calculate required weight per gallon for desired fold level
    required_weight_per_gallon_g = weight_per_gallon_1_fold_g * folds

    # Calculate number of gallons needed to use the given number of beans for the specified fold level
    gallons_needed = total_bean_weight_g / required_weight_per_gallon_g

    # Calculate final volume in mL and ounces
    final_volume_ml = gallons_needed * ml_per_gallon
    final_volume_oz = gallons_needed * ounces_per_gallon

    # Calculate the volume of alcohol and water needed based on final volume
    alcohol_volume_ml = (
        0.35 * final_volume_ml
    )  # 35% of the final volume should be alcohol
    water_volume_ml = final_volume_ml - alcohol_volume_ml  # rest is water

    # Pricing (just a rough proportional estimation for simplicity)
    # Using price from 1-fold data as base price per ounce of final product
    base_price_per_oz_usd = 585.92 / 127.98
    base_price_per_oz_brl = 2929.59 / 127.98

    # Calculate total price
    price_usd = final_volume_oz * base_price_per_oz_usd
    price_brl = final_volume_oz * base_price_per_oz_brl

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
            "Price (USD)",
            "Price (BRL)",
        ],
        "Value": [
            bean_count,
            folds,
            total_bean_weight_g,
            round(alcohol_volume_ml, 2),
            round(water_volume_ml, 2),
            round(final_volume_ml, 2),
            round(final_volume_oz, 2),
            round(price_usd, 2),
            round(price_brl, 2),
        ],
    }

    return pd.DataFrame(data)


# Streamlit App
st.title("Vanilla Extract Calculator")

# Inputs
bean_count = st.number_input("Number of Beans", min_value=0, value=33, step=1)
folds = st.number_input("Number of Folds", min_value=1, value=1, step=1)

# Calculate and display the results
if st.button("Calculate"):
    results_df = vanilla_extract_calculator_df(bean_count, folds)
    st.write(results_df)
