import streamlit as st
import pandas as pd
import json
from math import pi

st.set_page_config(
    page_title="Smart Unit Converter Of Haider",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .formula-box {
        background-color: #fffde7;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffd54f;
        margin: 10px 0;
    }
    .stSelectbox, .stNumberInput {
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #757575;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


conversion_data = {
    "Length": {
        "Metre": 1.0,
        "Kilometre": 1000.0,
        "Centimetre": 0.01,
        "Millimetre": 0.001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
        "Nautical Mile": 1852.0
    },
    "Weight/Mass": {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Metric Ton": 1000.0,
        "Pound": 0.453592,
        "Ounce": 0.0283495,
        "Stone": 6.35029
    },
    "Volume": {
        "Cubic Metre": 1.0,
        "Litre": 0.001,
        "Millilitre": 0.000001,
        "Gallon (US)": 0.00378541,
        "Gallon (UK)": 0.00454609,
        "Quart": 0.000946353,
        "Pint": 0.000473176,
        "Cup": 0.000236588,
        "Fluid Ounce": 0.0000295735
    },
    "Temperature": {
        "Celsius": "base",
        "Fahrenheit": "special",
        "Kelvin": "special"
    },
    "Area": {
        "Square Metre": 1.0,
        "Square Kilometre": 1000000.0,
        "Square Centimetre": 0.0001,
        "Square Millimetre": 0.000001,
        "Square Mile": 2589988.11,
        "Square Yard": 0.836127,
        "Square Foot": 0.092903,
        "Square Inch": 0.00064516,
        "Acre": 4046.86,
        "Hectare": 10000.0
    },
    "Time": {
        "Second": 1.0,
        "Minute": 60.0,
        "Hour": 3600.0,
        "Day": 86400.0,
        "Week": 604800.0,
        "Month (30 days)": 2592000.0,
        "Year (365 days)": 31536000.0
    },
    "Speed": {
        "Metre per second": 1.0,
        "Kilometre per hour": 0.277778,
        "Mile per hour": 0.44704,
        "Knot": 0.514444,
        "Foot per second": 0.3048
    },
    "Pressure": {
        "Pascal": 1.0,
        "Kilopascal": 1000.0,
        "Bar": 100000.0,
        "PSI": 6894.76,
        "Atmosphere": 101325.0,
        "Millimetre of Mercury": 133.322
    },
    "Energy": {
        "Joule": 1.0,
        "Kilojoule": 1000.0,
        "Calorie": 4.184,
        "Kilocalorie": 4184.0,
        "Watt-hour": 3600.0,
        "Kilowatt-hour": 3600000.0,
        "Electronvolt": 1.602176634e-19,
        "British Thermal Unit": 1055.06
    },
    "Data": {
        "Bit": 1.0,
        "Byte": 8.0,
        "Kilobit": 1000.0,
        "Kilobyte": 8000.0,
        "Megabit": 1000000.0,
        "Megabyte": 8000000.0,
        "Gigabit": 1000000000.0,
        "Gigabyte": 8000000000.0,
        "Terabit": 1000000000000.0,
        "Terabyte": 8000000000000.0
    },
    "Angle": {
        "Degree": 1.0,
        "Radian": 57.2958,
        "Gradian": 0.9,
        "Minute of Arc": 0.0166667,
        "Second of Arc": 0.000277778
    }
}

def temp_convert(value, from_unit, to_unit):
    
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15

    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15

def get_formula(category, from_unit, to_unit, value=None, result=None):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return f"({value}°C × 9/5) + 32 = {result}°F"
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return f"{value}°C + 273.15 = {result}K"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return f"({value}°F - 32) × 5/9 = {result}°C"
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return f"({value}°F - 32) × 5/9 + 273.15 = {result}K"
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return f"{value}K - 273.15 = {result}°C"
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return f"({value}K - 273.15) × 9/5 + 32 = {result}°F"
        elif from_unit == to_unit:
            return f"{value}{get_unit_symbol(from_unit)} = {result}{get_unit_symbol(to_unit)}"
    else:
        if from_unit == to_unit:
            return f"{value}{get_unit_symbol(from_unit)} = {result}{get_unit_symbol(to_unit)}"
        
        from_value = conversion_data[category][from_unit]
        to_value = conversion_data[category][to_unit]
        
        if from_value > to_value:
            factor = from_value / to_value
            return f"multiply the {from_unit.lower()} value by {factor}"
        else:
            factor = to_value / from_value
            return f"divide the {from_unit.lower()} value by {factor}"

def get_unit_symbol(unit):
    symbols = {
        "Metre": "m", "Kilometre": "km", "Centimetre": "cm", "Millimetre": "mm",
        "Mile": "mi", "Yard": "yd", "Foot": "ft", "Inch": "in",
        "Kilogram": "kg", "Gram": "g", "Milligram": "mg",
        "Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K",
        "Second": "s", "Minute": "min", "Hour": "h", "Day": "d",
        "Litre": "L", "Millilitre": "mL",
        "Square Metre": "m²", "Square Kilometre": "km²", "Square Centimetre": "cm²",
        "Metre per second": "m/s", "Kilometre per hour": "km/h", "Mile per hour": "mph",
        "Pascal": "Pa", "Kilopascal": "kPa", "Bar": "bar",
        "Joule": "J", "Kilojoule": "kJ", "Calorie": "cal", "Kilocalorie": "kcal",
        "Bit": "b", "Byte": "B", "Kilobyte": "KB", "Megabyte": "MB", "Gigabyte": "GB"
    }
    return symbols.get(unit, "")

def format_number(number):
    """Format numbers for better readability"""
    if number == 0:
        return "0"
    elif abs(number) < 0.001 or abs(number) >= 1000000:
        return f"{number:.6e}"
    elif abs(number) < 0.01:
        return f"{number:.6f}"
    elif abs(number) < 0.1:
        return f"{number:.5f}"
    elif abs(number) < 1:
        return f"{number:.4f}"
    elif abs(number) < 10:
        return f"{number:.3f}"
    elif abs(number) < 100:
        return f"{number:.2f}"
    else:
        return f"{number:.1f}"

st.markdown('<h1 class="main-header">🔄 Smart Unit Converter</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">Convert between different units of measurement with ease</p>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

category = st.selectbox("Select Category", list(conversion_data.keys()))

col1, col2 = st.columns(2)

with col1:
    st.subheader("From")
    from_unit = st.selectbox("From Unit", list(conversion_data[category].keys()), key="from_unit")
    input_value = st.number_input("Enter Value", value=1.0, format="%.6f", step=0.1)

with col2:
    st.subheader("To")
    to_unit = st.selectbox("To Unit", list(conversion_data[category].keys()), key="to_unit")

if category == "Temperature" and (from_unit != to_unit):
    result = temp_convert(input_value, from_unit, to_unit)
else:
    if from_unit == to_unit:
        result = input_value
    else:
        from_factor = conversion_data[category][from_unit]
        to_factor = conversion_data[category][to_unit]
        if from_factor != "base" and to_factor != "base":
            result = input_value * (from_factor / to_factor)

st.markdown('<h2 class="sub-header" style="text-align: center; margin-top: 20px;">Result</h2>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align: center; font-size: 1.8rem; background-color: #e3f2fd; padding: 15px; border-radius: 10px;">{input_value} {from_unit} = <span style="color: #1E88E5; font-weight: bold;">{format_number(result)} {to_unit}</span></div>', unsafe_allow_html=True)

formula = get_formula(category, from_unit, to_unit, input_value, format_number(result))
st.markdown('<div class="formula-box">', unsafe_allow_html=True)
st.markdown('<span style="font-weight: bold;">Formula:</span>', unsafe_allow_html=True)
st.markdown(f'<span>{formula}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📊 View Conversion Table"):
    if category != "Temperature": 
        units = list(conversion_data[category].keys())
        if len(units) > 1:
            base_value = 1.0 
            conversions = []
            for unit in units:
                if unit != from_unit:
                    if category == "Temperature":
                        converted = temp_convert(base_value, from_unit, unit)
                    else:
                        from_factor = conversion_data[category][from_unit]
                        to_factor = conversion_data[category][unit]
                        converted = base_value * (from_factor / to_factor)
                    
                    conversions.append({
                        "Unit": unit,
                        f"Value (for 1 {from_unit})": format_number(converted)
                    })
            
          
            if conversions:
                conversion_df = pd.DataFrame(conversions)
                st.table(conversion_df)


with st.expander("💡 Tips and Examples"):
    st.markdown("""
    ### Common Conversions:
    
    - 1 meter = 100 centimeters = 3.28 feet
    - 1 kilogram = 1000 grams = 2.20 pounds
    - 1 liter = 1000 milliliters = 0.26 US gallons
    - Water freezes at 0°C = 32°F = 273.15K
    
    ### Tips:
    
    - For precision measurements, use scientific units (meters, kilograms)
    - For recipes, common units are cups, tablespoons, and teaspoons
    - For DIY projects, inches and feet are often used in the US
    """)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">More Features</h2>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Bulk Conversion", "Common Equivalents"])

with tab1:
    st.markdown("""
    ### Convert Multiple Values at Once
    
    Enter multiple values separated by commas or new lines:
    """)
    
    bulk_input = st.text_area("Enter values (separated by commas or new lines):", 
                            value="1, 5, 10, 25, 100", height=100)
    
    if st.button("Convert Bulk Values"):
        try:
           
            values = []
            for line in bulk_input.split('\n'):
                for val in line.split(','):
                    try:
                        values.append(float(val.strip()))
                    except ValueError:
                        pass
            
            if values:
                results = []
                for val in values:
                    if category == "Temperature" and (from_unit != to_unit):
                        converted = temp_convert(val, from_unit, to_unit)
                    else:
                        if from_unit == to_unit:
                            converted = val
                        else:
                            from_factor = conversion_data[category][from_unit]
                            to_factor = conversion_data[category][to_unit] 
                            converted = val * (from_factor / to_factor)
                    
                    results.append({
                        "Input Value": val,
                        f"Result ({to_unit})": format_number(converted)
                    })
                st.table(pd.DataFrame(results))
        except Exception as e:
            st.error(f"Error processing bulk conversion: {e}")

with tab2:
    if category == "Length":
        st.markdown("""
        ### Common Length Equivalents
        - 1 inch = 2.54 centimeters
        - 1 foot = 30.48 centimeters
        - 1 yard = 0.9144 meters
        - 1 mile = 1.60934 kilometers
        """)
    elif category == "Weight/Mass":
        st.markdown("""
        ### Common Weight/Mass Equivalents
        - 1 ounce = 28.3495 grams
        - 1 pound = 0.453592 kilograms
        - 1 stone = 6.35029 kilograms
        - 1 US ton = 0.907185 metric tons
        """)
    elif category == "Volume":
        st.markdown("""
        ### Common Volume Equivalents
        - 1 US fluid ounce = 29.5735 milliliters
        - 1 US cup = 236.588 milliliters
        - 1 US gallon = 3.78541 liters
        - 1 UK gallon = 4.54609 liters
        """)
    elif category == "Temperature":
        st.markdown("""
        ### Common Temperature Equivalents
        - Water freezes: 0°C = 32°F = 273.15K
        - Room temperature: 20-25°C = 68-77°F = 293-298K
        - Water boils: 100°C = 212°F = 373.15K
        """)
    else:
        st.markdown(f"""
        ### Common {category} Equivalents
        Check the conversion table for detailed equivalents between different units.
        """)

st.markdown('</div>', unsafe_allow_html=True)

with st.expander("ℹ️ About this Unit Converter"):
    st.markdown("""
    This comprehensive unit converter allows you to convert between various units across different categories:
    
    - Length: meters, kilometers, inches, feet, etc.
    - Weight/Mass: kilograms, grams, pounds, etc.
    - Volume: liters, gallons, cups, etc.
    - Temperature: Celsius, Fahrenheit, Kelvin
    - Area: square meters, acres, square feet, etc.
    - Time: seconds, minutes, hours, days, etc.
    - Speed: km/h, mph, m/s, etc.
    - And more!
    
    The converter provides exact formulas and conversion factors, making it useful for students, professionals, and anyone who needs to convert between different units of measurement.
    """)

# Footer
st.markdown('<div class="footer">Created by Haider Hussain 👨‍💻 using Python and Streamlit</div>', unsafe_allow_html=True)
