import streamlit as st
import pandas as pd

st.set_page_config(page_title="MSME AIF-PMFME Project Dashboard", layout="wide")
st.title("MSME AIF-PMFME Project Dashboard")

def compute_msme_aif_pmfme_metrics(msme_price_inc_gst: float,
                                   coconut_procurement_price_from_fig: float,
                                   number_of_nuts_day: float,
                                   per_nut_weight_factor: float,
                                   months_working_year: float,
                                   number_of_working_days_month: float,
                                   number_of_litres_day: float,
                                   skilled_wages_month: float,
                                   number_of_skilled: int,
                                   semi_skilled_wages_salary_month: float,
                                   number_of_semi_skilled: int,
                                   maintenance_and_expenses: float,
                                   interest_on_loan: float,
                                   depreciation_on_fixed_asset: float,
                                   miscellaneous_expenses: float):
    # 1. Revenue
    total_revenue_collected = (
        msme_price_inc_gst
        * number_of_litres_day
        * number_of_working_days_month
        * months_working_year
    )

    # 2. Variable Costs
    raw_material_direct_expenses = (
        number_of_nuts_day
        * per_nut_weight_factor
        * coconut_procurement_price_from_fig
        * number_of_working_days_month
        * months_working_year
    )

    salaries_and_wages = (
        skilled_wages_month * months_working_year * number_of_skilled
        + semi_skilled_wages_salary_month * months_working_year * number_of_semi_skilled
    )

    variable_costs = (
        raw_material_direct_expenses
        + salaries_and_wages
        + maintenance_and_expenses
        + (miscellaneous_expenses * 0.90)
    )

    # 3. Contribution
    contribution = total_revenue_collected - variable_costs

    # 4. Fixed Costs
    fixed_costs = interest_on_loan + depreciation_on_fixed_asset + (miscellaneous_expenses * 0.10)

    # 5. Net Profit
    net_profit = contribution - fixed_costs

    # Break-even analysis
    break_even_ratio = (fixed_costs / contribution) if contribution != 0 else 0.0
    break_even_point_percentage = break_even_ratio * 100.0
    break_even_point_sales = break_even_ratio * total_revenue_collected

    return {
        "total_revenue_collected": total_revenue_collected,
        "raw_material_direct_expenses": raw_material_direct_expenses,
        "salaries_and_wages": salaries_and_wages,
        "maintenance_and_expenses": maintenance_and_expenses,
        "interest_on_loan": interest_on_loan,
        "depreciation_on_fixed_asset": depreciation_on_fixed_asset,
        "miscellaneous_expenses": miscellaneous_expenses,
        "variable_costs": variable_costs,
        "contribution": contribution,
        "fixed_costs": fixed_costs,
        "net_profit": net_profit,
        "break_even_point_percentage": break_even_point_percentage,
        "break_even_point_sales": break_even_point_sales,
    }

# ------------------------ Sidebar Inputs ------------------------
with st.sidebar:
    st.header("Inputs")

    msme_price_inc_gst = st.number_input(
        "MSME Price (Incl. GST) per litre (₹)",
        value=80.00, min_value=0.0, step=0.01
    )

    coconut_procurement_price_from_fig = st.number_input(
        "Coconut Procurement Price from FIG (₹/kg)",
        value=51.64, min_value=0.0, step=0.01
    )

    with st.expander("Production Parameters", expanded=True):
        per_nut_weight_factor = st.number_input(
            "Per Nut Weight Factor (kg/nut)", value=0.4, min_value=0.0, step=0.01, format="%.2f",
            help="Average coconut weight per nut in kg"
        )
        months_working_year = st.number_input("Months Working in a Year", value=12.0, min_value=0.0, step=1.0)
        number_of_working_days_month = st.number_input("Working Days per Month", value=25.0, min_value=0.0, step=1.0)
        number_of_litres_day = st.number_input("Number of Litres per Day", value=175.0, min_value=0.0, step=1.0)

        # Computed number of nuts/day based on litres/day
        number_of_nuts_day = (number_of_litres_day * 0.91) / (per_nut_weight_factor * 0.3 * 0.6)
        st.text(f"Calculated Number of Nuts per Day: {number_of_nuts_day:,.0f}")

    with st.expander("Salary & Wages", expanded=False):
        skilled_wages_month = st.number_input("Skilled Wages per Month (₹)", value=25000.0, min_value=0.0, step=1000.0)
        number_of_skilled = st.number_input("Number of Skilled Workers", value=1, min_value=0, step=1)
        semi_skilled_wages_salary_month = st.number_input("Semi-Skilled Wages per Month (₹)", value=15000.0, min_value=0.0, step=1000.0)
        number_of_semi_skilled = st.number_input("Number of Semi-Skilled Workers", value=10, min_value=0, step=1)

    with st.expander("Fixed Costs & Overheads", expanded=False):
        maintenance_and_expenses = st.number_input("Maintenance & Expenses (₹)", value=1800000.0, min_value=0.0, step=10000.0)
        interest_on_loan = st.number_input("Interest on Loan (₹)", value=245000.0, min_value=0.0, step=1000.0)
        depreciation_on_fixed_asset = st.number_input("Depreciation on Fixed Assets (₹)", value=407000.0, min_value=0.0, step=1000.0)
        miscellaneous_expenses = st.number_input("Miscellaneous Expenses (₹)", value=50000.0, min_value=0.0, step=1000.0)

# ------------------------ Compute Metrics ------------------------
metrics = compute_msme_aif_pmfme_metrics(
    msme_price_inc_gst=msme_price_inc_gst,
    coconut_procurement_price_from_fig=coconut_procurement_price_from_fig,
    number_of_nuts_day=number_of_nuts_day,
    per_nut_weight_factor=per_nut_weight_factor,
    months_working_year=months_working_year,
    number_of_working_days_month=number_of_working_days_month,
    number_of_litres_day=number_of_litres_day,
    skilled_wages_month=skilled_wages_month,
    number_of_skilled=number_of_skilled,
    semi_skilled_wages_salary_month=semi_skilled_wages_salary_month,
    number_of_semi_skilled=number_of_semi_skilled,
    maintenance_and_expenses=maintenance_and_expenses,
    interest_on_loan=interest_on_loan,
    depreciation_on_fixed_asset=depreciation_on_fixed_asset,
    miscellaneous_expenses=miscellaneous_expenses,
)

# ------------------------ Display Key Metrics ------------------------
st.subheader("Key Performance Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue Collected (₹)", f"{metrics['total_revenue_collected']:,.2f}")
c2.metric("Contribution (₹)", f"{metrics['contribution']:,.2f}")
c3.metric("Net Profit (₹)", f"{metrics['net_profit']:,.2f}")

c4, c5 = st.columns(2)
c4.metric("Break-even Point (%)", f"{metrics['break_even_point_percentage']:.2f}%")
c5.metric("Break-even Point (Sales, ₹)", f"{metrics['break_even_point_sales']:,.2f}")

# ------------------------ Profit & Loss Table ------------------------
st.subheader("Profit & Loss Statement (Annual)")
pl_df = pd.DataFrame({
    "Category": [
        "Revenue",
        "Variable Costs",
        "   Raw Material",
        "   Salaries & Wages",
        "   Maintenance & Expenses",
        "   Miscellaneous (90%)",
        "Contribution",
        "Fixed Costs",
        "   Interest on Loan",
        "   Depreciation on Fixed Asset",
        "   Miscellaneous (10%)",
        "Net Profit"
    ],
    "Amount (₹)": [
        metrics['total_revenue_collected'],
        metrics['variable_costs'],
        metrics['raw_material_direct_expenses'],
        metrics['salaries_and_wages'],
        metrics['maintenance_and_expenses'],
        metrics['miscellaneous_expenses'] * 0.90,
        metrics['contribution'],
        metrics['fixed_costs'],
        metrics['interest_on_loan'],
        metrics['depreciation_on_fixed_asset'],
        metrics['miscellaneous_expenses'] * 0.10,
        metrics['net_profit']
    ]
})
st.dataframe(pl_df.style.format({"Amount (₹)": "{:,.2f}"}), use_container_width=True)
