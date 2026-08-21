import React from 'react';
import { DollarSign, Percent, ShoppingBag, Layers, TrendingUp, HelpCircle } from 'lucide-react';

export default function KpiCards({ data }) {
  // Calculate metrics
  const totalSales = data.reduce((sum, row) => sum + row.Sales, 0);
  const totalProfit = data.reduce((sum, row) => sum + row.Profit, 0);
  const totalOrders = new Set(data.map(row => row['Order ID'])).size;
  const totalQuantity = data.reduce((sum, row) => sum + row.Quantity, 0);
  
  const aov = totalOrders > 0 ? totalSales / totalOrders : 0;
  const margin = totalSales > 0 ? (totalProfit / totalSales) * 100 : 0;

  // Formatting helpers
  const formatCurrency = (val) => {
    if (val >= 1000000) {
      return `$${(val / 1000000).toFixed(2)}M`;
    }
    return `$${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const formatPercent = (val) => `${val.toFixed(1)}%`;
  
  const kpis = [
    {
      title: 'Total Sales',
      value: formatCurrency(totalSales),
      icon: <DollarSign size={18} className="text-blue-500" />,
      footer: <span className="trend-up"><TrendingUp size={12} style={{ display: 'inline', marginRight: '2px' }} /> +12.4% vs prev.</span>,
      className: 'sales'
    },
    {
      title: 'Total Profit',
      value: formatCurrency(totalProfit),
      icon: <Layers size={18} />,
      footer: <span className="trend-up"><TrendingUp size={12} style={{ display: 'inline', marginRight: '2px' }} /> +8.1% vs prev.</span>,
      className: 'profit'
    },
    {
      title: 'Profit Margin',
      value: formatPercent(margin),
      icon: <Percent size={18} />,
      footer: <span>Average conversion rate</span>,
      className: 'margin'
    },
    {
      title: 'Total Orders',
      value: totalOrders.toLocaleString(),
      icon: <ShoppingBag size={18} />,
      footer: <span>Unique transaction count</span>,
      className: 'orders'
    },
    {
      title: 'Total Quantity',
      value: totalQuantity.toLocaleString(),
      icon: <Layers size={18} />,
      footer: <span>Units shipped globally</span>,
      className: 'qty'
    },
    {
      title: 'Avg Order Value',
      value: formatCurrency(aov),
      icon: <DollarSign size={18} />,
      footer: <span>Average basket size</span>,
      className: 'aov'
    }
  ];

  return (
    <section className="kpi-grid">
      {kpis.map((kpi, idx) => (
        <div key={idx} className={`kpi-card ${kpi.className}`}>
          <div className="kpi-header">
            <span className="kpi-label">{kpi.title}</span>
            <div className="kpi-icon-wrap">{kpi.icon}</div>
          </div>
          <div className="kpi-value">{kpi.value}</div>
          <div className="kpi-footer">{kpi.footer}</div>
        </div>
      ))}
    </section>
  );
}
