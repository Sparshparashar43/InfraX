from flask import Flask, request, jsonify, render_template
import qrcode

app = Flask(__name__)

# **Updated Material Costs (Per Square Foot)**
AAC_COST_PER_SQFT = 105  # INR (Adjusted realistic cost)
RED_BRICK_COST_PER_SQFT = 120  # INR (Market-based cost)
LABOR_COST_PER_SQFT_AAC = 30  # INR (Lower labor cost for AAC)
LABOR_COST_PER_SQFT_RED = 50  # INR (Higher labor cost for bricks)

# **CO₂ Reduction (Per Square Foot)**
CO2_SAVED_PER_SQFT = 1.5  # kg CO₂ saved per sqft (Lowered further)

# **Dealer Profit Margins**
DEALER_PROFIT_MARGIN_AAC = 8  # Reduced from 10% to 8%
DEALER_PROFIT_MARGIN_RED = 5  # Reduced from 6% to 5%

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        sqft = float(request.json.get('sqft', 0))

        if sqft <= 0:
            return jsonify({"error": "Invalid input. Please enter a valid square footage."})

        # **Cost Calculations**
        total_aac_cost = sqft * AAC_COST_PER_SQFT
        total_red_brick_cost = sqft * RED_BRICK_COST_PER_SQFT

        # **Labor Cost Calculations**
        total_labor_aac = sqft * LABOR_COST_PER_SQFT_AAC
        total_labor_red_brick = sqft * LABOR_COST_PER_SQFT_RED

        # **Total Cost with Labor**
        total_aac = total_aac_cost + total_labor_aac
        total_red_brick = total_red_brick_cost + total_labor_red_brick

        # **Final Cost Savings Calculation**
        total_savings = max((total_red_brick - total_aac) * 0.6, 500)  # Reduced overall savings

        # **CO₂ Savings Calculation**
        co2_saved = sqft * CO2_SAVED_PER_SQFT  # Adjusted to per sqft values

        # **Dealer Profit Calculation**
        dealer_profit_aac = total_aac_cost * (DEALER_PROFIT_MARGIN_AAC / 100)
        dealer_profit_red_brick = total_red_brick_cost * (DEALER_PROFIT_MARGIN_RED / 100)

        # **Time Savings in Hours (Reduced Significantly)**
        time_savings_hours = round(sqft * 0.04, 1)  # Approx **hours saved** per sqft

        return jsonify({
            "cost_savings": round(total_savings, 2),
            "time_savings": round(time_savings_hours, 2),  # **Now in hours**
            "co2_reduction": round(co2_saved, 2),
            "dealer_profit_aac": round(dealer_profit_aac, 2),
            "dealer_profit_red": round(dealer_profit_red_brick, 2)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/generate_qr')
def generate_qr():
    qr = qrcode.make("http://your-web-app-url.com")
    qr.save("static/qrcode.png")
    return jsonify({"qr_code": "static/qrcode.png"})

if __name__ == '__main__':
    app.run(debug=True)