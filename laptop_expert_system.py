import pandas as pd

# Define the path to the CSV file
csv_file_path = 'laptops.csv'
# Try to load the dataset
try:
    laptops_data = pd.read_csv(csv_file_path)
    # Calculate the price percentiles for use in the filter_laptops function
    price_percentiles = laptops_data['Price_NGN'].quantile([0.25, 0.5, 0.75])
except FileNotFoundError:
    print(f"The file at {csv_file_path} was not found.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

def filter_laptops_cli(df, profile, os_choice):
    # Filtering based on user profile
    if profile == '1':  # Budget Conscious
        max_price = price_percentiles[0.25]
        filtered_df = df[(df['Price_NGN'] <= max_price)]
    elif profile == '2':  # Student
        min_price = price_percentiles[0.25]
        max_price = price_percentiles[0.50]
        filtered_df = df[(df['Price_NGN'] >= min_price) & (df['Price_NGN'] <= max_price)]
    elif profile == '3':  # Professional
        # Assuming professional laptops have higher RAM and possibly SSD storage
        filtered_df = df[(df['RAM_GB'] >= 8) & (df['Storage'].str.contains('SSD'))]
    elif profile == '4':  # Gamer
        # For gamers, high RAM, and a dedicated GPU are important
        filtered_df = df[(df['RAM_GB'] >= 16) & (df['Gpu'].str.contains('Nvidia|AMD'))]
    elif profile == '5':  # Casual User
        max_price = price_percentiles[0.50]
        filtered_df = df[(df['Price_NGN'] <= max_price)]
    else:
        return pd.DataFrame()  # Return empty DataFrame for invalid input
    
    if os_choice != 'Any':
        filtered_df = filtered_df[filtered_df['OpSys'] == os_choice]

    return filtered_df


def laptop_expert_system_cli(df):
    print("Welcome to the Laptop Expert System")
    print("Please select a user profile for laptop recommendations:")
    print("1 - Budget Conscious")
    print("2 - Student")
    print("3 - Professional")
    print("4 - Gamer")
    print("5 - Casual User")

    profile_choice = input("Enter the number corresponding to your profile: ")

    # List available operating systems
    unique_os = df['OpSys'].unique()
    print("\nAvailable Operating Systems:", ", ".join(unique_os))
    print("Please select your preferred Operating System (type 'Any' for no preference):")
    os_choice = input("Enter your choice: ")

    # Filter laptops based on the selected criteria
    filtered_df = filter_laptops_cli(df, profile_choice, os_choice)

    if not filtered_df.empty:
        sorted_df = filtered_df.sort_values(by='Price_NGN')
        print("\nTop 5 laptop recommendations:")
        print(sorted_df[['Brand', 'Product', 'RAM_GB', 'Cpu', 'Gpu', 'Price_NGN']].head().to_string(index=False))
    else:
        print("No laptops found for the selected profile and operating system.")

if __name__ == "__main__":
    laptop_expert_system_cli(laptops_data)