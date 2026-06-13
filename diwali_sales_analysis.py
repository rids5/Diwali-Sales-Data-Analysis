import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings, os

warnings.filterwarnings('ignore')

os.makedirs('plots', exist_ok=True)

DIWALI_PALETTE = ['#FF6B35', '#FFD700', '#C0392B', '#2ECC71', '#8E44AD',
                  '#E67E22', '#3498DB', '#1ABC9C', '#E91E63', '#795548', '#607D8B']
BG    = '#FFF8F0'
ACCENT = '#FF6B35'
DARK  = '#1A1A2E'
GOLD  = '#FFD700'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG,
    'axes.edgecolor': '#CCCCCC', 'axes.labelcolor': DARK,
    'axes.titlesize': 14, 'axes.titleweight': 'bold',
    'axes.titlecolor': DARK, 'xtick.color': DARK,
    'ytick.color': DARK, 'text.color': DARK,
    'grid.color': '#E5E5E5', 'grid.linestyle': '--', 'grid.linewidth': 0.6,
})

def save(fig, name):
    fig.savefig(f'plots/{name}', dpi=150, bbox_inches='tight', facecolor=BG)
    print(f"  ✓ Saved → plots/{name}")
    plt.close(fig)

def fmt_inr(x, _):
    if x >= 1e7: return f'₹{x/1e7:.1f}Cr'
    if x >= 1e5: return f'₹{x/1e5:.1f}L'
    if x >= 1e3: return f'₹{x/1e3:.0f}K'
    return f'₹{x:.0f}'

# ── Load & Clean ──────────────────────────────────────────
print("\n📦 Loading data...")
df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
print(f"   Shape (raw): {df.shape}")

df.drop(columns=[c for c in ['Status', 'unnamed1'] if c in df.columns], inplace=True)
df.dropna(subset=['Amount'], inplace=True)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Orders'] = pd.to_numeric(df['Orders'], errors='coerce').astype(int)
df['Age']    = pd.to_numeric(df['Age'], errors='coerce').astype(int)
print(f"   Shape (clean): {df.shape}")
print(df[['Amount','Orders','Age']].describe().round(2))

# ── 1. Gender ─────────────────────────────────────────────
print("\n🔍 [1/8] Gender Analysis...")
gender_counts  = df['Gender'].value_counts()
gender_revenue = df.groupby('Gender')['Amount'].sum().sort_values(ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('🪔 Gender Analysis — Buyers & Revenue', fontsize=16, fontweight='bold')
colors = [ACCENT, GOLD]
b1 = axes[0].bar(gender_counts.index, gender_counts.values, color=colors, width=0.5, edgecolor='white')
axes[0].set_title('Number of Buyers by Gender')
axes[0].bar_label(b1, fmt='%,d', padding=4, fontweight='bold')
axes[0].set_ylim(0, gender_counts.max() * 1.15)
axes[0].grid(axis='y')
b2 = axes[1].bar(gender_revenue.index, gender_revenue.values, color=colors, width=0.5, edgecolor='white')
axes[1].set_title('Total Revenue by Gender')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
for bar, val in zip(b2, gender_revenue.values):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+gender_revenue.max()*0.01,
                 fmt_inr(val,None), ha='center', fontweight='bold')
axes[1].set_ylim(0, gender_revenue.max() * 1.15)
axes[1].grid(axis='y')
plt.tight_layout()
save(fig, '01_gender_analysis.png')

# ── 2. Age Group ──────────────────────────────────────────
print("🔍 [2/8] Age Group Analysis...")
age_order   = ['0-17','18-25','26-35','36-45','46-50','51-55','55+']
age_counts  = df['Age Group'].value_counts().reindex(age_order, fill_value=0)
age_revenue = df.groupby('Age Group')['Amount'].sum().reindex(age_order, fill_value=0)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('🪔 Age Group Analysis', fontsize=16, fontweight='bold')
pal = sns.color_palette(DIWALI_PALETTE[:len(age_order)])
b = axes[0].bar(age_order, age_counts.values, color=pal, edgecolor='white')
axes[0].set_title('Buyers by Age Group')
axes[0].bar_label(b, fmt='%,d', padding=3, fontsize=9)
axes[0].set_ylim(0, age_counts.max()*1.15)
axes[0].grid(axis='y')
b2 = axes[1].bar(age_order, age_revenue.values, color=pal, edgecolor='white')
axes[1].set_title('Revenue by Age Group')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
for bar, val in zip(b2, age_revenue.values):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+age_revenue.max()*0.01,
                 fmt_inr(val,None), ha='center', fontsize=8.5, fontweight='bold')
axes[1].set_ylim(0, age_revenue.max()*1.15)
axes[1].grid(axis='y')
plt.tight_layout()
save(fig, '02_age_group_analysis.png')

# ── 3. State ──────────────────────────────────────────────
print("🔍 [3/8] State Analysis...")
top_states_orders  = df.groupby('State')['Orders'].sum().sort_values(ascending=False).head(10)
top_states_revenue = df.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('🪔 Top 10 States — Orders & Revenue', fontsize=16, fontweight='bold')
cs = sns.color_palette('YlOrRd', 10)[::-1]
axes[0].barh(top_states_orders.index[::-1], top_states_orders.values[::-1], color=cs, edgecolor='white')
axes[0].set_title('Total Orders by State (Top 10)')
axes[0].grid(axis='x')
axes[1].barh(top_states_revenue.index[::-1], top_states_revenue.values[::-1], color=cs, edgecolor='white')
axes[1].set_title('Total Revenue by State (Top 10)')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[1].grid(axis='x')
plt.tight_layout()
save(fig, '03_state_analysis.png')

# ── 4. Marital Status ─────────────────────────────────────
print("🔍 [4/8] Marital Status Analysis...")
df['Marital_Label'] = df['Marital_Status'].map({0:'Single', 1:'Married'})
ms_gender = df.groupby(['Marital_Label','Gender'])['Amount'].sum().unstack()
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('🪔 Marital Status Analysis', fontsize=16, fontweight='bold')
ms_counts = df['Marital_Label'].value_counts()
axes[0].pie(ms_counts.values, labels=ms_counts.index, autopct='%1.1f%%',
            colors=[ACCENT, GOLD], wedgeprops={'linewidth':2,'edgecolor':BG},
            textprops={'fontsize':12,'fontweight':'bold'})
axes[0].set_title('Buyer Split — Single vs Married')
ms_gender.plot(kind='bar', ax=axes[1], color=[ACCENT, GOLD], edgecolor='white', width=0.6)
axes[1].set_title('Revenue by Marital Status & Gender')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
axes[1].legend(title='Gender')
axes[1].grid(axis='y')
plt.tight_layout()
save(fig, '04_marital_status_analysis.png')

# ── 5. Occupation ─────────────────────────────────────────
print("🔍 [5/8] Occupation Analysis...")
occ_revenue = df.groupby('Occupation')['Amount'].sum().sort_values(ascending=False)
occ_counts  = df['Occupation'].value_counts()
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('🪔 Occupation Analysis', fontsize=16, fontweight='bold')
axes[0].barh(occ_revenue.index[::-1], occ_revenue.values[::-1],
             color=sns.color_palette('magma', len(occ_revenue))[::-1], edgecolor='white')
axes[0].set_title('Revenue by Occupation')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[0].grid(axis='x')
axes[1].barh(occ_counts.index[::-1], occ_counts.values[::-1],
             color=sns.color_palette('viridis', len(occ_counts))[::-1], edgecolor='white')
axes[1].set_title('Number of Buyers by Occupation')
axes[1].grid(axis='x')
plt.tight_layout()
save(fig, '05_occupation_analysis.png')

# ── 6. Product Category ───────────────────────────────────
print("🔍 [6/8] Product Category Analysis...")
cat_revenue = df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False)
cat_orders  = df.groupby('Product_Category')['Orders'].sum().sort_values(ascending=False)
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('🪔 Product Category Analysis', fontsize=16, fontweight='bold')
colors_cat = sns.color_palette(DIWALI_PALETTE, len(cat_revenue))
b = axes[0].bar(cat_revenue.index, cat_revenue.values, color=colors_cat, edgecolor='white')
axes[0].set_title('Revenue by Product Category')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[0].set_xticklabels(cat_revenue.index, rotation=30, ha='right', fontsize=9)
axes[0].grid(axis='y')
b2 = axes[1].bar(cat_orders.index, cat_orders.values, color=colors_cat, edgecolor='white')
axes[1].set_title('Total Orders by Product Category')
axes[1].bar_label(b2, fmt='%,d', padding=3, fontsize=8)
axes[1].set_xticklabels(cat_orders.index, rotation=30, ha='right', fontsize=9)
axes[1].grid(axis='y')
plt.tight_layout()
save(fig, '06_product_category_analysis.png')

# ── 7. Top Products ───────────────────────────────────────
print("🔍 [7/8] Top Products Analysis...")
top_products = df.groupby('Product_ID')['Orders'].sum().sort_values(ascending=False).head(15)
fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(top_products.index, top_products.values,
              color=sns.color_palette('rocket', 15)[::-1], edgecolor='white')
ax.set_title('🪔 Top 15 Products by Orders Placed', fontsize=15, fontweight='bold')
ax.set_xticklabels(top_products.index, rotation=45, ha='right', fontsize=9)
ax.bar_label(bars, fmt='%,d', padding=3, fontsize=9)
ax.grid(axis='y')
plt.tight_layout()
save(fig, '07_top_products.png')

# ── 8. Zone + Heatmap ─────────────────────────────────────
print("🔍 [8/8] Zone & Heatmap Analysis...")
zone_rev = df.groupby('Zone')['Amount'].sum().sort_values(ascending=False)
pivot = df.pivot_table(index='Age Group', columns='Product_Category',
                       values='Amount', aggfunc='sum').reindex(age_order)
fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.suptitle('🪔 Zone Revenue & Age×Category Heatmap', fontsize=16, fontweight='bold')
bars = axes[0].bar(zone_rev.index, zone_rev.values,
                   color=[ACCENT, GOLD, '#C0392B', '#2ECC71'][:len(zone_rev)],
                   edgecolor='white', width=0.5)
axes[0].set_title('Revenue by Zone')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[0].grid(axis='y')
sns.heatmap(pivot/1e5, ax=axes[1], cmap='YlOrRd', linewidths=0.5,
            annot=True, fmt='.0f', annot_kws={'size':8},
            cbar_kws={'label':'Revenue (₹ Lakhs)'})
axes[1].set_title('Revenue Heatmap: Age Group × Product Category')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=40, ha='right', fontsize=8)
plt.tight_layout()
save(fig, '08_zone_heatmap.png')

print("\n✅ Analysis Complete! Check the plots/ folder for all charts.")
