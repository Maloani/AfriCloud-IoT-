import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# =========================================================
# SIMULATION : 10 000 CAPTEURS IoT
# COMPARAISON :
# 1. Architecture classique (tout au cloud)
# 2. Architecture optimisée (Edge + Cloud)
# =========================================================

np.random.seed(42)

# -----------------------------
# PARAMETRES DE SIMULATION
# -----------------------------
NUM_SENSORS = 10000
EDGE_THRESHOLD_TEMP = 28.0
EDGE_THRESHOLD_TRAFFIC = 60.0

# -----------------------------
# GENERATION DES DONNEES IoT
# -----------------------------
sensor_ids = np.arange(1, NUM_SENSORS + 1)

iot_data = pd.DataFrame({
    "sensor_id": sensor_ids,
    "temperature": np.random.uniform(15, 45, NUM_SENSORS),
    "humidity": np.random.uniform(20, 95, NUM_SENSORS),
    "traffic_density": np.random.uniform(0, 100, NUM_SENSORS),
    "energy_usage": np.random.uniform(100, 1000, NUM_SENSORS),
    "latency_ms": np.random.uniform(10, 300, NUM_SENSORS),
})

# =========================================================
# 1. ARCHITECTURE CLASSIQUE
# Tout est envoyé au cloud sans prétraitement
# =========================================================
start_classic = time.time()

classic_volume = len(iot_data)

# simulation d'un traitement complet cloud
classic_temp_mean = iot_data["temperature"].mean()
classic_humidity_mean = iot_data["humidity"].mean()
classic_traffic_mean = iot_data["traffic_density"].mean()

# simulation d'une latence moyenne plus forte
classic_network_latency = iot_data["latency_ms"].mean() * 1.15

end_classic = time.time()
classic_processing_time = end_classic - start_classic

# estimation de coût (arbitraire qui est cohérente pour comparaison)
classic_cost = (
    classic_volume * 0.0025
    + classic_network_latency * 0.01
    + classic_processing_time * 100
)

# =========================================================
# 2. ARCHITECTURE OPTIMISEE
# Prétraitement Edge + envoi sélectif au cloud
# =========================================================
start_optimized = time.time()

# Edge filtering : seuls les événements significatifs montent au cloud
edge_filtered = iot_data[
    (iot_data["temperature"] > EDGE_THRESHOLD_TEMP) |
    (iot_data["traffic_density"] > EDGE_THRESHOLD_TRAFFIC)
].copy()

optimized_volume = len(edge_filtered)

# traitement cloud réduit car déjà filtré au niveau edge
optimized_temp_mean = edge_filtered["temperature"].mean()
optimized_humidity_mean = edge_filtered["humidity"].mean()
optimized_traffic_mean = edge_filtered["traffic_density"].mean()

# latence réduite grâce au prétraitement local
optimized_network_latency = edge_filtered["latency_ms"].mean() * 0.70

end_optimized = time.time()
optimized_processing_time = end_optimized - start_optimized

# estimation de coût
optimized_cost = (
    optimized_volume * 0.0025
    + optimized_network_latency * 0.01
    + optimized_processing_time * 100
)

# =========================================================
# RESULTATS TEXTUELS
# =========================================================
print("=" * 60)
print("RESULTATS DE LA SIMULATION")
print("=" * 60)

print("\n--- Architecture classique ---")
print(f"Nombre total de capteurs traités : {classic_volume}")
print(f"Température moyenne : {classic_temp_mean:.2f} °C")
print(f"Humidité moyenne : {classic_humidity_mean:.2f} %")
print(f"Densité moyenne du trafic : {classic_traffic_mean:.2f}")
print(f"Latence moyenne estimée : {classic_network_latency:.2f} ms")
print(f"Temps de traitement : {classic_processing_time:.6f} s")
print(f"Coût estimé : {classic_cost:.2f}")

print("\n--- Architecture optimisée (Edge + Cloud) ---")
print(f"Nombre de capteurs transmis au cloud : {optimized_volume}")
print(f"Température moyenne : {optimized_temp_mean:.2f} °C")
print(f"Humidité moyenne : {optimized_humidity_mean:.2f} %")
print(f"Densité moyenne du trafic : {optimized_traffic_mean:.2f}")
print(f"Latence moyenne estimée : {optimized_network_latency:.2f} ms")
print(f"Temps de traitement : {optimized_processing_time:.6f} s")
print(f"Coût estimé : {optimized_cost:.2f}")

# =========================================================
# TABLEAU COMPARATIF
# =========================================================
comparison_df = pd.DataFrame({
    "Architecture": ["Classique", "Optimisée"],
    "Volume transmis au cloud": [classic_volume, optimized_volume],
    "Latence moyenne (ms)": [classic_network_latency, optimized_network_latency],
    "Temps de traitement (s)": [classic_processing_time, optimized_processing_time],
    "Coût estimé": [classic_cost, optimized_cost]
})

print("\n")
print("=" * 60)
print("TABLEAU COMPARATIF")
print("=" * 60)
print(comparison_df)

# =========================================================
# GRAPHIQUE 1 : VOLUME DE DONNEES TRANSMIS AU CLOUD
# =========================================================
plt.figure(figsize=(8, 5))
plt.bar(
    comparison_df["Architecture"],
    comparison_df["Volume transmis au cloud"]
)
plt.title("Volume de données transmis au cloud")
plt.ylabel("Nombre de capteurs / enregistrements")
plt.xlabel("Type d'architecture")
plt.tight_layout()
plt.show()

# =========================================================
# GRAPHIQUE 2 : LATENCE MOYENNE
# =========================================================
plt.figure(figsize=(8, 5))
plt.bar(
    comparison_df["Architecture"],
    comparison_df["Latence moyenne (ms)"]
)
plt.title("Comparaison de la latence moyenne")
plt.ylabel("Latence moyenne (ms)")
plt.xlabel("Type d'architecture")
plt.tight_layout()
plt.show()

# =========================================================
# GRAPHIQUE 3 : COUT ESTIME
# =========================================================
plt.figure(figsize=(8, 5))
plt.bar(
    comparison_df["Architecture"],
    comparison_df["Coût estimé"]
)
plt.title("Comparaison du coût estimé")
plt.ylabel("Coût estimé")
plt.xlabel("Type d'architecture")
plt.tight_layout()
plt.show()