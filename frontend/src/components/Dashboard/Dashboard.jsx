import React from 'react';
import { useSelector } from 'react-redux';
import styles from './Dashboard.module.css';

const Dashboard = () => {
  const customers = useSelector((state) => state.customers.items);
  const products = useSelector((state) => state.products.items);
  const invoices = useSelector((state) => state.invoices.items);

  const stats = [
    {
      title: 'Total Customers',
      value: customers.length,
      color: '#4CAF50',
      icon: '👥',
    },
    {
      title: 'Total Products',
      value: products.length,
      color: '#2196F3',
      icon: '📦',
    },
    {
      title: 'Total Invoices',
      value: invoices.length,
      color: '#FF9800',
      icon: '📄',
    },
    {
      title: 'Total Revenue',
      value: `$${invoices
        .reduce((sum, inv) => sum + (parseFloat(inv.total_amount) || 0), 0)
        .toFixed(2)}`,
      color: '#f44336',
      icon: '💰',
    },
  ];

  const inventoryValue = products.reduce(
    (sum, prod) => sum + (parseFloat(prod.price) || 0) * (parseInt(prod.quantity) || 0),
    0
  );

  const pendingInvoices = invoices.filter((inv) => inv.status === 'pending').length;
  const paidInvoices = invoices.filter((inv) => inv.status === 'paid').length;

  return (
    <div className={styles.container}>
      <h2>Dashboard</h2>

      <div className={styles.statsGrid}>
        {stats.map((stat, index) => (
          <div key={index} className={styles.statCard}>
            <div className={styles.statIcon}>{stat.icon}</div>
            <div className={styles.statContent}>
              <div className={styles.statTitle}>{stat.title}</div>
              <div className={styles.statValue} style={{ color: stat.color }}>
                {stat.value}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className={styles.analyticsGrid}>
        <div className={styles.analyticsCard}>
          <h3>Inventory Value</h3>
          <div className={styles.analyticsValue}>
            ${inventoryValue.toFixed(2)}
          </div>
          <p className={styles.analyticsLabel}>
            {products.length} products in stock
          </p>
        </div>

        <div className={styles.analyticsCard}>
          <h3>Invoice Status</h3>
          <div className={styles.statusList}>
            <div className={styles.statusItem}>
              <span>Paid:</span> <strong>{paidInvoices}</strong>
            </div>
            <div className={styles.statusItem}>
              <span>Pending:</span> <strong>{pendingInvoices}</strong>
            </div>
            <div className={styles.statusItem}>
              <span>Total:</span> <strong>{invoices.length}</strong>
            </div>
          </div>
        </div>

        <div className={styles.analyticsCard}>
          <h3>Quick Stats</h3>
          <div className={styles.quickStats}>
            <p>
              <strong>Avg. Product Price:</strong> $
              {products.length > 0
                ? (
                    products.reduce(
                      (sum, p) => sum + (parseFloat(p.price) || 0),
                      0
                    ) / products.length
                  ).toFixed(2)
                : '0.00'}
            </p>
            <p>
              <strong>Low Stock Items:</strong>{' '}
              {products.filter((p) => parseInt(p.quantity) < 5).length}
            </p>
          </div>
        </div>
      </div>

      <div className={styles.recentActivity}>
        <h3>System Information</h3>
        <div className={styles.infoBox}>
          <p>
            <strong>API Version:</strong> 1.0.0
          </p>
          <p>
            <strong>Name:</strong> Inventory Management API
          </p>
          <p>
            <strong>Available Endpoints:</strong>
          </p>
          <ul>
            <li>/api/customers</li>
            <li>/api/products</li>
            <li>/api/invoices</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
