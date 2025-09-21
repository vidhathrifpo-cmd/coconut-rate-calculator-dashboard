import streamlit as st
import pandas as pd

class CoconutSupplyChainRateCalculator:
    def __init__(self):
        self.parameters = {}
    
    def set_parameters(self, **kwargs):
        self.parameters.update(kwargs)
    
    def calculate_costs(self):
        # FIG to FIG Enterprise/MSME Supply Chain
        coconut_procurement_price = self.parameters['coconut_procurement_price']
        copra_making_percentage = self.parameters['copra_making_percentage']
        oil_making_percentage = self.parameters['oil_making_percentage']
        msme_gst_percentage = self.parameters['msme_gst_percentage']
        
        # Step 1: Copra Price
        copra_price = coconut_procurement_price / 0.3 * (1 + copra_making_percentage / 100)
        
        # Step 2: Oil MSME Landing Price Per Litre
        oil_msme_landing_price = copra_price / 0.6 * 0.91 * (1 + oil_making_percentage / 100)
        
        # Step 3: MSME Price (Inc of GST)
        msme_price = oil_msme_landing_price * (1 + msme_gst_percentage / 100)
        
        # FIG Enterprise/MSME Supply Chain to FPC
        primary_packing = self.parameters['primary_packing']
        secondary_packing = self.parameters['secondary_packing']
        tertiary_packing = self.parameters['tertiary_packing']
        brand_margin_percentage = self.parameters['brand_margin_percentage']
        branding_margin_percentage = self.parameters['branding_margin_percentage']
        
        # Oil Selling Price at Vidhathri FPC
        packing_total = primary_packing + secondary_packing + tertiary_packing
        oil_selling_price_at_fpc = (msme_price + packing_total) * (1 + brand_margin_percentage / 100) * (1 + branding_margin_percentage / 100)
        
        # Final calculation based on sales channel
        sales_channel = self.parameters['sales_channel']
        platform_charges_percentage = self.parameters['platform_charges_percentage']
        delivery_charge = self.parameters['delivery_charge']
        retail_margin_percentage = self.parameters['retail_margin_percentage']
        gst_percentage = self.parameters['gst_percentage']
        
        if sales_channel == "Online through VidhathriFFE":
            platform_charges = oil_selling_price_at_fpc * (platform_charges_percentage / 100)
            before_gst = oil_selling_price_at_fpc + platform_charges + delivery_charge
            final_price = before_gst * (1 + gst_percentage / 100)
        else:  # Offline
            # FIXED: Correct retail margin calculation
            retail_margin_amount = oil_selling_price_at_fpc * (retail_margin_percentage / 100)
            before_gst = oil_selling_price_at_fpc + retail_margin_amount
            final_price = before_gst * (1 + gst_percentage / 100)
        
        return {
            'coconut_procurement_price': coconut_procurement_price,
            'copra_price': copra_price,
            'oil_msme_landing_price': oil_msme_landing_price,
            'msme_price': msme_price,
            'oil_selling_price_at_fpc': oil_selling_price_at_fpc,
            'packing_total': packing_total,
            'brand_margin_amount': oil_selling_price_at_fpc * (brand_margin_percentage / 100),
            'branding_margin_amount': oil_selling_price_at_fpc * (branding_margin_percentage / 100),
            'platform_charges': platform_charges if sales_channel == "Online through VidhathriFFE" else 0,
            'delivery_charge': delivery_charge if sales_channel == "Online through VidhathriFFE" else 0,
            'retail_margin_amount': retail_margin_amount if sales_channel == "Offline" else 0,
            'before_gst': before_gst,
            'gst_amount': final_price - before_gst,
            'final_price': final_price
        }

def main():
    st.set_page_config(page_title="Coconut Supply Chain Rate Calculator", layout="wide")
    
    st.title(" Coconut Supply Chain Rate Calculator")
    st.subheader("Vidhathri Farmers Producer Company Limited")
    
    # Create calculator instance
    calculator = CoconutSupplyChainRateCalculator()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📝 Input Parameters")
        
        # Basic Parameters
        variant_name = st.text_input("Variant Name", value="Health Care and Wellness Oil 100 ml")
        
        # FIG to FIG Enterprise/MSME Supply Chain
        st.subheader("FIG to MSME Supply Chain")
        coconut_procurement_price = st.number_input("Coconut Procurement Price from FIG to Vidhathri", value=51.64, min_value=0.0, step=0.01)
        copra_making_percentage = st.number_input("Copra Making Charges in Percentage", value=10.0, min_value=0.0, step=0.1)
        oil_making_percentage = st.number_input("Oil Making Charges in Percentage", value=10.0, min_value=0.0, step=0.1)
        msme_gst_percentage = st.number_input("MSME GST Percentage", value=5.0, min_value=0.0, step=0.1)
        
        # FPC Additional Costs
        st.subheader("FPC Additional Costs")
        primary_packing = st.number_input("Primary Packing Charges", value=10.0, min_value=0.0, step=0.01)
        secondary_packing = st.number_input("Secondary Packing Charges", value=3.0, min_value=0.0, step=0.01)
        tertiary_packing = st.number_input("Tertiary Packing Charges", value=1.0, min_value=0.0, step=0.01)
        brand_margin_percentage = st.number_input("Brand Margin Percentage", value=10.0, min_value=0.0, step=0.1)
        branding_margin_percentage = st.number_input("Branding Margin Percentage", value=10.0, min_value=0.0, step=0.1)
        
        # Sales Channel and Final Pricing
        st.subheader("Sales Channel & Final Pricing")
        sales_channel = st.selectbox("Sales Channel", ["Online through VidhathriFFE", "Offline"])
        
        if sales_channel == "Online through VidhathriFFE":
            platform_charges_percentage = st.number_input("Platform Charges in Percentage", value=30.0, min_value=0.0, step=0.1)
            delivery_charge = st.number_input("Delivery Charges", value=10.0, min_value=0.0, step=0.01)
        else:  # Offline
            platform_charges_percentage = 0
            delivery_charge = 0
            retail_margin_percentage = st.number_input("Retail Margin Percentage", value=20.0, min_value=0.0, step=0.1)
        
        gst_percentage = st.number_input("Vidhathri GST Percentage", value=5.0, min_value=0.0, step=0.1)
    
    # Set parameters
    calculator.set_parameters(
        variant_name=variant_name,
        coconut_procurement_price=coconut_procurement_price,
        copra_making_percentage=copra_making_percentage,
        oil_making_percentage=oil_making_percentage,
        msme_gst_percentage=msme_gst_percentage,
        primary_packing=primary_packing,
        secondary_packing=secondary_packing,
        tertiary_packing=tertiary_packing,
        brand_margin_percentage=brand_margin_percentage,
        branding_margin_percentage=branding_margin_percentage,
        sales_channel=sales_channel,
        platform_charges_percentage=platform_charges_percentage,
        delivery_charge=delivery_charge,
        retail_margin_percentage=retail_margin_percentage if sales_channel == "Offline" else 0,
        gst_percentage=gst_percentage
    )
    
    # Calculate costs
    costs = calculator.calculate_costs()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # FIG to FIG Enterprise/MSME Supply Chain
        st.subheader("FIG to FIG Enterprise/MSME Supply Chain")
        msme_steps = {
            'Step': [
                'Coconut Procurement Price from FIG to Vidhathri',
                'Copra Price',
                'Oil MSME Landing Price Per Litre',
                'MSME Price(Inc of GST)'
            ],
            'Value (₹)': [
                f"{costs['coconut_procurement_price']:.2f}",
                f"{costs['copra_price']:.2f}",
                f"{costs['oil_msme_landing_price']:.2f}",
                f"{costs['msme_price']:.2f}"
            ]
        }
        st.dataframe(msme_steps, use_container_width=True)
        
        # FPC Selling Price - Simplified section
        st.subheader("FPC Selling Price")
        if sales_channel == "Online through VidhathriFFE":
            fpc_selling_price = {
                'Step': [
                    'FPC Selling Price',
                    'Platform Charges',
                    'Delivery Charges',
                    'Before GST',
                    'GST Amount',
                    'Final Price'
                ],
                'Value (₹)': [
                    f"{costs['oil_selling_price_at_fpc']:.2f}",
                    f"{costs['platform_charges']:.2f}",
                    f"{costs['delivery_charge']:.2f}",
                    f"{costs['before_gst']:.2f}",
                    f"{costs['gst_amount']:.2f}",
                    f"{costs['final_price']:.2f}"
                ]
            }
        else:  # Offline
            fpc_selling_price = {
                'Step': [
                    'FPC Selling Price',
                    'Retail Margin',
                    'Before GST',
                    'GST Amount',
                    'Final Price'
                ],
                'Value (₹)': [
                    f"{costs['oil_selling_price_at_fpc']:.2f}",
                    f"{costs['retail_margin_amount']:.2f}",
                    f"{costs['before_gst']:.2f}",
                    f"{costs['gst_amount']:.2f}",
                    f"{costs['final_price']:.2f}"
                ]
            }
        st.dataframe(fpc_selling_price, use_container_width=True)
    
    with col2:
        # Summary
        st.subheader("📊 Summary")
        st.metric("Variant Name", variant_name)
        st.metric("Sales Channel", sales_channel)
        st.metric("Final Price", f"₹{costs['final_price']:.2f}")
        
        # Export functionality
        st.subheader("📤 Export")
        if st.button("Export to CSV"):
            # Create summary data
            summary_data = {
                'Parameter': [
                    'Variant Name',
                    'Coconut Procurement Price',
                    'Copra Making %',
                    'Oil Making %',
                    'MSME GST %',
                    'Primary Packing',
                    'Secondary Packing',
                    'Tertiary Packing',
                    'Brand Margin %',
                    'Branding Margin %',
                    'Sales Channel',
                    'Platform Charges %' if sales_channel == "Online through VidhathriFFE" else 'Retail Margin %',
                    'Delivery Charges' if sales_channel == "Online through VidhathriFFE" else 'N/A',
                    'Vidhathri GST %',
                    'Final Price'
                ],
                'Value': [
                    variant_name,
                    f"{coconut_procurement_price:.2f}",
                    f"{copra_making_percentage:.1f}%",
                    f"{oil_making_percentage:.1f}%",
                    f"{msme_gst_percentage:.1f}%",
                    f"{primary_packing:.2f}",
                    f"{secondary_packing:.2f}",
                    f"{tertiary_packing:.2f}",
                    f"{brand_margin_percentage:.1f}%",
                    f"{branding_margin_percentage:.1f}%",
                    sales_channel,
                    f"{platform_charges_percentage:.1f}%" if sales_channel == "Online through VidhathriFFE" else f"{retail_margin_percentage:.1f}%",
                    f"{delivery_charge:.2f}" if sales_channel == "Online through VidhathriFFE" else "N/A",
                    f"{gst_percentage:.1f}%",
                    f"{costs['final_price']:.2f}"
                ]
            }
            
            df = pd.DataFrame(summary_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"coconut_calculator_{variant_name.replace(' ', '_')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
