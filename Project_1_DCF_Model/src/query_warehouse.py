import getpass
from sqlalchemy import create_engine
import pandas as pd

# 1. Securely prompt for your MySQL root password
password = getpass.getpass("Enter your MySQL root password: ")

# 2. Connect to your enterprise_valuation database
connection_string = f"mysql+pymysql://root:{password}@localhost:3306/enterprise_valuation"
engine = create_engine(connection_string)

# 3. Query data directly using your new index (e.g., pulling a specific ticker like MSFT)
query = "SELECT * FROM market_warehouse WHERE Ticker = 'MSFT' ORDER BY Date DESC LIMIT 100;"

# 4. Load results into a Pandas DataFrame
df = pd.read_sql(query, engine)

print("Successfully queried database!")
print(df.head())