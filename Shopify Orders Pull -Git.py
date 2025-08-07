#Airgop Project 1
#download and import libraries we are going to use
import pandas as pd
import requests
import json

# Directly set your Shopify credentials here
ACCESS_TOKEN = 'your_access_token_here'
SHOP_NAME = 'shopname.com'  # Include only the domain part

# Set up the URL and headers for the request
url = f'https://{SHOP_NAME}/admin/api/2023-01/orders.json'
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Add opt
# ional parameters to filter results (e.g., specific status)
params = {
    "status": "any",    # You can specify 'open', 'closed', 'cancelled', or 'any'
    "limit": 200 # Limits number of results (adjust as needed)
}

# Make the request
response = requests.get(url, headers=headers, params=params)

# Check for successful response
if response.status_code == 200:
    orders = response.json().get('orders', [])
    # Print the orders or process as needed
    print(json.dumps(orders, indent=2))
else:
    print("Failed to fetch orders:", response.status_code, response.text)


#SHIPPING
# Define the shipping costs for each category
# Define the data as a list of lists
data = [
    ["Box Now", "everywhere", 1.50],
    ["Box Now", "cash on delivery", 1.00],
    ["ACS", "city", 1.80],
    ["ACS", "out of city", 2.10],
    ["ACS", "islands", 2.30],
    ["ACS", "faraway", 4.00],
    ["ACS", "cash on delivery", 1.20]
]
# Define the column names
columns = ["Company", "Service", "Rate"]
# Create a DataFrame from lists with column names
df = pd.DataFrame(data, columns=columns)
# Display the table
print(df)


#ZIP CODES
import pandas as pd
import requests

# Load the "Faraway" region zip codes from the newly uploaded files
attiki_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/attikidp.xlsx')
eparxia_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/eparxiadp.xlsx')
nisia_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/nisiadp.xlsx')

# Extract zip codes from the appropriate unnamed columns in each DataFrame
attiki_zip_codes = attiki_df.iloc[:, 5].astype(str).tolist()  # Assuming 6th column holds the zip code in attiki_df
eparxia_zip_codes = eparxia_df.iloc[:, 5].astype(str).tolist()  # Assuming 6th column holds the zip code in eparxia_df
nisia_zip_codes = nisia_df.iloc[:, 5].astype(str).tolist()  # Assuming 6th column holds the zip code in nisia_df

# Combine all extracted zip codes into a single list for "Faraway" classification
faraway_zip_codes = attiki_zip_codes + eparxia_zip_codes + nisia_zip_codes

# Display a sample of the combined list and the total count to confirm correct extraction
faraway_zip_codes[:10], len(faraway_zip_codes)

# Load faraway zip codes from the combined list we created
faraway_zip_codes



#lets load the island zip codes
# Load all the newly provided Excel files containing island zip codes
crete_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/crete_zip_codes.xlsx')
ionian_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/ionian_islands_zip_codes.xlsx')
north_aegean_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/north_aegean_zip_codes.xlsx')
south_aegean_df = pd.read_excel('/Users/lazarus/Desktop/ShopifyProjectPublic/airgop/south_aegean_zip_codes.xlsx')

# Combine the zip codes into a single list for marking as island regions
island_zip_codes = pd.concat([crete_df, ionian_df, north_aegean_df, south_aegean_df])["Zip Code"].astype(str).tolist()

# Display the combined list of zip codes to confirm successful loading and combination
island_zip_codes[:10], len(island_zip_codes)

# Function to classify location based on zip code
def classify_location(zip_code):
    if zip_code in faraway_zip_codes:
        return "Faraway"
    elif zip_code in island_zip_codes:
        return "Island"
    elif zip_code.startswith(('10', '11', '12', '13', '14', '15', '16', '17', '18', '19')):
        return "City"
    else:
        return "Out of City"

# Fetch orders from Shopify (real request setup)
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    orders = response.json().get('orders', [])
    
    # Process each order
    order_data = []
    for order in orders:
        order_id = order['id']
        name = order.get('name', "N/A")  # Fetch the name field, default to "N/A" if missing
        first_name = order['shipping_address']['first_name'] if order.get('shipping_address') else None
        last_name = order['shipping_address']['last_name'] if order.get('shipping_address') else None
        order_date = order['created_at']
        zip_code = order['shipping_address']['zip'] if order.get('shipping_address') else None
        payment_method = ", ".join(order['payment_gateway_names'])  # Join multiple payment gateways if present
        shipping_method = order['shipping_lines'][0]['title'] if order.get('shipping_lines') else None
        tags = order.get('tags', "").strip()  # Get tags or default to an empty string
        if not tags or tags.lower() != "box-now":
            tags = "acs"  # Assign 'acs' if no tag or not 'box-now'
        fulfillment_status = order.get('fulfillment_status') or "unfulfilled"  # Default to "unfulfilled" if null or missing

        # Classify location based on zip code
        location_type = classify_location(zip_code)
        
        # Check if payment method is cash on delivery
        cod = "Cash on Delivery" in payment_method
        
        # Prepare data for each order
        order_info = {
            "Order ID": order_id,
            "Name": name,  # Include name field
            "First Name": first_name,
            "Last Name": last_name,
            "Order Date": order_date,
            "Zip Code": zip_code,
            "Payment Method": payment_method,
            "Tags": tags,
            "Location Type": location_type,
            "Cash on Delivery": cod,
            "Fulfillment Status": fulfillment_status  # Ensure non-null fulfillment status
        }
        order_data.append(order_info)

    # Convert order data to DataFrame and save to Excel
    df = pd.DataFrame(order_data)
    df.to_excel("shopify_orders_classified.xlsx", index=False)
    print("Data saved to shopify_orders_classified.xlsx")
else:
    print("Failed to fetch orders:", response.status_code, response.text)


###Final Function
import pandas as pd

# Load the classified Excel file
input_file = "shopify_orders_classified.xlsx"
df = pd.read_excel(input_file)

# Function to calculate shipping price
def calculate_shipping_price(row):
    shipping_price = 0
    tag = row['Tags'].lower()
    payment_method = row['Payment Method'].lower()
    location_type = row['Location Type']
    cod = "cash on delivery" in payment_method

    if "box-now" in tag:
        # Box-now pricing
        shipping_price = 1.5
        if cod:
            shipping_price += 1.
    elif "acs" in tag:
        # ACS pricing based on location type
        if location_type == "City":
            shipping_price = 1.80
        elif location_type == "Out of City":
            shipping_price = 2.10
        elif location_type == "Island":
            shipping_price = 2.30
        elif location_type == "Faraway":
            shipping_price = 4.00
        
        # Add cash on delivery fee for ACS
        if cod:
            shipping_price += 1.20
    return shipping_price


# Apply the shipping price calculation
df['Shipping Price'] = df.apply(calculate_shipping_price, axis=1)


# Save the updated DataFrame to a new Excel file
output_file = "shopify_orders_with_shipping_fulfillment.xlsx"
df.to_excel(output_file, index=False)

print(f"Updated data saved to {output_file}")

