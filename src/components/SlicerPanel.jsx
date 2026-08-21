import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Filter, RotateCcw } from 'lucide-react';

export default function SlicerPanel({
  uniqueValues,
  filters,
  onFilterChange,
  onClearFilters
}) {
  // Accordion state (default expanded for Year, Region, Category)
  const [expanded, setExpanded] = useState({
    'Order Year': true,
    'Region': true,
    'Category': true,
    'Sub-Category': false,
    'Salesperson': false,
    'Payment Method': false
  });

  const toggleExpand = (key) => {
    setExpanded(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleCheckboxChange = (filterKey, value) => {
    const activeValues = filters[filterKey] || [];
    let newValues;
    if (activeValues.includes(value)) {
      newValues = activeValues.filter(v => v !== value);
    } else {
      newValues = [...activeValues, value];
    }
    onFilterChange(filterKey, newValues);
  };

  const slicerConfigs = [
    { key: 'Order Year', label: 'Year' },
    { key: 'Region', label: 'Region' },
    { key: 'Category', label: 'Category' },
    { key: 'Sub-Category', label: 'Sub-Category' },
    { key: 'Salesperson', label: 'Salesperson' },
    { key: 'Payment Method', label: 'Payment Method' }
  ];

  return (
    <aside className="slicer-sidebar">
      <div className="sidebar-title">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <Filter size={15} />
          <span>Filters</span>
        </div>
        <button onClick={onClearFilters} className="clear-btn" title="Reset all filters">
          <RotateCcw size={13} style={{ marginRight: '3px' }} />
          Reset
        </button>
      </div>

      {slicerConfigs.map(({ key, label }) => {
        const items = uniqueValues[key] || [];
        const activeFilters = filters[key] || [];
        const isExpanded = expanded[key];

        return (
          <div key={key} className="slicer-group">
            <div className="slicer-header" onClick={() => toggleExpand(key)}>
              <span>{label} {activeFilters.length > 0 && `(${activeFilters.length})`}</span>
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </div>

            {isExpanded && (
              <div className="slicer-items">
                {items.map(val => {
                  const isChecked = activeFilters.includes(val);
                  return (
                    <label key={val} className="slicer-item">
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => handleCheckboxChange(key, val)}
                      />
                      <span>{val}</span>
                    </label>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </aside>
  );
}
