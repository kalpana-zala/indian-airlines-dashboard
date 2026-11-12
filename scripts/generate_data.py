"""Generate the sample Indian airlines dataset (2023-2025) used by the dashboard.
Run in Google Colab or any Python 3 with pandas + numpy. Outputs Fact_Flights.csv and Dim_Airline.csv."""
import pandas as pd, numpy as np
np.random.seed(42)

airlines = ["Air India", "IndiGo", "Akasa Air", "SpiceJet", "Star Air"]
routes = {"AMD → IXB": ("Ahmedabad", "Bagdogra"), "BBI → IXB": ("Bhubaneswar", "Bagdogra"),
          "BLR → IXB": ("Bengaluru", "Bagdogra"), "BOM → IXB": ("Mumbai", "Bagdogra"),
          "CCU → IXB": ("Kolkata", "Bagdogra"), "DEL → GOI": ("Delhi", "Goa"),
          "BOM → DEL": ("Mumbai", "Delhi")}
scale = {"Air India": 1.0, "IndiGo": 1.3, "Akasa Air": 0.5, "SpiceJet": 0.6, "Star Air": 0.1}

rows = []
for d in pd.date_range("2023-01-01", "2025-12-31", freq="D"):
    season = 1 + 0.25 * np.sin((d.month - 3) / 12 * 2 * np.pi)
    for a in airlines:
        for r, (src, dst) in routes.items():
            if np.random.rand() < 0.3:
                cap = int(np.random.choice([72, 180, 186, 232]))
                pax = max(1, int(cap * np.random.uniform(0.6, 0.98) * scale[a] * season))
                rows.append([d.date(), a, r, src, dst, pax, cap,
                             round(np.random.uniform(250, 360), 2),
                             round(np.random.uniform(60, 320), 2),
                             round(np.random.uniform(120, 260), 2),
                             round(pax * np.random.uniform(800, 2500), 2)])

fact = pd.DataFrame(rows, columns=["Date", "Airline", "Route", "SourceCity", "DestinationCity",
                                   "Passengers", "Capacity", "FuelEfficiency", "CO2PerPax",
                                   "FlightDuration", "Profit"])
fact.to_csv("Fact_Flights.csv", index=False)

base = "https://raw.githubusercontent.com/kalpana-zala/indian-airlines-dashboard/main/images/"
pd.DataFrame({"Airline": airlines,
              "Rating": [4.13, 4.08, 3.85, 3.60, 3.81],
              "BrandColor": ["#D7263D", "#1F3C88", "#F26522", "#E21B23", "#E84A27"],
              "PlaneImageURL": [base + f for f in ["air_india.png", "indigo.png", "akasa_air.png",
                                                   "spicejet.png", "star_air.png"]]}
             ).to_csv("Dim_Airline.csv", index=False)
print(len(fact), "flights written")
