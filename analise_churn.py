from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
URL_DADOS = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

print("🔄 1/3 - Baixando e tratando os dados...")
df = pd.read_csv(URL_DADOS)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])

def categorizar_tempo(meses):
    if meses <= 6:
        return "0 a 6m"
    elif meses <= 12:
        return "7 a 12m"
    elif meses <= 24:
        return "1 a 2 anos"
    elif meses <= 48:
        return "2 a 4 anos"
    else:
        return "+4 anos"


df["Faixa_Tenure"] = df["tenure"].apply(categorizar_tempo)

total_clientes = len(df)
total_churn = len(df[df["Churn"] == "Yes"])
taxa_churn = (total_churn / total_clientes) * 100
mrr_perdido = df[df["Churn"] == "Yes"]["MonthlyCharges"].sum()
ticket_medio = df["MonthlyCharges"].mean()

print("\n" + "=" * 45)
print("📊 RESUMO EXECUTIVO DO NEGÓCIO")
print("=" * 45)
print(f"• Total de Clientes Analisados : {total_clientes:,}")
print(f"• Clientes que Cancelaram      : {total_churn:,}")
print(f"• Taxa Geral de Churn          : {taxa_churn:.2f}%")
print(f"• Receita Mensal Perdida (MRR) : R$ {mrr_perdido:,.2f}")
print(f"• Ticket Médio Mensal          : R$ {ticket_medio:.2f}")
print("=" * 45 + "\n")

print("🎨 2/3 - Gerando o painel de gráficos...")

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

paleta = {"No": "#2b5c8f", "Yes": "#d9534f"}

# Gráfico 1
sns.countplot(
    data=df,
    x="Contract",
    hue="Churn",
    palette=paleta,
    ax=axes[0, 0],
)
axes[0, 0].set_title(
    "1. Cancelamentos por Tipo de Contrato", fontsize=12, fontweight="bold"
)
axes[0, 0].set_xlabel("Tipo de Contrato")
axes[0, 0].set_ylabel("Quantidade de Clientes")

# Gráfico 2
ordem = ["0 a 6m", "7 a 12m", "1 a 2 anos", "2 a 4 anos", "+4 anos"]
sns.countplot(
    data=df,
    x="Faixa_Tenure",
    hue="Churn",
    order=ordem,
    palette=paleta,
    ax=axes[0, 1],
)
axes[0, 1].set_title(
    "2. Cancelamentos por Tempo de Casa (Tenure)", fontsize=12, fontweight="bold"
)
axes[0, 1].set_xlabel("Tempo com o Serviço")
axes[0, 1].set_ylabel("Quantidade de Clientes")

# Gráfico 3
sns.countplot(
    data=df,
    x="TechSupport",
    hue="Churn",
    palette=paleta,
    ax=axes[1, 0],
)
axes[1, 0].set_title(
    "3. Impacto de Ter Suporte Técnico no Churn", fontsize=12, fontweight="bold"
)
axes[1, 0].set_xlabel("Possui Suporte Técnico?")
axes[1, 0].set_ylabel("Quantidade de Clientes")

# Gráfico 4
sns.countplot(
    data=df,
    y="PaymentMethod",
    hue="Churn",
    palette=paleta,
    ax=axes[1, 1],
)
axes[1, 1].set_title(
    "4. Cancelamento por Forma de Pagamento", fontsize=12, fontweight="bold"
)
axes[1, 1].set_xlabel("Quantidade de Clientes")
axes[1, 1].set_ylabel("Método de Pagamento")

fig.suptitle(
    f"Painel Executivo de Churn | Taxa de Cancelamento: {taxa_churn:.1f}% | MRR Perdido: R$ {mrr_perdido:,.0f}/mês",
    fontsize=16,
    fontweight="bold",
    y=0.98,
)

plt.tight_layout()
plt.subplots_adjust(top=0.92)

caminho_imagem = BASE_DIR / "painel_executivo_churn.png"
plt.savefig(caminho_imagem, dpi=300)
print(f"✅ 3/3 - Painel salvo com sucesso em: {caminho_imagem.name}")
plt.show()