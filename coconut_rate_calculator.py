import streamlit as st
import pandas as pd

class CoconutSupplyChainRateCalculator:
    def __init__(self):
        self.parameters = {
            'variant_name': '',
            'coconut_market_rate': 0.0,
            'fpc_support_price': 0.0,
            'coconut_procurement_price': 0.0,
            'copra_making_charges_percentage': 0.0,
            'oil_making_charges_percentage': 0.0,
            'msme_gst_percentage': 0.0,
            'label_packing': {
                'primary': 0.0,
                'secondary': 0.0,
                'tertiary': 0.0
            },
            'brand_margin_percentage': 0.0,
            'branding_margin_percentage': 0.0,
            'platform_charges_percentage': 0.0,
            'retail_margin_percentage': 0.0,
            'delivery_charges': 0.0,
            'gst_percentage': 5.0,
            'sales_channel': 'Online'
        }
    
    def set_variant_name(self, name):
        self.parameters['variant_name'] = name
    
    def set_coconut_inputs(self, coconut_market_rate, fpc_support_price, coconut_procurement_price, 
                          copra_making_charges_percentage, oil_making_charges_percentage, msme_gst_percentage):
        self.parameters['coconut_market_rate'] = coconut_market_rate
        self.parameters['fpc_support_price'] = fpc_support_price
        self.parameters['coconut_procurement_price'] = coconut_procurement_price
        self.parameters['copra_making_charges_percentage'] = copra_making_charges_percentage
        self.parameters['oil_making_charges_percentage'] = oil_making_charges_percentage
        self.parameters['msme_gst_percentage'] = msme_gst_percentage
    
    def set_label_packing_costs(self, primary=0, secondary=0, tertiary=0):
        self.parameters['label_packing'] = {
            'primary': primary,
            'secondary': secondary,
            'tertiary': tertiary
        }
    
    def set_margin_percentages(self, brand_margin, branding_margin, platform_charges, retail_margin):
        self.parameters['brand_margin_percentage'] = brand_margin
        self.parameters['branding_margin_percentage'] = branding_margin
        self.parameters['platform_charges_percentage'] = platform_charges
        self.parameters['retail_margin_percentage'] = retail_margin
    
    def set_delivery_charges(self, charges):
        self.parameters['delivery_charges'] = charges
    
    def set_gst_percentage(self, percentage):
        self.parameters['gst_percentage'] = percentage
    
    def set_sales_channel(self, channel):
        self.parameters['sales_channel'] = channel
    
    def calculate_msme_price(self):
        """Calculate MSME price using the new formula"""
        # Step 1: Copra Price = Coconut Procurement Price from FIG to Vidhathri × 0.3 × Copra Making Charges in Percentage
        copra_price = self.parameters['coconut_procurement_price'] * 0.3 * (self.parameters['copra_making_charges_percentage'] / 100)
        
        # Step 2: Oil MSME Landing Price Per Litre = Copra Price × 0.6 × 0.91 × Oil Making Charges in Percentage/100
        oil_msme_landing_price = copra_price * 0.6 * 0.91 * (self.parameters['oil_making_charges_percentage'] / 100)
        
        # Step 3: MSME Price(Inc of GST) = Oil MSME Landing Price Per Litre × MSME GST Percentage/100
        msme_price = oil_msme_landing_price * (self.parameters['msme_gst_percentage'] / 100)
        
        return {
            'copra_price': copra_price,
            'oil_msme_landing_price': oil_msme_landing_price,
            'msme_price': msme_price
        }
    
    def calculate_oil_selling_price_at_fpc(self):
        """Calculate Oil Selling Price at Vidhathri FPC"""
        msme_calculation = self.calculate_msme_price()
        msme_price = msme_calculation['msme_price']
        
        # Step 1: new_value = MSME Price + Primary + Secondary + Tertiary Packing Charges
        new_value = (msme_price + 
                    self.parameters['label_packing']['primary'] + 
                    self.parameters['label_packing']['secondary'] + 
                    self.parameters['label_packing']['tertiary'])
        
        # Step 2: new_value = new_value + new_value × Brand Margin/100
        new_value = new_value + (new_value * self.parameters['brand_margin_percentage'] / 100)
        
        # Step 3: Oil Selling Price at Vidhathri FPC = new_value + new_value × Branding Margin/100
        oil_selling_price_at_fpc = new_value + (new_value * self.parameters['branding_margin_percentage'] / 100)
        
        return {
            'step1_value': msme_price + self.parameters['label_packing']['primary'] + self.parameters['label_packing']['secondary'] + self.parameters['label_packing']['tertiary'],
            'step2_value': new_value,
            'oil_selling_price_at_fpc': oil_selling_price_at_fpc
        }
    
    def calculate_final_price(self):
        """Calculate final price based on sales channel"""
        fpc_calculation = self.calculate_oil_selling_price_at_fpc()
        oil_selling_price_at_fpc = fpc_calculation['oil_selling_price_at_fpc']
        
        if self.parameters['sales_channel'] == 'Online':
            # Online through VidhathriFFE
            platform_charge = oil_selling_price_at_fpc * (self.parameters['platform_charges_percentage'] / 100)
            before_gst = platform_charge + self.parameters['delivery_charges']
            final_price = before_gst * (self.parameters['gst_percentage'] / 100)
            
            return {
                'platform_charge': platform_charge,
                'before_gst': before_gst,
                'final_price': final_price,
                'channel': 'Online'
            }
        else:
            # Offline
            retail_margin = oil_selling_price_at_fpc * (self.parameters['retail_margin_percentage'] / 100)
            before_gst = retail_margin
            final_price = before_gst * (self.parameters['gst_percentage'] / 100)
            
            return {
                'retail_margin': retail_margin,
                'before_gst': before_gst,
                'final_price': final_price,
                'channel': 'Offline'
            }
    
    def calculate_total_cost(self):
        msme_calculation = self.calculate_msme_price()
        fpc_calculation = self.calculate_oil_selling_price_at_fpc()
        final_calculation = self.calculate_final_price()
        
        costs = {
            'coconut_market_rate': self.parameters['coconut_market_rate'],
            'fpc_support_price': self.parameters['fpc_support_price'],
            'coconut_procurement_price': self.parameters['coconut_procurement_price'],
            'copra_price': msme_calculation['copra_price'],
            'oil_msme_landing_price': msme_calculation['oil_msme_landing_price'],
            'msme_price': msme_calculation['msme_price'],
            'label_packing_primary': self.parameters['label_packing']['primary'],
            'label_packing_secondary': self.parameters['label_packing']['secondary'],
            'label_packing_tertiary': self.parameters['label_packing']['tertiary'],
            'total_label_packing': (self.parameters['label_packing']['primary'] + 
                                  self.parameters['label_packing']['secondary'] + 
                                  self.parameters['label_packing']['tertiary']),
            'step1_value': fpc_calculation['step1_value'],
            'step2_value': fpc_calculation['step2_value'],
            'oil_selling_price_at_fpc': fpc_calculation['oil_selling_price_at_fpc'],
            'brand_margin_percentage': self.parameters['brand_margin_percentage'],
            'branding_margin_percentage': self.parameters['branding_margin_percentage'],
            'platform_charges_percentage': self.parameters['platform_charges_percentage'],
            'retail_margin_percentage': self.parameters['retail_margin_percentage'],
            'delivery_charges': self.parameters['delivery_charges'],
            'gst_percentage': self.parameters['gst_percentage'],
            'sales_channel': self.parameters['sales_channel']
        }
        
        # Add final calculation results
        costs.update(final_calculation)
        
        return costs

# Streamlit Dashboard
def main():
    st.set_page_config(
        page_title="Coconut Supply Chain Rate Calculator",
        page_icon="🥥",
        layout="wide"
    )
    
    st.title(" Coconut Supply Chain Rate Calculator")
    st.subheader("Vidhathri Farmers Producer Company Limited")
    
    # Create calculator instance
    calculator = CoconutSupplyChainRateCalculator()
    
    # Sidebar for inputs
    st.sidebar.header("📝 Input Parameters")
    
    # Input fields
    variant_name = st.sidebar.text_input(
        "Variant Name", 
        value="Health Care and Wellness Oil 100 ml",
        help="Enter the product variant name"
    )
    
    st.sidebar.subheader("🥥 Coconut Processing Inputs")
    coconut_market_rate = st.sidebar.number_input(
        "Coconut Market Rate (₹)", 
        min_value=0.0, 
        value=10.0, 
        step=0.01,
        help="Base coconut market rate"
    )
    
    fpc_support_price = st.sidebar.number_input(
        "FPC Support Price to FPC/FIG Members (₹)", 
        min_value=0.0, 
        value=2.0, 
        step=0.01,
        help="Support price paid to FPC/FIG members"
    )
    
    coconut_procurement_price = st.sidebar.number_input(
        "Coconut Procurement Price from FIG to Vidhathri (₹)", 
        min_value=0.0, 
        value=1.0, 
        step=0.01,
        help="Procurement price from FIG to Vidhathri"
    )
    
    copra_making_charges_percentage = st.sidebar.number_input(
        "Copra Making Charges in Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=80.0, 
        step=0.1,
        help="Percentage charges for copra making"
    )
    
    oil_making_charges_percentage = st.sidebar.number_input(
        "Oil Making Charges in Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=70.0, 
        step=0.1,
        help="Percentage charges for oil making"
    )
    
    msme_gst_percentage = st.sidebar.number_input(
        "MSME GST Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=5.0, 
        step=0.1,
        help="GST percentage for MSME"
    )
    
    st.sidebar.subheader(" Vidhathri Additional Costs")
    
    st.sidebar.subheader("Label & Packing Costs (₹)")
    primary_packing = st.sidebar.number_input("Primary Packing Charges", min_value=0.0, value=10.0, step=0.01)
    secondary_packing = st.sidebar.number_input("Secondary Packing Charges", min_value=0.0, value=3.0, step=0.01)
    tertiary_packing = st.sidebar.number_input("Tertiary Packing Charges", min_value=0.0, value=1.0, step=0.01)
    
    st.sidebar.subheader("Margin Percentages (%)")
    brand_margin_percentage = st.sidebar.number_input(
        "Brand Margin Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=10.0, 
        step=0.1,
        help="Brand margin percentage"
    )
    
    branding_margin_percentage = st.sidebar.number_input(
        "Branding Margin Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=10.0, 
        step=0.1,
        help="Branding margin percentage"
    )
    
    platform_charges_percentage = st.sidebar.number_input(
        "Platform Charges in Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=30.0, 
        step=0.1,
        help="Platform charges percentage for online sales"
    )
    
    retail_margin_percentage = st.sidebar.number_input(
        "Retail Margin Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=20.0, 
        step=0.1,
        help="Retail margin percentage for offline sales"
    )
    
    delivery_charges = st.sidebar.number_input(
        "Delivery Charges (₹)", 
        min_value=0.0, 
        value=10.0, 
        step=0.01,
        help="Delivery charges as per input provided"
    )
    
    gst_percentage = st.sidebar.number_input(
        "Vidhathri GST Percentage (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=5.0, 
        step=0.1,
        help="GST percentage for Vidhathri"
    )
    
    st.sidebar.subheader("Sales Channel")
    sales_channel = st.sidebar.selectbox(
        "Select Sales Channel",
        ["Online", "Offline"],
        help="Choose between Online (VidhathriFFE) or Offline sales"
    )
    
    # Set calculator parameters
    calculator.set_variant_name(variant_name)
    calculator.set_coconut_inputs(coconut_market_rate, fpc_support_price, coconut_procurement_price, 
                                 copra_making_charges_percentage, oil_making_charges_percentage, msme_gst_percentage)
    calculator.set_label_packing_costs(primary_packing, secondary_packing, tertiary_packing)
    calculator.set_margin_percentages(brand_margin_percentage, branding_margin_percentage, 
                                     platform_charges_percentage, retail_margin_percentage)
    calculator.set_delivery_charges(delivery_charges)
    calculator.set_gst_percentage(gst_percentage)
    calculator.set_sales_channel(sales_channel)
    
    # Calculate costs
    costs = calculator.calculate_total_cost()
    
    # Main dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"📊 Cost Breakdown - {variant_name}")
        
        # FIG to FIG Enterprise/MSME Supply Chain
        st.subheader("�� FIG to FIG Enterprise/MSME Supply Chain")
        msme_steps = {
            'Step': [
                'Coconut Procurement Price from FIG to Vidhathri',
                'Copra Price = Procurement Price × 0.3 × Copra Making Charges %',
                'Oil MSME Landing Price Per Litre = Copra Price × 0.6 × 0.91 × Oil Making Charges %',
                'MSME Price(Inc of GST) = Oil Landing Price × MSME GST %'
            ],
            'Value (₹)': [
                f"{costs['coconut_procurement_price']:.2f}",
                f"{costs['copra_price']:.2f}",
                f"{costs['oil_msme_landing_price']:.2f}",
                f"{costs['msme_price']:.2f}"
            ]
        }
        
        df_msme = pd.DataFrame(msme_steps)
        st.dataframe(df_msme, use_container_width=True)
        
        # FIG Enterprise/MSME Supply Chain to FPC
        st.subheader(" FPC Additional Costs")
        fpc_steps = {
            'Step': [
                'MSME Price + Packing Charges',
                'Step 1 + Brand Margin %',
                'Step 2 + Branding Margin %',
                'Oil Selling Price at Vidhathri FPC'
            ],
            'Value (₹)': [
                f"{costs['step1_value']:.2f}",
                f"{costs['step2_value']:.2f}",
                f"{costs['oil_selling_price_at_fpc']:.2f}",
                f"{costs['oil_selling_price_at_fpc']:.2f}"
            ]
        }
        
        df_fpc = pd.DataFrame(fpc_steps)
        st.dataframe(df_fpc, use_container_width=True)
        
        # Final Price Calculation
        st.subheader(f"�� Final Price Calculation - {sales_channel} Sales")
        if sales_channel == 'Online':
            final_steps = {
                'Step': [
                    'Oil Selling Price at Vidhathri FPC',
                    'Platform Charge = FPC Price × Platform Charges %',
                    'Platform Charge + Delivery Charges',
                    f'Final Price = Above × Vidhathri GST {gst_percentage}%'
                ],
                'Value (₹)': [
                    f"{costs['oil_selling_price_at_fpc']:.2f}",
                    f"{costs['platform_charge']:.2f}",
                    f"{costs['before_gst']:.2f}",
                    f"{costs['final_price']:.2f}"
                ]
            }
        else:
            final_steps = {
                'Step': [
                    'Oil Selling Price at Vidhathri FPC',
                    'Retail Margin = FPC Price × Retail Margin %',
                    f'Final Price = Retail Margin × Vidhathri GST {gst_percentage}%'
                ],
                'Value (₹)': [
                    f"{costs['oil_selling_price_at_fpc']:.2f}",
                    f"{costs['retail_margin']:.2f}",
                    f"{costs['final_price']:.2f}"
                ]
            }
        
        df_final = pd.DataFrame(final_steps)
        st.dataframe(df_final, use_container_width=True)
    
    with col2:
        st.header(" Summary")
        
        # Key metrics
        st.metric("Final Price", f"₹{costs['final_price']:.2f}")
        st.metric("MSME Price", f"₹{costs['msme_price']:.2f}")
        st.metric("FPC Price", f"₹{costs['oil_selling_price_at_fpc']:.2f}")
        st.metric("Sales Channel", f"{sales_channel}")
        
        # Percentage breakdown
        msme_percentage = (costs['msme_price'] / costs['final_price']) * 100
        fpc_percentage = (costs['oil_selling_price_at_fpc'] / costs['final_price']) * 100
        
        st.metric("MSME Price % of Final", f"{msme_percentage:.1f}%")
        st.metric("FPC Price % of Final", f"{fpc_percentage:.1f}%")
    
    # Additional insights
    st.header("📈 Cost Analysis")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("Cost Distribution")
        st.write(f"• MSME Price: ₹{costs['msme_price']:.2f}")
        st.write(f"• Packing: ₹{costs['total_label_packing']:.2f}")
        st.write(f"• Brand Margin: {brand_margin_percentage}%")
        st.write(f"• Branding Margin: {branding_margin_percentage}%")
        if sales_channel == 'Online':
            st.write(f"• Platform Charge: {platform_charges_percentage}%")
        else:
            st.write(f"• Retail Margin: {retail_margin_percentage}%")
        st.write(f"• GST: {gst_percentage}%")
    
    with col4:
        st.subheader("Key Ratios")
        st.write(f"• Brand Margin: {brand_margin_percentage}%")
        st.write(f"• Branding Margin: {branding_margin_percentage}%")
        if sales_channel == 'Online':
            st.write(f"• Platform Charge: {platform_charges_percentage}%")
        else:
            st.write(f"• Retail Margin: {retail_margin_percentage}%")
        st.write(f"• Total Markup: {(costs['final_price'] - costs['msme_price'])/costs['msme_price']*100:.1f}% of MSME price")
    
    with col5:
        st.subheader("Quick Facts")
        st.write(f"• Sales Channel: {sales_channel}")
        st.write(f"• GST Rate: {gst_percentage}%")
        st.write(f"• Total Components: 8")
        st.write(f"• Cost per ₹1 MSME: ₹{costs['final_price']/costs['msme_price']:.2f}")
    
    # Export functionality
    st.header("📤 Export Results")
    
    if st.button("📋 Copy Results to Clipboard"):
        result_text = f"""
Coconut Supply Chain Rate Calculator Results
==========================================
Product: {variant_name}
Sales Channel: {sales_channel}
MSME Price: ₹{costs['msme_price']:.2f}
FPC Price: ₹{costs['oil_selling_price_at_fpc']:.2f}
Final Price: ₹{costs['final_price']:.2f}
GST Rate: {gst_percentage}%
        """
        st.code(result_text)
        st.success("Results copied! You can now paste this in your WhatsApp group.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Vidhathri Farmers Producer Company Limited** | Built with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
