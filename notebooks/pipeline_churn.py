from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DASHBOARDS_DIR = BASE_DIR / "dashboards"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARDS_DIR.mkdir(parents=True, exist_ok=True)

print("==> 1. Baixando e carregando os dados...")
url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)
df.to_csv(RAW_DIR / "Telco-Customer-Churn.csv", index=False)

print("==> 2. Tratando valores e tipos...")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])
df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})

print("==> 3. Gerando visualizações de diagnóstico...")
sns.set_theme(style="whitegrid")

# Gráfico 1
plt.figure(figsize=(7, 4))
sns.countplot(
    data=df,
    x="Contract",
    hue="Churn",
    palette={"No": "#2b5c8f", "Yes": "#d9534f"},
)
plt.title("Cancelamentos por Tipo de Contrato", fontsize=12, fontweight="bold")
plt.xlabel("Tipo de Contrato")
plt.ylabel("Qtd Clientes")
plt.tight_layout()
plt.savefig(DASHBOARDS_DIR / "eda_contrato_churn.png")
plt.close()

# Gráfico 2
plt.figure(figsize=(7, 4))
sns.kdeplot(
    data=df,
    x="tenure",
    hue="Churn",
    fill=True,
    common_norm=False,
    palette={"No": "#2b5c8f", "Yes": "#d9534f"},
)
plt.title(
    "Distribuição do Tempo de Casa (Tenure) por Churn",
    fontsize=12,
    fontweight="bold",
)
plt.xlabel("Meses de Permanência")
plt.tight_layout()
plt.savefig(DASHBOARDS_DIR / "eda_tenure_churn.png")
plt.close()

# modelagem dimensional
print("==> 4. Separando em Tabelas Fato e Dimensão...")

# dimensão cliente
d_cliente = df[
    ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents"]
].drop_duplicates()
d_cliente.to_csv(PROCESSED_DIR / "dCliente.csv", index=False)

# dimensão serviços
d_servicos = df[
    [
        "customerID",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]
].drop_duplicates()
d_servicos.to_csv(PROCESSED_DIR / "dServicos.csv", index=False)

# dimensão contrato
d_contrato = df[
    ["customerID", "Contract", "PaperlessBilling", "PaymentMethod"]
].drop_duplicates()
d_contrato.to_csv(PROCESSED_DIR / "dContrato.csv", index=False)

# fato assinaturas
f_assinaturas = df[
    ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
].copy()
f_assinaturas["ChurnNumeric"] = (f_assinaturas["Churn"] == "Yes").astype(int)
f_assinaturas.to_csv(PROCESSED_DIR / "fAssinaturas.csv", index=False)

print("==> Processo concluído com sucesso!")