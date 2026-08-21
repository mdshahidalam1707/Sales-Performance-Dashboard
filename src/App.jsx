import React, { useState, useMemo } from 'react';
import rawData from './data/cleaned_sales_data.json';
import SlicerPanel from './components/SlicerPanel';
import KpiCards from './components/KpiCards';
import ChartGrid from './components/ChartGrid';
import { AlertCircle, CheckCircle, Lightbulb } from 'lucide-react';

export default function App() {
  // 1. Initial State for Slicer Filters
  const [filters, setFilters] = useState({
    'Order Year': [],
    'Region': [],
    'Category': [],
    'Sub-Category': [],
    'Salesperson': [],
    'Payment Method': []
  });

  // 2. Pre-calculate lists of unique values from the base dataset for slicer menus
  const uniqueValues = useMemo(() => {
    return {
      'Order Year': [...new Set(rawData.map(row => row['Order Year']))].sort((a, b) => b - a),
      'Region': [...new Set(rawData.map(row => row.Region))].sort(),
      'Category': [...new Set(rawData.map(row => row.Category))].sort(),
      'Sub-Category': [...new Set(rawData.map(row => row['Sub-Category']))].sort(),
      'Salesperson': [...new Set(rawData.map(row => row.Salesperson))].sort(),
      'Payment Method': [...new Set(rawData.map(row => row['Payment Method']))].sort()
    };
  }, []);

  // 3. Filtering logic applied to the dataset based on active slicer selections
  const filteredData = useMemo(() => {
    return rawData.filter(row => {
      for (const key in filters) {
        const selectedValues = filters[key];
        if (selectedValues.length > 0) {
          if (!selectedValues.includes(row[key])) {
            return false;
          }
        }
      }
      return true;
    });
  }, [filters]);

  // Handle a change in filter checkboxes
  const handleFilterChange = (filterKey, selectedValues) => {
    setFilters(prev => ({
      ...prev,
      [filterKey]: selectedValues
    }));
  };

  // Reset all filters to initial state
  const handleClearFilters = () => {
    setFilters({
      'Order Year': [],
      'Region': [],
      'Category': [],
      'Sub-Category': [],
      'Salesperson': [],
      'Payment Method': []
    });
  };

  // 4. Dynamic Business Insights calculated from the ACTIVE filtered data
  const dynamicInsights = useMemo(() => {
    if (filteredData.length === 0) return [];
    
    // Regional revenue leader
    const regSales = {};
    filteredData.forEach(row => {
      regSales[row.Region] = (regSales[row.Region] || 0) + row.Sales;
    });
    const topRegion = Object.keys(regSales).reduce((a, b) => regSales[a] > regSales[b] ? a : b, 'N/A');

    // Table discount assessment
    const tables = filteredData.filter(row => row['Sub-Category'] === 'Tables');
    const tableSales = tables.reduce((sum, row) => sum + row.Sales, 0);
    const tableProfit = tables.reduce((sum, row) => sum + row.Profit, 0);
    const avgTableDiscount = tables.length > 0 ? (tables.reduce((sum, row) => sum + row.Discount, 0) / tables.length) * 100 : 0;
    const isTableInLoss = tableProfit < 0;

    // Technology margin assessment
    const tech = filteredData.filter(row => row.Category === 'Technology');
    const techSales = tech.reduce((sum, row) => sum + row.Sales, 0);
    const techProfit = tech.reduce((sum, row) => sum + row.Profit, 0);
    const techMargin = techSales > 0 ? (techProfit / techSales) * 100 : 0;

    const insights = [];
    if (topRegion !== 'N/A') {
      insights.push({
        title: `Regional Revenue Leader: ${topRegion}`,
        desc: `Under current filters, the ${topRegion} region represents the strongest territory, generating $${regSales[topRegion].toLocaleString(undefined, { maximumFractionDigits: 0 })} in sales.`,
        type: 'success'
      });
    }

    if (tables.length > 0) {
      if (isTableInLoss) {
        insights.push({
          title: 'Table Discount Margin Erosion Warning',
          desc: `Tables generated $${tableSales.toLocaleString(undefined, { maximumFractionDigits: 0 })} in sales but recorded a net loss of $${Math.abs(tableProfit).toLocaleString(undefined, { maximumFractionDigits: 0 })} due to a high average discount rate of ${avgTableDiscount.toFixed(1)}%.`,
          type: 'danger'
        });
      } else {
        insights.push({
          title: 'Table Discount Margin Warning',
          desc: `Tables generated a profit of $${tableProfit.toLocaleString(undefined, { maximumFractionDigits: 0 })}. Keep discounts below 15% to maintain margin stability (currently averaging ${avgTableDiscount.toFixed(1)}%).`,
          type: 'warning'
        });
      }
    }

    if (tech.length > 0) {
      insights.push({
        title: `High Technology Profit Margin: ${techMargin.toFixed(1)}%`,
        desc: `Technology products contributed a net profit of $${techProfit.toLocaleString(undefined, { maximumFractionDigits: 0 })}. Standardize corporate contracts around this category.`,
        type: 'info'
      });
    }

    return insights;
  }, [filteredData]);

  return (
    <div className="app-container">
      {/* Dashboard Top Header */}
      <header className="header">
        <div className="header-left">
          <h1>Sales Performance Cockpit</h1>
          <p>Interactive Business Intelligence Cockpit & KPI Analytics</p>
        </div>
        <div className="header-right">
          <div className="user-badge">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=150&auto=format&fit=crop" alt="Sarah J." />
            <span>Sarah J. (Senior Analyst)</span>
          </div>
        </div>
      </header>

      {/* Main Layout Workspace */}
      <div className="dashboard-workspace">
        {/* Left Interactive Slicer Panel */}
        <SlicerPanel
          uniqueValues={uniqueValues}
          filters={filters}
          onFilterChange={handleFilterChange}
          onClearFilters={handleClearFilters}
        />

        {/* Right Cockpit Content */}
        <main className="dashboard-content">
          {/* Top KPI Cards row */}
          <KpiCards data={filteredData} />

          {/* Dynamic Insights Panel */}
          {dynamicInsights.length > 0 && (
            <div className="insights-panel">
              <div className="insights-panel-header">
                <Lightbulb size={20} />
                <h3>Active Cockpit Insights</h3>
              </div>
              <div className="insights-list">
                {dynamicInsights.map((insight, index) => (
                  <div key={index} className="insight-item">
                    <strong style={{
                      color: insight.type === 'danger' ? 'var(--color-rose)' :
                             insight.type === 'warning' ? 'var(--color-amber)' :
                             insight.type === 'success' ? 'var(--color-emerald)' : 'var(--color-cyan)'
                    }}>
                      {insight.title}
                    </strong>
                    <span>{insight.desc}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recharts Grid Section */}
          {filteredData.length > 0 ? (
            <ChartGrid data={filteredData} />
          ) : (
            <div style={{ textAlign: 'center', padding: '3rem', border: '1px dashed var(--border-color)', borderRadius: '12px', color: 'var(--text-secondary)' }}>
              <AlertCircle size={40} style={{ margin: '0 auto 1rem', color: 'var(--color-rose)' }} />
              <h3>No Data Found For Selected Filters</h3>
              <p style={{ marginTop: '0.5rem' }}>Please adjust your slicer selections to display the dashboard visuals.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
