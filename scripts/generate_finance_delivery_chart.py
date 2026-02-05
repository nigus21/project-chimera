"""
Generate a client-facing line chart comparing Finance vs Delivery totals
over the last three months.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Data from the email (in thousands)
months = ['Nov 2024', 'Dec 2024', 'Jan 2025']
finance_totals = [124.5, 131.8, 119.2]  # in thousands
delivery_totals = [118.2, 127.4, 115.9]  # in thousands

# Create the figure with professional styling
plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the lines
line1 = ax.plot(months, finance_totals, marker='o', linewidth=2.5, markersize=8, 
                label='Finance', color='#2E86AB', markerfacecolor='#2E86AB', 
                markeredgecolor='white', markeredgewidth=1.5)

line2 = ax.plot(months, delivery_totals, marker='s', linewidth=2.5, markersize=8, 
                label='Delivery', color='#A23B72', markerfacecolor='#A23B72', 
                markeredgecolor='white', markeredgewidth=1.5)

# Add value labels on each point
for i, (fin, deliv) in enumerate(zip(finance_totals, delivery_totals)):
    ax.annotate(f'${fin:.1f}K', (i, fin), textcoords="offset points", 
                xytext=(0,10), ha='center', fontsize=9, fontweight='bold', color='#2E86AB')
    ax.annotate(f'${deliv:.1f}K', (i, deliv), textcoords="offset points", 
                xytext=(0,-15), ha='center', fontsize=9, fontweight='bold', color='#A23B72')

# Customize the chart
ax.set_title('Finance vs Delivery Totals: Last 3 Months Comparison', 
             fontsize=16, fontweight='bold', pad=20, color='#1a1a1a')
ax.set_xlabel('Month', fontsize=12, fontweight='bold', color='#333333')
ax.set_ylabel('Total Value (Thousands USD)', fontsize=12, fontweight='bold', color='#333333')

# Format y-axis to show currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.0f}K'))
ax.set_ylim(bottom=110, top=135)

# Add grid for better readability
ax.grid(True, linestyle='--', alpha=0.3, linewidth=0.8)
ax.set_axisbelow(True)

# Add legend
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
          fontsize=11, framealpha=0.95)

# Improve spacing
plt.tight_layout()

# Save the chart
output_path = 'docs/finance_vs_delivery_chart.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Chart saved to: {output_path}")

plt.close()
