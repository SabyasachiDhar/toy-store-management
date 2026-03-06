import React, { useState } from 'react';
import Navigation from './components/Navigation/Navigation';
import Dashboard from './components/Dashboard/Dashboard';
import Customers from './components/Customers/Customers';
import Products from './components/Products/Products';
import Invoices from './components/Invoices/Invoices';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'customers':
        return <Customers />;
      case 'products':
        return <Products />;
      case 'invoices':
        return <Invoices />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="App">
      <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="main-content">{renderContent()}</main>
      <footer className="footer">
        <p>&copy; 2024 Toy Store Management System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
