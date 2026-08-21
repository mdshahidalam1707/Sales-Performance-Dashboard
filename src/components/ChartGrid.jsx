import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export default function ChartGrid({ data }) {
  
  // 1. Aggregation: Monthly Sales & Profit
  // We can group by "Order Year" + "Order Month" (e.g. "2023 Dec")
  // Let's create a combined Year-Month sorting key
  const monthlyMap = {};
  data.forEach(row => {
    const key = `${row['Order Year']} ${row['Order Month']}`;
    const sortVal = row['Order Year'] * 12 + row['Order Month Number'];
    if (!monthlyMap[key]) {
      monthlyMap[key] = {
        name: key,
        Sales: 0,
        Profit: 0,
        sortVal
      };
    }
    monthlyMap[key].Sales += row.Sales;
    monthlyMap[key].Profit += row.Profit;
  });
  
  const monthlyData = Object.values(monthlyMap)
    .sort((a, b) => a.sortVal - b.sortVal)
    .map(item => ({
      name: item.name,
      Sales: Math.round(item.Sales),
      Profit: Math.round(item.Profit)
    }));

  // 2. Aggregation: Regional Sales & Profit
  const regionMap = {};
  data.forEach(row => {
    const reg = row.Region;
    if (!regionMap[reg]) {
      regionMap[reg] = { name: reg, Sales: 0, Profit: 0 };
    }
    regionMap[reg].Sales += row.Sales;
    regionMap[reg].Profit += row.Profit;
  });
  const regionData = Object.values(regionMap).map(item => ({
    name: item.name,
    Sales: Math.round(item.Sales),
    Profit: Math.round(item.Profit)
  }));

  // 3. Aggregation: Category Sales & Profit
  const catMap = {};
  data.forEach(row => {
    const cat = row.Category;
    if (!catMap[cat]) {
      catMap[cat] = { name: cat, Sales: 0, Profit: 0 };
    }
    catMap[cat].Sales += row.Sales;
    catMap[cat].Profit += row.Profit;
  });
  const catData = Object.values(catMap).map(item => ({
    name: item.name,
    Sales: Math.round(item.Sales),
    Profit: Math.round(item.Profit)
  }));

  // 4. Aggregation: Top 10 Products by Sales
  const prodMap = {};
  data.forEach(row => {
    const prod = row['Product Name'];
    if (!prodMap[prod]) {
      prodMap[prod] = { name: prod, Sales: 0 };
    }
    prodMap[prod].Sales += row.Sales;
  });
  const allProducts = Object.values(prodMap).map(item => ({
    name: item.name.length > 25 ? item.name.substring(0, 25) + '...' : item.name,
    Sales: Math.round(item.Sales)
  }));
  const top10Products = [...allProducts].sort((a, b) => b.Sales - a.Sales).slice(0, 10);
  const bot10Products = [...allProducts].sort((a, b) => a.Sales - b.Sales).slice(0, 10);

  // 5. Aggregation: Salesperson Performance
  const spMap = {};
  data.forEach(row => {
    const sp = row.Salesperson;
    if (!spMap[sp]) {
      spMap[sp] = { name: sp, Sales: 0, Profit: 0 };
    }
    spMap[sp].Sales += row.Sales;
    spMap[sp].Profit += row.Profit;
  });
  const spData = Object.values(spMap)
    .sort((a, b) => b.Sales - a.Sales)
    .map(item => ({
      name: item.name,
      Sales: Math.round(item.Sales),
      Profit: Math.round(item.Profit)
    }));

  // 6. Aggregation: Payment Method Distribution
  const payMap = {};
  data.forEach(row => {
    const pay = row['Payment Method'];
    if (!payMap[pay]) {
      payMap[pay] = { name: pay, value: 0 };
    }
    payMap[pay].value += row.Sales;
  });
  const payData = Object.values(payMap).map(item => ({
    name: item.name,
    value: Math.round(item.value)
  }));

  // 7. Aggregation: Sales vs Profit (Scatter sample, max 200 items for performance)
  const scatterData = data.slice(0, 200).map(row => ({
    x: Math.round(row.Sales),
    y: Math.round(row.Profit),
    name: row['Product Name']
  }));

  // Theme colors
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899'];

  // Tooltip formatter
  const formatTooltip = (value) => `$${value.toLocaleString()}`;

  return (
    <section className="charts-grid">
      
      {/* 1. Monthly Revenue & Profit Trend */}
      <div className="chart-card wide">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Monthly Revenue & Profit Trend</h4>
            <p className="chart-subtitle">Time-series overview of corporate revenue growth and profit conversions</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={monthlyData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
              <YAxis stroke="#9ca3af" tick={{ fill: '#9ca3af' }} formatter={v => `$${v.toLocaleString()}`} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)', color: '#fff' }} />
              <Legend />
              <Line type="monotone" dataKey="Sales" stroke="#3b82f6" strokeWidth={3} dot={{ r: 2 }} activeDot={{ r: 6 }} />
              <Line type="monotone" dataKey="Profit" stroke="#10b981" strokeWidth={3} dot={{ r: 2 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Regional Performance */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Sales & Profit by Region</h4>
            <p className="chart-subtitle">Regional breakdown of sales revenue versus net margin contribution</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={regionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" formatter={v => `$${v.toLocaleString()}`} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Legend />
              <Bar dataKey="Sales" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Profit" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 3. Category Performance */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Category Sales & Profit</h4>
            <p className="chart-subtitle">Profit margins across core retail categories</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={catData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" formatter={v => `$${v.toLocaleString()}`} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Legend />
              <Bar dataKey="Sales" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Profit" fill="#06b6d4" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 4. Top 10 Products */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Top 10 Products by Sales</h4>
            <p className="chart-subtitle">Products driving the highest gross transaction values</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={top10Products} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" stroke="#9ca3af" formatter={v => `$${v.toLocaleString()}`} />
              <YAxis dataKey="name" type="category" stroke="#9ca3af" width={100} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Bar dataKey="Sales" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 5. Bottom 10 Products */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Bottom 10 Products by Sales</h4>
            <p className="chart-subtitle">Underperforming items requiring review</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={bot10Products} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" stroke="#9ca3af" formatter={v => `$${v.toLocaleString()}`} />
              <YAxis dataKey="name" type="category" stroke="#9ca3af" width={100} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Bar dataKey="Sales" fill="#f43f5e" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 6. Salesperson Rankings */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Salesperson Rankings</h4>
            <p className="chart-subtitle">Individual salesperson sales revenue achievements</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={spData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" formatter={v => `$${v.toLocaleString()}`} />
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Bar dataKey="Sales" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 7. Payment Methods */}
      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Payment Method Share</h4>
            <p className="chart-subtitle">Breakdown of gross transactions by payment channel</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={payData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {payData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={formatTooltip} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 8. Sales vs Profit Relationship */}
      <div className="chart-card wide">
        <div className="chart-header">
          <div>
            <h4 className="chart-title">Sales vs Profit Distribution (Transactions)</h4>
            <p className="chart-subtitle">Scatter mapping of order value vs. net margin showing margin erosion outliers (under 50% discount cases)</p>
          </div>
        </div>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" dataKey="x" name="Sales" unit="$" stroke="#9ca3af" />
              <YAxis type="number" dataKey="y" name="Profit" unit="$" stroke="#9ca3af" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Scatter name="Transactions" data={scatterData} fill="#06b6d4" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

    </section>
  );
}
