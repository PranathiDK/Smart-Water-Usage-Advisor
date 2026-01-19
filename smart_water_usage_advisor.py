# --- STEP 1: INSTALL GRADIO (Run once) ---
try:
    import gradio as gr
except ImportError:
    import os
    os.system('pip install gradio')
    import gradio as gr

# --- STEP 2: DEFINE THE LOGIC ---
def calculate_water_footprint(family_size, shower_time, laundry_loads, ro_usage):
    # Logic Constants
    FLOW_RATE_SHOWER = 10   # Liters/min
    FLUSH_VOLUME = 6        # Liters/flush
    FLUSHES_PER_DAY = 4     # Uses/person
    LAUNDRY_VOLUME = 60     # Liters/load
    RO_WASTE_RATIO = 3      # 3L wasted per 1L drunk

    # Input Cleaning
    if family_size <= 0: return "Please enter a valid family size."
    
    # Calculations
    daily_shower = family_size * shower_time * FLOW_RATE_SHOWER
    daily_flush = family_size * FLUSHES_PER_DAY * FLUSH_VOLUME
    daily_laundry = (laundry_loads * LAUNDRY_VOLUME) / 7
    
    daily_ro = 0
    if ro_usage == "Yes":
        daily_ro = family_size * 2 * RO_WASTE_RATIO

    total_daily = daily_shower + daily_flush + daily_laundry + daily_ro
    per_person = total_daily / family_size

    # Formatting the Report
    report = f"""
    📊 YOUR WATER AUDIT REPORT
    ================================================
    💧 Total Household Usage: {int(total_daily)} Liters/day
    👤 Usage Per Person:      {int(per_person)} Liters/day
    ================================================
    """
    
    if per_person <= 135:
        report += "\n✅ STATUS: EXCELLENT! You are water efficient."
    else:
        report += "\n⚠️ STATUS: HIGH USAGE. (Standard is 135L)."

    report += "\n\n💡 RECOMMENDATIONS & FIXES:\n" + "-"*30
    
    if daily_shower > daily_flush and daily_shower > daily_laundry:
        report += f"\n1. BIGGEST WASTE: SHOWERS ({int(daily_shower)} L/day)"
        report += "\n   👉 Fix: Install a low-flow aerator (Cost: ₹150). It cuts flow by 50%."
    elif daily_ro > 50:
        report += f"\n1. BIGGEST WASTE: RO PURIFIER ({int(daily_ro)} L/day)"
        report += "\n   👉 Fix: Keep a bucket under the waste pipe. Use it for cleaning."
    elif daily_laundry > 200:
        report += "\n1. BIGGEST WASTE: LAUNDRY"
        report += "\n   👉 Fix: Run the machine only when fully loaded."
    else:
        report += "\n1. GENERAL TIP"
        report += "\n   👉 Check for leaky taps; a single drip wastes 20L a day."

    report += "\n\n2. SECONDARY TIP"
    report += "\n   👉 Turn off the tap while brushing teeth to save 15L/day."

    return report

# --- STEP 3: BUILD THE INTERFACE (Now with Larger Screen) ---
app = gr.Interface(
    fn=calculate_water_footprint,
    inputs=[
        gr.Slider(1, 15, step=1, label="Family Size (People)"),
        gr.Slider(1, 60, step=1, value=10, label="Avg Shower Time (Mins)"),
        gr.Number(label="Laundry Loads per Week", value=5),
        gr.Radio(["Yes", "No"], label="Do you use an RO Purifier?", value="Yes")
    ],
    # CHANGE IS HERE: We set lines=25 to make the box tall!
    outputs=gr.Textbox(label="Analysis Report", lines=25),
    title="💧 Smart Water Usage Advisor",
    description="Enter your daily habits to see your Water Footprint.",
    theme="soft"
)

# --- STEP 4: LAUNCH ---
if __name__ == "__main__":
    app.launch(share=True)