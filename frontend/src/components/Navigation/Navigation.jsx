import React from 'react';
import styles from './Navigation.module.css';

const Navigation = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'customers', label: 'Customers' },
    { id: 'products', label: 'Products' },
    { id: 'invoices', label: 'Invoices' },
  ];

  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <h1>🧸 Toy Store Management</h1>
        </div>
        <ul className={styles.navList}>
          {tabs.map((tab) => (
            <li key={tab.id}>
              <button
                className={`${styles.navLink} ${
                  activeTab === tab.id ? styles.active : ''
                }`}
                onClick={() => onTabChange(tab.id)}
              >
                {tab.label}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;
