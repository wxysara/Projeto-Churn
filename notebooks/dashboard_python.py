import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
df = pd.read_csv(url)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

def classificar_faixa(meses):
    if meses <= 6: return "0-6 meses"
    elif meses <= 12: return "7-12 meses"
    elif meses <= 24: return "1-2 anos"
    elif meses <= 48: return "2-4 anos"
    else: return "+4 anos"

df["Faixa_Tenure"] = df["tenure"].apply(classificar_faixa)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("📊 Painel Executivo - Análise de Churn (Cancelamento de Clientes)", fontsize=16, fontweight="bold", y=0.98)

cor_retido = "#2b5c8f"
cor_churn = "#d9534f"

sns.countplot(data=df, x="Contract", hue="Churn", palette={"No": cor_retido, "Yes": cor_churn}, ax=axes[0, 0])
axes[0, 0].set_title("Cancelamento por Tipo de Contrato", fontweight="bold")
axes[0, 0].set_xlabel("Contrato")
axes[0, 0].set_ylabel("Quantidade de Clientes")

ordem_faixas = ["0-6 meses", "7-12 meses", "1-2 anos", "2-4 anos", "+4 anos"]
sns.countplot(data=df, x="Faixa_Tenure", hue="Churn", order=ordem_faixas, palette={"No": cor_retido, "Yes": cor_churn}, ax=axes[0, 1])
axes[0, 1].set_title("Cancelamento por Tempo de Permanência", fontweight="bold")
axes[0, 1].set_xlabel("Tempo com o Serviço")
axes[0, 1].set_ylabel("Quantidade de Clientes")

sns.countplot(data=df, x="TechSupport", hue="Churn", palette={"No": cor_retido, "Yes": cor_churn}, ax=axes[1, 0])
axes[1, 0].set_title("Cancelamento vs Suporte Técnico", fontweight="bold")
axes[1, 0].set_xlabel("Tem Suporte Técnico?")
axes[1, 0].set_ylabel("Quantidade de Clientes")

sns.countplot(data=df, y="PaymentMethod", hue="Churn", palette={"No": cor_retido, "Yes": cor_churn}, ax=axes[1, 1])
axes[1, 1].set_title("Cancelamento por Forma de Pagamento", fontweight="bold")
axes[1, 1].set_xlabel("Quantidade de Clientes")
axes[1, 1].set_ylabel("Forma de Pagamento")

plt.tight_layout()
plt.subplots_adjust(top=0.92)

plt.savefig("dashboard_final.png", dpi=300)
print("Painel gerado com sucesso! Arquivo salvo como dashboard_final.png")
plt.show()