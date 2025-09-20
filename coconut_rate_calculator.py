import streamlit as st
import pandas as pd

class CoconutSupplyChainRateCalculator:
    def __init__(self):
        self.parameters = {
            'variant_name': '',
            'msme_purchase_price': 0.0,
            'label_packing': {
                'primary': 0.0,
                'secondary': 0.0,
                'tertiary': 0.0
            },
            'brand_percentage': 10.0,
            'branding_percentage': 10.0,
            'mrp_percentage': 5.0,
            'platform_charge_percentage': 30.0,
            'delivery_charge': 0.0,
            'gst_rate': 5.0
        }
    
    def set_variant_name(self, name):
        self.parameters['variant_name'] = name
    
    def set_msme_purchase_price(self, price):
        self.parameters['msme_purchase_price'] = price
    
    def set_label_packing_costs(self, primary=0, secondary=0, tertiary=0):
        self.parameters['label_packing'] = {
            'primary': primary,
            'secondary': secondary,
            'tertiary': tertiary
        }
    
    def set_delivery_charge(self, charge):
        self.parameters['delivery_charge'] = charge
    
    def set_gst_rate(self, rate):
        self.parameters['gst_rate'] = rate
    
    def calculate_brand_cost(self):
        return self.parameters['msme_purchase_price'] * (self.parameters['brand_percentage'] / 100)
    
    def calculate_branding_cost(self):
        return self.parameters['msme_purchase_price'] * (self.parameters['branding_percentage'] / 100)
    
    def calculate_mrp_cost(self):
        return self.parameters['msme_purchase_price'] * (self.parameters['mrp_percentage'] / 100)
    
    def calculate_platform_charge(self):
        return self.parameters['msme_purchase_price'] * (self.parameters['platform_charge_percentage'] / 100)
    
    def calculate_gst_on_total(self):
        base_cost = (self.parameters['msme_purchase_price'] + 
                    self.calculate_total_label_packing_cost() + 
                    self.calculate_brand_cost() + 
                    self.calculate_branding_cost() + 
                    self.calculate_mrp_cost() + 
                    self.calculate_platform_charge())
        return base_cost * (self.parameters['gst_rate'] / 100)
    
    def calculate_total_label_packing_cost(self):
        return (self.parameters['label_packing']['primary'] + 
                self.parameters['label_packing']['secondary'] + 
                self.parameters['label_packing']['tertiary'])
    
    def calculate_total_cost(self):
        msme_price = self.parameters['msme_purchase_price']
        
        costs = {
            'msme_purchase_price': msme_price,
            'label_packing_primary': self.parameters['label_packing']['primary'],
            'label_packing_secondary': self.parameters['label_packing']['secondary'],
            'label_packing_tertiary': self.parameters['label_packing']['tertiary'],
            'total_label_packing': self.calculate_total_label_packing_cost(),
            'brand_cost': self.calculate_brand_cost(),
            'branding_cost': self.calculate_branding_cost(),
            'mrp_cost': self.calculate_mrp_cost(),
            'platform_charge': self.calculate_platform_charge(),
            'gst_amount': self.calculate_gst_on_total(),
            'delivery_charge': self.parameters['delivery_charge']
        }
        
        costs['total_cost'] = (msme_price + 
                              costs['total_label_packing'] + 
                              costs['brand_cost'] + 
                              costs['branding_cost'] + 
                              costs['mrp_cost'] + 
                              costs['platform_charge'] + 
                              costs['gst_amount'] + 
                              costs['delivery_charge'])
        
        return costs

# Streamlit Dashboard
def main():
    st.set_page_config(
        page_title="Coconut Supply Chain Rate Calculator",
        page_icon="🥥",
        layout="wide"
    )
    
    st.title("�� Coconut Supply Chain Rate Calculator")
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
    
    msme_price = st.sidebar.number_input(
        "MSME Purchase Price (₹)", 
        min_value=0.0, 
        value=51.64, 
        step=0.01,
        help="Price Vidhathri pays to MSME"
    )
    
    st.sidebar.subheader("Label & Packing Costs (₹)")
    primary_packing = st.sidebar.number_input("Primary Packing", min_value=0.0, value=10.0, step=0.01)
    secondary_packing = st.sidebar.number_input("Secondary Packing", min_value=0.0, value=3.0, step=0.01)
    tertiary_packing = st.sidebar.number_input("Tertiary Packing", min_value=0.0, value=1.0, step=0.01)
    
    delivery_charge = st.sidebar.number_input(
        "Delivery Charge (₹)", 
        min_value=0.0, 
        value=10.0, 
        step=0.01,
        help="Delivery charge as per input provided"
    )
    
    gst_rate = st.sidebar.number_input(
        "GST Rate (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=5.0, 
        step=0.1,
        help="GST rate percentage"
    )
    
    # Set calculator parameters
    calculator.set_variant_name(variant_name)
    calculator.set_msme_purchase_price(msme_price)
    calculator.set_label_packing_costs(primary_packing, secondary_packing, tertiary_packing)
    calculator.set_delivery_charge(delivery_charge)
    calculator.set_gst_rate(gst_rate)
    
    # Calculate costs
    costs = calculator.calculate_total_cost()
    
    # Main dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"📊 Cost Breakdown - {variant_name}")
        
        # Create a nice data table
        cost_data = {
            'Cost Component': [
                'MSME Purchase Price (Base)',
                'Label & Packing (Primary)',
                'Label & Packing (Secondary)', 
                'Label & Packing (Tertiary)',
                'Total Label & Packing',
                'Brand Cost (10% of MSME price)',
                'Branding Cost (10% of MSME price)',
                'MRP Cost (5% of MSME price)',
                'Platform Charge (30% of MSME price)',
                f'GST ({gst_rate}% on base + charges)',
                'Delivery Charge'
            ],
            'Amount (₹)': [
                f"{costs['msme_purchase_price']:.2f}",
                f"{costs['label_packing_primary']:.2f}",
                f"{costs['label_packing_secondary']:.2f}",
                f"{costs['label_packing_tertiary']:.2f}",
                f"{costs['total_label_packing']:.2f}",
                f"{costs['brand_cost']:.2f}",
                f"{costs['branding_cost']:.2f}",
                f"{costs['mrp_cost']:.2f}",
                f"{costs['platform_charge']:.2f}",
                f"{costs['gst_amount']:.2f}",
                f"{costs['delivery_charge']:.2f}"
            ]
        }
        
        df = pd.DataFrame(cost_data)
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.header("�� Summary")
        
        # Key metrics
        st.metric("Total Cost per Unit", f"₹{costs['total_cost']:.2f}")
        st.metric("MSME Price", f"₹{costs['msme_purchase_price']:.2f}")
        st.metric("Vidhathri Markup", f"₹{costs['total_cost'] - costs['msme_purchase_price']:.2f}")
        
        # Percentage breakdown
        msme_percentage = (costs['msme_purchase_price'] / costs['total_cost']) * 100
        markup_percentage = ((costs['total_cost'] - costs['msme_purchase_price']) / costs['total_cost']) * 100
        
        st.metric("MSME Price % of Total", f"{msme_percentage:.1f}%")
        st.metric("Vidhathri Markup % of Total", f"{markup_percentage:.1f}%")
    
    # Additional insights
    st.header("📈 Cost Analysis")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.subheader("Cost Distribution")
        st.write(f"• Base Cost: ₹{costs['msme_purchase_price']:.2f}")
        st.write(f"• Packing: ₹{costs['total_label_packing']:.2f}")
        st.write(f"• Branding: ₹{costs['brand_cost'] + costs['branding_cost']:.2f}")
        st.write(f"• Platform: ₹{costs['platform_charge']:.2f}")
        st.write(f"• GST: ₹{costs['gst_amount']:.2f}")
        st.write(f"• Delivery: ₹{costs['delivery_charge']:.2f}")
    
    with col4:
        st.subheader("Key Ratios")
        st.write(f"• Brand Cost: {costs['brand_cost']/costs['msme_purchase_price']*100:.1f}% of MSME price")
        st.write(f"• Platform Charge: {costs['platform_charge']/costs['msme_purchase_price']*100:.1f}% of MSME price")
        st.write(f"• Total Markup: {(costs['total_cost'] - costs['msme_purchase_price'])/costs['msme_purchase_price']*100:.1f}% of MSME price")
    
    with col5:
        st.subheader("Quick Facts")
        st.write(f"• GST Rate: {gst_rate}%")
        st.write(f"• Total Components: 11")
        st.write(f"• Cost per ₹1 MSME: ₹{costs['total_cost']/costs['msme_purchase_price']:.2f}")
    
    # Export functionality
    st.header("📤 Export Results")
    
    if st.button("📋 Copy Results to Clipboard"):
        result_text = f"""
Coconut Supply Chain Rate Calculator Results
==========================================
Product: {variant_name}
MSME Purchase Price: ₹{costs['msme_purchase_price']:.2f}
Total Cost: ₹{costs['total_cost']:.2f}
Vidhathri Markup: ₹{costs['total_cost'] - costs['msme_purchase_price']:.2f}
GST Rate: {gst_rate}%
        """
        st.code(result_text)
        st.success("Results copied! You can now paste this in your WhatsApp group.")
    
    # Footer
    st.markdown("---")
    st.markdown("**Vidhathri Farmers Producer Company Limited** | Built with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
