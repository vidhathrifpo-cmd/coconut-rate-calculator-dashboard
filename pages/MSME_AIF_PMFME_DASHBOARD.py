# --- MSME AIF-PMFME PROJECT DASHBOARD (Enhanced Input Section) ---

def compute_msme_aif_pmfme_metrics(coconut_procurement_price_from_fig: float,
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
    # A. TOTAL REVENUE COLLECTED
    total_revenue_collected = (
        coconut_procurement_price_from_fig
        * number_of_litres_day
        * number_of_working_days_month
        * months_working_year
    )

    # B. OPERATING EXPENSES
    # 1) Raw material direct expenses
    raw_material_direct_expenses = (
        number_of_nuts_day
        * per_nut_weight_factor
        * coconut_procurement_price_from_fig
        * number_of_working_days_month
        * months_working_year
    )

    # 2) Salaries and wages
    salaries_and_wages = (
        skilled_wages_month * months_working_year * number_of_skilled
        + semi_skilled_wages_salary_month * months_working_year * number_of_semi_skilled
    )

    # Fixed cost
    fixed_cost = interest_on_loan + depreciation_on_fixed_asset + (miscellaneous_expenses * 0.10)

    # Contribution
    contribution = total_revenue_collected - (
        raw_material_direct_expenses
        + salaries_and_wages
        + maintenance_and_expenses
        + (miscellaneous_expenses * 0.90)
    )

    # Break-even
    break_even_ratio = fixed_cost / contribution if contribution != 0 else 0.0
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
        "fixed_cost": fixed_cost,
        "contribution": contribution,
        "break_even_point_percentage": break_even_point_percentage,
        "break_even_point_sales": break_even_point_sales,
    }

# In your Streamlit main layout, replace the MSME section with this enhanced version:
with st.expander("MSME AIF-PMFME PROJECT DASHBOARD", expanded=True):
    st.caption("Enhanced input section with salary and fixed cost controls")
    
    # 1. PRODUCTION PARAMETERS (Collapsible)
    with st.expander("�� Production Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            number_of_nuts_day = st.number_input("Number of Nuts per Day", value=2500.0, min_value=0.0, step=1.0, help="Daily coconut processing capacity")
            per_nut_weight_factor = st.number_input("Per Nut Weight Factor", value=0.4, min_value=0.0, step=0.01, format="%.2f", help="Weight factor for coconut processing")
            months_working_year = st.number_input("Months Working in a Year", value=12.0, min_value=0.0, step=1.0, help="Annual working months")
        with col2:
            number_of_working_days_month = st.number_input("Working Days per Month", value=25.0, min_value=0.0, step=1.0, help="Monthly working days")
            number_of_litres_day = st.number_input("Number of Litres per Day", value=175.0, min_value=0.0, step=1.0, help="Daily oil production capacity")
    
    # 2. SALARY & WAGES (Collapsible)
    with st.expander("💰 Salary & Wages", expanded=False):
        st.subheader("Skilled Workers")
        col1, col2 = st.columns(2)
        with col1:
            skilled_wages_month = st.number_input("Skilled Wages per Month (₹)", value=25000.0, min_value=0.0, step=1000.0, help="Monthly salary for skilled workers")
        with col2:
            number_of_skilled = st.number_input("Number of Skilled Workers", value=1, min_value=0, step=1, help="Total skilled workforce")
        
        st.subheader("Semi-Skilled Workers")
        col3, col4 = st.columns(2)
        with col3:
            semi_skilled_wages_salary_month = st.number_input("Semi-Skilled Wages per Month (₹)", value=15000.0, min_value=0.0, step=1000.0, help="Monthly salary for semi-skilled workers")
        with col4:
            number_of_semi_skilled = st.number_input("Number of Semi-Skilled Workers", value=10, min_value=0, step=1, help="Total semi-skilled workforce")
        
        # Calculate total annual wages
        total_skilled_annual = skilled_wages_month * 12 * number_of_skilled
        total_semi_skilled_annual = semi_skilled_wages_salary_month * 12 * number_of_semi_skilled
        total_annual_wages = total_skilled_annual + total_semi_skilled_annual
        
        st.metric("Total Annual Wages (₹)", f"{total_annual_wages:,.2f}")
    
    # 3. FIXED COSTS (Collapsible)
    with st.expander("�� Fixed Costs & Overheads", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            maintenance_and_expenses = st.number_input("Maintenance & Expenses (₹)", value=1800000.0, min_value=0.0, step=10000.0, help="Annual maintenance costs")
            interest_on_loan = st.number_input("Interest on Loan (₹)", value=245000.0, min_value=0.0, step=1000.0, help="Annual interest payments")
        with col2:
            depreciation_on_fixed_asset = st.number_input("Depreciation on Fixed Assets (₹)", value=407000.0, min_value=0.0, step=1000.0, help="Annual depreciation")
            miscellaneous_expenses = st.number_input("Miscellaneous Expenses (₹)", value=50000.0, min_value=0.0, step=1000.0, help="Other annual expenses")
        
        # Calculate total fixed costs
        total_fixed_costs = maintenance_and_expenses + interest_on_loan + depreciation_on_fixed_asset + miscellaneous_expenses
        st.metric("Total Fixed Costs (₹)", f"{total_fixed_costs:,.2f}")

    # Source coconut price from your existing sidebar input
    coconut_procurement_price_from_fig = coconut_procurement_price

    # Calculate metrics
    metrics = compute_msme_aif_pmfme_metrics(
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

    # Key Metrics Display
    st.subheader("�� Key Performance Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue Collected (₹)", f"{metrics['total_revenue_collected']:,.2f}")
    c2.metric("Fixed Cost (₹)", f"{metrics['fixed_cost']:,.2f}")
    c3.metric("Contribution (₹)", f"{metrics['contribution']:,.2f}")

    c4, c5 = st.columns(2)
    c4.metric("Break-even Point (%)", f"{metrics['break_even_point_percentage']:.2f}%")
    c5.metric("Break-even Point (Sales, ₹)", f"{metrics['break_even_point_sales']:,.2f}")

    # Operating Expenses Breakdown
    st.subheader("💸 Operating Expenses (Annual)")
    st.dataframe({
        "Expense Category": [
            "Raw Material (Direct)",
            "Salaries and Wages",
            "Maintenance and Expenses",
            "Interest on Loan",
            "Depreciation on Fixed Asset",
            "Miscellaneous Expenses"
        ],
        "Amount (₹)": [
            f"{metrics['raw_material_direct_expenses']:,.2f}",
            f"{metrics['salaries_and_wages']:,.2f}",
            f"{metrics['maintenance_and_expenses']:,.2f}",
            f"{metrics['interest_on_loan']:,.2f}",
            f"{metrics['depreciation_on_fixed_asset']:,.2f}",
            f"{metrics['miscellaneous_expenses']:,.2f}",
        ]
    }, use_container_width=True)
