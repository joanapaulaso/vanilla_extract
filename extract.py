import streamlit as st
import pandas as pd


# Define the function to calculate vanilla extract values
def vanilla_extract_calculator_df(
    bean_count, folds, usd_to_brl_exchange_rate, eur_to_brl_exchange_rate, eur_to_usd
):
    # Constants
    bean_weight_per_bean_g = 3  # Each bean weighs 3 grams
    ounces_per_gallon = 128  # Fluid ounces per gallon
    grams_per_ounce = 28.3495  # Grams per ounce
    ml_per_gallon = 3785.41  # Milliliters per gallon
    alcohol_price_per_l_usd = 23.0  # Alcohol price in USD per liter
    land_price_per_ha_brl = 14300  # Land price in BRL per hectare
    beans_per_land_unit = 30  # Number of beans per 4 m²
    m2_per_ha = 10000  # Square meters per hectare
    m2_per_bean_unit = 4  # Square meters required per 30 beans

    # Pricing per fold level
    fold_prices = {1: 1.0, 2: 20.0, 3: 30.0}
    base_price_per_oz_usd = fold_prices[folds]

    # Cost calculations
    bean_cost_per_kg_usd = 150  # Cost for 1000 grams of vanilla beans
    bean_weight_per_kg_g = 1000
    cost_per_gram_usd = bean_cost_per_kg_usd / bean_weight_per_kg_g

    # Vanilla producer information
    green_vanilla_price_eur_min = 15.6
    green_vanilla_price_eur_max = 16.6
    curing_space_m2_per_800kg = 1600

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
    alcohol_volume_l = alcohol_volume_ml / 1000

    # Calculate prices in USD and BRL
    base_price_per_oz_brl = base_price_per_oz_usd * usd_to_brl_exchange_rate
    price_usd = final_volume_oz * base_price_per_oz_usd
    price_brl = final_volume_oz * base_price_per_oz_brl

    # Calculate the cost of the beans used
    total_bean_cost_usd = total_bean_weight_g * cost_per_gram_usd

    # Calculate the added value (final price minus cost of beans)
    added_value_usd = price_usd - total_bean_cost_usd

    # Calculate the land space needed for cultivation (4 m² for every 30 beans)
    cultivation_space_m2 = (bean_count / beans_per_land_unit) * m2_per_bean_unit
    cultivation_space_ha = cultivation_space_m2 / m2_per_ha

    # Estimate the cost of vanilla production based on cultivation space
    total_producer_cost_min_usd = (
        green_vanilla_price_eur_min * cultivation_space_ha * eur_to_usd
    )
    total_producer_cost_max_usd = (
        green_vanilla_price_eur_max * cultivation_space_ha * eur_to_usd
    )
    total_producer_cost_mean_usd = (
        total_producer_cost_min_usd + total_producer_cost_max_usd
    ) / 2

    # Calculate the space needed for curing based on 800 kg per month
    curing_space_required_m2 = (
        (total_bean_weight_g / 1000) / 800 * curing_space_m2_per_800kg
    )

    # Calculate costs and gains
    alcohol_cost_usd = alcohol_volume_l * alcohol_price_per_l_usd
    land_price_usd = (
        land_price_per_ha_brl / usd_to_brl_exchange_rate * (cultivation_space_ha + (curing_space_required_m2 / 10000))
    )

    # Separate costs and gains into a DataFrame
    costs_and_gains_data = {
        "Parameter": [
            "Alcohol Cost (USD)",
            "Producer Cost (Mean, USD)",
            "Land Price (USD)",
            "Extract Price (USD)",
        ],
        "Value": [
            round(alcohol_cost_usd, 2),
            round(total_producer_cost_mean_usd, 2),
            round(land_price_usd, 2),
            round(price_usd, 2),
        ],
    }
    costs_and_gains_df = pd.DataFrame(costs_and_gains_data)

    # Calculate the final balance
    total_costs_usd = alcohol_cost_usd + total_producer_cost_mean_usd + land_price_usd
    final_balance_usd = price_usd - total_costs_usd

    # Add the balance to the DataFrame
    costs_and_gains_df.loc[len(costs_and_gains_df.index)] = [
        "Final Balance (USD)",
        round(final_balance_usd, 2),
    ]

    # Creating a DataFrame for the overall calculation
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
            "Producer Cost Min (USD)",
            "Producer Cost Max (USD)",
            "Cultivation Space (ha)",
            "Curing Space (ha)",
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
            round(total_producer_cost_min_usd, 2),
            round(total_producer_cost_max_usd, 2),
            round(cultivation_space_ha, 2),
            round(curing_space_required_m2 / 10000, 2),
        ],
    }

    main_df = pd.DataFrame(data)
    return main_df, costs_and_gains_df


# Streamlit App
st.title("Vanilla Extract Calculator")

# Display the logo image at the top
st.image("logo.png", use_column_width=True, caption="Your Logo", output_format="PNG")

# Inputs
bean_count = st.number_input("Number of Beans", min_value=0, value=333, step=1)
folds = st.selectbox("Number of Folds", [1, 2, 3])
usd_to_brl_exchange_rate = st.number_input(
    "USD to BRL Exchange Rate", min_value=1.0, value=5.0, step=0.1
)
eur_to_brl_exchange_rate = st.number_input(
    "EUR to BRL Exchange Rate", min_value=1.0, value=6.0, step=0.1
)
eur_to_usd = st.number_input(
    "EUR to USD Exchange Rate", min_value=0.5, value=1.08, step=0.01
)

# Calculate and display the results
if st.button("Calculate"):
    main_df, costs_and_gains_df = vanilla_extract_calculator_df(
        bean_count,
        folds,
        usd_to_brl_exchange_rate,
        eur_to_brl_exchange_rate,
        eur_to_usd,
    )
    st.write("**Overview of Extract Production**")
    st.table(main_df)

    st.write("**Costs and Gains Breakdown**")
    st.table(costs_and_gains_df)

# Display the diagram image after the data frame
st.image(
    "diagram.png",
    use_column_width=True,
    caption="Vanilla Beans Price Projection",
    output_format="PNG",
)
